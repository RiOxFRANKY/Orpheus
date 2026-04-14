"""
Silence Remover — strip silent intervals from the signal.

Uses ``librosa.effects.split`` + ``librosa.effects.remix``.
"""

from typing import Any, Dict, Tuple

import librosa
import numpy as np

from core.base_preprocessor import BasePreprocessor


class SilenceRemover(BasePreprocessor):
    """Remove non-speech (silent) intervals from the audio."""

    DEFAULT_TOP_DB = 30

    @property
    def name(self) -> str:
        return "silence_removal"

    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        top_db = int(settings.get("silenceTopDb", self.DEFAULT_TOP_DB))

        intervals = librosa.effects.split(y, top_db=top_db)
        if len(intervals) == 0:
            return y, sr

        y_trimmed = librosa.effects.remix(y, intervals)
        return y_trimmed, sr
