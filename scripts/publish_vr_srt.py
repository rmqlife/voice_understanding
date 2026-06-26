#!/usr/bin/env python3
"""Copy generated SRT files next to source VR videos on NFS (/mnt/fnos/jav or gvfs)."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.vr_sources import LEGACY_PRESETS, finished_dir, resolve_jav_root, video_from_local_stem  # noqa: E402

DEFAULT_SRT_DIR = ROOT / "results" / "srt"

# Legacy preset → wav stem under data/vr when using vr-subtitle-test after sync-vr-audio --preset.
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
        shutil.copyfile(src, dest)
        written.append(dest)
        print(dest)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish SRT next to VR video on NFS (/mnt/fnos/jav)")
    parser.add_argument("--preset", choices=sorted(LEGACY_PRESETS), action="append", default=[])
    parser.add_argument("--video", type=Path, default=None, help="Source video (overrides --preset)")
    parser.add_argument("--stem", type=str, default=None, help="Local wav/srt stem under --srt-dir (finds mp4 on #finished)")
    parser.add_argument("--mount", action="store_true", help="Mount gvfs jav if /mnt/fnos/jav missing")
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

    if args.stem:
        finished = finished_dir(jav_root=resolve_jav_root(mount=args.mount))
        video_path = video_from_local_stem(args.stem, finished)
        if video_path is None:
            raise SystemExit(f"mp4 not found for stem {args.stem!r} under {finished}")
        publish_srt(video_path, args.srt_dir, srt_stem=args.stem, kinds=kinds)
        return

    if not args.preset:
        raise SystemExit("Provide --preset (repeatable), --video, or --stem")

    for preset in args.preset:
        video_path = Path(LEGACY_PRESETS[preset])
        srt_stem = args.srt_stem or PRESET_SRT_STEM.get(preset, f"vr_{preset}")
        publish_srt(video_path, args.srt_dir, srt_stem=srt_stem, kinds=kinds)


if __name__ == "__main__":
    main()
