"""
High-Pass Filter — attenuate frequencies below a configurable cutoff.

Uses a Butterworth filter via ``scipy.signal``.
"""

from typing import Any, Dict, Tuple

import numpy as np
from scipy.signal import butter, sosfilt

from core.base_preprocessor import BasePreprocessor


class HighPassFilter(BasePreprocessor):
    """Apply a 4th-order Butterworth high-pass filter."""

    DEFAULT_CUTOFF_HZ = 80
    FILTER_ORDER = 4

    @property
    def name(self) -> str:
        return "highpass_filter"

    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        cutoff_hz = self.DEFAULT_CUTOFF_HZ
        hp_config = settings.get("high_pass_hz", {})
        if isinstance(hp_config, dict):
            cutoff_hz = int(hp_config.get("frequency", self.DEFAULT_CUTOFF_HZ))
        elif "highpassCutoff" in settings:
            cutoff_hz = int(settings["highpassCutoff"])
        nyquist = sr / 2.0

        print(f"\n{'─'*60}")
        print(f"[HighPassFilter] Input array    : shape={y.shape}, dtype={y.dtype}")
        print(f"[HighPassFilter] Sample rate    : {sr} Hz")
        print(f"[HighPassFilter] Nyquist freq   : {nyquist:.1f} Hz")
        print(f"[HighPassFilter] Cutoff freq    : {cutoff_hz} Hz  (normalised: {cutoff_hz/nyquist:.5f})")
        print(f"[HighPassFilter] Filter order   : {self.FILTER_ORDER} (Butterworth)")
        print(f"[HighPassFilter] Amplitude pre  : min={y.min():.6f}, max={y.max():.6f}, rms={float(np.sqrt(np.mean(y**2))):.6f}")
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=40)
        print(f"[HighPassFilter] y BEFORE (first 20 samples):")
        print(f"                 {y[:20]}")

        if cutoff_hz >= nyquist:
            print(f"[HighPassFilter] ⚠ Cutoff ({cutoff_hz} Hz) ≥ Nyquist ({nyquist} Hz) — skipping filter.")
            return y, sr

        sos = butter(
            self.FILTER_ORDER,
            cutoff_hz / nyquist,
            btype="high",
            output="sos",
        )
        print(f"[HighPassFilter] SOS coefficients: shape={sos.shape}  (sections × 6)")
        print(f"[HighPassFilter]   SOS[0] = {sos[0].round(8).tolist()}")

        y_filtered = sosfilt(sos, y).astype(np.float32)

        print(f"[HighPassFilter] Output array   : shape={y_filtered.shape}, dtype={y_filtered.dtype}")
        print(f"[HighPassFilter] Amplitude post : min={y_filtered.min():.6f}, max={y_filtered.max():.6f}, rms={float(np.sqrt(np.mean(y_filtered**2))):.6f}")
        print(f"[HighPassFilter] y AFTER  (first 20 samples):")
        print(f"                 {y_filtered[:20]}")
        print(f"[HighPassFilter] ✔ High-pass filter applied  (cutoff={cutoff_hz} Hz)")
        return y_filtered, sr
