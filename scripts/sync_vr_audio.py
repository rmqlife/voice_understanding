#!/usr/bin/env python3
"""Extract 16 kHz mono WAV from VR videos on NFS (gvfs) via ffmpeg."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_NFS_GLOB = {
    "kavr500_part2": (
        "/run/user/1000/gvfs/smb-share:server=atop-nuc-fnos.local,share=jav/"
        "KAVR-5008K/489155.com@KAVR-500.PART2_8K.mp4"
    ),
    "kavr500_part3": (
        "/run/user/1000/gvfs/smb-share:server=atop-nuc-fnos.local,share=jav/"
        "KAVR-5008K/489155.com@KAVR-500.PART3_8K.mp4"
    ),
}


def extract_wav(input_path: Path, output_path: Path, *, sample_rate: int = 16000) -> None:
    if not input_path.is_file():
        raise FileNotFoundError(f"input not found: {input_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-map",
        "0:a:0",
        "-ar",
        str(sample_rate),
        "-ac",
        "1",
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]
    subprocess.run(cmd, check=True)
    print(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract VR audio from NFS/gvfs to WAV")
    parser.add_argument("--input", type=Path, default=None, help="Source video (overrides --preset)")
    parser.add_argument(
        "--preset",
        choices=sorted(DEFAULT_NFS_GLOB),
        default=None,
        help="Known NFS source under gvfs jav/KAVR-5008K",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output WAV (default: test_voice_clips/vr_<preset>.wav)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "test_voice_clips",
        help="Directory when --output omitted",
    )
    args = parser.parse_args()

    if args.input is None and args.preset is None:
        raise SystemExit("Provide --input or --preset")

    if args.input is not None:
        input_path = args.input
        output_path = args.output or args.output_dir / f"{input_path.stem}.wav"
    else:
        input_path = Path(DEFAULT_NFS_GLOB[args.preset])
        output_path = args.output or args.output_dir / f"vr_{args.preset}.wav"
        env_key = f"VR_SOURCE_{args.preset.upper()}"
        if os.environ.get(env_key):
            input_path = Path(os.environ[env_key])

    extract_wav(input_path, output_path)


if __name__ == "__main__":
    main()
