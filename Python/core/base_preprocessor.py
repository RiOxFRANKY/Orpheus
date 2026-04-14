"""
Abstract base class for all audio preprocessing steps.

Each concrete preprocessor (resampling, noise reduction, etc.) must subclass
`BasePreprocessor` and implement the two abstract members.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

import numpy as np


class BasePreprocessor(ABC):
    """Contract that every preprocessing step must fulfill."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a short, lowercase identifier for this step.

        Examples: ``"resample"``, ``"noise_reduction"``, ``"normalize"``.
        """

    @abstractmethod
    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        """Apply the preprocessing step and return the modified signal.

        Parameters
        ----------
        y : np.ndarray
            Mono audio time-series.
        sr : int
            Current sampling rate.
        settings : dict
            User-provided preprocessing settings from the GUI config.

        Returns
        -------
        tuple[np.ndarray, int]
            ``(processed_signal, new_sample_rate)``
        """
