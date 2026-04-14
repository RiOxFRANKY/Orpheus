"""
Spectral Feature Extractor.

Computes the following spectral descriptors and reports mean + std for each:
  - Spectral Centroid
  - Spectral Bandwidth
  - Spectral Roll-off (85 %)
  - Spectral Contrast (7 bands)
  - Spectral Flatness

Total features: 2 + 2 + 2 + 14 + 2 = **22 scalar features**.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class SpectralExtractor(BaseFeatureExtractor):
    """Extract spectral shape descriptors."""

    N_CONTRAST_BANDS = 7

    @property
    def name(self) -> str:
        return "spectral"

    def column_names(self) -> List[str]:
        cols: List[str] = [
            "spectral_centroid_mean", "spectral_centroid_std",
            "spectral_bandwidth_mean", "spectral_bandwidth_std",
            "spectral_rolloff_mean", "spectral_rolloff_std",
        ]
        for i in range(1, self.N_CONTRAST_BANDS + 1):
            cols.append(f"spectral_contrast_{i}_mean")
            cols.append(f"spectral_contrast_{i}_std")
        cols += ["spectral_flatness_mean", "spectral_flatness_std"]
        return cols

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        features: Dict[str, float] = {}

        # Spectral Centroid
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        features["spectral_centroid_mean"] = self._safe_mean(cent)
        features["spectral_centroid_std"] = self._safe_std(cent)

        # Spectral Bandwidth
        bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        features["spectral_bandwidth_mean"] = self._safe_mean(bw)
        features["spectral_bandwidth_std"] = self._safe_std(bw)

        # Spectral Roll-off (85 %)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)[0]
        features["spectral_rolloff_mean"] = self._safe_mean(rolloff)
        features["spectral_rolloff_std"] = self._safe_std(rolloff)

        # Spectral Contrast (7 frequency bands)
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr, n_bands=self.N_CONTRAST_BANDS)
        for i in range(self.N_CONTRAST_BANDS):
            features[f"spectral_contrast_{i + 1}_mean"] = self._safe_mean(contrast[i])
            features[f"spectral_contrast_{i + 1}_std"] = self._safe_std(contrast[i])

        # Spectral Flatness
        flat = librosa.feature.spectral_flatness(y=y)[0]
        features["spectral_flatness_mean"] = self._safe_mean(flat)
        features["spectral_flatness_std"] = self._safe_std(flat)

        return features
