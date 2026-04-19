"""
Resampler — resample audio to a target sample rate.
"""

from typing import Any, Dict, Tuple

import librosa
import numpy as np

from core.base_preprocessor import BasePreprocessor


class Resampler(BasePreprocessor):
    """Resample the audio signal to a configurable target sample rate."""

    DEFAULT_TARGET_SR = 16_000

    @property
    def name(self) -> str:
        return "resample"

    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        target_sr = self.DEFAULT_TARGET_SR
        resampling_config = settings.get("resampling", {})
        if isinstance(resampling_config, dict):
            target_str = resampling_config.get("target", "")
            if isinstance(target_str, str) and target_str:
                try:
                    target_sr = int(target_str.replace(" Hz", "").strip())
                except ValueError:
                    pass
            elif isinstance(target_str, int):
                target_sr = target_str
        elif "targetSampleRate" in settings:
            target_sr = int(settings["targetSampleRate"])

        print(f"\n{'─'*60}")
        print(f"[Resampler] Input array  : shape={y.shape}, dtype={y.dtype}")
        print(f"[Resampler] Sample rate  : {sr} Hz  →  target: {target_sr} Hz")
        print(f"[Resampler] Duration     : {len(y)/sr:.4f}s  ({len(y):,} samples)")
        print(f"[Resampler] Amplitude    : min={y.min():.6f}, max={y.max():.6f}, mean={y.mean():.6f}")
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=40)
        print(f"[Resampler] y BEFORE (first 20 samples):")
        print(f"            {y[:20]}")

        if sr == target_sr:
            print(f"[Resampler] Already at target rate — skipping resample.")
            return y, sr

        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)

        print(f"[Resampler] Output array : shape={y_resampled.shape}, dtype={y_resampled.dtype}")
        print(f"[Resampler] New duration : {len(y_resampled)/target_sr:.4f}s  ({len(y_resampled):,} samples)")
        print(f"[Resampler] Amplitude    : min={y_resampled.min():.6f}, max={y_resampled.max():.6f}")
        print(f"[Resampler] y AFTER  (first 20 samples):")
        print(f"            {y_resampled[:20]}")
        print(f"[Resampler] ✔ Resample complete  ({sr} Hz → {target_sr} Hz)")
        return y_resampled, target_sr
