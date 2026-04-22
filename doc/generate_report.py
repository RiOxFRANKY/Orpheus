"""
Orpheus Audio Dashboard — PDF Project Report Generator
Run: python doc/generate_report.py
Output: doc/Orpheus_Project_Report.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.lib.utils import ImageReader
import os
from reportlab.platypus.flowables import Flowable

OUTPUT_PATH = "doc/Orpheus_Project_Report.pdf"

# ── Colour palette (black & white) ──────────────────────────────────────────
PURPLE      = colors.HexColor("#1A1A1A")   # near-black  (was purple)
PURPLE_LIGHT= colors.HexColor("#F0F0F0")   # light gray  (was purple-light)
PURPLE_MID  = colors.HexColor("#333333")   # dark gray   (was purple-mid)
CYAN        = colors.HexColor("#555555")   # mid gray    (was cyan)
CYAN_LIGHT  = colors.HexColor("#F5F5F5")   # near-white  (was cyan-light)
GREEN       = colors.HexColor("#444444")   # dark gray   (was green)
GREEN_LIGHT = colors.HexColor("#F0F0F0")   # light gray  (was green-light)
DARK        = colors.HexColor("#111111")   # black text
MUTED       = colors.HexColor("#666666")   # medium gray
BORDER      = colors.HexColor("#CCCCCC")   # light gray border
SURFACE     = colors.HexColor("#F7F7F7")   # off-white row bg
WHITE       = colors.white
CODE_BG     = colors.HexColor("#2B2B2B")   # dark gray code bg
CODE_FG     = colors.HexColor("#F0F0F0")   # near-white code text

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

body   = S("body",   fontName="Helvetica",       fontSize=9.5,  leading=15,  textColor=DARK,  spaceAfter=6)
bodyJ  = S("bodyJ",  fontName="Helvetica",       fontSize=9.5,  leading=15,  textColor=DARK,  spaceAfter=6, alignment=TA_JUSTIFY)
h1     = S("h1",     fontName="Helvetica-Bold",  fontSize=28,   leading=34,  textColor=WHITE, spaceAfter=6,  alignment=TA_CENTER)
h2     = S("h2",     fontName="Helvetica-Bold",  fontSize=14,   leading=20,  textColor=WHITE, spaceAfter=4)
h3     = S("h3",     fontName="Helvetica-Bold",  fontSize=10.5, leading=15,  textColor=DARK,  spaceAfter=4, spaceBefore=10)
h4     = S("h4",     fontName="Helvetica-Bold",  fontSize=9.5,  leading=14,  textColor=DARK,  spaceAfter=3, spaceBefore=6)
code   = S("code",   fontName="Courier",         fontSize=8.5,  leading=13,  textColor=CODE_FG, backColor=CODE_BG,
           leftIndent=8, rightIndent=8, spaceAfter=8, spaceBefore=4)
muted_s= S("muted",  fontName="Helvetica",       fontSize=8.5,  leading=13,  textColor=MUTED, spaceAfter=4)
cover_sub = S("csub",fontName="Helvetica",       fontSize=12,   leading=18,  textColor=MUTED, alignment=TA_CENTER)
tag_s  = S("tag",    fontName="Helvetica-Bold",  fontSize=8,    leading=12,  textColor=MUTED, alignment=TA_CENTER)
bullet = S("bullet", fontName="Helvetica",       fontSize=9.5,  leading=15,  textColor=DARK,  leftIndent=12, bulletIndent=0, spaceAfter=2)
callout_s = S("callout", fontName="Helvetica",   fontSize=9,    leading=14,  textColor=DARK,  leftIndent=10, rightIndent=10)


# ── Helper flowables ─────────────────────────────────────────────────────────

class ColorRect(Flowable):
    """A simple filled rectangle, used for section header backgrounds."""
    def __init__(self, width, height, fill_color, radius=4):
        super().__init__()
        self.width  = width
        self.height = height
        self.fill   = fill_color
        self.radius = radius

    def draw(self):
        self.canv.setFillColor(self.fill)
        self.canv.roundRect(0, 0, self.width, self.height, self.radius, fill=1, stroke=0)


def section_header(title, emoji=""):
    """Returns a framed section heading block."""
    content_width = PAGE_W - 2 * MARGIN
    text = f"{emoji}  {title}" if emoji else title
    return KeepTogether([
        Spacer(1, 14),
        Table(
            [[Paragraph(text, h2)]],
            colWidths=[content_width],
            style=TableStyle([
                ("BACKGROUND",    (0,0), (-1,-1), PURPLE),
                ("ROUNDEDCORNERS",(0,0), (-1,-1), [6]),
                ("TOPPADDING",    (0,0), (-1,-1), 9),
                ("BOTTOMPADDING", (0,0), (-1,-1), 9),
                ("LEFTPADDING",   (0,0), (-1,-1), 14),
            ]),
        ),
        Spacer(1, 8),
    ])


def callout(text, bg=PURPLE_LIGHT, border=PURPLE, label="Note"):
    cw = PAGE_W - 2 * MARGIN
    lbl = Paragraph(f"<b>{label.upper()}</b>", ParagraphStyle("cl", fontName="Helvetica-Bold",
        fontSize=7.5, textColor=border, leading=12))
    txt = Paragraph(text, callout_s)
    return KeepTogether([
        Spacer(1, 4),
        Table([[lbl], [txt]], colWidths=[cw - 16],
            style=TableStyle([
                ("BACKGROUND",   (0,0), (-1,-1), bg),
                ("LINEAFTER",   (0,0), (0,-1), 4, border),
                ("LEFTPADDING",  (0,0), (-1,-1), 12),
                ("RIGHTPADDING", (0,0), (-1,-1), 12),
                ("TOPPADDING",   (0,0), (-1,-1), 8),
                ("BOTTOMPADDING",(0,0), (-1,-1), 8),
                ("ROUNDEDCORNERS",(0,0),(-1,-1),[4]),
            ]),
        ),
        Spacer(1, 8),
    ])


def std_table(headers, rows, col_widths=None):
    cw = PAGE_W - 2 * MARGIN
    if col_widths is None:
        n = len(headers)
        col_widths = [cw / n] * n

    def cell(s, bold=False):
        style = ParagraphStyle("tc", fontName="Helvetica-Bold" if bold else "Helvetica",
            fontSize=8.5, leading=13, textColor=WHITE if bold else DARK)
        return Paragraph(str(s), style)

    data = [[cell(h, bold=True) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), ParagraphStyle("tr", fontName="Helvetica",
            fontSize=8.5, leading=13, textColor=DARK)) for c in row])

    ts = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), PURPLE),
        ("BACKGROUND",    (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, SURFACE]),
        ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ])
    return KeepTogether([Table(data, colWidths=col_widths, style=ts), Spacer(1, 10)])


def code_block(text):
    lines = [Paragraph(line.replace(" ", "&nbsp;"), code) for line in text.strip().split("\n")]
    cw = PAGE_W - 2 * MARGIN
    return KeepTogether([
        Spacer(1, 4),
        Table([[item] for item in lines], colWidths=[cw],
            style=TableStyle([
                ("BACKGROUND",   (0,0), (-1,-1), CODE_BG),
                ("TOPPADDING",   (0,0), (-1,-1), 2),
                ("BOTTOMPADDING",(0,0), (-1,-1), 2),
                ("LEFTPADDING",  (0,0), (-1,-1), 14),
                ("RIGHTPADDING", (0,0), (-1,-1), 14),
            ]),
        ),
        Spacer(1, 8),
    ])


def bullets(items):
    return [Paragraph(f"• &nbsp;{item}", bullet) for item in items]


def two_col_table(left_title, left_items, right_title, right_items):
    cw = PAGE_W - 2 * MARGIN

    def card(title, items):
        rows = [Paragraph(f"• {it}", ParagraphStyle("ci", fontName="Helvetica", fontSize=8.5, leading=14, textColor=DARK))]
        return [Paragraph(title, ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=8.5, leading=14, textColor=PURPLE))] + \
               [Paragraph(f"• {it}", ParagraphStyle("ci", fontName="Helvetica", fontSize=8.5, leading=14, textColor=DARK)) for it in items]

    left_content  = "\n".join([left_title]  + [f"• {it}" for it in left_items])
    right_content = "\n".join([right_title] + [f"• {it}" for it in right_items])

    def make_cell(title, items):
        inner = [[Paragraph(title, ParagraphStyle("boxh", fontName="Helvetica-Bold", fontSize=9, textColor=DARK, leading=14))]]
        for it in items:
            inner.append([Paragraph(f"• {it}", ParagraphStyle("boxi", fontName="Helvetica", fontSize=8.5, textColor=DARK, leading=14))])
        return Table(inner, colWidths=[(cw/2)-8], style=TableStyle([
            ("BACKGROUND",   (0,0),(-1,-1), SURFACE),
            ("BOX",          (0,0),(-1,-1), 0.5, BORDER),
            ("TOPPADDING",   (0,0),(-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
            ("LEFTPADDING",  (0,0),(-1,-1), 10),
            ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ]))

    t = Table([[make_cell(left_title, left_items), make_cell(right_title, right_items)]],
              colWidths=[cw/2, cw/2],
              style=TableStyle([("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]))
    return KeepTogether([t, Spacer(1,10)])

def insert_screenshot(story, path):
    if not os.path.exists(path):
        return
    ir = ImageReader(path)
    iw, ih = ir.getSize()
    ratio = ih / iw
    img = Image(path, width=PAGE_W - 2*MARGIN, height=(PAGE_W - 2*MARGIN)*ratio)
    story.append(img)
    story.append(Spacer(1, 10))


# ── Page templates ───────────────────────────────────────────────────────────

def on_first_page(canvas, doc):
    canvas.saveState()
    # Black header banner
    canvas.setFillColor(colors.black)
    canvas.rect(0, PAGE_H - 120*mm, PAGE_W, 130*mm, fill=1, stroke=0)
    # Thin black bar at bottom
    canvas.setFillColor(colors.black)
    canvas.rect(0, 0, PAGE_W, 2, fill=1, stroke=0)
    canvas.restoreState()


def on_later_pages(canvas, doc):
    canvas.saveState()
    # Thin top rule
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 12*mm, PAGE_W - MARGIN, PAGE_H - 12*mm)
    # Header text
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, PAGE_H - 10*mm, "Orpheus Audio Dashboard — Project Report")
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 10*mm, f"Page {doc.page}")
    # Footer line
    canvas.setStrokeColor(BORDER)
    canvas.line(MARGIN, 12*mm, PAGE_W - MARGIN, 12*mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(PAGE_W / 2, 8*mm, "Python 3.11 + FastAPI + Librosa  ·  Java 17 + Swing + FlatLaf  ·  Docker")
    canvas.restoreState()


# ── Build document ───────────────────────────────────────────────────────────

def build():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN + 4*mm, bottomMargin=20*mm,
        title="Orpheus Audio Dashboard — Project Report",
        author="Orpheus Project",
    )

    story = []
    cw = PAGE_W - 2 * MARGIN

    # ── COVER PAGE ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 52*mm))
    story.append(Paragraph("PROJECT REPORT", tag_s))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Orpheus Audio Dashboard", h1))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "A Dual-Architecture Speech &amp; Audio Feature Extraction System<br/>"
        "combining a Java Swing desktop GUI with a Python FastAPI ML backend.",
        cover_sub))
    story.append(Spacer(1, 24))

    meta = [
        ["Category",  "Digital Signal Processing / AI Tooling"],
        ["Backend",   "Python 3.11 · FastAPI · Uvicorn · Librosa · SciPy"],
        ["Frontend",  "Java 17 · Swing · FlatLaf 3.4 · MigLayout"],
        ["Transport", "HTTP/JSON over localhost:9999"],
        ["Distribution", "Docker (multi-stage) · Maven Shade Fat JAR"],
        ["Version",   "1.0"],
    ]
    story.append(
        Table(
            [[Paragraph(k, ParagraphStyle("mk", fontName="Helvetica-Bold", fontSize=8, textColor=DARK, leading=13)),
              Paragraph(v, ParagraphStyle("mv", fontName="Helvetica",      fontSize=8.5, textColor=DARK, leading=13))]
             for k, v in meta],
            colWidths=[40*mm, cw - 40*mm],
            style=TableStyle([
                ("BACKGROUND",   (0,0),(-1,-1), PURPLE_LIGHT),
                ("BOX",          (0,0),(-1,-1), 0.5, BORDER),
                ("LINEBELOW",    (0,0),(-1,-2), 0.4, BORDER),
                ("TOPPADDING",   (0,0),(-1,-1), 6),
                ("BOTTOMPADDING",(0,0),(-1,-1), 6),
                ("LEFTPADDING",  (0,0),(-1,-1), 12),
                ("RIGHTPADDING", (0,0),(-1,-1), 12),
            ]),
        )
    )
    story.append(PageBreak())

    # ── PROJECT TEAM ─────────────────────────────────────────────────────────
    story.append(Paragraph("Project Team & Contributions", ParagraphStyle("toch",
        fontName="Helvetica-Bold", fontSize=13, textColor=DARK, leading=20, spaceAfter=10)))
    
    story.append(std_table(
        ["Team Member", "Domain", "Primary Contributions"],
        [
            ["Abhirup Sarkar", "Integration Lead", "Feature selection logic, cross-language JSON serialization, Execution state, and async SwingWorker orchestration. (Major Contribution)"],
            ["Aayush Dey",     "Frontend", "Input/Output interface components and basic file save dialogs. (Minor Contribution)"],
            ["Toufik Mamud",   "Backend", "Core DSP preprocessing algorithms and librosa feature extraction implementation. (Major Contribution)"],
            ["Subhrojyoti Bala", "Backend Lead", "FastAPI server infrastructure, REST endpoints, ThreadPool execution management, data flow, and containerization. (Major Contribution)"],
            ["Anwesha",        "Frontend", "Assisted with GUI architecture, UI/UX design, and FlatLaf theming. (Minor Contribution)"],
        ],
        col_widths=[35*mm, 30*mm, cw - 65*mm]
    ))
    story.append(Spacer(1, 10*mm))

    # ── TABLE OF CONTENTS ────────────────────────────────────────────────────
    story.append(Paragraph("Table of Contents", ParagraphStyle("toch",
        fontName="Helvetica-Bold", fontSize=13, textColor=DARK, leading=20, spaceAfter=10)))
    toc_items = [
        ("1.", "Project Overview"),
        ("2.", "System Architecture"),
        ("3.", "End-to-End Data Flow"),
        ("4.", "DSP Preprocessing Pipeline"),
        ("5.", "Feature Extraction Modules"),
        ("6.", "Complete Feature Inventory"),
        ("7.", "Java Desktop GUI"),
        ("8.", "REST API Reference"),
        ("9.", "Docker Deployment"),
        ("10.", "Tech Stack Summary"),
        ("11.", "Repository Structure"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(
            f'<b>{num}</b>&nbsp;&nbsp;{title}',
            ParagraphStyle("toc", fontName="Helvetica", fontSize=10, leading=18, textColor=DARK, leftIndent=4)))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    story.append(Spacer(1, 6))

    # ════════════════════════════════════════════════════════════════════════
    # 1. PROJECT OVERVIEW
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("1.  Project Overview", "🎶"))
    story.append(Paragraph(
        "<b>Orpheus</b> is a production-grade, dual-architecture audio analysis platform that automates the "
        "extraction of acoustic feature vectors from raw speech and audio recordings. It is designed for AI "
        "researchers, speech scientists, and data engineers who need structured, machine-learning-ready CSV "
        "datasets from large audio collections — without writing any DSP code themselves.",
        bodyJ))
    story.append(Paragraph(
        "The system consists of two fully decoupled components that communicate exclusively over HTTP/JSON "
        "on localhost. This makes each layer independently upgradeable, testable, and deployable.",
        bodyJ))

    story.append(two_col_table(
        "Java Desktop GUI",
        ["Built with Java 17 Swing + FlatLaf Dark theme",
         "Drag-and-drop audio file ingestion",
         "Toggle-based preprocessing and feature controls",
         "Live progress bar via SwingWorker HTTP polling",
         "One-click CSV and ZIP download"],
        "Python FastAPI Backend",
        ["FastAPI + Uvicorn REST server on port 9999",
         "Librosa / SciPy / NumPy DSP computation engine",
         "Registry-pattern plugin architecture",
         "ThreadPoolExecutor for non-blocking CPU work",
         "Auto-creates output directories and archives"],
    ))

    story.append(Paragraph("Key Capabilities", h3))
    features = [
        "MFCC + Δ + ΔΔ → 78 features per file",
        "Chroma STFT (12 pitch classes) → 24 features",
        "Spectral Centroid, Bandwidth, Roll-off, Contrast, Flatness → 22 features",
        "F0 Pitch + Jitter via probabilistic YIN (pyin) → 5 features",
        "RMS Energy + Shimmer + HNR (autocorrelation) → 6 features",
        "Zero-Crossing Rate → 2 features",
        "Tempo (BPM) + Duration → 2 features",
        "Butterworth 4th-order High-Pass Filter (SciPy)",
        "Spectral Gating Noise Reduction (noisereduce)",
        "Docker-ready deployment — no Python install needed on host",
    ]
    story.extend(bullets(features))
    story.append(Spacer(1, 8))

    # ════════════════════════════════════════════════════════════════════════
    # 2. SYSTEM ARCHITECTURE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("2.  System Architecture", "🏗"))
    story.append(Paragraph(
        "Orpheus follows a strict <b>microservice-inspired separation of concerns</b>. The Java GUI is a "
        "pure presentation layer with no ML or DSP logic whatsoever. All computation is delegated to the "
        "Python server over HTTP. The server is stateless per-request (progress state lives in a shared "
        "dict updated by callbacks), making it straightforward to add concurrent job support in future.",
        bodyJ))
    arch = """\
