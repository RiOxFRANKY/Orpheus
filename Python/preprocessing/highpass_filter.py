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

        if cutoff_hz >= nyquist:
            return y, sr

        sos = butter(
            self.FILTER_ORDER,
            cutoff_hz / nyquist,
            btype="high",
            output="sos",
        )
        y_filtered = sosfilt(sos, y).astype(np.float32)
        return y_filtered, sr
