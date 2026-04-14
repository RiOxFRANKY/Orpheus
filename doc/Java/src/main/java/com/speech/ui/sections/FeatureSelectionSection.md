# FeatureSelectionSection.java Documentation

## Location
`Java/src/main/java/com/speech/ui/sections/FeatureSelectionSection.java`

## Overview
A Dashboard component dedicated specifically to allowing granular user selection of exactly which mathematical speech feature extraction pipelines should run dynamically.

## Key Responsibilities
- Builds a dynamically scaling internal layout separated into 3 main pillars (Cepstral & Tonal, Spectral, and Prosodic/Energy).
- Manages a master list of checkboxes representing selectable features (MFCC, Pitch, Chroma, etc).
- Provides global `Select All` and `Deselect All` utility buttons for ease of use.
- Exposes `exportSelections()` API to the `ExecutionSection` to gather boolean states natively.
