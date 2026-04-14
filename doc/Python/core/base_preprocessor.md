# base_preprocessor.py Documentation

## Location
`Python/core/base_preprocessor.py`

## Overview
An abstract base class mathematically outlining rules for digital signal preprocessing (DSP) steps altering the raw target audio matrices identically prior to dataset extractions.

## Key Responsibilities
- Enforces `process()` pipeline signatures cleanly, mutating numpy arrays cleanly returning a tuple `(processed_signal, new_sample_rate)` intelligently.
- Demands a `name` index allowing pipeline resolvers dynamically to route UI checkboxes logically to running active class instances effectively.
