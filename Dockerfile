# ============================================================================
#  Orpheus Audio Dashboard — Multi-stage Docker Image
#  Stage 1: Build the Java fat JAR (Maven + JDK 17)
#  Stage 2: Runtime with Python 3.11 + JRE 17, serving the FastAPI backend
# ============================================================================

# ── Stage 1: Build Java fat JAR ─────────────────────────────────────────────
FROM maven:3.9-eclipse-temurin-17 AS java-builder

WORKDIR /build/Java
COPY Java/pom.xml .
# Download dependencies first (layer cache optimisation)
RUN mvn dependency:go-offline -B

COPY Java/src ./src
RUN mvn clean package -B -DskipTests


# ── Stage 2: Runtime ────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Install system-level dependencies required by librosa / soundfile / scipy
RUN apt-get update && apt-get install -y --no-install-recommends \
        libsndfile1 \
        ffmpeg \
        openjdk-21-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Python dependencies ─────────────────────────────────────────────────────
COPY Python/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy Python backend source ──────────────────────────────────────────────
COPY Python/ ./Python/

# ── Copy Java fat JAR from builder stage ────────────────────────────────────
COPY --from=java-builder /build/Java/target/*.jar ./Java/SpeechDashboard.jar

# ── Copy launcher script ────────────────────────────────────────────────────
COPY run.sh ./run.sh
RUN chmod +x ./run.sh

# ── Create output directories ───────────────────────────────────────────────
RUN mkdir -p /app/Python/output/processed \
             /app/Python/output/features  \
             /app/Python/output/archives

# ── Expose the FastAPI port ─────────────────────────────────────────────────
EXPOSE 9999

# ── Health check ─────────────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9999/')" || exit 1

# ── Default: run only the Python backend (headless-friendly) ─────────────────
#    The Java GUI requires a display — run it separately or use docker-compose.
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999"]
WORKDIR /app/Python
