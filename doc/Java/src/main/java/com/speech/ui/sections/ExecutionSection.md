# ExecutionSection.java Documentation

## Location
`Java/src/main/java/com/speech/ui/sections/ExecutionSection.java`

## Overview
The "Run" or "Execution" section of the Dashboard. It serves as the primary bridge between the front-end Java state and the FastAPI Python core.

## Key Responsibilities
- Houses the primary call-to-action button ("Run") with a `SpecialGlow` AnimatedButton.
- Manages a UI ProgressBar and a Read-Only Console Text Area to stream real-time pipeline logs back to the user seamlessly.
- Aggregates configuration states organically from its sibling sections (`InputSection`, `PreprocessingSection`, `FeatureSelectionSection`).
- Serializes the settings into an `extraction_settings.json` file in target output directory.
- Initiates background HTTP requests to `http://127.0.0.1:9999/api/config`.
- Utilizes `SwingWorker` for background polling of the `/api/status` endpoint so as to not block the main Event Thread, dynamically syncing the progress bar and console log.
