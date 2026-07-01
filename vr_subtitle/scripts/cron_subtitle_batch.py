#!/usr/bin/env python3
"""Cron-friendly subtitle batch: generate a task.toml, then run it."""

from __future__ import annotations

import argparse
import fcntl
import subprocess
import sys
from pathlib import Path

from _paths import PROJECT_ROOT

DEFAULT_FOLDER = Path("/mnt/fnos/jav/#finished")
DEFAULT_TASK = PROJECT_ROOT / "tasks" / "cron_finished.toml"
DEFAULT_LOCK = PROJECT_ROOT / "tasks" / ".cron_subtitle.lock"


def run_command(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and run the default VR subtitle cron batch")
    parser.add_argument("--folder", type=Path, default=DEFAULT_FOLDER, help="Folder to scan for mp4 files")
    parser.add_argument("--task", type=Path, default=DEFAULT_TASK, help="Generated task.toml path")
    parser.add_argument("--lock-file", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--name-filter", default=None)
    parser.add_argument("--all-mp4", action="store_true")
    parser.add_argument("--include-completed", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--from", type=int, default=1, dest="from_index", metavar="N")
    args = parser.parse_args()

    folder = args.folder.expanduser().resolve()
    if not folder.is_dir():
        raise SystemExit(f"folder not found: {folder}")

    task_path = args.task if args.task.is_absolute() else PROJECT_ROOT / args.task
    lock_path = args.lock_file if args.lock_file.is_absolute() else PROJECT_ROOT / args.lock_file
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(f"another subtitle cron batch is already running ({lock_path})", flush=True)
            return

        gen_cmd = [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "gen_subtitle_task.py"),
            "--folder",
            str(folder),
            "--label",
            "cron_finished",
            "--output",
            str(task_path),
        ]
        if args.name_filter:
            gen_cmd.extend(["--name-filter", args.name_filter])
        if args.all_mp4:
            gen_cmd.append("--all-mp4")
        if args.include_completed:
            gen_cmd.append("--include-completed")
        run_command(gen_cmd)

        run_cmd = [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "run_subtitle_task.py"),
            str(task_path),
            "--from",
            str(args.from_index),
        ]
        if args.continue_on_error:
            run_cmd.append("--continue-on-error")
        if args.dry_run:
            run_cmd.append("--dry-run")
        run_command(run_cmd)


if __name__ == "__main__":
    sys.exit(main())
