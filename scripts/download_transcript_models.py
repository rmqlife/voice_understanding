#!/usr/bin/env python3
"""Pre-download FunASR models for transcript pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from sense_voice.models import (  # noqa: E402
    huggingface_cache_dir,
    modelscope_cache_dir,
    warm_funasr_asr,
    warm_funasr_diarize,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download transcript-related models")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--skip-asr", action="store_true", help="Skip SenseVoiceSmall warm-up")
    parser.add_argument("--skip-diarize", action="store_true", help="Skip FunASR cam++ warm-up")
    args = parser.parse_args()

    print(f"ModelScope cache: {modelscope_cache_dir()}")
    print(f"Hugging Face cache: {huggingface_cache_dir()}")

    if not args.skip_asr:
        print("Warming FunASR ASR (SenseVoiceSmall)...")
        warm_funasr_asr(device=args.device)
        print("OK")

    if not args.skip_diarize:
        print("Warming FunASR diarization (cam++)...")
        warm_funasr_diarize(device=args.device)
        print("OK")

    print("Done.")


if __name__ == "__main__":
    main()
