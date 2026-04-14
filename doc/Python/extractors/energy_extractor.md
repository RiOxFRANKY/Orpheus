# energy_extractor.py Documentation

## Location
`Python/extractors/energy_extractor.py`

## Overview
A powerful Prosodic feature extractor specialized primarily to map and analyze amplitude intensity structures strictly (Loudness, Shimmer, Harmonics vs Background statics).

## Key Responsibilities
- Calculates global Root Mean Square Energy bounds statistically (`rms_mean`, `rms_min`, `rms_max`, `rms_std`).
- Calculates Shimmer numerically mapping sequential local amplitude discrepancies.
- Implements a sophisticated custom `_estimate_hnr()` function natively orchestrating auto-correlation metrics across safe vocal fundamental thresholds automatically (75Hz - 500Hz) mapping logical peak ratios successfully.
- Generates 6 discrete scalar features per process loop.
