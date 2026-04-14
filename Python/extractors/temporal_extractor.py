"""
Temporal Feature Extractor.

Computes:
  - Duration (seconds)
  - Estimated tempo (BPM via onset envelope)

Total: **2 scalar features**.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class TemporalExtractor(BaseFeatureExtractor):
    """Extract temporal / rhythmic descriptors."""

    @property
    def name(self) -> str:
        return "temporal"

    def column_names(self) -> List[str]:
        return ["duration_sec", "tempo_bpm"]

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        duration = float(librosa.get_duration(y=y, sr=sr))

        # Tempo estimation via onset envelope
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
        tempo_val = float(tempo[0]) if len(tempo) > 0 else 0.0

        return {
            "duration_sec": duration,
            "tempo_bpm": tempo_val,
        }
