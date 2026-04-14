# zcr_extractor.py Documentation

## Location
`Python/extractors/zcr_extractor.py`

## Overview
Zero-Crossing Rate calculates precisely how rapidly raw audio signals toggle structurally across the 0-value axis baseline per-frame predicting overall percussive noisiness effectively.

## Key Responsibilities
- Spawns simple discrete averages (`zcr_mean`) and standard structural standard deviations (`zcr_std`).
- Resolves rapidly pushing exactly 2 array values dynamically per pass over `y`.
