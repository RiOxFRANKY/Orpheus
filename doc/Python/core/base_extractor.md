# base_extractor.py Documentation

## Location
`Python/core/base_extractor.py`

## Overview
A critical abstract base class (ABC) formulating the universal contract forced upon all mathematical feature extraction pipelines (MFCC, Chroma, etc).

## Key Responsibilities
- Mandates `name` and strictly sorted `column_names()` representations.
- Enforces the `extract()` mathematical entrypoint cleanly requiring `y` (numpy time-series array) and `sr` (sample rate integer).
- Provides robust protected numeric helpers intrinsically (`_safe_mean`, `_safe_std`, `_safe_max`, `_safe_min`) heavily safeguarding subsequent NumPy analytics algorithms gracefully bypassing division-by-zeros or NaN matrix collapses safely.
