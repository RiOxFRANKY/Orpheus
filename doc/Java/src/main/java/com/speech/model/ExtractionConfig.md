# ExtractionConfig.java Documentation

## Location
`Java/src/main/java/com/speech/model/ExtractionConfig.java`

## Overview
This class acts as a data model representing the configuration that User sets up using the Orpheus UI. 

## Key Responsibilities
- Holds lists of target audio files (`audioFiles`).
- Holds a map of required preprocessing pipelines (`preprocessingSettings`).
- Holds a map of selected speech feature extractors (`featureSelection`).
- Primarily structured to be easily serialized into JSON format using GSON so it can be passed to the Python Backend.
