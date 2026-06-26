#!/usr/bin/env python3
"""Generate a subtitle batch task.toml listing mp4 paths."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.subtitle_task import (  # noqa: E402
    SubtitleDefaults,
    new_task_from_videos,
    print_task_summary,
    write_subtitle_task,
)
from sense_voice.vr_sources import (  # noqa: E402
    finished_dir,
    iter_finished_mp4s,
    resolve_jav_root,
)

DEFAULT_OUTPUT = ROOT / "tasks" / "subtitle_batch.toml"


def collect_videos(args: argparse.Namespace, finished: Path) -> list[Path]:
    if args.video:
        videos = [Path(v).resolve() for v in args.video]
    elif args.scan_finished:
        videos = iter_finished_mp4s(
            finished,
            vr_only=not args.all_mp4,
            name_filter=args.name_filter,
            sort_by="path",
        )
    else:
        raise SystemExit("Provide --video (repeatable) or --scan-finished")
    return sorted(videos, key=lambda path: path.as_posix().casefold())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate subtitle task.toml from mp4 paths")
    parser.add_argument("--video", type=Path, action="append", default=[], help="mp4 path (repeatable)")
    parser.add_argument("--scan-finished", action="store_true", help="Scan jav/#finished for VR mp4")
    parser.add_argument("--name-filter", default=None)
    parser.add_argument("--all-mp4", action="store_true")
    parser.add_argument("--mount", action="store_true")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--label", default=None, help="Task label (default: output stem)")
    parser.add_argument("--no-skip-existing", action="store_true", help="Set skip_existing=false in task defaults")
    parser.add_argument(
        "--include-completed",
        action="store_true",
        help="Keep videos that already have .asr/.zh.srt as enabled=true",
    )
    parser.add_argument("--list-only", action="store_true", help="Print paths; do not write task.toml")
    args = parser.parse_args()

    jav_root = resolve_jav_root(mount=args.mount)
    finished = finished_dir(jav_root=jav_root)
    videos = collect_videos(args, finished)
    if not videos:
        raise SystemExit("No videos matched")

    if args.list_only:
        for video in videos:
            print(video)
        print(f"total: {len(videos)}", file=sys.stderr)
        return

    label = args.label or args.output.stem
    defaults = SubtitleDefaults(skip_existing=not args.no_skip_existing, mount=args.mount)
    wav_dir = ROOT / defaults.wav_dir
    srt_dir = ROOT / defaults.srt_dir
    task = new_task_from_videos(
        videos,
        label=label,
        defaults=defaults,
        finished_root=finished,
        wav_dir=wav_dir,
        srt_dir=srt_dir,
        disable_completed=not args.include_completed,
    )
    if not task.created:
        task.created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_subtitle_task(args.output, task)
    print(f"Wrote {args.output} ({len(videos)} videos)", flush=True)
    print_task_summary(task)


if __name__ == "__main__":
    main()
