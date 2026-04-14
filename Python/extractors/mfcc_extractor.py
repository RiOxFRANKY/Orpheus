"""
MFCC Feature Extractor.

Extracts 13 Mel-Frequency Cepstral Coefficients plus their first-order
(delta) and second-order (delta-delta) derivatives.  For each of the 39
coefficient tracks the mean and standard deviation are computed, yielding
**78 scalar features** per audio file.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class MFCCExtractor(BaseFeatureExtractor):
    """Extract MFCC, delta-MFCC, and delta²-MFCC statistics."""

    N_MFCC = 13

    @property
    def name(self) -> str:
        return "mfcc"

    def column_names(self) -> List[str]:
        cols: List[str] = []
        for prefix in ("mfcc", "mfcc_delta", "mfcc_delta2"):
            for i in range(1, self.N_MFCC + 1):
                cols.append(f"{prefix}_{i}_mean")
                cols.append(f"{prefix}_{i}_std")
        return cols

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.N_MFCC)
        mfcc_delta = librosa.feature.delta(mfccs)
        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)

        features: Dict[str, float] = {}

        for prefix, data in [
            ("mfcc", mfccs),
            ("mfcc_delta", mfcc_delta),
            ("mfcc_delta2", mfcc_delta2),
        ]:
            for i in range(self.N_MFCC):
                features[f"{prefix}_{i + 1}_mean"] = self._safe_mean(data[i])
                features[f"{prefix}_{i + 1}_std"] = self._safe_std(data[i])

        return features