┌─────────────────────────────────────────────────────┐
│           Java Desktop Application (Swing)          │
│                                                     │
│  InputSection ──► PreprocessingSection              │
│  FeatureSelectionSection ──► ExecutionSection       │
│  (SwingWorker polls /api/status every 500ms)        │
│  OutputSection  (Download CSV / ZIP)                │
└──────────────────────┬──────────────────────────────┘
                       │  HTTP/JSON  (localhost:9999)
┌──────────────────────▼──────────────────────────────┐
│         Python FastAPI ML/DSP Backend               │
│                                                     │
│  POST /api/config  ──► ExtractionService.run()      │
│                            │                        │
│              ┌─────────────┼──────────────┐         │
│          Preprocessors  Extractors  CSVExporter     │
│    (Resample, HPF,   (MFCC, Chroma,   (features     │
│     NoiseReduce,      Spectral, ZCR,   .csv +       │
│     Silence, Norm)    Pitch, Energy,   .zip)        │
│                       Temporal)                     │
│                                                     │
│  GET /api/status    GET /api/download/csv|zip       │
└─────────────────────────────────────────────────────┘"""
    story.append(code_block(arch))

    # ════════════════════════════════════════════════════════════════════════
    # 3. END-TO-END DATA FLOW
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("3.  End-to-End Data Flow", "🔄"))
    steps = [
        ("1. File Ingestion",         "User selects .wav/.mp3 files in the Java InputSection. Paths are stored as absolute strings."),
        ("2. Config Assembly",         "Java assembles an ExtractionConfig POJO (audioFiles, preprocessingSettings, featureSelection) and serialises it to JSON via GSON."),
        ("3. POST /api/config",        "JSON is sent to FastAPI. Pydantic validates the payload and the pipeline is queued as a BackgroundTask to keep the event loop free."),
        ("4. Pipeline Execution",      "ExtractionService.run() runs in a ThreadPoolExecutor. For each file: resolve path → load (librosa) → run preprocessors in order → save processed WAV → run all active extractors → accumulate feature row."),
        ("5. Progress Reporting",      "A shared status dict is updated via status_callback(). Java SwingWorker polls GET /api/status every 500 ms and renders a live progress bar."),
        ("6. Export & Archive",        "All rows are written to output/features/features.csv. Processed WAVs and the CSV are bundled into output/archives/speech_features.zip."),
        ("7. Download",               "Java OutputSection triggers GET /api/download/csv or GET /api/download/zip. FastAPI returns a FileResponse which the GUI saves to disk."),
    ]
    story.append(std_table(
        ["Step", "Description"],
        steps,
        col_widths=[38*mm, cw - 38*mm],
    ))

    # ════════════════════════════════════════════════════════════════════════
    # 4. DSP PREPROCESSING PIPELINE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("4.  DSP Preprocessing Pipeline", "⚙"))
    story.append(Paragraph(
        "All preprocessing steps are plugins conforming to the <b>BasePreprocessor</b> abstract class. "
        "Regardless of which steps the GUI enables, the execution order is always fixed and canonical to "
        "ensure deterministic, reproducible output.",
        bodyJ))
    story.append(callout(
        "Fixed Execution Order: Resample → High-Pass Filter → Noise Reduction → Silence Removal → Normalisation",
        bg=PURPLE_LIGHT, border=PURPLE, label="Fixed Order"))
    story.append(std_table(
        ["#", "Step", "Class", "Algorithm / Library", "Key Parameters"],
        [
            ["1", "Resample",          "Resampler",       "librosa.resample",                          "Supports 8kHz, 16kHz, 22.05kHz, 44.1kHz, 48kHz"],
            ["2", "High-Pass Filter",  "HighPassFilter",  "4th-order Butterworth via scipy.signal",    "Cutoff Hz (default 80 Hz)"],
            ["3", "Noise Reduction",   "NoiseReducer",    "Stationary spectral gating (noisereduce)",  "stationary=True"],
            ["4", "Silence Removal",   "SilenceRemover",  "librosa.effects.trim",                      "top_db threshold"],
            ["5", "Normalise",         "Normalizer",      "dBFS peak normalisation (NumPy)",            "Target (default −1 dBFS)"],
        ],
        col_widths=[8*mm, 28*mm, 35*mm, 60*mm, cw - 131*mm],
    ))
    story.append(Paragraph("High-Pass Filter Detail", h3))
    story.append(Paragraph(
        "A 4th-order Butterworth filter is designed with <b>scipy.signal.butter</b> and applied via "
        "<b>sosfilt</b> (second-order sections) to avoid numerical instability. "
        "The cutoff frequency is normalised to the Nyquist before design:", body))
    story.append(code_block(
        "sos = butter(4, cutoff_hz / nyquist, btype='high', output='sos')\n"
        "y_filtered = sosfilt(sos, y).astype(np.float32)"))
    story.append(Paragraph("Noise Reduction Detail", h3))
    story.append(Paragraph(
        "Spectral gating estimates the noise floor from the quietest spectral regions and subtracts it "
        "in the frequency domain. <b>stationary=True</b> assumes a consistent background noise profile:", body))
    story.append(code_block("y_clean = nr.reduce_noise(y=y, sr=sr, stationary=True)"))

    story.append(Paragraph("NumPy Vector Telemetry & Array Transformations", h3))
    story.append(Paragraph(
        "A critical aspect of the backend pipeline is the continuous logging and transformation of "
        "the audio signal, represented as a 1D NumPy array. High-resolution telemetry monitors the "
        "array's shape, value bounds, and datatype synchronously at each step of processing to guarantee "
        "data integrity before feature extraction:", bodyJ))
    
    story.append(Paragraph(
        "<b>Array Semantics:</b> The 1D NumPy array contains discrete, uncompressed floating-point "
        "samples of the audio waveform in the time domain. Each scalar value denotes the sound pressure "
        "amplitude at a specific point in time, bounded between roughly -1.0 and 1.0. The array length "
        "<i>N</i> represents the total number of frames, meaning the exact time coordinate of any given "
        "value can be derived via <code>index / sample_rate = seconds</code>.", bodyJ))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph(
        "<b>Audio to Array Conversion:</b> To generate this array, the backend uses <code>librosa.load()</code>, "
        "which relies on the <code>soundfile</code> library to decode the raw binary headers and byte streams of the "
        "<code>.wav</code> or <code>.mp3</code> files. During this ingestion phase, multi-channel stereo audio is "
        "automatically downmixed to a mono signal by averaging the spatial channels, and the native 16-bit or 24-bit "
        "integer PCM amplitudes are scaled and cast down into normalized 32-bit floating-point numbers.", bodyJ))
    story.append(Spacer(1, 4))
    story.append(std_table(
        ["Processing Phase", "NumPy Shape Change", "Value Range / Mutation", "Data Type"],
        [
            ["1. Ingestion (load)", "Native shape → (N,)",                     "Native (typically [-1.0, 1.0])", "float32"],
            ["2. Resampler",        "(N,) → (N_resampled,)",                   "Interpolated variations",        "float32"],
            ["3. High-Pass Filter", "No shape change",                         "Attenuates low-freq DC offset",  "float32"],
            ["4. Noise Reduction",  "No shape change",                         "Spectral variance reduced",      "float32"],
            ["5. Silence Removal",  "(N_resampled,) → (N_trimmed,)",           "Unchanged (silent frames dropped)","float32"],
            ["6. Normalizer",       "No shape change",                         "Strictly scaled to [-1.0, 1.0]", "float32"],
        ],
        col_widths=[32*mm, 45*mm, 58*mm, cw - 135*mm],
    ))

    example_trace = """\
