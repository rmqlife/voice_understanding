#!/usr/bin/env python3
"""Extract 16 kHz mono WAV from VR videos on NFS (gvfs) via ffmpeg."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.audio import extract_wav_from_media  # noqa: E402
from sense_voice.vr_sources import (  # noqa: E402
    LEGACY_PRESETS,
    finished_dir,
    iter_finished_mp4s,
    local_wav_path,
    resolve_jav_root,
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract VR audio from NFS/gvfs to data/vr/")
    parser.add_argument("--input", type=Path, default=None, help="Source video")
    parser.add_argument(
        "--preset",
        choices=sorted(LEGACY_PRESETS),
        default=None,
        help="Legacy jav/KAVR-5008K paths",
    )
    parser.add_argument(
        "--scan-finished",
        action="store_true",
        help="Extract all VR mp4 under jav/#finished",
    )
    parser.add_argument("--name-filter", default=None, help="Filter when scanning #finished")
    parser.add_argument("--all-mp4", action="store_true", help="Include non-VR mp4 in #finished scan")
    parser.add_argument("--mount", action="store_true", help="gio mount smb://192.168.1.188/jav if needed")
    parser.add_argument("--list-only", action="store_true", help="List matched videos without extracting")
    parser.add_argument("--output", type=Path, default=None, help="Output WAV for single --input")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "data" / "vr",
        help="WAV output directory",
    )
    parser.add_argument("--start", default=None, help="ffmpeg -ss")
    parser.add_argument("--duration", default=None, help="ffmpeg -t (seconds or HH:MM:SS)")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if output WAV exists")
    args = parser.parse_args()

    if args.scan_finished:
        jav_root = resolve_jav_root(mount=args.mount)
        finished = finished_dir(jav_root=jav_root)
        videos = iter_finished_mp4s(
            finished,
            vr_only=not args.all_mp4,
            name_filter=args.name_filter,
        )
        if not videos:
            raise SystemExit("No mp4 matched under jav/#finished")
        for video in videos:
            wav_path = local_wav_path(video, finished, args.output_dir)
            if args.list_only:
                print(video)
                print(f"  -> {wav_path}")
                continue
            if args.skip_existing and wav_path.is_file():
                print(f"skip existing {wav_path}")
                continue
            print(f"extract {video}", flush=True)
            extract_wav_from_media(
                video,
                wav_path,
                start=args.start,
                duration=args.duration,
            )
            print(wav_path)
        return

    if args.input is None and args.preset is None:
        raise SystemExit("Provide --input, --preset, or --scan-finished")

    if args.input is not None:
        input_path = args.input
        output_path = args.output or args.output_dir / f"{input_path.stem}.wav"
    else:
        input_path = Path(LEGACY_PRESETS[args.preset])
        output_path = args.output or args.output_dir / f"vr_{args.preset}.wav"
        env_key = f"VR_SOURCE_{args.preset.upper()}"
        if os.environ.get(env_key):
            input_path = Path(os.environ[env_key])

    if args.list_only:
        print(input_path)
        print(f"  -> {output_path}")
        return

    extract_wav_from_media(
        input_path,
        output_path,
        start=args.start,
        duration=args.duration,
    )
    print(output_path)


if __name__ == "__main__":
    main()
