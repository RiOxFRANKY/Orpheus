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
        print(f"\n{'─'*60}")
        print(f"[Energy] Input array   : shape={y.shape}, dtype={y.dtype}, sr={sr} Hz")

        # ── RMS Energy ───────────────────────────────────────────
        rms = librosa.feature.rms(y=y)[0]
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=200)
        print(f"[Energy] RMS array     : shape={rms.shape}  (one value per frame)")
        print(f"[Energy] RMS values    (all frames):")
        print(rms)
        print(f"[Energy] RMS range     : min={rms.min():.6f}, max={rms.max():.6f}, mean={rms.mean():.6f}")

        features: Dict[str, float] = {
            "rms_mean": self._safe_mean(rms),
            "rms_std":  self._safe_std(rms),
            "rms_min":  self._safe_min(rms),
            "rms_max":  self._safe_max(rms),
        }
        print(f"[Energy] rms_mean={features['rms_mean']:.6f}, "
              f"rms_std={features['rms_std']:.6f}, "
              f"rms_min={features['rms_min']:.6f}, "
              f"rms_max={features['rms_max']:.6f}")

        # ── Shimmer (relative) ───────────────────────────────────
        # Mean absolute difference of consecutive frame amplitudes
        # normalised by the mean amplitude.
        if len(rms) > 1:
            diffs    = np.abs(np.diff(rms))
            mean_amp = np.mean(rms)
            shimmer  = float(np.mean(diffs) / mean_amp) if mean_amp > 0 else 0.0
            features["shimmer_relative"] = shimmer
            print(f"[Energy] Shimmer calc  : mean|Δrms|={np.mean(diffs):.6f} / mean_rms={mean_amp:.6f} "
                  f"= {shimmer:.6f} (relative)")
        else:
            features["shimmer_relative"] = 0.0
            print(f"[Energy] Shimmer       : not enough frames — set to 0.0")

        # ── HNR (Harmonics-to-Noise Ratio) ───────────────────────
        print(f"[Energy] HNR           : estimating via autocorrelation...")
        features["hnr_db"] = self._estimate_hnr(y, sr)
        print(f"[Energy] hnr_db        : {features['hnr_db']:.4f} dB")

        print(f"[Energy] ✔ Energy extraction complete")
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

        print(f"[Energy]   HNR lag range : {min_lag}–{max_lag} samples "
              f"({sr/max_lag:.0f} Hz – {sr/min_lag:.0f} Hz)")

        if max_lag >= len(y):
            print(f"[Energy]   HNR ⚠ signal too short — returning 0.0")
            return 0.0

        # Normalised autocorrelation
        y_centered = y - np.mean(y)
        autocorr = np.correlate(y_centered[:max_lag * 2], y_centered[:max_lag * 2], mode="full")
        autocorr = autocorr[len(autocorr) // 2:]  # keep positive lags
        if autocorr[0] == 0:
            print(f"[Energy]   HNR ⚠ zero energy signal — returning 0.0")
            return 0.0
        autocorr = autocorr / autocorr[0]

        print(f"[Energy]   Autocorr array: shape={autocorr.shape}, "
              f"peak_in_range=at lag {np.argmax(autocorr[min_lag:max_lag]) + min_lag}")

        # Find the peak in the valid lag range
        if min_lag >= len(autocorr) or max_lag >= len(autocorr):
            return 0.0

        search_region = autocorr[min_lag:max_lag]
        if len(search_region) == 0:
            return 0.0

        r_max = float(np.max(search_region))
        r_max = np.clip(r_max, 1e-10, 1.0 - 1e-10)
        hnr   = 10.0 * np.log10(r_max / (1.0 - r_max))
        print(f"[Energy]   r_max={r_max:.6f}  →  HNR=10*log10({r_max:.4f}/{1-r_max:.4f})={hnr:.4f} dB")
        return float(hnr)

