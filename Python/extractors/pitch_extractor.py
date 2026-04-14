"""
Pitch (F0) Feature Extractor.

Uses ``librosa.pyin`` to estimate the fundamental frequency and derives:
  - F0 mean, std, min, max
  - Jitter (mean absolute pitch perturbation, relative)

Total: **5 scalar features**.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class PitchExtractor(BaseFeatureExtractor):
    """Extract pitch-related features via probabilistic YIN (pyin)."""

    @property
    def name(self) -> str:
        return "pitch"

    def column_names(self) -> List[str]:
        return [
            "f0_mean", "f0_std", "f0_min", "f0_max",
            "jitter_relative",
        ]

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # pyin returns (f0, voiced_flag, voiced_prob)
        f0, voiced_flag, _ = librosa.pyin(
            y,
            sr=sr,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7"),
        )

        # Keep only voiced frames (non-NaN)
        f0_voiced = f0[~np.isnan(f0)] if f0 is not None else np.array([])

        features: Dict[str, float] = {
            "f0_mean": self._safe_mean(f0_voiced) if len(f0_voiced) > 0 else 0.0,
            "f0_std": self._safe_std(f0_voiced) if len(f0_voiced) > 0 else 0.0,
            "f0_min": self._safe_min(f0_voiced) if len(f0_voiced) > 0 else 0.0,
            "f0_max": self._safe_max(f0_voiced) if len(f0_voiced) > 0 else 0.0,
        }

        # Jitter — mean absolute difference between consecutive F0 values
        # normalised by mean F0
        if len(f0_voiced) > 1:
            diffs = np.abs(np.diff(f0_voiced))
            mean_f0 = np.mean(f0_voiced)
            features["jitter_relative"] = (
                float(np.mean(diffs) / mean_f0) if mean_f0 > 0 else 0.0
            )
        else:
            features["jitter_relative"] = 0.0

        return features
