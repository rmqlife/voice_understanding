#!/usr/bin/env python3
"""Smoke tests for subtitle display split and timestamp parsing (no GPU)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.srt import (  # noqa: E402
    DEFAULT_MAX_SRT_DURATION,
    DEFAULT_MAX_SRT_WEIGHT,
    _split_text_chunks,
    split_entries_for_display,
)
from sense_voice.subtitle import DEFAULT_MAX_SRT_CHARS, build_asr_srt_entries  # noqa: E402
from sense_voice.transcribe import _ms_to_seconds  # noqa: E402


def test_ms_to_seconds() -> None:
    assert _ms_to_seconds(510) == 0.51
    assert _ms_to_seconds(12000) == 12.0
    assert _ms_to_seconds(2.13) == 2.13


def test_defaults() -> None:
    assert DEFAULT_MAX_SRT_DURATION is None
    assert DEFAULT_MAX_SRT_CHARS == 18
    assert DEFAULT_MAX_SRT_WEIGHT == 18.0


def test_punctuation_split() -> None:
    assert _split_text_chunks("反正我我对我是有物业，", 18) == ["反正我我对我是有物业，"]
    chunks = _split_text_chunks("你要我正在跟他联系呢，我刚才跟他联系，", 18)
    assert chunks[0].endswith("呢，")
    assert "我刚才" in chunks[1]


def test_no_hard_cut_mid_word() -> None:
    chunks = _split_text_chunks("这我不是在等他们这帮王八蛋吗？", 18)
    assert len(chunks) == 1
    assert "王八蛋" in chunks[0]


def test_display_split_merge() -> None:
    words = [
        {"text": "你", "start": 0.0, "end": 0.1},
        {"text": "好", "start": 0.1, "end": 0.2},
        {"text": "，", "start": 0.2, "end": 0.25},
        {"text": "世", "start": 0.25, "end": 0.35},
        {"text": "界", "start": 0.35, "end": 0.45},
    ]
    entries = split_entries_for_display([(0.0, 0.45, "你好，世界")], words)
    assert len(entries) == 1
    assert entries[0][2] == "你好，世界"


def test_build_asr_srt_entries() -> None:
    words = [{"text": "测", "start": 0.0, "end": 0.1}, {"text": "试", "start": 0.1, "end": 0.2}]
    segments = [{"start": 0.0, "end": 0.2, "text": "测试"}]
    entries = build_asr_srt_entries(segments, words)
    assert entries and entries[0][2] == "测试"


def main() -> None:
    tests = [
        test_ms_to_seconds,
        test_defaults,
        test_punctuation_split,
        test_no_hard_cut_mid_word,
        test_display_split_merge,
        test_build_asr_srt_entries,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"passed {len(tests)} tests")


if __name__ == "__main__":
    main()
