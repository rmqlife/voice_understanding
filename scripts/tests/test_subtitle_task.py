#!/usr/bin/env python3
"""Smoke tests for subtitle task.toml load/write."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))

from sense_voice.subtitle_task import (  # noqa: E402
    SubtitleDefaults,
    SubtitleTask,
    SubtitleVideo,
    load_subtitle_task,
    write_subtitle_task,
)


def test_roundtrip() -> None:
    task = SubtitleTask(
        label="sample",
        created="2026-06-25T00:00:00Z",
        defaults=SubtitleDefaults(skip_existing=True, polish_model="nsfw-local:27b"),
        videos=[
            SubtitleVideo(path="/tmp/a.mp4", enabled=True),
            SubtitleVideo(path="/tmp/b.mp4", enabled=False, note="srt exists"),
        ],
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "task.toml"
        write_subtitle_task(path, task)
        loaded = load_subtitle_task(path)
        assert loaded.label == "sample"
        assert len(loaded.videos) == 2
        assert len(loaded.enabled_videos()) == 1
        assert loaded.defaults.polish_model == "nsfw-local:27b"


def main() -> None:
    test_roundtrip()
    print("ok test_roundtrip")
    print("passed 1 tests")


if __name__ == "__main__":
    main()
