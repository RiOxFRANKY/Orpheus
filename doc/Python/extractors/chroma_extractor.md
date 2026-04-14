# chroma_extractor.py Documentation

## Location
`Python/extractors/chroma_extractor.py`

## Overview
Calculates structural harmonic pitch-classes (Chroma) over the audio utilizing Short-Time Fourier Transforms (STFT).

## Key Responsibilities
- Computes standard 12-bin structural semitone classes logically mapping to Western musical scales statically.
- Generates numeric outputs tracking explicit means (`_mean`) and standard variance spreads (`_std`) tightly over all 12 target structural bins.
- Produces exactly 24 discrete floating-point features directly per file dynamically.
