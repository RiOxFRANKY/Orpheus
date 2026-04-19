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
        fmin = librosa.note_to_hz("C2")
        fmax = librosa.note_to_hz("C7")

        print(f"\n{'─'*60}")
        print(f"[Pitch] Input array    : shape={y.shape}, dtype={y.dtype}, sr={sr} Hz")
        print(f"[Pitch] Algorithm      : probabilistic YIN (pyin)")
        print(f"[Pitch] F0 search range: {fmin:.2f} Hz (C2) — {fmax:.2f} Hz (C7)")

        # pyin returns (f0, voiced_flag, voiced_prob)
        f0, voiced_flag, voiced_prob = librosa.pyin(
            y,
            sr=sr,
            fmin=fmin,
            fmax=fmax,
        )

        total_frames   = len(f0) if f0 is not None else 0
        voiced_frames  = int(np.sum(voiced_flag)) if voiced_flag is not None else 0
        unvoiced_frames = total_frames - voiced_frames

        print(f"[Pitch] F0 array       : shape={f0.shape}  (one value per frame)")
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=200)
        print(f"[Pitch] F0 raw array   (NaN = unvoiced frame):")
        print(f0)
        print(f"[Pitch] Total frames   : {total_frames}")
        print(f"[Pitch] Voiced frames  : {voiced_frames}  ({voiced_frames/total_frames*100:.1f}%)")
        print(f"[Pitch] Unvoiced frames: {unvoiced_frames}  (NaN in F0 array)")

        # Keep only voiced frames (non-NaN)
        f0_voiced = f0[~np.isnan(f0)] if f0 is not None else np.array([])

        if len(f0_voiced) > 0:
            print(f"[Pitch] F0 voiced values: min={f0_voiced.min():.2f} Hz, "
                  f"max={f0_voiced.max():.2f} Hz, "
                  f"mean={f0_voiced.mean():.2f} Hz")
            print(f"[Pitch] F0 voiced array (Hz):")
            print(f0_voiced)
        else:
            print(f"[Pitch] ⚠ No voiced frames detected — all F0 features will be 0.0")

        features: Dict[str, float] = {
            "f0_mean": self._safe_mean(f0_voiced) if len(f0_voiced) > 0 else 0.0,
            "f0_std":  self._safe_std(f0_voiced)  if len(f0_voiced) > 0 else 0.0,
            "f0_min":  self._safe_min(f0_voiced)  if len(f0_voiced) > 0 else 0.0,
            "f0_max":  self._safe_max(f0_voiced)  if len(f0_voiced) > 0 else 0.0,
        }

        # Jitter — mean absolute difference between consecutive F0 values
        # normalised by mean F0
        if len(f0_voiced) > 1:
            diffs    = np.abs(np.diff(f0_voiced))
            mean_f0  = np.mean(f0_voiced)
            jitter   = float(np.mean(diffs) / mean_f0) if mean_f0 > 0 else 0.0
            features["jitter_relative"] = jitter
            print(f"[Pitch] Jitter calc    : mean|Δf0|={np.mean(diffs):.4f} Hz / mean_f0={mean_f0:.4f} Hz "
                  f"= {jitter:.6f} (relative)")
        else:
            features["jitter_relative"] = 0.0
            print(f"[Pitch] Jitter         : not enough voiced frames — set to 0.0")

        print(f"[Pitch] f0_mean={features['f0_mean']:.2f} Hz, "
              f"f0_std={features['f0_std']:.2f} Hz, "
              f"jitter={features['jitter_relative']:.6f}")
        print(f"[Pitch] ✔ Pitch extraction complete")
        return features

