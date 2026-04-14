import requests
import json

# Define the url where the FastAPI server is listening
url = "http://127.0.0.1:9999/api/config"

# Create a sample mock configuration (similar to what the Java GUI builds)
data = {
    "audioFiles": [
        "audio/sample1.wav",
        "audio/sample2.wav"
    ],
    "preprocessingSettings": {
        "resample": True,
        "targetSampleRate": 16000,
        "noiseReduction": "spectral_gating"
    },
    "featureSelection": {
        "mfcc": True,
        "spectral_centroid": True,
        "pitch": False
    }
}

# 1. Output the JSON to the terminal
print("--- JSON Output ---")
json_string = json.dumps(data, indent=4)
print(json_string)

# 2. Output the JSON to a local file
file_path = "mock_output.json"
with open(file_path, "w") as f:
    json.dump(data, f, indent=4)
print(f"\nSaved mockup JSON to: {file_path}")

# 3. Send the JSON to the FastAPI Backend (just like the Java App does)
try:
    print(f"\nSending JSON to FastAPI server at {url}...")
    response = requests.post(url, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print("\nError: Could not connect to FastAPI. Is the server running? (Run: python -m uvicorn main:app --reload)")
