# Orpheus Audio Dashboard 🎶

Orpheus is a powerful, dual-architecture **Speech & Audio Feature Extraction System**. It combines a sleek, modern desktop interface written in Java with an incredibly fast computational Machine Learning backend driven by Python (`librosa`, `scipy`). 

The Orpheus pipeline is designed to automate complex digital signal processing (DSP). You can dynamically ingest raw audio files (`.wav`, `.mp3`), instantly apply deep preprocessing operations (like Butterworth High-Pass filters and Spectral Subtraction Noise Reduction), and export massive arrays of mathematical data points (MFCCs, Chroma, F0 Pitch, Shimmer, HNR, Spectral Centroids) strictly into finalized CSV datasets ready for Artificial Intelligence training!

## ✨ Key Features
- **Modern GUI Application**: Built natively in Java using `FlatLaf` Dark Themes, SVG Salamander icons, and MigLayout.
- **Python Machine Learning Engine**: Completely decoupled `FastAPI` REST server serving `librosa` pipelines on localhost.
- **Deep Control Matrix**: Filter specific features via toggle buttons to save on computing power (dynamically loads only required Python Extractors).
- **Auto-Bootstrapping Backend**: Does not require users to understand virtual environments; internally scaffolds `.venv` setups on demand!
- **Cross-Lingual Bridging**: Achieved strictly via localized `JSON` configuration maps passed through HTTP protocols.

---

## ⚡ Installation (For Users)
The absolute easiest way to run Orpheus is to use the official GitHub Release Bundle!
1. Go to the **Releases** tab on GitHub and download `Orpheus_Release_v1.x.zip`. 
2. Extract the folder anywhere on your Windows PC.
3. You must have **Java 17+** and **Python 3.10+** installed.
4. Double-click `Start-Orpheus.bat`!
   - On your very first run, it will automatically download the heavy `librosa` machine-learning libraries into a hidden folder for you safely.
   - It will automatically launch the UI and the server together!

---

## 💻 Developer Setup (For Contributors)
If you want to manually edit the source code and compile Orpheus yourself:

### Prerequisites:
- JDK 17+
- Maven (`mvn`)
- Python 3.10+

### Steps:
1. Clone the repository natively.
2. Ensure you are in the root directory.
3. On Windows, just execute `.\run.ps1` in PowerShell.
   > The developer PS1 script will automatically invoke Maven to natively compile the UI code dynamically, while spinning up `uvicorn` in a detached secondary window!

---

## 🛠️ Tech Stack
- **Frontend GUI**: Java Swing, Maven, FlatLaf, GSON
- **Backend Core**: Python 3.10, FastAPI, Uvicorn 
- **DSP Engine**: Librosa, NumPy, SciPy, NoiseReduce
- **Distribution**: PowerShell Automated Batching, Maven Shade Plugin