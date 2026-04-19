"""
Silence Remover — strip silent intervals from the signal.

Uses ``librosa.effects.split`` + ``librosa.effects.remix``.
"""

from typing import Any, Dict, Tuple

import librosa
import numpy as np

from core.base_preprocessor import BasePreprocessor


class SilenceRemover(BasePreprocessor):
    """Remove non-speech (silent) intervals from the audio."""

    DEFAULT_TOP_DB = 30

    @property
    def name(self) -> str:
        return "silence_removal"

    def process(
        self,
        y: np.ndarray,
        sr: int,
        settings: Dict[str, Any],
    ) -> Tuple[np.ndarray, int]:
        top_db = int(settings.get("silenceTopDb", self.DEFAULT_TOP_DB))

        duration_before = len(y) / sr

        print(f"\n{'─'*60}")
        print(f"[SilenceRemover] Input array     : shape={y.shape}, dtype={y.dtype}")
        print(f"[SilenceRemover] Sample rate     : {sr} Hz")
        print(f"[SilenceRemover] Duration before : {duration_before:.4f}s  ({len(y):,} samples)")
        print(f"[SilenceRemover] Amplitude       : min={y.min():.6f}, max={y.max():.6f}")
        print(f"[SilenceRemover] Silence thresh  : top_db={top_db}  (anything {top_db} dB below peak = silent)")
        np.set_printoptions(precision=8, suppress=False, linewidth=120, threshold=40)
        print(f"[SilenceRemover] y BEFORE (first 20 samples):")
        print(f"                 {y[:20]}")

        intervals = librosa.effects.split(y, top_db=top_db)

        print(f"[SilenceRemover] Non-silent intervals found: {len(intervals)}")
        for idx, (start, end) in enumerate(intervals):
            start_sec = start / sr
            end_sec   = end / sr
            print(f"[SilenceRemover]   [{idx+1}] samples {start:,}–{end:,}  "
                  f"({start_sec:.3f}s – {end_sec:.3f}s, "
                  f"duration={end_sec - start_sec:.3f}s)")

        if len(intervals) == 0:
            print(f"[SilenceRemover] ⚠ No non-silent regions found — returning original signal.")
            return y, sr

        y_trimmed = librosa.effects.remix(y, intervals)

        duration_after = len(y_trimmed) / sr
        removed_sec    = duration_before - duration_after

        print(f"[SilenceRemover] Output array    : shape={y_trimmed.shape}, dtype={y_trimmed.dtype}")
        print(f"[SilenceRemover] Duration after  : {duration_after:.4f}s  ({len(y_trimmed):,} samples)")
        print(f"[SilenceRemover] Silence removed : {removed_sec:.4f}s  "
              f"({removed_sec/duration_before*100:.1f}% of original)")
        print(f"[SilenceRemover] y AFTER  (first 20 samples):")
        print(f"                 {y_trimmed[:20]}")
        print(f"[SilenceRemover] ✔ Silence removal complete")
        return y_trimmed, sr

