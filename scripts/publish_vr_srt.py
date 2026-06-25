#!/usr/bin/env python3
"""Copy generated SRT files next to source VR videos on NFS (gvfs)."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_vr_audio import DEFAULT_NFS_GLOB
DEFAULT_SRT_DIR = ROOT / "reports" / "srt"

# WAV stem used in reports/srt/ when produced via sync_vr_audio + vr-subtitle-test.
PRESET_SRT_STEM = {
    "kavr500_part2": "vr_kavr500_part2",
    "kavr500_part3": "vr_kavr500_part3",
}


def publish_srt(
    video_path: Path,
    srt_dir: Path,
    *,
    srt_stem: str,
    kinds: tuple[str, ...] = ("asr", "zh"),
) -> list[Path]:
    if not video_path.is_file():
        raise FileNotFoundError(f"video not found: {video_path}")
    dest_dir = video_path.parent
    dest_stem = video_path.stem
    written: list[Path] = []
    for kind in kinds:
        src = srt_dir / f"{srt_stem}.{kind}.srt"
        if not src.is_file():
            raise FileNotFoundError(f"SRT not found: {src}")
        dest = dest_dir / f"{dest_stem}.{kind}.srt"
        shutil.copy2(src, dest)
        written.append(dest)
        print(dest)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish SRT next to NFS/gvfs VR video (same stem)")
    parser.add_argument("--preset", choices=sorted(DEFAULT_NFS_GLOB), action="append", default=[])
    parser.add_argument("--video", type=Path, default=None, help="Source video (overrides --preset)")
    parser.add_argument("--srt-stem", type=str, default=None, help="Stem under --srt-dir (default: video stem)")
    parser.add_argument("--srt-dir", type=Path, default=DEFAULT_SRT_DIR)
    parser.add_argument("--kinds", default="asr,zh", help="Comma-separated: asr, zh")
    args = parser.parse_args()

    kinds = tuple(k.strip() for k in args.kinds.split(",") if k.strip())
    if not kinds:
        raise SystemExit("No SRT kinds selected")

    if args.video is not None:
        publish_srt(
            args.video,
            args.srt_dir,
            srt_stem=args.srt_stem or args.video.stem,
            kinds=kinds,
        )
        return

    if not args.preset:
        raise SystemExit("Provide --preset (repeatable) or --video")

    for preset in args.preset:
        video_path = Path(DEFAULT_NFS_GLOB[preset])
        srt_stem = args.srt_stem or PRESET_SRT_STEM.get(preset, f"vr_{preset}")
        publish_srt(video_path, args.srt_dir, srt_stem=srt_stem, kinds=kinds)


if __name__ == "__main__":
    main()
