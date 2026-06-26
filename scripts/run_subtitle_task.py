#!/usr/bin/env python3
"""Run subtitle pipeline for each mp4 listed in a task.toml."""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))

from sense_voice.subtitle_task import load_subtitle_task, print_task_summary  # noqa: E402
from sense_voice.vr_sources import finished_dir, resolve_finished_video, resolve_jav_root  # noqa: E402
from add_subtitle import add_subtitle_for_video  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Process mp4 paths from subtitle task.toml")
    parser.add_argument("task", type=Path, help="Path to task.toml")
    parser.add_argument("--from", type=int, default=1, dest="from_index", metavar="N", help="1-based start index")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--extract-only", action="store_true")
    parser.add_argument("--subtitle-only", action="store_true")
    parser.add_argument("--publish-only", action="store_true")
    parser.add_argument("--repolish-only", action="store_true", help="Re-run LLM from existing .asr.srt")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--log", type=Path, default=None, help="Append stdout/stderr to log file")
    args = parser.parse_args()

    if not args.task.is_file():
        raise SystemExit(f"task file not found: {args.task}")

    task = load_subtitle_task(args.task, repo_root=ROOT)
    enabled = task.enabled_videos()
    if args.from_index < 1 or args.from_index > len(enabled):
        raise SystemExit(f"--from must be between 1 and {len(enabled)}")

    defaults = task.defaults
    jav_root = resolve_jav_root(mount=defaults.mount)
    finished = finished_dir(jav_root=jav_root)
    wav_dir = (ROOT / defaults.wav_dir).resolve()
    srt_dir = (ROOT / defaults.srt_dir).resolve()

    print(f"task: {task.label} ({len(enabled)} enabled videos)", flush=True)
    if args.dry_run:
        print_task_summary(task)

    failures: list[str] = []
    batch = enabled[args.from_index - 1 :]
    for offset, video_entry in enumerate(batch):
        index = args.from_index + offset
        video = resolve_finished_video(Path(video_entry.path), finished_root=finished)
        is_last = offset == len(batch) - 1
        prefix = f"[{index}/{len(enabled)}]"
        print(f"\n{prefix} {video}", flush=True)
        if video_entry.note:
            print(f"{prefix} note: {video_entry.note}", flush=True)
        if not video.is_file():
            message = f"{prefix} missing: {video}"
            print(message, flush=True)
            failures.append(message)
            if not args.continue_on_error:
                raise SystemExit(message)
            continue
        try:
            add_subtitle_for_video(
                video,
                finished_root=finished,
                wav_dir=wav_dir,
                srt_dir=srt_dir,
                mount=defaults.mount,
                skip_existing=False if args.repolish_only else defaults.skip_existing,
                extract_only=args.extract_only,
                subtitle_only=args.subtitle_only,
                publish_only=args.publish_only,
                start=None,
                duration=None,
                language=defaults.language,
                profile=defaults.profile,
                asr_backend=defaults.asr_backend,
                asr_device=defaults.asr_device,
                asr_model=defaults.asr_model,
                polish_model=defaults.polish_model,
                chunk_chars=defaults.chunk_chars,
                chunk_segments_size=defaults.chunk_segments,
                llm_timeline=defaults.llm_timeline,
                skip_polish=defaults.skip_polish,
                use_gpu_lock=defaults.use_gpu_lock,
                dry_run=args.dry_run,
                repolish_only=args.repolish_only,
                release_model_after=not args.repolish_only or is_last,
            )
        except Exception as exc:
            message = f"{prefix} failed: {exc}"
            print(message, flush=True)
            traceback.print_exc()
            failures.append(message)
            if not args.continue_on_error:
                raise
    if failures:
        print(f"\nfinished with {len(failures)} failure(s)", flush=True)
        raise SystemExit(1)
    print(f"\nfinished {len(enabled) - (args.from_index - 1)} video(s)", flush=True)


if __name__ == "__main__":
    main()
