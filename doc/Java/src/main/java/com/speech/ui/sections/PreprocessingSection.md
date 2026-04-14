# PreprocessingSection.java Documentation

## Location
`Java/src/main/java/com/speech/ui/sections/PreprocessingSection.java`

## Overview
A Dashboard component dedicated to allowing the user to configure automated Digital Signal Processing (DSP) steps that run conditionally over raw audio before mathematical feature extraction takes place.

## Key Responsibilities
- Houses dynamically layered checkboxes, comboboxes, and numeric spinners representing DSP capabilities.
- Supports configuring: target Resampling Rates (16000 Hz, 44100 Hz), Noise Reduction methods (Spectral Subtraction vs Simple filtering), Decibel Normalization limits (dBFS), and aggressive High-Pass Butterworth filtering ranges natively.
- Provides an `exportSettings()` function designed identically to map to the structure expected by the Python Librosa preprocessing core engine via the `ExtractionConfig` model.
