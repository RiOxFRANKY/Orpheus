"""
Core module — Abstract base classes for the Speech Feature Extraction pipeline.

Provides extensible contracts for:
  - Feature extractors (BaseFeatureExtractor)
  - Audio preprocessors (BasePreprocessor)
  - Data exporters (BaseExporter)
"""

from core.base_extractor import BaseFeatureExtractor
from core.base_preprocessor import BasePreprocessor
from core.base_exporter import BaseExporter

__all__ = [
    "BaseFeatureExtractor",
    "BasePreprocessor",
    "BaseExporter",
]
