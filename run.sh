#!/bin/bash

# Exit on any error
set -e

echo -e "\033[0;36m========================================\033[0m"
echo -e "\033[0;36m   Starting Speech Extraction System    \033[0m"
echo -e "\033[0;36m========================================\033[0m"

# Get the directory of the script
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 1. Start Python Server in the background
echo -e "\n\033[0;33m[1/2] Starting Python FastAPI Backend on port 9999...\033[0m"
PYTHON_DIR="$BASE_DIR/Python"

# Detect OS to determine venv python path
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Git Bash / Windows
    PY_EXE="$BASE_DIR/.venv/Scripts/python.exe"
else
    # Linux / macOS
    PY_EXE="$BASE_DIR/.venv/bin/python"
fi

# Launch Python backend in background
cd "$PYTHON_DIR"
"$PY_EXE" -m uvicorn main:app --host 127.0.0.1 --port 9999 &
PYTHON_PID=$!

# Ensure the background process is killed when this script exits
trap "kill $PYTHON_PID 2>/dev/null || true" EXIT

# Give the server a few seconds to fully initialize
sleep 3

# 2. Start Java Frontend
echo -e "\n\033[0;33m[2/2] Compiling and starting Java UI Application...\033[0m"
JAVA_DIR="$BASE_DIR/Java"
cd "$JAVA_DIR"

# Build and run using Maven
mvn clean compile exec:java

echo -e "\n\033[0;90mFrontend exited. Closing Python backend server...\033[0m"
# The 'trap' will handle killing the process, but we call it explicitly here for clarity
kill $PYTHON_PID 2>/dev/null || true

echo -e "\033[0;32mDone.\033[0m"
