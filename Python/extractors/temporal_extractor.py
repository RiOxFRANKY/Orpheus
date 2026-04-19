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
        print(f"\n{'─'*60}")
        print(f"[Temporal] Input array    : shape={y.shape}, dtype={y.dtype}, sr={sr} Hz")

        duration = float(librosa.get_duration(y=y, sr=sr))
        print(f"[Temporal] Duration       : {duration:.4f}s  ({len(y):,} samples @ {sr} Hz)")

        # Tempo estimation via onset envelope
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        print(f"[Temporal] Onset envelope : shape={onset_env.shape}  (strength per frame)")
        print(f"[Temporal] Onset range    : min={onset_env.min():.4f}, max={onset_env.max():.4f}, "
              f"mean={onset_env.mean():.4f}")

        tempo = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
        tempo_val = float(tempo[0]) if len(tempo) > 0 else 0.0
        print(f"[Temporal] Tempo array    : {tempo.round(2).tolist()}")
        print(f"[Temporal] Estimated tempo: {tempo_val:.2f} BPM")
        print(f"[Temporal] ✔ Temporal extraction complete")

        return {
            "duration_sec": duration,
            "tempo_bpm":    tempo_val,
        }

