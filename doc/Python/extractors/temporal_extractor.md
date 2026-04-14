# temporal_extractor.py Documentation

## Location
`Python/extractors/temporal_extractor.py`

## Overview
A rhythmic-focused feature extractor calculating simplistic dimensional timing properties for track sequencing.

## Key Responsibilities
- Calculates raw global length via `duration_sec` mappings.
- Evaluates estimated structural tempo by calculating peak onset envelopes estimating rhythmic BPM (`tempo_bpm`) dynamically.
- Returns precisely 2 features natively.
