"""
CSV Exporter — write extracted features to a structured CSV file.
"""

import csv
from pathlib import Path
from typing import Any, Dict, List

from core.base_exporter import BaseExporter


class CSVExporter(BaseExporter):
    """Export feature data to a structured CSV file."""

    @property
    def name(self) -> str:
        return "csv"

    def export(
        self,
        rows: List[Dict[str, Any]],
        column_order: List[str],
        output_path: Path,
    ) -> Path:
        """Write rows to *output_path* as a CSV.

        Parameters
        ----------
        rows : list[dict]
            One dict per audio file.  Keys are column names.
        column_order : list[str]
            Desired column ordering (the ``filename`` column is always
            prepended automatically if not present).
        output_path : Path
            Target ``.csv`` file.

        Returns
        -------
        Path
            The path that was written.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Ensure 'filename' is the first column
        headers = list(column_order)
        if "filename" not in headers:
            headers.insert(0, "filename")

        with open(output_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        return output_path