[TRACE] audio_file: speech_sample.wav
[TRACE] 1_Ingestion   | y.shape=(1323000,) | min=-0.83, max=0.84 | dtype=float32
[TRACE] 2_Resampling  | y.shape=(661500,)  | min=-0.84, max=0.85 | dtype=float32
[TRACE] 3_HighPass    | y.shape=(661500,)  | min=-0.82, max=0.84 | dtype=float32
[TRACE] 4_NoiseReduce | y.shape=(661500,)  | min=-0.79, max=0.81 | dtype=float32
[TRACE] 5_TrimSilence | y.shape=(610200,)  | min=-0.79, max=0.81 | dtype=float32
[TRACE] 6_Normalize   | y.shape=(610200,)  | min=-1.00, max=1.00 | dtype=float32"""
    story.append(Paragraph("<b>Example: Real-time Telemetry Trace</b>", bodyJ))
    story.append(code_block(example_trace))
    story.append(Spacer(1, 4))

    # ════════════════════════════════════════════════════════════════════════
    # 5. FEATURE EXTRACTION MODULES
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("5.  Feature Extraction Modules", "🧬"))
    story.append(Paragraph(
        "All extractors inherit from <b>BaseFeatureExtractor</b>, which mandates a <b>name</b> property, "
        "a <b>column_names()</b> list, and an <b>extract(y, sr)</b> method. The registry pattern in "
        "<b>ExtractionService</b> maps JSON key strings to extractor classes, enabling dynamic loading "
        "without modifying core orchestration logic.",
        bodyJ))

    modules = [
        ("MFCC Extractor", "78 features",
         "Computes 13 Mel-Frequency Cepstral Coefficients, first-order deltas, and second-order "
         "delta-deltas via librosa.feature.mfcc and librosa.feature.delta. For each of the 39 coefficient "
         "tracks (13 × 3), mean and standard deviation are reported.",
         "mfcc_1_mean … mfcc_13_std, mfcc_delta_1_mean … mfcc_delta2_13_std"),
        ("Chroma Extractor", "24 features",
         "Computes an STFT magnitude spectrogram then maps it to a 12-bin pitch-class (chroma) "
         "representation via librosa.feature.chroma_stft. Bins correspond to C, C#, D, D#, E, F, "
         "F#, G, G#, A, A#, B. Mean and std per bin.",
         "chroma_1_mean … chroma_12_std"),
        ("Spectral Extractor", "22 features",
         "Extracts spectral centroid, bandwidth, roll-off (85th percentile), contrast across 7 "
         "sub-bands, and flatness. Mean + std reported for each descriptor.",
         "spectral_centroid_mean/std, bandwidth_mean/std, rolloff_mean/std, contrast_1-7_mean/std, flatness_mean/std"),
        ("Pitch (F0) Extractor", "5 features",
         "Uses librosa.pyin (probabilistic YIN) to estimate frame-level F0. Search range C2–C7 "
         "(65–2093 Hz). Unvoiced frames (NaN) excluded. Jitter = mean|Δf0| / mean_f0 on voiced frames.",
         "f0_mean, f0_std, f0_min, f0_max, jitter_relative"),
        ("Energy Extractor", "6 features",
         "RMS energy per frame via librosa.feature.rms. Shimmer = mean|ΔRMS| / mean_RMS. "
         "HNR estimated via normalised autocorrelation: HNR = 10·log10(r_max / (1 − r_max)) "
         "where r_max is the peak autocorrelation in the 75–500 Hz lag range.",
         "rms_mean, rms_std, rms_min, rms_max, shimmer_relative, hnr_db"),
        ("Zero-Crossing Rate", "2 features",
         "Counts the rate of sign changes per frame via librosa.feature.zero_crossing_rate. "
         "High ZCR correlates with fricatives; low ZCR with voiced speech.",
         "zcr_mean, zcr_std"),
        ("Temporal Extractor", "2 features",
         "Duration via librosa.get_duration. Tempo estimated in BPM via onset strength envelope "
         "and librosa.feature.tempo.",
         "duration_sec, tempo_bpm"),
    ]
    for name, count, desc, cols in modules:
        story.append(KeepTogether([
            Paragraph(f"{name}   ({count})", h3),
            Paragraph(desc, body),
            Paragraph(f"<i>Columns: {cols}</i>", muted_s),
            Spacer(1, 4),
        ]))

    story.append(PageBreak())
    story.append(Paragraph("Execution Telemetry Screenshots", h3))
    story.append(Paragraph("The exact terminal pipeline trace tracking NumPy array shapes and magnitudes:", body))
    story.append(Spacer(1, 10))
    
    import glob
    screenshots = sorted(glob.glob("doc/images/media__*.png"))
    for scr_path in screenshots:
        insert_screenshot(story, scr_path)

    # ════════════════════════════════════════════════════════════════════════
    # 6. COMPLETE FEATURE INVENTORY
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("6.  Complete Feature Inventory", "📊"))
    story.append(callout(
        "When all extractors are enabled: 78 + 24 + 22 + 5 + 6 + 2 + 2 = 139 scalar features per audio file (plus filename column).",
        bg=GREEN_LIGHT, border=GREEN, label="Total"))
    story.append(std_table(
        ["Module", "Feature Group", "Count", "Description"],
        [
            ["MFCC",     "mfcc_1…13 (mean + std)",            "26", "Mel-Frequency Cepstral Coefficients"],
            ["MFCC",     "mfcc_delta_1…13 (mean + std)",      "26", "First-order temporal derivatives"],
            ["MFCC",     "mfcc_delta2_1…13 (mean + std)",     "26", "Second-order temporal derivatives"],
            ["Chroma",   "chroma_1…12 (mean + std)",          "24", "Pitch-class energy per semitone"],
            ["Spectral", "centroid, bandwidth, rolloff",       "6",  "Core spectral shape descriptors"],
            ["Spectral", "contrast_1…7 (mean + std)",         "14", "Spectral contrast per sub-band"],
            ["Spectral", "flatness (mean + std)",              "2",  "Tonality vs. noise-likeness ratio"],
            ["Pitch",    "f0_mean, f0_std, f0_min, f0_max",   "4",  "Fundamental frequency statistics"],
            ["Pitch",    "jitter_relative",                    "1",  "Pitch perturbation quotient"],
            ["Energy",   "rms_mean, rms_std, rms_min, rms_max","4", "Root-Mean-Square energy stats"],
            ["Energy",   "shimmer_relative",                   "1",  "Amplitude perturbation quotient"],
            ["Energy",   "hnr_db",                             "1",  "Harmonics-to-Noise Ratio (dB)"],
            ["ZCR",      "zcr_mean, zcr_std",                 "2",  "Zero-Crossing Rate statistics"],
            ["Temporal", "duration_sec, tempo_bpm",            "2",  "Duration and estimated rhythm"],
            ["TOTAL",    "",                                   "139","Scalar features per audio file"],
        ],
        col_widths=[22*mm, 64*mm, 16*mm, cw - 102*mm],
    ))

    # ════════════════════════════════════════════════════════════════════════
    # 7. JAVA DESKTOP GUI
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("7.  Java Desktop GUI", "🖥"))
    story.append(Paragraph(
        "The GUI is a standard Java Swing application themed with <b>FlatLaf 3.4</b> (Mac Dark variant), "
        "laid out with <b>MigLayout 11.4.2</b>, and uses <b>SVG Salamander</b> for vector icon rendering. "
        "All I/O and HTTP calls execute off the Event Dispatch Thread via <b>SwingWorker</b> to prevent UI freezing.",
        bodyJ))
    story.append(std_table(
        ["UI Section", "Class", "Responsibility"],
        [
            ["Input Section",      "InputSection",           "File picker / drag-drop; assembles the audio file list"],
            ["Preprocessing",      "PreprocessingSection",   "Toggle switches and sliders for each DSP step"],
            ["Feature Selection",  "FeatureSelectionSection","Checkbox grid to enable/disable individual extractors"],
            ["Execution",          "ExecutionSection",       "Run button, JProgressBar, SwingWorker HTTP request/poll logic"],
            ["Output",             "OutputSection",          "Download CSV / Download ZIP buttons; file-save dialogs"],
        ],
        col_widths=[33*mm, 48*mm, cw - 81*mm],
    ))
    story.append(Paragraph("Cross-Language Contract", h3))
    story.append(Paragraph(
        "The Java <b>ExtractionConfig</b> POJO mirrors the Python Pydantic model field-for-field. "
        "GSON serialises on the Java side; Pydantic deserialises and validates on arrival. "
        "No IDL or code-generation tool is required — the contract is maintained by keeping both "
        "models in sync manually, which is safe given the HTTP boundary is internal and versioned "
        "together with the release.", bodyJ))
    story.append(code_block(
        "// Java (ExtractionConfig.java)\n"
        "List<String>         audioFiles;\n"
        "Map<String, Object>  preprocessingSettings;\n"
        "Map<String, Boolean> featureSelection;\n"
        "\n"
        "# Python (main.py — Pydantic)\n"
        "audioFiles:            List[str]\n"
        "preprocessingSettings: Dict[str, Any]\n"
        "featureSelection:      Dict[str, bool]"))

    # ════════════════════════════════════════════════════════════════════════
    # 8. REST API REFERENCE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("8.  REST API Reference", "🌐"))
    story.append(Paragraph(
        "The Python backend exposes five HTTP endpoints served by Uvicorn on port 9999. "
        "CORS is fully open (allow_origins=[\"*\"]) to permit the Java desktop client to connect "
        "from any localhost port.", body))
    story.append(std_table(
        ["Method", "Path", "Description", "Response"],
        [
            ["GET",  "/",                  "Health check",             'JSON: {"status":"ok","message":"..."}'],
            ["POST", "/api/config",        "Submit extraction job",     '{"status":"success","message":"Pipeline started"}'],
            ["GET",  "/api/status",        "Poll pipeline progress",    '{"progress":%,"message":"...","is_complete":bool}'],
            ["GET",  "/api/download/csv",  "Download features CSV",    "FileResponse (text/csv)"],
            ["GET",  "/api/download/zip",  "Download archive ZIP",     "FileResponse (application/zip)"],
        ],
        col_widths=[14*mm, 40*mm, 52*mm, cw - 106*mm],
    ))
    story.append(Paragraph("Concurrency Model", h3))
    story.append(Paragraph(
        "The extraction pipeline is CPU-bound (librosa, scipy, numba). "
        "To avoid blocking FastAPI's asyncio event loop it runs inside a "
        "<b>ThreadPoolExecutor(max_workers=2)</b> via <b>asyncio.loop.run_in_executor</b>. "
        "A <b>409 Conflict</b> is returned if a job is already running. "
        "Progress is communicated via a shared in-process status dict rather than a database, "
        "keeping the architecture simple and zero-dependency.", bodyJ))

    # ════════════════════════════════════════════════════════════════════════
    # 9. DOCKER DEPLOYMENT
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("9.  Docker Deployment", "🐳"))
    story.append(Paragraph(
        "Orpheus ships with a <b>multi-stage Dockerfile</b> and <b>docker-compose.yml</b> that containerise "
        "the Python backend. The Java GUI runs natively on the host and connects to the containerised server. "
        "No Python, pip, Maven, or librosa installation is needed on the target machine.", bodyJ))
    story.append(callout(
        "Host Requirements: Docker Desktop (any platform) + Java 17+ JRE. Nothing else.",
        bg=CYAN_LIGHT, border=CYAN, label="Minimal Host Requirements"))
    story.append(std_table(
        ["Stage", "Base Image", "What it does"],
        [
            ["java-builder", "maven:3.9-eclipse-temurin-17",
             "Compiles Java source and packages everything into a fat JAR via Maven Shade Plugin"],
            ["runtime",      "python:3.11-slim",
             "Installs libsndfile1, ffmpeg, openjdk-21-jre-headless; installs all Python packages; "
             "copies Python source and the compiled fat JAR"],
        ],
        col_widths=[26*mm, 54*mm, cw - 80*mm],
    ))
    story.append(Paragraph("Quick Start Commands", h3))
    story.append(code_block(
        "# 1. Build and start the backend\n"
        "docker-compose up --build\n"
        "\n"
        "# 2. Copy the compiled GUI JAR (first time only)\n"
        "docker cp orpheus-backend:/app/Java/SpeechDashboard.jar ./SpeechDashboard.jar\n"
        "\n"
        "# 3. Run the Java GUI on host (connects to localhost:9999 automatically)\n"
        "java -jar SpeechDashboard.jar\n"
        "\n"
        "# Verify backend health\n"
        "curl http://localhost:9999/"))
    story.append(std_table(
        ["Host Path", "Container Path", "Purpose"],
        [
            ["./data/input/",  "/app/Python/input/",  "Drop .wav/.mp3 files here before running"],
            ["./data/output/", "/app/Python/output/", "CSVs, processed audio, and ZIP archive appear here"],
        ],
        col_widths=[40*mm, 50*mm, cw - 90*mm],
    ))

    # ════════════════════════════════════════════════════════════════════════
    # 10. TECH STACK SUMMARY
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("10. Tech Stack Summary", "🛠"))
    story.append(std_table(
        ["Layer", "Technology", "Version", "Role"],
        [
            ["Desktop GUI",     "Java Swing",            "17",        "Application window and user controls"],
            ["GUI Theme",       "FlatLaf",               "3.4",       "Mac Dark modern look-and-feel"],
            ["GUI Layout",      "MigLayout",             "11.4.2",    "Responsive panel layout engine"],
            ["GUI Icons",       "SVG Salamander",        "1.0",       "Resolution-independent vector icons"],
            ["JSON (Java)",     "GSON",                  "2.11.0",    "Java ↔ JSON serialisation"],
            ["Build (Java)",    "Maven + Shade Plugin",  "3.9/3.5.1", "Dependency management and fat JAR"],
            ["API Server",      "FastAPI + Uvicorn",     "latest",    "Async REST server on port 9999"],
            ["Validation",      "Pydantic",              "v2",        "Request model validation"],
            ["Audio Loading",   "Librosa + SoundFile",   "0.11+",     "WAV/MP3 ingestion and DSP utilities"],
            ["DSP Filters",     "SciPy",                 "latest",    "Butterworth filter design and sosfilt"],
            ["Noise Reduction", "NoiseReduce",           "3.x",       "Stationary spectral gating"],
            ["Numerics",        "NumPy",                 "2.x",       "Array operations throughout the pipeline"],
            ["Data Export",     "Python csv (stdlib)",   "—",         "CSV writing with dynamic column headers"],
            ["Containerisation","Docker (multi-stage)",  "29.x",      "Reproducible zero-install deployment"],
        ],
        col_widths=[34*mm, 40*mm, 22*mm, cw - 96*mm],
    ))

    # ════════════════════════════════════════════════════════════════════════
    # 11. REPOSITORY STRUCTURE
    # ═══════════════════════════════════════════════════════════════════════
    story.append(section_header("11. Repository Structure", "📁"))
    story.append(code_block(
        "Orpheus/\n"
        "├── Java/                          # Desktop GUI (Maven project)\n"
        "│   ├── pom.xml\n"
        "│   └── src/main/java/com/speech/\n"
        "│       ├── App.java               # Entry point\n"
        "│       ├── model/ExtractionConfig.java\n"
        "│       ├── ui/\n"
        "│       │   ├── MainDashboard.java\n"
        "│       │   ├── components/AnimatedButton.java\n"
        "│       │   └── sections/\n"
        "│       │       ├── InputSection.java\n"
        "│       │       ├── PreprocessingSection.java\n"
        "│       │       ├── FeatureSelectionSection.java\n"
        "│       │       ├── ExecutionSection.java\n"
        "│       │       └── OutputSection.java\n"
        "│       └── util/ (FontHelper, SVGIconHelper)\n"
        "│\n"
        "├── Python/                        # ML/DSP Backend (FastAPI)\n"
        "│   ├── main.py                    # FastAPI app + 5 endpoints\n"
        "│   ├── requirements.txt\n"
        "│   ├── core/  (base_extractor, base_preprocessor, base_exporter)\n"
        "│   ├── preprocessing/\n"
        "│   │   ├── resampler.py  highpass_filter.py  noise_reducer.py\n"
        "│   │   ├── silence_remover.py  normalizer.py\n"
        "│   ├── extractors/\n"
        "│   │   ├── mfcc_extractor.py    chroma_extractor.py\n"
        "│   │   ├── spectral_extractor.py  zcr_extractor.py\n"
        "│   │   ├── pitch_extractor.py   energy_extractor.py\n"
        "│   │   └── temporal_extractor.py\n"
        "│   ├── services/extraction_service.py  # Pipeline orchestrator\n"
        "│   ├── exporters/csv_exporter.py\n"
        "│   └── output/ (processed/ features/ archives/)\n"
        "│\n"
        "├── Dockerfile                     # Multi-stage build\n"
        "├── docker-compose.yml\n"
        "├── .dockerignore\n"
        "├── run.ps1  /  run.sh             # Dev launchers\n"
        "└── README.md"))

    # ── Build ────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
