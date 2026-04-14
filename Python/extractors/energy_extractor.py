"""
Energy Feature Extractor.

Computes:
  - RMS Energy (mean, std, min, max)
  - Shimmer (amplitude perturbation — relative)
  - HNR — Harmonics-to-Noise Ratio (estimated via autocorrelation)

Total: **6 scalar features**.
"""

from typing import Dict, List

import librosa
import numpy as np

from core.base_extractor import BaseFeatureExtractor


class EnergyExtractor(BaseFeatureExtractor):
    """Extract energy / amplitude-related features."""

    @property
    def name(self) -> str:
        return "energy"

    def column_names(self) -> List[str]:
        return [
            "rms_mean", "rms_std", "rms_min", "rms_max",
            "shimmer_relative",
            "hnr_db",
        ]

    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        # ── RMS Energy ───────────────────────────────────────────
        rms = librosa.feature.rms(y=y)[0]

        features: Dict[str, float] = {
            "rms_mean": self._safe_mean(rms),
            "rms_std": self._safe_std(rms),
            "rms_min": self._safe_min(rms),
            "rms_max": self._safe_max(rms),
        }

        # ── Shimmer (relative) ───────────────────────────────────
        # Mean absolute difference of consecutive frame amplitudes
        # normalised by the mean amplitude.
        if len(rms) > 1:
            diffs = np.abs(np.diff(rms))
            mean_amp = np.mean(rms)
            features["shimmer_relative"] = (
                float(np.mean(diffs) / mean_amp) if mean_amp > 0 else 0.0
            )
        else:
            features["shimmer_relative"] = 0.0

        # ── HNR (Harmonics-to-Noise Ratio) ───────────────────────
        features["hnr_db"] = self._estimate_hnr(y, sr)

        return features

    # ── private helpers ──────────────────────────────────────────

    @staticmethod
    def _estimate_hnr(y: np.ndarray, sr: int) -> float:
        """Estimate HNR via autocorrelation of the signal.

        HNR = 10 · log10(r_max / (1 − r_max))  where r_max is the peak
        of the normalised autocorrelation in the plausible pitch range.
        """
        # Restrict the search to the F0 range 75 Hz – 500 Hz
        min_lag = int(sr / 500)
        max_lag = int(sr / 75)

        if max_lag >= len(y):
            return 0.0

        # Normalised autocorrelation
        y_centered = y - np.mean(y)
        autocorr = np.correlate(y_centered[:max_lag * 2], y_centered[:max_lag * 2], mode="full")
        autocorr = autocorr[len(autocorr) // 2:]  # keep positive lags
        if autocorr[0] == 0:
            return 0.0
        autocorr = autocorr / autocorr[0]

        # Find the peak in the valid lag range
        if min_lag >= len(autocorr) or max_lag >= len(autocorr):
            return 0.0

        search_region = autocorr[min_lag:max_lag]
        if len(search_region) == 0:
            return 0.0

        r_max = float(np.max(search_region))
        r_max = np.clip(r_max, 1e-10, 1.0 - 1e-10)
        hnr = 10.0 * np.log10(r_max / (1.0 - r_max))
        return float(hnr)
