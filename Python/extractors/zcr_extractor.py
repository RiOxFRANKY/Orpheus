"""
Zero-Crossing Rate Extractor.

Reports the mean and standard deviation of the frame-level ZCR —
**2 scalar features**.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class ZCRExtractor(BaseFeatureExtractor):
    """Extract Zero-Crossing Rate statistics."""

    @property
    def name(self) -> str:
        return "zcr"

    def column_names(self) -> List[str]:
        return ["zcr_mean", "zcr_std"]

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        return {
            "zcr_mean": self._safe_mean(zcr),
            "zcr_std": self._safe_std(zcr),
        }
