#!/usr/bin/env python3
"""Extract benchmark-ready WAV audio from media files."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Input audio/video file")
    parser.add_argument("output", type=Path, help="Output WAV path")
    parser.add_argument("--start", default=None, help="Optional start timestamp, e.g. 00:02:00")
    parser.add_argument("--duration", default=None, help="Optional duration, e.g. 180 or 00:03:00")
    parser.add_argument("--sample-rate", type=int, default=16000)
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"input not found: {args.input}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y"]
    if args.start:
        cmd.extend(["-ss", args.start])
    cmd.extend(["-i", str(args.input)])
    if args.duration:
        cmd.extend(["-t", args.duration])
    cmd.extend(
        [
            "-vn",
            "-map",
            "0:a:0",
            "-ar",
            str(args.sample_rate),
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(args.output),
        ]
    )
    subprocess.run(cmd, check=True)
    print(args.output)


if __name__ == "__main__":
    main()
