$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting Speech Extraction System    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$baseDir = $PSScriptRoot

# 1. Start Python Server in a new window
Write-Host "`n[1/2] Starting Python FastAPI Backend on port 9999..." -ForegroundColor Yellow
$pythonDir = Join-Path $baseDir "Python"

# We use Start-Process to launch it directly so we can grab its exact Process ID for cleanup
$pyExe = Join-Path $baseDir ".venv\Scripts\python.exe"
$pythonProcess = Start-Process -FilePath $pyExe -ArgumentList "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "9999" -WorkingDirectory $pythonDir -PassThru

# Give the server a few seconds to fully initialize
Start-Sleep -Seconds 3

# 2. Start Java Frontend in the current window
Write-Host "`n[2/2] Compiling and starting Java UI Application..." -ForegroundColor Yellow
$javaDir = Join-Path $baseDir "Java"
Set-Location -Path $javaDir

# Build and run using Maven
mvn clean compile exec:java

# Ensure we cleanup the backend process when the Java UI is closed
Write-Host "`nFrontend exited. Closing Python backend server..." -ForegroundColor DarkGray
if ($pythonProcess -and !$pythonProcess.HasExited) {
    Stop-Process -Id $pythonProcess.Id -Force -ErrorAction SilentlyContinue
}
Write-Host "Done." -ForegroundColor Green
