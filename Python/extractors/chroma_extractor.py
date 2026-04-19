"""
Chroma Feature Extractor.

Computes the 12-bin chroma representation (STFT-based) and reports the
mean and standard deviation of each bin — **24 scalar features**.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class ChromaExtractor(BaseFeatureExtractor):
    """Extract chroma (pitch-class) statistics from the STFT."""

    N_CHROMA = 12

    @property
    def name(self) -> str:
        return "chroma"

    def column_names(self) -> List[str]:
        cols: List[str] = []
        for i in range(1, self.N_CHROMA + 1):
            cols.append(f"chroma_{i}_mean")
            cols.append(f"chroma_{i}_std")
        return cols

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        print(f"\n{'─'*60}")
        print(f"[Chroma] Input array   : shape={y.shape}, dtype={y.dtype}, sr={sr} Hz")
        print(f"[Chroma] n_chroma      : {self.N_CHROMA}  (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)")

        stft = np.abs(librosa.stft(y))
        print(f"[Chroma] STFT magnitude: shape={stft.shape}  (freq_bins × frames)")
        print(f"[Chroma] STFT range    : min={stft.min():.6f}, max={stft.max():.6f}, mean={stft.mean():.6f}")

        chroma = librosa.feature.chroma_stft(S=stft, sr=sr, n_chroma=self.N_CHROMA)
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=200)
        print(f"[Chroma] Chroma matrix : shape={chroma.shape}  (12 pitch classes × frames)")
        print(f"[Chroma] Value range   : min={chroma.min():.4f}, max={chroma.max():.4f}")
        print(f"[Chroma] Full chroma matrix (12 rows = pitch classes, cols = first 20 frames):")
        print(chroma[:, :20])
        print(f"[Chroma] Row means     : {chroma.mean(axis=1).round(4).tolist()}  (C C# D D# E F F# G G# A A# B)")

        features: Dict[str, float] = {}
        for i in range(self.N_CHROMA):
            features[f"chroma_{i + 1}_mean"] = self._safe_mean(chroma[i])
            features[f"chroma_{i + 1}_std"] = self._safe_std(chroma[i])

        print(f"[Chroma] Computed {len(features)} features  (mean+std per pitch class)")
        print(f"[Chroma] ✔ Chroma extraction complete")
        return features

