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
        print(f"\n{'─'*60}")
        print(f"[ZCR] Input array  : shape={y.shape}, dtype={y.dtype}, sr={sr} Hz")
        print(f"[ZCR] Duration     : {len(y)/sr:.4f}s")

        zcr = librosa.feature.zero_crossing_rate(y)[0]
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=200)
        zcr_mean = self._safe_mean(zcr)
        zcr_std  = self._safe_std(zcr)

        print(f"[ZCR] ZCR array    : shape={zcr.shape}  (one value per frame)")
        print(f"[ZCR] ZCR values   (all frames):")
        print(zcr)
        print(f"[ZCR] Value range  : min={zcr.min():.6f}, max={zcr.max():.6f}")
        print(f"[ZCR] zcr_mean     : {zcr_mean:.6f}  (avg sign-changes per frame)")
        print(f"[ZCR] zcr_std      : {zcr_std:.6f}")
        print(f"[ZCR] ✔ ZCR extraction complete")

        return {
            "zcr_mean": zcr_mean,
            "zcr_std":  zcr_std,
        }

