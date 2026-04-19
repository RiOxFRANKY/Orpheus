"""
Normalizer — peak-normalise audio to a target dBFS level.
"""

from typing import Any, Dict, Tuple

import numpy as np

from core.base_preprocessor import BasePreprocessor


class Normalizer(BasePreprocessor):
    """Peak-normalise the signal so that max amplitude matches target dBFS."""

    DEFAULT_TARGET_DBFS = -3.0

    @property
    def name(self) -> str:
        return "normalize"

    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        target_dbfs = self.DEFAULT_TARGET_DBFS
        norm_config = settings.get("normalization_dbfs", {})
        if isinstance(norm_config, dict):
            target_dbfs = float(norm_config.get("value", self.DEFAULT_TARGET_DBFS))
        elif "targetDbfs" in settings:
            target_dbfs = float(settings["targetDbfs"])

        peak = np.max(np.abs(y))
        current_dbfs = 20.0 * np.log10(peak) if peak > 0 else float("-inf")

        print(f"\n{'─'*60}")
        print(f"[Normalizer] Input array   : shape={y.shape}, dtype={y.dtype}")
        print(f"[Normalizer] Sample rate   : {sr} Hz")
        print(f"[Normalizer] Amplitude     : min={y.min():.6f}, max={y.max():.6f}")
        print(f"[Normalizer] Peak sample   : {peak:.6f}  ({current_dbfs:.2f} dBFS)")
        print(f"[Normalizer] Target level  : {target_dbfs:.2f} dBFS")
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=40)
        print(f"[Normalizer] y BEFORE (first 20 samples):")
        print(f"             {y[:20]}")

        if peak == 0:
            print(f"[Normalizer] ⚠ Signal is all-zeros — skipping normalization.")
            return y, sr

        # Convert target dBFS to linear gain
        target_linear = 10.0 ** (target_dbfs / 20.0)
        gain = target_linear / peak

        print(f"[Normalizer] Target linear : {target_linear:.6f}")
        print(f"[Normalizer] Gain applied  : ×{gain:.6f}  ({20*np.log10(gain):+.2f} dB)")

        y_norm = (y * gain).astype(y.dtype)
        new_peak = np.max(np.abs(y_norm))

        print(f"[Normalizer] Output array  : shape={y_norm.shape}, dtype={y_norm.dtype}")
        print(f"[Normalizer] New peak      : {new_peak:.6f}  ({20*np.log10(new_peak) if new_peak>0 else 0:.2f} dBFS)")
        print(f"[Normalizer] y AFTER  (first 20 samples):")
        print(f"             {y_norm[:20]}")
        print(f"[Normalizer] ✔ Normalization complete  (target={target_dbfs} dBFS)")
        return y_norm, sr
