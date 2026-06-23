#!/usr/bin/env python3
"""Smoke test: transcribe the bundled Chinese sample audio."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from sense_voice import SenseVoice

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "models" / "asr_example_zh.wav"


def main() -> None:
    if not SAMPLE.is_file():
        print("Sample audio missing. Run: pixi run download-model")
        sys.exit(1)

    sv = SenseVoice(use_gpu=True)
    result = sv.transcribe(SAMPLE, raw=True)
    print("Raw output:")
    print(result.raw)
    print("\nTranscription:")
    print(result.text)
    print(
        f"\n音频 {result.audio_seconds:.1f}s | "
        f"处理 {result.process_seconds:.1f}s | "
        f"RTF {result.rtf:.3f}"
    )


if __name__ == "__main__":
    main()
