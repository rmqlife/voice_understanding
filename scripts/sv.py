#!/usr/bin/env python3
"""Transcribe audio (wav/mp3/...) to text."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from sense_voice import SenseVoice

WAV_EXTS = {".wav", ".wave"}


def to_wav(src: Path) -> tuple[Path, bool]:
    """Return a 16kHz mono WAV path. Second value is whether caller should delete it."""
    if src.suffix.lower() in WAV_EXTS:
        return src, False

    tmp = Path(tempfile.mktemp(suffix=".wav"))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(tmp),
        ],
        check=True,
    )
    return tmp, True


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sv",
        description="Transcribe audio to text (wav, mp3, m4a, flac, ...)",
    )
    parser.add_argument("audio", help="Input audio file")
    parser.add_argument("-l", "--language", default="zh", help="Language (auto/zh/en/...)")
    parser.add_argument("-t", "--threads", type=int, default=4, help="CPU threads")
    parser.add_argument("--cpu", action="store_true", help="Disable Metal GPU")
    parser.add_argument(
        "--no-punct",
        action="store_true",
        help="Disable punctuation (ITN)",
    )
    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        help="Hide VAD segment timestamps",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide timing summary",
    )
    args = parser.parse_args()

    src = Path(args.audio)
    if not src.is_file():
        print(f"file not found: {src}", file=sys.stderr)
        sys.exit(1)

    wav, cleanup = to_wav(src)
    try:
        sv = SenseVoice(
            threads=args.threads,
            use_gpu=not args.cpu,
            language=args.language,
            use_itn=not args.no_punct,
        )
        result = sv.transcribe(
            wav,
            raw=True,
            with_timestamps=not args.no_timestamps,
        )
        print(result.text, flush=True)
        if not args.quiet:
            print(
                f"\n音频 {result.audio_seconds:.1f}s | "
                f"处理 {result.process_seconds:.1f}s | "
                f"RTF {result.rtf:.3f}",
                file=sys.stderr,
                flush=True,
            )
    finally:
        if cleanup:
            wav.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
