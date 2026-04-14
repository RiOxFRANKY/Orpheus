"""
Noise Reducer — spectral-gating noise reduction.

Uses the ``noisereduce`` library for stationary noise reduction.
"""

from typing import Any, Dict, Tuple

import numpy as np

from core.base_preprocessor import BasePreprocessor


class NoiseReducer(BasePreprocessor):
    """Apply spectral-gating noise reduction."""

    @property
    def name(self) -> str:
        return "noise_reduction"

    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        try:
            import noisereduce as nr

            y_clean = nr.reduce_noise(y=y, sr=sr, stationary=True)
            return y_clean, sr
        except ImportError:
            # Graceful fallback — noisereduce not installed
            print("[NoiseReducer] noisereduce not installed, skipping.")
            return y, sr
