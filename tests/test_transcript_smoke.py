#!/usr/bin/env python3
"""Smoke tests for transcript assembly (no GPU)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from sense_voice.diarize import SpeakerTurn  # noqa: E402
from sense_voice.segments import parse_asr_segments  # noqa: E402
from sense_voice.speaker_names import (  # noqa: E402
    apply_speaker_names,
    parse_speaker_names,
)
from sense_voice.transcript import (  # noqa: E402
    assign_segments_to_turns,
    build_transcript_llm_input,
    merge_adjacent_turns,
    parse_polished_transcript,
    sort_turns,
    turn_header,
)


def test_assign_segments_to_turns() -> None:
    turns = [
        SpeakerTurn("SPEAKER_00", 0.0, 5.0),
        SpeakerTurn("SPEAKER_01", 5.0, 10.0),
    ]
    segments = [
        {"start": 0.5, "end": 2.0, "text": "你好"},
        {"start": 6.0, "end": 8.0, "text": "在吗"},
    ]
    assigned = assign_segments_to_turns(turns, segments)
    assert assigned[0].text == "你好"
    assert assigned[1].text == "在吗"


def test_assign_segments_no_duplicate() -> None:
    turns = [
        SpeakerTurn("SPEAKER_00", 0.0, 100.0),
        SpeakerTurn("SPEAKER_01", 20.0, 80.0),
    ]
    segments = [{"start": 50.0, "end": 55.0, "text": "一句"}]
    assigned = assign_segments_to_turns(turns, segments)
    texts = [turn.text for turn in assigned if turn.text]
    assert texts == ["一句"]


def test_merge_adjacent_turns() -> None:
    turns = [
        SpeakerTurn("SPEAKER_00", 0.0, 2.0, "第一句"),
        SpeakerTurn("SPEAKER_00", 2.2, 4.0, "第二句"),
        SpeakerTurn("SPEAKER_01", 5.0, 7.0, "对方"),
    ]
    merged = merge_adjacent_turns(turns, same_speaker=True, gap_s=1.0)
    assert len(merged) == 2
    assert merged[0].text == "第一句第二句"


def test_parse_polished_transcript_by_turn_index() -> None:
    turns = [
        SpeakerTurn("SPEAKER_00", 0.0, 5.0, "旧A"),
        SpeakerTurn("SPEAKER_01", 5.0, 10.0, "旧B"),
    ]
    polished = (
        "## Turn 1 · SPEAKER_00 [00:00-00:05]\n整理A。\n\n"
        "## Turn 2 · SPEAKER_01 [00:05-00:10]\n整理B。"
    )
    updated = parse_polished_transcript(polished, turns)
    assert "整理A" in updated[0].text
    assert "整理B" in updated[1].text


def test_build_transcript_llm_input() -> None:
    turns = [SpeakerTurn("SPEAKER_00", 0.0, 1.0, "测试")]
    text = build_transcript_llm_input(turns)
    assert "## Turn 1 · SPEAKER_00" in text
    assert "测试" in text


def test_sort_turns() -> None:
    turns = [
        SpeakerTurn("SPEAKER_01", 10.0, 12.0, "b"),
        SpeakerTurn("SPEAKER_00", 0.0, 2.0, "a"),
    ]
    ordered = sort_turns(turns)
    assert ordered[0].text == "a"


def test_turn_header() -> None:
    assert "Turn 3" in turn_header(SpeakerTurn("SPEAKER_01", 92.0, 96.0), index=3)


def test_parse_asr_segments_from_sentences() -> None:
    payload = {
        "sentences": [{"start": 0.0, "end": 1.0, "text": "你好"}],
        "timing_source": "char_timestamp",
    }
    segments = parse_asr_segments("", "", 10.0, asr_payload=payload)
    assert len(segments) == 1
    assert segments[0]["text"] == "你好"


def test_display_label_with_name() -> None:
    turn = SpeakerTurn("SPEAKER_00", 0.0, 1.0, "测试", name="业主")
    assert turn.display_label() == "业主"
    assert "业主" in turn_header(turn, index=1)


def test_parse_speaker_names_json() -> None:
    raw = '说明\n{"SPEAKER_00": "物业", "SPEAKER_01": "业主"}'
    assert parse_speaker_names(raw) == {"SPEAKER_00": "物业", "SPEAKER_01": "业主"}


def test_apply_speaker_names() -> None:
    turns = [SpeakerTurn("SPEAKER_00", 0.0, 1.0, "你好")]
    named = apply_speaker_names(turns, {"SPEAKER_00": "物业"})
    assert named[0].name == "物业"


def main() -> None:
    tests = [
        test_assign_segments_to_turns,
        test_assign_segments_no_duplicate,
        test_merge_adjacent_turns,
        test_parse_polished_transcript_by_turn_index,
        test_build_transcript_llm_input,
        test_sort_turns,
        test_turn_header,
        test_parse_asr_segments_from_sentences,
        test_display_label_with_name,
        test_parse_speaker_names_json,
        test_apply_speaker_names,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"{len(tests)}/{len(tests)} passed")


if __name__ == "__main__":
    main()
