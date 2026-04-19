package com.speech.ui.sections;

import com.speech.ui.AbstractDashboardSection;
import net.miginfocom.swing.MigLayout;

import javax.swing.*;
import java.awt.Font;
import java.util.Map;
import java.util.LinkedHashMap;
import com.speech.util.FontHelper;

public class PreprocessingSection extends AbstractDashboardSection {
    // Member references for automated state extraction
    private JCheckBox resamplingCheck, noiseReductionCheck, normalCheck, hpFilterCheck, silentCheck;
    private JComboBox<String> resamplingCombo, noiseReductionCombo;
    private JSpinner normalSpinner, hpSpinner;

    @Override
    public String getSectionTitle() {
        return "2. Preprocessing Operations";
    }

    @Override
    protected void initializeComponents() {
        // Distribute components vertically with equal gaps to fill the box
        panel.setLayout(new MigLayout("fillx, insets 10", "[][grow]", "[]push[]push[]push[]push[]"));

        // Resampling
        resamplingCheck = new JCheckBox("Resampling");
        resamplingCheck.setFont(FontHelper.getAnticycloneFont(Font.PLAIN, 11f));
        resamplingCombo = new JComboBox<>(new String[]{"8000 Hz", "16000 Hz", "22050 Hz", "44100 Hz", "48000 Hz"});
        panel.add(resamplingCheck);
        panel.add(resamplingCombo, "wrap");

        // Noise Reduction
        noiseReductionCheck = new JCheckBox("Noise Reduction");
        noiseReductionCheck.setFont(FontHelper.getAnticycloneFont(Font.PLAIN, 11f));
        noiseReductionCombo = new JComboBox<>(new String[]{"Spectral Subtraction", "Simple Filtering"});
        panel.add(noiseReductionCheck);
        panel.add(noiseReductionCombo, "wrap");

        // Normalization
        normalCheck = new JCheckBox("Normalization (dBFS)");
        normalCheck.setFont(FontHelper.getAnticycloneFont(Font.PLAIN, 11f));
        normalSpinner = new JSpinner(new SpinnerNumberModel(-1.0, -100.0, 0.0, 0.1));
        panel.add(normalCheck);
        panel.add(normalSpinner, "wrap");

        // High-Pass Filter
        hpFilterCheck = new JCheckBox("High-Pass Filter (Hz)");
        hpFilterCheck.setFont(FontHelper.getAnticycloneFont(Font.PLAIN, 11f));
        hpSpinner = new JSpinner(new SpinnerNumberModel(100, 0, 20000, 10));
        panel.add(hpFilterCheck);
        panel.add(hpSpinner, "wrap");

        // Silent Interval Removal
        silentCheck = new JCheckBox("Silent Interval Removal");
        silentCheck.setFont(FontHelper.getAnticycloneFont(Font.PLAIN, 11f));
        panel.add(silentCheck, "span 2, wrap");
    }

    /**
     * Natively extracts and converts the UI state into a machine-readable configuration map.
     */
    public Map<String, Object> exportSettings() {
        Map<String, Object> settings = new LinkedHashMap<>();
        
        settings.put("resampling", Map.of("enabled", resamplingCheck.isSelected(), "target", resamplingCombo.getSelectedItem()));
        settings.put("noise_reduction", Map.of("enabled", noiseReductionCheck.isSelected(), "method", noiseReductionCombo.getSelectedItem()));
        settings.put("normalization_dbfs", Map.of("enabled", normalCheck.isSelected(), "value", normalSpinner.getValue()));
        settings.put("high_pass_hz", Map.of("enabled", hpFilterCheck.isSelected(), "frequency", hpSpinner.getValue()));
        settings.put("silent_removal", silentCheck.isSelected());
        
        return settings;
    }
}
