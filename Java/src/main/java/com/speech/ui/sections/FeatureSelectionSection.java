package com.speech.ui.sections;

import com.speech.ui.AbstractDashboardSection;
import com.speech.ui.components.AnimatedButton;
import net.miginfocom.swing.MigLayout;

import javax.swing.*;
import java.awt.event.ActionListener;
import java.awt.Font;
import java.util.ArrayList;
import java.util.List;

public class FeatureSelectionSection extends AbstractDashboardSection {

    private AnimatedButton selectAllButton;
    private AnimatedButton deselectAllButton;
    private List<JCheckBox> allCheckBoxes = new ArrayList<>();

    @Override
    public String getSectionTitle() {
        return "3. Feature Selection";
    }

    @Override
    protected void initializeComponents() {
        // Master layout for Section 3
        panel.setLayout(new MigLayout("fill, insets 10", "[grow]", "[]15![grow]"));

        selectAllButton = new AnimatedButton("Select All");
        deselectAllButton = new AnimatedButton("Deselect All");

        // Use FlowLayout.RIGHT to position buttons as requested
        JPanel buttonPanel = new JPanel(new java.awt.FlowLayout(java.awt.FlowLayout.RIGHT, 15, 0));
        buttonPanel.add(selectAllButton);
        buttonPanel.add(deselectAllButton);
        
        // Aligned RIGHT for standard dashboard action positioning
        panel.add(buttonPanel, "growx, wrap");

        // Internal Checklist Panel - removed 'fillx' to ensure horizontal scrollbar triggers correctly on narrow windows
        JPanel checklistPanel = new JPanel(new MigLayout("insets 0", "[grow][grow][grow]", "[]10![grow]"));
        checklistPanel.setOpaque(false);

        // Group Definitions mapped natively onto UIResource for elastic shrinking
        JLabel group1 = new JLabel("Cepstral & Tonal");
        group1.setFont(new javax.swing.plaf.FontUIResource(com.speech.util.FontHelper.getGlontoFont(Font.BOLD, 12f)));
        JLabel group2 = new JLabel("Spectral");
        group2.setFont(new javax.swing.plaf.FontUIResource(com.speech.util.FontHelper.getGlontoFont(Font.BOLD, 12f)));
        JLabel group3 = new JLabel("Prosodic, Energy & Other");
        group3.setFont(new javax.swing.plaf.FontUIResource(com.speech.util.FontHelper.getGlontoFont(Font.BOLD, 12f)));

        checklistPanel.add(group1);
        checklistPanel.add(group2);
        checklistPanel.add(group3, "wrap 10");

        // Col 1: Cepstral & Tonal
        JPanel col1 = new JPanel(new MigLayout("insets 0, wrap 1, gapy 10"));
        col1.add(addCheckBox("MFCCs"));
        col1.add(addCheckBox("Chroma Features"));
        checklistPanel.add(col1, "aligny top");

        // Col 2: Spectral
        JPanel col2 = new JPanel(new MigLayout("insets 0, wrap 1, gapy 10"));
        col2.add(addCheckBox("Zero-Crossing Rate"));
        col2.add(addCheckBox("Spectral Centroid"));
        col2.add(addCheckBox("Spectral Bandwidth"));
        col2.add(addCheckBox("Spectral Roll-Off"));
        checklistPanel.add(col2, "aligny top");

        // Col 3: Prosodic & Energy / Other
        JPanel col3 = new JPanel(new MigLayout("insets 0, wrap 1, gapy 10"));
        col3.add(addCheckBox("Pitch (F0)"));
        col3.add(addCheckBox("RMSE Energy"));
        col3.add(addCheckBox("Short-Term Energy"));
        col3.add(addCheckBox("Harmonic-to-Noise Ratio"));
        col3.add(addCheckBox("Jitter"));
        col3.add(addCheckBox("Shimmer"));
        checklistPanel.add(col3, "aligny top");

        // Wrap the entire checklist in a JScrollPane to handle small window sizes
        JScrollPane scrollPane = new JScrollPane(checklistPanel);
        scrollPane.setBorder(null);
        scrollPane.setOpaque(false);
        scrollPane.getViewport().setOpaque(false);
        // Show both scrollbars only when necessary to ensure zero clipping in ultra-narrow views
        scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED);
        scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_AS_NEEDED);
        
        panel.add(scrollPane, "grow, pushy");

        ActionListener selectAction = e -> {
            boolean select = e.getSource() == selectAllButton;
            for (JCheckBox cb : allCheckBoxes) {
                cb.setSelected(select);
            }
        };

        selectAllButton.addActionListener(selectAction);
        deselectAllButton.addActionListener(selectAction);
    }

    private JCheckBox addCheckBox(String text) {
        JCheckBox cb = new JCheckBox(text);
        // Reduce font size to 11f for a clean, professional look
        cb.setFont(com.speech.util.FontHelper.getAnticycloneFont(Font.PLAIN, 11f));
        allCheckBoxes.add(cb);
        return cb;
    }

    /**
     * Natively extracts and returns a map of all feature tokens and their selected state.
     */
    public java.util.Map<String, Boolean> exportSelections() {
        java.util.Map<String, Boolean> selections = new java.util.LinkedHashMap<>();
        for (JCheckBox cb : allCheckBoxes) {
            selections.put(cb.getText(), cb.isSelected());
        }
        return selections;
    }
}
