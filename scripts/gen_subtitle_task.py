#!/usr/bin/env python3
"""Generate a subtitle batch task.toml listing mp4 paths."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from _paths import PROJECT_ROOT, add_main_paths

add_main_paths()

from sense_voice.subtitle_task import (  # noqa: E402
    SubtitleDefaults,
    new_task_from_videos,
    print_task_summary,
    write_subtitle_task,
)
from sense_voice.vr_sources import finished_dir, iter_finished_mp4s, resolve_jav_root  # noqa: E402

DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "tasks" / "subtitle_batch.toml"


def collect_videos(args: argparse.Namespace, finished: Path) -> list[Path]:
    if args.video:
        videos = [Path(v).resolve() for v in args.video]
    elif args.scan_finished:
        videos = iter_finished_mp4s(finished, vr_only=not args.all_mp4, name_filter=args.name_filter, sort_by="path")
    else:
        raise SystemExit("Provide --video (repeatable) or --scan-finished")
    return sorted(videos, key=lambda path: path.as_posix().casefold())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate subtitle task.toml from mp4 paths")
    parser.add_argument("--video", type=Path, action="append", default=[], help="mp4 path (repeatable)")
    parser.add_argument("--scan-finished", action="store_true", help="Scan jav/#finished for VR mp4")
    parser.add_argument("--folder", type=Path, default=None, help="Scan this folder instead of resolving jav/#finished")
    parser.add_argument("--name-filter", default=None)
    parser.add_argument("--all-mp4", action="store_true")
    parser.add_argument("--mount", action="store_true")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--label", default=None, help="Task label (default: output stem)")
    parser.add_argument("--no-skip-existing", action="store_true", help="Set skip_existing=false in task defaults")
    parser.add_argument("--include-completed", action="store_true", help="Keep completed videos enabled")
    parser.add_argument("--list-only", action="store_true", help="Print paths; do not write task.toml")
    args = parser.parse_args()

    if args.folder is not None:
        finished = args.folder.expanduser().resolve()
        if not finished.is_dir():
            raise SystemExit(f"folder not found: {finished}")
        args.scan_finished = True
    else:
        finished = finished_dir(jav_root=resolve_jav_root(mount=args.mount))
    videos = collect_videos(args, finished)
    if not videos:
        raise SystemExit("No videos matched")
    if args.list_only:
        for video in videos:
            print(video)
        print(f"total: {len(videos)}", file=sys.stderr)
        return

    label = args.label or args.output.stem
    defaults = SubtitleDefaults(
        skip_existing=not args.no_skip_existing,
        mount=args.mount,
        finished_root=str(finished) if args.folder is not None else "",
    )
    task = new_task_from_videos(
        videos,
        label=label,
        defaults=defaults,
        finished_root=finished,
        wav_dir=PROJECT_ROOT / defaults.wav_dir,
        srt_dir=PROJECT_ROOT / defaults.srt_dir,
        disable_completed=not args.include_completed,
    )
    if not task.created:
        task.created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    write_subtitle_task(args.output, task)
    print(f"Wrote {args.output} ({len(videos)} videos)", flush=True)
    print_task_summary(task)


if __name__ == "__main__":
    sys.exit(main())
