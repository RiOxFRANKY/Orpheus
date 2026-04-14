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
        if peak == 0:
            return y, sr

        # Convert target dBFS to linear gain
        target_linear = 10.0 ** (target_dbfs / 20.0)
        gain = target_linear / peak

        return (y * gain).astype(y.dtype), sr
