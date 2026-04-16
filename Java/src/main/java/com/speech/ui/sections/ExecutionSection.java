package com.speech.ui.sections;

import com.speech.ui.AbstractDashboardSection;
import com.speech.ui.components.AnimatedButton;
import net.miginfocom.swing.MigLayout;

import javax.swing.*;
import java.awt.Font;
import java.awt.Color;
import java.util.List;
import java.util.Map;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.io.File;
import java.io.FileWriter;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.speech.model.ExtractionConfig;

public class ExecutionSection extends AbstractDashboardSection {

    private AnimatedButton runButton;
    private JProgressBar progressBar;
    private JTextArea consoleArea;
    private OutputSection outputSection;
    
    // Sibling section references for master data extraction
    private InputSection inputSection;
    private PreprocessingSection prepSection;
    private FeatureSelectionSection featureSection;

    public ExecutionSection(InputSection inputSection, 
                          PreprocessingSection prepSection, 
                          FeatureSelectionSection featureSection) {
        this.inputSection = inputSection;
        this.prepSection = prepSection;
        this.featureSection = featureSection;
    }

    public void setOutputSection(OutputSection outputSection) {
        this.outputSection = outputSection;
    }

    @Override
    public String getSectionTitle() {
        return "4. Execution & Status";
    }

