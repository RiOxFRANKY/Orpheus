"""
Abstract base class for data export strategies.

Concrete exporters (CSV, JSON, etc.) must subclass `BaseExporter` and
implement the two abstract members.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BaseExporter(ABC):
    """Contract that every export strategy must fulfill."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a short identifier for the export format.

        Examples: ``"csv"``, ``"json"``.
        """

    @abstractmethod
    def export(
        self,
        rows: List[Dict[str, Any]],
        column_order: List[str],
        output_path: Path,
    ) -> Path:
        """Write feature data to disk.

        Parameters
        ----------
        rows : list[dict[str, Any]]
            One dict per audio file; keys are column names.
        column_order : list[str]
            Desired column ordering in the output.
        output_path : Path
            Destination file path.

        Returns
        -------
        Path
            The actual file path that was written.
        """
