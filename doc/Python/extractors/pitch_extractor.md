# pitch_extractor.py Documentation

## Location
`Python/extractors/pitch_extractor.py`

## Overview
A complex fundamental tone (F0) frequency extraction component focusing specifically upon resolving exact literal pitch estimations avoiding octave bleed.

## Key Responsibilities
- Deploys the sophisticated probabilistic YIN parameterization framework (`librosa.pyin`) mapping absolute human fundamental frequency parameters natively (tracking specifically bounds `C2` - `C7` notes).
- Nullifies NaN artifacts logically preventing mathematical collapse efficiently specifically across un-voiced frames seamlessly.
- Estimates "Jitter" accurately measuring logical perturbations strictly tracing absolute discrete time structural F0 variances effectively dynamically.
