package com.speech.model;

import java.util.List;
import java.util.Map;

/**
 * High-fidelity model representing the complete speech extraction configuration.
 * Used for serialized JSON export in the output/ directory.
 */
public class ExtractionConfig {
    private List<String> audioFiles;
    private Map<String, Object> preprocessingSettings;
    private Map<String, Boolean> featureSelection;

    public ExtractionConfig(List<String> audioFiles, 
                            Map<String, Object> preprocessingSettings, 
                            Map<String, Boolean> featureSelection) {
        this.audioFiles = audioFiles;
        this.preprocessingSettings = preprocessingSettings;
        this.featureSelection = featureSelection;
    }

    // Getters for GSON serialization (though GSON uses fields directly)
    public List<String> getAudioFiles() { return audioFiles; }
    public Map<String, Object> getPreprocessingSettings() { return preprocessingSettings; }
    public Map<String, Boolean> getFeatureSelection() { return featureSelection; }
}
