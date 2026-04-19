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
        rms_before = float(np.sqrt(np.mean(y ** 2)))

        print(f"\n{'─'*60}")
        print(f"[NoiseReducer] Input array  : shape={y.shape}, dtype={y.dtype}")
        print(f"[NoiseReducer] Sample rate  : {sr} Hz")
        print(f"[NoiseReducer] RMS power    : {rms_before:.6f}  (before reduction)")
        print(f"[NoiseReducer] Amplitude    : min={y.min():.6f}, max={y.max():.6f}")
        print(f"[NoiseReducer] Algorithm    : stationary spectral gating (noisereduce)")
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=40)
        print(f"[NoiseReducer] y BEFORE (first 20 samples):")
        print(f"               {y[:20]}")

        try:
            import noisereduce as nr

            print(f"[NoiseReducer] Running spectral gate...")
            y_clean = nr.reduce_noise(y=y, sr=sr, stationary=True)

            rms_after = float(np.sqrt(np.mean(y_clean ** 2)))
            suppression_db = 20 * np.log10(rms_after / rms_before) if rms_before > 0 else 0.0

            print(f"[NoiseReducer] Output array : shape={y_clean.shape}, dtype={y_clean.dtype}")
            print(f"[NoiseReducer] RMS power    : {rms_after:.6f}  (after reduction)")
            print(f"[NoiseReducer] Noise change : {suppression_db:+.2f} dB")
            print(f"[NoiseReducer] y AFTER  (first 20 samples):")
            print(f"               {y_clean[:20]}")
            print(f"[NoiseReducer] ✔ Noise reduction complete")
            return y_clean, sr
        except ImportError:
            # Graceful fallback — noisereduce not installed
            print("[NoiseReducer] ⚠ noisereduce not installed, skipping.")
            return y, sr

