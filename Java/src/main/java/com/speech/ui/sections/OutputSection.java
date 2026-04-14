package com.speech.ui.sections;

import com.speech.ui.AbstractDashboardSection;
import com.speech.ui.components.AnimatedButton;
import net.miginfocom.swing.MigLayout;

import javax.swing.*;
import java.io.*;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class OutputSection extends AbstractDashboardSection {

    private AnimatedButton saveCsvButton;
    private AnimatedButton saveZipButton;

    @Override
    public String getSectionTitle() {
        return "5. Output Section (Download Results)";
    }

    @Override
    protected void initializeComponents() {
        // Increased gap between buttons for a cleaner layout
        panel.setLayout(new MigLayout("fillx, insets 10", "[grow]15[grow]", "[grow]"));

        saveCsvButton = new AnimatedButton("Save Processed Audio (CSV)");
        saveCsvButton.setIcon(com.speech.util.SVGIconHelper.getIcon("download.svg"));
        saveCsvButton.setEnabled(false);

        saveZipButton = new AnimatedButton("Save Processed Audio (ZIP)");
        saveZipButton.setIcon(com.speech.util.SVGIconHelper.getIcon("download.svg"));
        saveZipButton.setEnabled(false);

        // Allow Output buttons to demand a tall, prominent vertical space (minimum 50px, up to 100!)
        panel.add(saveCsvButton, "growx, h 50::100");
        panel.add(saveZipButton, "growx, h 50::100");

        // ── Download CSV action ────────────────────────────────────────
        saveCsvButton.addActionListener(e -> downloadFile(
                "http://127.0.0.1:9999/api/download/csv",
                "features.csv",
                "CSV Files (*.csv)",
                "csv"
        ));

        // ── Download ZIP action ────────────────────────────────────────
        saveZipButton.addActionListener(e -> downloadFile(
                "http://127.0.0.1:9999/api/download/zip",
                "speech_features.zip",
                "ZIP Archives (*.zip)",
                "zip"
        ));
    }

    /**
     * Downloads a file from the Python backend and lets the user choose where to save it.
     */
    private void downloadFile(String url, String defaultFilename, String filterDesc, String extension) {
        JFileChooser chooser = new JFileChooser();
        chooser.setDialogTitle("Save As");
        chooser.setSelectedFile(new File(defaultFilename));
        chooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter(filterDesc, extension));

        int result = chooser.showSaveDialog(panel);
        if (result != JFileChooser.APPROVE_OPTION) {
            return;
        }

        File target = chooser.getSelectedFile();
        // Ensure correct extension
        if (!target.getName().endsWith("." + extension)) {
            target = new File(target.getAbsolutePath() + "." + extension);
        }

        final File finalTarget = target;

        // Download in background to keep the UI responsive
        SwingWorker<Void, Void> worker = new SwingWorker<>() {
            @Override
            protected Void doInBackground() throws Exception {
                HttpClient client = HttpClient.newBuilder()
                        .version(HttpClient.Version.HTTP_1_1)
                        .build();
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .GET()
                        .build();

                HttpResponse<InputStream> response = client.send(request,
                        HttpResponse.BodyHandlers.ofInputStream());

                if (response.statusCode() == 200) {
                    try (InputStream in = response.body()) {
                        Files.copy(in, finalTarget.toPath(), StandardCopyOption.REPLACE_EXISTING);
                    }
                } else {
                    throw new IOException("Server returned status " + response.statusCode());
                }
                return null;
            }

            @Override
            protected void done() {
                try {
                    get(); // re-throw any exception from doInBackground
                    JOptionPane.showMessageDialog(panel,
                            "File saved to:\n" + finalTarget.getAbsolutePath(),
                            "Download Complete",
                            JOptionPane.INFORMATION_MESSAGE);
                } catch (Exception ex) {
                    JOptionPane.showMessageDialog(panel,
                            "Download failed: " + ex.getMessage()
                                    + "\n\nIs the Python backend running?",
                            "Download Error",
                            JOptionPane.ERROR_MESSAGE);
                }
            }
        };
        worker.execute();
    }

    public void enableButtons() {
        saveCsvButton.setEnabled(true);
        saveZipButton.setEnabled(true);
    }
}
