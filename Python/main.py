from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import asyncio

app = FastAPI(title="Speech Feature Extraction API")

# Global status tracker
current_job_status = {
    "progress": 100,
    "message": "System Ready",
    "is_complete": True
}

async def process_audio_job(config: "ExtractionConfig"):
    global current_job_status
    
    steps = [
        "Loading audio configurations...",
        "Resampling audio to 16kHz...",
        "Applying noise reduction (Spectral Subtraction)...",
        "Extracting MFCC features...",
        "Extracting Spectral Centroid & Roll-off...",
        "Extracting Prosodic features (Pitch, Jitter)...",
        "Aggregating feature vectors...",
        "Generating compressed output archives..."
    ]
    
    total_steps = len(steps)
    for i, step_msg in enumerate(steps):
        current_job_status["message"] = step_msg
        current_job_status["progress"] = int(((i + 1) / total_steps) * 100)
        
        # Simulate processing time depending on the job step
        await asyncio.sleep(1.0)
        
    current_job_status["message"] = "Completed Successfully"
    current_job_status["progress"] = 100
    current_job_status["is_complete"] = True

class ExtractionConfig(BaseModel):
    audioFiles: List[str]
    preprocessingSettings: Dict[str, Any]
    featureSelection: Dict[str, bool]

@app.post("/api/config")
async def receive_config(config: ExtractionConfig, background_tasks: BackgroundTasks):
    global current_job_status
    
    print("Received Configuration:")
    print(f"Audio Files: {config.audioFiles}")
    
    # Reset status
    current_job_status["progress"] = 0
    current_job_status["message"] = "Initializing..."
    current_job_status["is_complete"] = False
    
    # Queue background task to run process_audio_job
    background_tasks.add_task(process_audio_job, config)
    
    return {"status": "success", "message": "Job started in background"}

@app.get("/api/status")
async def get_status():
    return current_job_status

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "FastAPI backend is running. Send POST to /api/config."}
