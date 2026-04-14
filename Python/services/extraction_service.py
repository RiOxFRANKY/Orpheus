"""
Extraction Service — orchestrates the full preprocess → extract → export pipeline.

This is the central service that:
  1. Resolves audio file paths
  2. Runs the enabled preprocessing steps in order
  3. Saves preprocessed audio to ``output/processed/``
  4. Runs the enabled feature extractors
  5. Exports results to CSV via the exporter
  6. Creates a downloadable ZIP archive
  7. Reports real-time progress to a shared status dict
"""

import shutil
import zipfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import librosa
import numpy as np
import soundfile as sf

from core.base_extractor import BaseFeatureExtractor
from core.base_preprocessor import BasePreprocessor

from extractors import (
    MFCCExtractor,
    ChromaExtractor,
    SpectralExtractor,
    ZCRExtractor,
    PitchExtractor,
    EnergyExtractor,
    TemporalExtractor,
)
from preprocessing import (
    Resampler,
    NoiseReducer,
    Normalizer,
    SilenceRemover,
    HighPassFilter,
)
from exporters import CSVExporter


# ── Feature-key → Extractor class mapping ────────────────────────────
_EXTRACTOR_REGISTRY: Dict[str, type] = {
    "mfcc": MFCCExtractor,
    "mfccs": MFCCExtractor,
    "chroma": ChromaExtractor,
    "chroma features": ChromaExtractor,
    "spectral_centroid": SpectralExtractor,
    "spectral centroid": SpectralExtractor,
    "spectral_bandwidth": SpectralExtractor,
    "spectral bandwidth": SpectralExtractor,
    "spectral_rolloff": SpectralExtractor,
    "spectral roll-off": SpectralExtractor,
    "spectral_contrast": SpectralExtractor,
    "spectral_flatness": SpectralExtractor,
    "zcr": ZCRExtractor,
    "zero_crossing_rate": ZCRExtractor,
    "zero-crossing rate": ZCRExtractor,
    "pitch": PitchExtractor,
    "pitch (f0)": PitchExtractor,
    "f0": PitchExtractor,
    "jitter": PitchExtractor,
    "energy": EnergyExtractor,
    "rmse": EnergyExtractor,
    "rmse energy": EnergyExtractor,
    "short-term energy": EnergyExtractor,
    "rms": EnergyExtractor,
    "shimmer": EnergyExtractor,
    "hnr": EnergyExtractor,
    "harmonic-to-noise ratio": EnergyExtractor,
    "tempo": TemporalExtractor,
    "duration": TemporalExtractor,
}

# ── Preprocessor-key → class mapping ────────────────────────────────
_PREPROCESSOR_REGISTRY: Dict[str, type] = {
    "resample": Resampler,
    "resampling": Resampler,
    "noise_reduction": NoiseReducer,
    "noiseReduction": NoiseReducer,
    "spectral_gating": NoiseReducer,
    "normalize": Normalizer,
    "normalization": Normalizer,
    "normalization_dbfs": Normalizer,
    "silence_removal": SilenceRemover,
    "silent_removal": SilenceRemover,
    "silenceRemoval": SilenceRemover,
    "highpass_filter": HighPassFilter,
    "high_pass_hz": HighPassFilter,
    "highpassFilter": HighPassFilter,
}

# Fixed processing order for preprocessors
_PREPROCESSOR_ORDER = [
    Resampler,
    HighPassFilter,
    NoiseReducer,
    SilenceRemover,
    Normalizer,
]


