"""
Abstract base class for all feature extractors.

Every concrete extractor (MFCC, Chroma, Spectral, etc.) must subclass
`BaseFeatureExtractor` and implement the three abstract methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np


class BaseFeatureExtractor(ABC):
    """Contract that every speech-feature extractor must fulfill."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a short, lowercase identifier for this feature group.

        Examples: ``"mfcc"``, ``"chroma"``, ``"spectral"``.
        """

    @abstractmethod
    def column_names(self) -> List[str]:
        """Return the ordered list of CSV column headers this extractor produces.

        The length **must** match the number of values returned by
        :meth:`extract`.
        """

    @abstractmethod
    def extract(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract features from the raw audio signal.

        Parameters
        ----------
        y : np.ndarray
            Mono audio time-series.
        sr : int
            Sampling rate of *y*.

        Returns
        -------
        dict[str, float]
            Mapping of column-name → scalar feature value.
        """

    # ── convenience helpers ──────────────────────────────────────────

    @staticmethod
    def _safe_mean(arr: np.ndarray) -> float:
        """Return the mean, gracefully handling NaN arrays."""
        val = np.nanmean(arr)
        return 0.0 if np.isnan(val) else float(val)

    @staticmethod
    def _safe_std(arr: np.ndarray) -> float:
        """Return the std, gracefully handling NaN arrays."""
        val = np.nanstd(arr)
        return 0.0 if np.isnan(val) else float(val)

    @staticmethod
    def _safe_min(arr: np.ndarray) -> float:
        """Return the min, ignoring NaNs."""
        valid = arr[~np.isnan(arr)] if isinstance(arr, np.ndarray) else arr
        return float(np.min(valid)) if len(valid) > 0 else 0.0

    @staticmethod
    def _safe_max(arr: np.ndarray) -> float:
        """Return the max, ignoring NaNs."""
        valid = arr[~np.isnan(arr)] if isinstance(arr, np.ndarray) else arr
        return float(np.max(valid)) if len(valid) > 0 else 0.0