    @Override
    protected void initializeComponents() {
        panel.setLayout(new MigLayout("fillx, insets 5", "[grow]", "[]10[]10[grow]"));

        runButton = new AnimatedButton("Run Preprocessing & Extraction");
        // Apply Special Blue HUD Glow to the main extraction trigger
        runButton.setSpecialGlow(true);
        // Make the button large and prominent
        runButton.setFont(runButton.getFont().deriveFont(Font.BOLD, 14f));
        // Force the button to be disabled until audio files are Browsed
        runButton.setEnabled(false);
        panel.add(runButton, "growx, h 45!, wrap");

        progressBar = new JProgressBar();
        progressBar.setStringPainted(true);
        panel.add(progressBar, "growx, h 0:35:, wrap");

        consoleArea = new JTextArea();
        consoleArea.setEditable(false);
        consoleArea.setBackground(new Color(25, 25, 25));
        consoleArea.setForeground(new Color(200, 200, 200));
        consoleArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
        consoleArea.setText("====== SYSTEM READY ======\n");

        JScrollPane scrollPane = new JScrollPane(consoleArea);
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        panel.add(scrollPane, "grow, pushy, h 0::");

        // Action Listener for Run Button
        runButton.addActionListener(e -> {
            runButton.setEnabled(false);
            progressBar.setValue(0);
            progressBar.setString("Initializing...");
            
            log("Gathering extraction parameters...");
            
            try {
                // 1. Gather all dashboard state natively from the sibling sections
                List<String> files = inputSection.getSelectedRelativePaths();
                Map<String, Object> prep = prepSection.exportSettings();
                Map<String, Boolean> features = featureSection.exportSelections();

                // 2. Wrap into our model for GSON serialization
                ExtractionConfig config = new ExtractionConfig(files, prep, features);

                // 3. Ensure the 'output' directory exists safely
                Path outputDirPath = Paths.get("output");
                Files.createDirectories(outputDirPath);
                File outputDir = outputDirPath.toFile();

                // 4. Serialize to JSON using Google GSON
                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                String json = gson.toJson(config);

                // 5. Write to the target file
                File target = new File(outputDir, "extraction_settings.json");
                try (FileWriter writer = new FileWriter(target)) {
                    writer.write(json);
                }

                log("Configuration saved to: " + target.getPath());

                // 6. Send JSON output to Python FastAPI backend
                log("Sending configuration to Python FastAPI backend...");
                try {
                    HttpClient client = HttpClient.newBuilder()
                            .version(HttpClient.Version.HTTP_1_1)
                            .build();
                    HttpRequest request = HttpRequest.newBuilder()
                            .uri(URI.create("http://127.0.0.1:9999/api/config"))
                            .header("Content-Type", "application/json")
                            .POST(HttpRequest.BodyPublishers.ofString(json))
                            .build();

                    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                    if (response.statusCode() == 200) {
                        log("FastAPI backend accepted the configuration.");
                    } else {
                        log("FastAPI backend returned status: " + response.statusCode());
                        log("Response: " + response.body());
                        runButton.setEnabled(true);
                        return;
                    }
                } catch (Exception httpEx) {
                    log("WARNING: Could not connect to FastAPI backend (is it running on port 9999?)");
                    log("Error details: " + httpEx.getMessage());
                    runButton.setEnabled(true);
                    return;
                }

                log("Starting preprocessing and feature extraction pipeline...");
            } catch (Exception ex) {
                log("ERROR: Failed to generate extraction configuration: " + ex.getMessage());
                ex.printStackTrace();
                runButton.setEnabled(true);
                return;
            }
            
            // Re-importing inside for simple scope handling in this prototype
            SwingWorker<String, String> worker = new SwingWorker<>() {
                @Override
                protected String doInBackground() throws Exception {
                    HttpClient statusClient = HttpClient.newBuilder()
                            .version(HttpClient.Version.HTTP_1_1)
                            .build();
                    HttpRequest statusRequest = HttpRequest.newBuilder()
                            .uri(URI.create("http://127.0.0.1:9999/api/status"))
                            .GET()
                            .build();

                    String lastMessage = "";

                    while (true) {
                        try {
                            HttpResponse<String> statusResponse = statusClient.send(statusRequest, HttpResponse.BodyHandlers.ofString());
                            if (statusResponse.statusCode() == 200) {
                                JsonObject jsonObj = JsonParser.parseString(statusResponse.body()).getAsJsonObject();
                                boolean isComplete = jsonObj.get("is_complete").getAsBoolean();
                                int prog = jsonObj.get("progress").getAsInt();
                                String msg = jsonObj.get("message").getAsString();
                                
                                setProgress(prog);
                                
                                if (!msg.equals(lastMessage)) {
                                    publish(msg);
                                    lastMessage = msg;
                                }

                                if (isComplete && prog == 100) {
                                    break;
                                }
                            } else {
                                publish("Waiting for Python API response...");
                            }
                        } catch (Exception e) {
                            // Suppress transient errors
                        }
                        
                        Thread.sleep(500); // Polling interval
                    }
                    return lastMessage;
                }

                @Override
                protected void process(List<String> chunks) {
                    for (String msg : chunks) {
                        log(msg);
                        progressBar.setString(msg);
                    }
                }

                @Override
                protected void done() {
                    try {
                        String finalMsg = get();
                        if (finalMsg != null && finalMsg.startsWith("Error:")) {
                            progressBar.setString("Failed");
                            runButton.setEnabled(true);
                            JOptionPane.showMessageDialog(panel, 
                                "Pipeline Failed:\n" + finalMsg, 
                                "Extraction Error", 
                                JOptionPane.ERROR_MESSAGE);
                            return;
                        }
                    } catch (Exception e) {}

                    progressBar.setValue(100);
                    progressBar.setString("Completed Successfully");
                    log("Feature extraction completed successfully!");
                    log("Outputs are ready for download (CSV/ZIP).");
                    runButton.setEnabled(true);
                    
                    if (outputSection != null) {
                        outputSection.enableButtons();
                    }

                    // Native professional success notification
                    JOptionPane.showMessageDialog(panel, 
                        "Extraction Settings exported to 'output/extraction_settings.json'!\nPipeline completed successfully.", 
                        "Extraction Task Success", 
                        JOptionPane.INFORMATION_MESSAGE);
                }
            };
            
            worker.addPropertyChangeListener(evt -> {
                if ("progress".equals(evt.getPropertyName())) {
                    progressBar.setValue((Integer) evt.getNewValue());
                }
            });
            worker.execute();
        });
    }

    /**
     * Natively updates the Run button's enabled state.
     */
    public void updateRunButtonState(boolean enabled) {
        runButton.setEnabled(enabled);
    }

    public void log(String message) {
        consoleArea.append("> " + message + "\n");
        consoleArea.setCaretPosition(consoleArea.getDocument().getLength());
    }
}