class ExtractionService:
    """Orchestrate the speech-feature extraction pipeline."""

    def __init__(self, output_root: Path | str = "output"):
        self.output_root = Path(output_root)
        self.processed_dir = self.output_root / "processed"
        self.features_dir = self.output_root / "features"
        self.archives_dir = self.output_root / "archives"

        # Ensure directories exist
        for d in (self.processed_dir, self.features_dir, self.archives_dir):
            d.mkdir(parents=True, exist_ok=True)

        self._exporter = CSVExporter()

    # ── public interface ─────────────────────────────────────────

    def run(
        self,
        audio_paths: List[str],
        preprocessing_settings: Dict[str, Any],
        feature_selection: Dict[str, bool],
        status_callback: Optional[Callable[[int, str], None]] = None,
    ) -> Dict[str, Any]:
        """Execute the full pipeline.

        Parameters
        ----------
        audio_paths : list[str]
            Absolute or relative paths to audio files.
        preprocessing_settings : dict
            GUI preprocessing knobs (resample, noiseReduction, etc.).
        feature_selection : dict
            Mapping of feature-key → enabled (bool).
        status_callback : callable, optional
            ``(progress_int, message_str) -> None`` called to report progress.

        Returns
        -------
        dict
            Summary with paths to CSV and ZIP outputs.
        """
        self._report(status_callback, 0, "Resolving audio file paths…")
        resolved = self._resolve_paths(audio_paths)
        if not resolved:
            self._report(status_callback, 100, "No valid audio files found.")
            return {"error": "No valid audio files found", "csv": None, "archive": None}

        total_files = len(resolved)

        # ── 1. Determine active preprocessors ────────────────────
        preprocessors = self._build_preprocessors(preprocessing_settings)

        # ── 2. Determine active extractors (deduplicated) ────────
        extractors = self._build_extractors(feature_selection)
        if not extractors:
            # If nothing selected, enable all
            extractors = self._build_extractors({k: True for k in _EXTRACTOR_REGISTRY})

        column_order = ["filename"]
        for ext in extractors:
            column_order.extend(ext.column_names())

        all_rows: List[Dict[str, Any]] = []
        current_session_files: List[Path] = []

        for idx, audio_path in enumerate(resolved):
            file_label = Path(audio_path).name
            base_progress = int((idx / total_files) * 80)  # 0-80 % for files

            # ── Load audio ────────────────────────────────────────
            self._report(
                status_callback,
                base_progress,
                f"[{idx + 1}/{total_files}] Loading {file_label}…",
            )
            try:
                y, sr = librosa.load(audio_path, sr=None, mono=True)
            except Exception as exc:
                print(f"[ExtractionService] Failed to load {audio_path}: {exc}")
                continue

            # ── Preprocess ────────────────────────────────────────
            self._report(
                status_callback,
                base_progress + 2,
                f"[{idx + 1}/{total_files}] Preprocessing {file_label}…",
            )
            for pp in preprocessors:
                y, sr = pp.process(y, sr, preprocessing_settings)

            # ── Save processed audio ──────────────────────────────
            processed_path = self.processed_dir / file_label
            sf.write(str(processed_path), y, sr)
            current_session_files.append(processed_path)

            # ── Extract features ──────────────────────────────────
            self._report(
                status_callback,
                base_progress + 5,
                f"[{idx + 1}/{total_files}] Extracting features from {file_label}…",
            )
            row: Dict[str, Any] = {"filename": file_label}
            for ext in extractors:
                try:
                    features = ext.extract(y, sr)
                    row.update(features)
                except Exception as exc:
                    print(f"[{ext.name}] Error on {file_label}: {exc}")
                    # Fill with zeros on failure
                    for col in ext.column_names():
                        row.setdefault(col, 0.0)

            all_rows.append(row)

        # ── 3. Export CSV ─────────────────────────────────────────
        self._report(status_callback, 85, "Writing features CSV…")
        csv_path = self.features_dir / "features.csv"
        self._exporter.export(all_rows, column_order, csv_path)

        # ── 4. Create ZIP archive ─────────────────────────────────
        self._report(status_callback, 90, "Creating downloadable archive…")
        archive_path = self._create_archive(csv_path, current_session_files)

        self._report(status_callback, 100, "Extraction complete.")

        return {
            "csv": str(csv_path),
            "archive": str(archive_path),
            "files_processed": len(all_rows),
            "features_per_file": len(column_order) - 1,  # minus 'filename'
        }

    # ── private helpers ──────────────────────────────────────────

    @staticmethod
    def _resolve_paths(paths: List[str]) -> List[str]:
        """Return only paths that point to existing files."""
        resolved = []
        for p in paths:
            path = Path(p)
            if path.is_file():
                resolved.append(str(path.resolve()))
            else:
                print(f"[ExtractionService] File not found, skipping: {p}")
        return resolved

    @staticmethod
    def _build_preprocessors(
        settings: Dict[str, Any],
    ) -> List[BasePreprocessor]:
        """Instantiate enabled preprocessors in canonical order."""
        # Collect enabled preprocessor types
        enabled_types: set = set()
        for key, value in settings.items():
            is_enabled = False
            
            # Extract boolean effectively 
            if isinstance(value, bool):
                is_enabled = value
            elif isinstance(value, dict):
                is_enabled = value.get("enabled", False)

            if is_enabled and key in _PREPROCESSOR_REGISTRY:
                enabled_types.add(_PREPROCESSOR_REGISTRY[key])

        # Instantiate in fixed order
        return [cls() for cls in _PREPROCESSOR_ORDER if cls in enabled_types]

    @staticmethod
    def _build_extractors(
        selection: Dict[str, bool],
    ) -> List[BaseFeatureExtractor]:
        """Instantiate selected extractors, deduplicated."""
        seen_types: set = set()
        extractors: List[BaseFeatureExtractor] = []
        for key, enabled in selection.items():
            if not enabled:
                continue
            cls = _EXTRACTOR_REGISTRY.get(key.lower())
            if cls and cls not in seen_types:
                seen_types.add(cls)
                extractors.append(cls())
        return extractors

    def _create_archive(self, csv_path: Path, session_files: List[Path]) -> Path:
        """Bundle processed audio + CSV into a ZIP file."""
        archive_path = self.archives_dir / "speech_features.zip"
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # Add CSV
            zf.write(csv_path, arcname=f"features/{csv_path.name}")
            # Add ONLY the processed audio files belonging to the current run
            for audio_file in session_files:
                if audio_file.is_file():
                    zf.write(audio_file, arcname=f"processed/{audio_file.name}")
        return archive_path

    @staticmethod
    def _report(
        callback: Optional[Callable[[int, str], None]],
        progress: int,
        message: str,
    ) -> None:
        """Fire the status callback if provided."""
        if callback:
            callback(progress, message)
        print(f"[{progress:3d}%] {message}")
