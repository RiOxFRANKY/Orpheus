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

        if sr == target_sr:
            return y, sr

        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=target_sr)
        return y_resampled, target_sr
