package com.speech.ui.sections;

import com.speech.ui.AbstractDashboardSection;
import net.miginfocom.swing.MigLayout;
import com.speech.ui.components.AnimatedButton;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.awt.FlowLayout;
import com.speech.util.SVGIconHelper;

public class InputSection extends AbstractDashboardSection {

    private AnimatedButton browseButton;
    private AnimatedButton clearAllButton;
    private JTable fileTable;
    private DefaultTableModel fileTableModel;
    private List<File> selectedFiles = new ArrayList<>();
    private Runnable onFileChangeListener;

    public void setOnFileChangeListener(Runnable listener) {
        this.onFileChangeListener = listener;
    }

    @Override
    public String getSectionTitle() {
        return "1. Input Section (Upload Raw Audio)";
    }

    @Override
    protected void initializeComponents() {
        panel.setLayout(new MigLayout("fillx, insets 5", "[grow]", "[]0[grow]"));

        // Button Panel - Increased horizontal gap to 15px for an open, airy feel
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 15, 0));
        browseButton = new AnimatedButton("Browse Audio Files", SVGIconHelper.getIcon("folder.svg"));
        clearAllButton = new AnimatedButton("Clear Files");

        buttonPanel.add(browseButton);
        buttonPanel.add(clearAllButton);

        // Increase wrap gap to 15 to separate buttons from the table
        panel.add(buttonPanel, "growx, wrap 15");

        // Native Table
        fileTableModel = new DefaultTableModel(new String[]{"File Name", "Status"}, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        fileTable = new JTable(fileTableModel);
        
        fileTable.setRowHeight(24);
        fileTable.getTableHeader().setReorderingAllowed(false);

        JScrollPane scrollPane = new JScrollPane(fileTable);
        panel.add(scrollPane, "grow, h 0::, pushy");

        // Action Listeners
        browseButton.addActionListener(e -> {
            JFileChooser chooser = new JFileChooser();
            chooser.setMultiSelectionEnabled(true);
            
            // Native Sanitization: Only allow browsing for verified audio formats
            FileNameExtensionFilter filter = new FileNameExtensionFilter(
                "Audio Files (*.wav, *.mp3, *.ogg, *.flac, *.aac)", 
                "wav", "mp3", "ogg", "flac", "aac", "m4a", "wma"
            );
            chooser.setFileFilter(filter);
            chooser.setAcceptAllFileFilterUsed(false); // Force sanitization - user cannot select *.*

            int result = chooser.showOpenDialog(SwingUtilities.getWindowAncestor(panel));
            if (result == JFileChooser.APPROVE_OPTION) {
                File[] files = chooser.getSelectedFiles();
                for (File file : files) {
                    selectedFiles.add(file);
                    fileTableModel.addRow(new Object[]{file.getName(), "Ready"});
                }
                if (onFileChangeListener != null) onFileChangeListener.run();
            }
        });

        clearAllButton.addActionListener(e -> {
            fileTableModel.setRowCount(0);
            selectedFiles.clear();
            if (onFileChangeListener != null) onFileChangeListener.run();
        });
    }

    public boolean hasFiles() {
        return !selectedFiles.isEmpty();
    }

    /**
     * Natively calculates and returns absolute paths for all selected audio files.
     */
    public List<String> getSelectedRelativePaths() {
        List<String> paths = new ArrayList<>();
        for (File file : selectedFiles) {
            paths.add(file.getAbsolutePath());
        }
        return paths;
    }
}
