# main.py Documentation

## Location
`Python/main.py`

## Overview
The primary executable launch point for the Python core engine. It utilizes the asynchronous `FastAPI` framework combined with `uvicorn` to expose robust computational routes safely through port 9999.

## Key Responsibilities
- Configures global `CORSMiddleware` to prevent arbitrary HTTP drops natively when connected cross-process with the Java GUI layer.
- Specifies explicit REST schema mappings globally `/api/config`, `/api/status`, and `/api/download/*`.
- Offloads heavy computational ML blocks (the `ExtractionService`) implicitly onto a specialized detached `ThreadPoolExecutor` safely to guarantee zero thread congestion inside the async event loop serving UI status updates globally.
- Updates an internal tracking dictionary `current_job_status` periodically containing real-time values representing progress ticks synchronously passed back seamlessly into the polling Java `SwingWorker`.
