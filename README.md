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

## 🐳 Running with Docker (Recommended for New Systems)

Docker lets you run the full Orpheus backend on **any machine** with zero Python, Maven, or library setup.
You only need **Java 17+** on the host to run the GUI window.

### What you need
| Requirement | Where to get it |
|---|---|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | docker.com — free |
| Java 17+ JRE | [Adoptium](https://adoptium.net/) — only for the GUI |

---

### Step 1 — Clone & build
```bash
git clone https://github.com/YourUsername/Orpheus.git
cd Orpheus
docker-compose up --build
```

This single command will:
- Download JDK 17, Maven, Python, and all ML libraries automatically inside Docker
- Compile the Java fat JAR
- Install librosa, scipy, FastAPI, and every Python dependency
- Start the FastAPI backend on **port 9999**

Wait until you see this line in the terminal:
```
Uvicorn running on http://0.0.0.0:9999 (Press CTRL+C to quit)
```
The server is ready. Verify at → **http://localhost:9999/**

---

### Step 2 — Get the Java GUI JAR

The Dockerfile compiles the Java JAR during the build. Copy it to your host with one command:

```bash
docker cp orpheus-backend:/app/Java/SpeechDashboard.jar ./SpeechDashboard.jar
```

> **Note:** You only need to do this once. The JAR works permanently on your machine after that.

---

### Step 3 — Launch the GUI

```bash
java -jar SpeechDashboard.jar
```

The GUI will open and automatically connect to the backend running in Docker at `localhost:9999`. Everything works exactly as if you had set up Python locally.

---

### Step 4 — Place your audio files

The container shares two folders with your host machine via volume mounts:

| Drop files here (on your PC) | Referenced as this inside Docker |
|---|---|
| `./data/input/` | `/app/Python/input/` |
| `./data/output/` | `/app/Python/output/` |

Create the folders if they don't exist yet:
```bash
mkdir -p data/input data/output
```
Copy your `.wav` or `.mp3` files into `data/input/`, then use the path `/app/Python/input/your_file.wav` when selecting files in the GUI.

All results (CSV, processed audio, ZIP archive) will appear in `data/output/` on your host automatically.

---

### Useful commands

| Task | Command |
|---|---|
| First-time build + start | `docker-compose up --build` |
| Start in background | `docker-compose up -d` |
| View live logs | `docker-compose logs -f` |
| Stop the backend | `docker-compose down` |
| Rebuild after code changes | `docker-compose up --build` |
| Build image only | `docker build -t orpheus:latest .` |
| Run image without compose | `docker run -p 9999:9999 orpheus:latest` |

---

## 🛠️ Tech Stack

- **Frontend GUI**: Java Swing, Maven, FlatLaf, GSON
- **Backend Core**: Python 3.10, FastAPI, Uvicorn 
- **DSP Engine**: Librosa, NumPy, SciPy, NoiseReduce
- **Distribution**: PowerShell Automated Batching, Maven Shade Plugin