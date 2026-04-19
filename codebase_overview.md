# Orpheus Audio Dashboard — Codebase Overview 🎶

## What Is It?

**Orpheus** is a dual-architecture **Speech & Audio Feature Extraction System**. A modern desktop GUI (Java/Swing) acts as the front-end; a Python REST API (FastAPI + Librosa) acts as the ML/DSP computation engine. Communication between the two is pure HTTP/JSON over localhost.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────┐
│           Java Desktop GUI (Swing)          │
│   FlatLaf Dark Theme · MigLayout · GSON     │
│                                             │
│  InputSection → PreprocessingSection        │
│  FeatureSelectionSection → ExecutionSection │
│  OutputSection                              │
└──────────────────┬──────────────────────────┘
                   │  HTTP/JSON  (localhost:9999)
┌──────────────────▼──────────────────────────┐
│         Python FastAPI Backend              │
│   Uvicorn · Librosa · SciPy · NumPy         │
│                                             │
│  POST /api/config   → start pipeline        │
│  GET  /api/status   → poll progress         │
│  GET  /api/download/csv  → download CSV     │
│  GET  /api/download/zip  → download archive │
└─────────────────────────────────────────────┘
```

---

## Repository Layout

```
Orpheus/
├── Java/                   # Desktop GUI (Maven project)
│   ├── pom.xml
│   └── src/main/java/com/speech/
│       ├── App.java                    # Entry point
│       ├── model/
│       │   └── ExtractionConfig.java   # POJO matching Python's Pydantic model
│       ├── ui/
│       │   ├── MainDashboard.java      # Root JFrame, assembles sections
│       │   ├── ThemeSwitch.java        # Light/Dark toggle
│       │   ├── AbstractDashboardSection.java
│       │   ├── DashboardSection.java   # Interface
│       │   ├── components/
│       │   │   └── AnimatedButton.java
│       │   └── sections/
│       │       ├── InputSection.java           # File picker
│       │       ├── PreprocessingSection.java   # Preprocessing toggles/knobs
│       │       ├── FeatureSelectionSection.java# Feature checkboxes (MFCC, Chroma, etc.)
│       │       ├── ExecutionSection.java       # Run button, progress bar, SwingWorker
│       │       └── OutputSection.java          # Download buttons
│       └── util/
│           ├── FontHelper.java         # Loads Anticyclone custom font
│           └── SVGIconHelper.java      # Loads SVG icons via SVG Salamander
│
├── Python/                 # ML/DSP Backend (FastAPI)
│   ├── main.py             # FastAPI app, endpoints, thread pool
│   ├── requirements.txt    # librosa, fastapi, uvicorn, soundfile, noisereduce…
│   ├── core/               # Abstract base classes
│   │   ├── base_extractor.py
│   │   ├── base_preprocessor.py
│   │   └── base_exporter.py
│   ├── preprocessing/      # DSP preprocessing steps
│   │   ├── resampler.py
│   │   ├── highpass_filter.py   # Butterworth HPF (SciPy)
│   │   ├── noise_reducer.py     # Spectral gating (noisereduce)
│   │   ├── silence_remover.py   # librosa trim
│   │   └── normalizer.py        # dBFS normalisation
│   ├── extractors/         # Feature extraction modules
│   │   ├── mfcc_extractor.py
│   │   ├── chroma_extractor.py
│   │   ├── spectral_extractor.py  # centroid, bandwidth, rolloff, contrast, flatness
│   │   ├── zcr_extractor.py
│   │   ├── pitch_extractor.py     # F0, jitter
│   │   ├── energy_extractor.py    # RMS, shimmer, HNR
│   │   └── temporal_extractor.py  # tempo, duration
│   ├── services/
│   │   └── extraction_service.py  # Orchestrator (preprocess → extract → export)
│   ├── exporters/
│   │   └── csv_exporter.py
│   └── output/             # Runtime output directory
│       ├── processed/      # Preprocessed WAVs
│       ├── features/       # features.csv
│       └── archives/       # speech_features.zip
│
├── .venv/                  # Auto-bootstrapped Python venv
├── run.ps1                 # Windows dev launcher (starts uvicorn + Maven)
├── run.sh                  # Linux/macOS equivalent
└── doc/                    # Documentation assets
```

---

## Data Flow (End-to-End)

```
User drops audio files (WAV/MP3)
     ↓
InputSection (Java) — collects file paths
     ↓
PreprocessingSection — enables: resample, HPF, noise reduction, silence removal, normalize
FeatureSelectionSection — toggles: MFCC, Chroma, Spectral, ZCR, Pitch, Energy, Temporal
     ↓
ExecutionSection sends POST /api/config
  {
    audioFiles: [...],
    preprocessingSettings: { noiseReduction: true, high_pass_hz: 80, ... },
    featureSelection: { mfcc: true, chroma: true, ... }
  }
     ↓
Python ExtractionService.run()
  1. Resolve & validate file paths
  2. Build preprocessing chain (fixed order: Resample → HPF → Noise → Silence → Normalize)
  3. Build extractors (deduplicated by class, from registry map)
  4. For each file: load → preprocess → save processed WAV → extract features → accumulate row
  5. Export all rows → features.csv
  6. Zip (processed WAVs + CSV) → speech_features.zip
     ↓
Java SwingWorker polls GET /api/status every ~500ms → updates progress bar
     ↓
OutputSection — Download CSV / Download ZIP buttons hit
  GET /api/download/csv   → FileResponse
  GET /api/download/zip   → FileResponse
```

---

## Tech Stack Summary

| Layer | Technology |
|---|---|
| Desktop UI | Java 17, Java Swing |
| UI Theme | FlatLaf 3.4 (Mac Dark) |
| UI Layout | MigLayout 11.4.2 |
| Icons | SVG Salamander |
| JSON Serialization | GSON 2.11 |
| Build | Maven + Shade Plugin (fat JAR) |
| API Server | FastAPI + Uvicorn (port 9999) |
| Audio Loading | Librosa, SoundFile |
| DSP Filters | SciPy (Butterworth), NoiseReduce |
| Feature Extraction | Librosa, NumPy |
| Data Export | CSV (Python csv module) |
| Packaging | PowerShell / Bash launchers |

---

## Key Design Patterns

- **Registry Pattern**: Both `_EXTRACTOR_REGISTRY` and `_PREPROCESSOR_REGISTRY` in `extraction_service.py` map string keys (from JSON) to Python classes, making it trivial to add new extractors/preprocessors.
- **Fixed Preprocessor Order**: Preprocessing always runs in a canonical order regardless of what the GUI enables (`Resample → HPF → NoiseReduce → SilenceRemove → Normalize`).
- **Base Classes**: `BaseFeatureExtractor`, `BasePreprocessor`, `BaseExporter` define the contract all plugins must implement.
- **SwingWorker + Polling**: Java avoids blocking the EDT by using `SwingWorker` to poll `/api/status` on a background thread.
- **Thread Pool**: Python runs the CPU-heavy pipeline in a `ThreadPoolExecutor` to keep the async FastAPI event loop free.
- **Auto-bootstrap**: The launcher scripts create and populate the `.venv` automatically on first run.

---

## Entry Points

| How | Command |
|---|---|
| **Dev (Windows)** | `.\run.ps1` in repo root |
| **Dev (Linux/Mac)** | `./run.sh` in repo root |
| **Python only** | `uvicorn main:app --host 127.0.0.1 --port 9999` (from `Python/`) |
| **Java only** | `mvn clean compile exec:java` (from `Java/`) |
