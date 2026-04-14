"""
Speech Feature Extraction API — FastAPI backend.

Provides:
  - POST /api/config     — receive extraction config from the Java GUI and start the pipeline
  - GET  /api/status     — poll current job progress (progress %, message, is_complete)
  - GET  /api/download/csv — download the generated features CSV
  - GET  /api/download/zip — download the full archive (processed audio + CSV)
  - GET  /                — health check
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from services.extraction_service import ExtractionService

app = FastAPI(title="Speech Feature Extraction API")

# ── CORS — allow the Java desktop client (and any local tool) to connect ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Thread pool for CPU-bound extraction work ────────────────────────────
_executor = ThreadPoolExecutor(max_workers=2)

# ── Shared job status dict (polled by the Java SwingWorker) ──────────────
current_job_status: Dict[str, Any] = {
    "progress": 100,
    "message": "System Ready",
    "is_complete": True,
}

# ── Paths to the latest outputs (set after a successful run) ─────────────
_latest_csv: Path | None = None
_latest_archive: Path | None = None


# ── Request model (matches ExtractionConfig.java) ────────────────────────
class ExtractionConfig(BaseModel):
    audioFiles: List[str]
    preprocessingSettings: Dict[str, Any]
    featureSelection: Dict[str, bool]


# ── Helpers ──────────────────────────────────────────────────────────────

def _status_callback(progress: int, message: str) -> None:
    """Called by ExtractionService to report real-time progress."""
    current_job_status["progress"] = progress
    current_job_status["message"] = message
    current_job_status["is_complete"] = progress >= 100


def _run_pipeline(config: ExtractionConfig) -> None:
    """Synchronous pipeline runner — executed inside the thread pool."""
    global _latest_csv, _latest_archive

    try:
        service = ExtractionService(output_root="output")

        result = service.run(
            audio_paths=config.audioFiles,
            preprocessing_settings=config.preprocessingSettings,
            feature_selection=config.featureSelection,
            status_callback=_status_callback,
        )

        if result.get("error"):
            current_job_status["message"] = f"Error: {result['error']}"
            current_job_status["progress"] = 100
            current_job_status["is_complete"] = True
            return

        _latest_csv = Path(result["csv"]) if result.get("csv") else None
        _latest_archive = Path(result["archive"]) if result.get("archive") else None

        current_job_status["progress"] = 100
        current_job_status["message"] = "Completed Successfully"
        current_job_status["is_complete"] = True

        print(f"[Pipeline] Done — {result.get('files_processed', 0)} files, "
              f"{result.get('features_per_file', 0)} features each.")

    except Exception as exc:
        current_job_status["progress"] = 100
        current_job_status["message"] = f"Pipeline error: {exc}"
        current_job_status["is_complete"] = True
        print(f"[Pipeline] FATAL: {exc}")
        import traceback
        traceback.print_exc()


async def _run_pipeline_async(config: ExtractionConfig) -> None:
    """Run the blocking pipeline in a thread so we don't block the event loop."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(_executor, _run_pipeline, config)


# ── Endpoints ────────────────────────────────────────────────────────────

@app.post("/api/config")
async def receive_config(config: ExtractionConfig, background_tasks: BackgroundTasks):
    """Accept extraction config from the Java GUI and kick off the pipeline."""
    global current_job_status

    from fastapi import HTTPException
    if not current_job_status.get("is_complete", True):
        raise HTTPException(status_code=409, detail="A background extraction job is already in progress.")

    print("Received Configuration:")
    print(f"  Audio Files     : {config.audioFiles}")
    print(f"  Preprocessing   : {config.preprocessingSettings}")
    print(f"  Feature Selection: {config.featureSelection}")

    # Reset status
    current_job_status["progress"] = 0
    current_job_status["message"] = "Initializing..."
    current_job_status["is_complete"] = False

    # Queue the real pipeline as a background task
    background_tasks.add_task(_run_pipeline_async, config)

    return {"status": "success", "message": "Pipeline started in background"}


@app.get("/api/status")
async def get_status():
    """Return the current pipeline progress (polled by Java SwingWorker)."""
    return current_job_status


@app.get("/api/download/csv")
async def download_csv():
    """Serve the latest features CSV for download."""
    if _latest_csv and _latest_csv.is_file():
        return FileResponse(
            path=str(_latest_csv),
            filename="features.csv",
            media_type="text/csv",
        )
    return {"error": "No CSV file available. Run the pipeline first."}


@app.get("/api/download/zip")
async def download_zip():
    """Serve the latest ZIP archive (processed audio + CSV) for download."""
    if _latest_archive and _latest_archive.is_file():
        return FileResponse(
            path=str(_latest_archive),
            filename="speech_features.zip",
            media_type="application/zip",
        )
    return {"error": "No archive available. Run the pipeline first."}


@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "message": "Speech Feature Extraction API is running. POST to /api/config to start.",
    }
