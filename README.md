# Orpheus 🎙️
### High-Fidelity Speech Feature Extraction Dashboard

Orpheus is a modern, high-performance Java Swing dashboard designed to streamline the preprocessing and feature extraction pipeline for speech processing and machine learning workflows.

---

## 🚀 Key Features

### 1. Intelligent Audio Input
- **Sanitized Browsing**: Native file filters restricted exclusively to audio formats (`.wav`, `.mp3`, `.ogg`, `.flac`, etc.) to prevent invalid data entry.
- **Batch Processing**: Support for multi-file selection and real-time status tracking in an elastic HUD table.
- **Reactive Controls**: The extraction engine stays disabled until valid audio files are detected.

### 2. Advanced Preprocessing HUD
- Granular control over **Resampling**, **Noise Reduction** (Spectral Subtraction), **Normalization (dBFS)**, and **High-Pass Filtering**.
- **Silent Interval Removal** toggle for optimized data density.

### 3. Comprehensive Feature Selection
- Categorized selection for:
  - **Cepstral & Tonal**: MFCCs, Chroma Features.
  - **Spectral**: Zero-Crossing Rate, Centroid, Bandwidth, Roll-Off.
  - **Prosodic & Energy**: Pitch (F0), RMSE, Shimmer, Jitter, HNR.
- **Bulk Utility**: Instant "Select All" and "Deselect All" logic for rapid prototyping.

### 4. JSON Configuration Engine
- **One-Click Export**: Converts the entire dashboard state (relative file paths, preprocessing parameters, and feature toggles) into a professionally formatted `extraction_settings.json`.
- **Output Management**: Automatically generates and manages an `output/` directory for configuration persistence.

### 5. Premium UI/UX Design
- **Responsive Architecture**: Hand-tuned **MigLayout** configurations with "Smart Scroll" fallback—the UI remains elastic at high resolutions but provides master scrollbars for ultra-compact views (min-size: 800x600).
- **Dual-Theme Engine**: Smooth, animated transition between **Modern Dark** and **Clean Light** modes via a custom animated HUD switch.
- **Rich Visuals**: Integrated SVG icons and high-fidelity typography using the **Glonto** and **Anticyclone** font families.

---

## 🛠️ Technology Stack
- **Languages**: Java 17+
- **Build System**: Maven
- **Look & Feel**: [FlatLaf](https://github.com/JFormDesigner/FlatLaf) (Modern Swing L&F)
- **Layout Engine**: [MigLayout](http://www.miglayout.com/) (Fluid, elastic grid system)
- **Serialization**: [Google GSON](https://github.com/google/gson)
- **Graphics**: [SVG Salamander](https://github.com/blackberry/SVG-Salamander)

---

## 📦 Getting Started

### Prerequisites
- JDK 17 or higher
- Apache Maven

### Installation & Run
```bash
# Clone the repository
git clone https://github.com/RiOxFRANKY/Orpheus.git

# Navigate to the Java source
cd Orpheus/Java

# Clean, Compile and Launch
mvn clean compile exec:java
```

---

## 📄 License
Project status: **Operational / Feature Extraction Ready**