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
        print(f"\n{'─'*60}")
        print(f"[MFCC] Input array   : shape={y.shape}, dtype={y.dtype}, sr={sr} Hz")
        print(f"[MFCC] n_mfcc        : {self.N_MFCC}  →  computing 13 + delta + delta²")

        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.N_MFCC)
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=200)
        print(f"[MFCC] MFCC matrix   : shape={mfccs.shape}  (coefficients × frames)")
        print(f"[MFCC] Value range   : min={mfccs.min():.4f}, max={mfccs.max():.4f}")
        print(f"[MFCC] Full MFCC matrix (13 coefficients × first 20 frames):")
        print(mfccs[:, :20])

        mfcc_delta = librosa.feature.delta(mfccs)
        print(f"[MFCC] Delta matrix  : shape={mfcc_delta.shape}, range=[{mfcc_delta.min():.4f}, {mfcc_delta.max():.4f}]")
        print(f"[MFCC] Delta (first 20 frames):")
        print(mfcc_delta[:, :20])

        mfcc_delta2 = librosa.feature.delta(mfccs, order=2)
        print(f"[MFCC] Delta² matrix : shape={mfcc_delta2.shape}, range=[{mfcc_delta2.min():.4f}, {mfcc_delta2.max():.4f}]")
        print(f"[MFCC] Delta² (first 20 frames):")
        print(mfcc_delta2[:, :20])

        features: Dict[str, float] = {}

        for prefix, data in [
            ("mfcc", mfccs),
            ("mfcc_delta", mfcc_delta),
            ("mfcc_delta2", mfcc_delta2),
        ]:
            for i in range(self.N_MFCC):
                features[f"{prefix}_{i + 1}_mean"] = self._safe_mean(data[i])
                features[f"{prefix}_{i + 1}_std"] = self._safe_std(data[i])

        print(f"[MFCC] Computed {len(features)} features  (mean+std for each of 39 tracks)")
        print(f"[MFCC] mfcc_1_mean={features['mfcc_1_mean']:.4f}, "
              f"mfcc_1_std={features['mfcc_1_std']:.4f}, "
              f"mfcc_2_mean={features['mfcc_2_mean']:.4f}")
        print(f"[MFCC] ✔ MFCC extraction complete")
        return features

