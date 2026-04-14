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
        stft = np.abs(librosa.stft(y))
        chroma = librosa.feature.chroma_stft(S=stft, sr=sr, n_chroma=self.N_CHROMA)

        features: Dict[str, float] = {}
        for i in range(self.N_CHROMA):
            features[f"chroma_{i + 1}_mean"] = self._safe_mean(chroma[i])
            features[f"chroma_{i + 1}_std"] = self._safe_std(chroma[i])

        return features
