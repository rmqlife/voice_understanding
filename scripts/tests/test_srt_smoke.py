#!/usr/bin/env python3
"""Smoke tests for subtitle display split and timestamp parsing (no GPU)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))

from sense_voice.llm import (  # noqa: E402
    align_polished_texts_to_chunk,
    clean_polished_subtitle_text,
    extract_timeline_section,
    needs_chinese_translation,
    parse_translate_batch_output,
)  # noqa: E402
from sense_voice.srt import (  # noqa: E402
    DEFAULT_MAX_SRT_DURATION,
    DEFAULT_MAX_SRT_WEIGHT,
    _split_text_chunks,
    split_entries_for_display,
    split_entry_by_words,
)
from sense_voice.subtitle import (  # noqa: E402
    DEFAULT_MAX_SRT_CHARS,
    build_asr_srt_entries,
    build_zh_srt_entries_from_texts,
)
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


def test_align_polished_texts_to_chunk() -> None:
    chunk = [
        {"text": "あ", "start": 10.0},
        {"text": "い", "start": 12.0},
        {"text": "う", "start": 14.0},
    ]
    parsed = [(10.0, 11.0, "啊"), (12.0, 13.0, "咦")]
    assert align_polished_texts_to_chunk(parsed, chunk) == ["啊", "咦", ""]


def test_clean_polished_subtitle_text() -> None:
    assert clean_polished_subtitle_text("你好。[停顿]") == "你好。"
    assert clean_polished_subtitle_text("[不可辨语音][停顿]") == ""
    assert (
        clean_polished_subtitle_text('中的"いちも"可能是"身体"或"一滴"的误识别，结合上下文整理为"全身/身体"以通顺语义。')
        == ""
    )
    assert clean_polished_subtitle_text("嗯。") == ""
    assert clean_polished_subtitle_text("呀，有。") == ""
    assert clean_polished_subtitle_text("了。") == ""
    assert clean_polished_subtitle_text("想脱掉吗？。。") == "想脱掉吗？"


def test_needs_chinese_translation() -> None:
    assert needs_chinese_translation("次は 宿泊 コース に して、")
    assert not needs_chinese_translation("下次改成住宿套餐吧。")
    assert needs_chinese_translation(
        "中的“いちも”可能是“身体”或“一滴”的误识别，结合上下文整理为“全身/身体”以通顺语义。"
    )


def test_parse_translate_batch_output() -> None:
    raw = "- [3] 你好\n- [7] 再见"
    parsed = parse_translate_batch_output(raw)
    assert parsed[3] == "你好"
    assert parsed[7] == "再见"


def test_extract_timeline_section() -> None:
    raw = (
        "## Timeline\n"
        "- [0:00-1:00] 你好\n"
        "## Notes\n"
        "可能是误识别\n"
    )
    assert "你好" in extract_timeline_section(raw)
    assert "误识别" not in extract_timeline_section(raw)


def test_cross_language_display_split_monotonic() -> None:
    words = [
        {"text": "本", "start": 10.0, "end": 10.2},
        {"text": "日", "start": 10.2, "end": 10.4},
        {"text": "は", "start": 10.4, "end": 10.6},
    ]
    zh = "今天是九十分钟的课程，请问这样安排可以吗？"
    entries = split_entry_by_words(
        10.0,
        12.0,
        zh,
        words,
        timing_text="本日は90分コースで間違いないですか",
    )
    assert len(entries) >= 2
    for start, end, text in entries:
        assert end > start
        assert text


def test_build_zh_srt_entries_from_texts_uses_origin_times() -> None:
    segments = [
        {"start": 4.0, "end": 6.0, "text": "願します。", "origin_text": "願します。"},
        {"start": 40.0, "end": 44.0, "text": "ご来店", "origin_text": "ご来店"},
    ]
    entries = build_zh_srt_entries_from_texts(["请多关照。", "欢迎光临。"], segments, [])
    assert entries[0][0] == 4.0
    assert entries[0][1] == 6.0
    assert entries[1][0] == 40.0
    assert "欢迎" in entries[1][2]


def main() -> None:
    tests = [
        test_ms_to_seconds,
        test_defaults,
        test_punctuation_split,
        test_no_hard_cut_mid_word,
        test_display_split_merge,
        test_build_asr_srt_entries,
        test_align_polished_texts_to_chunk,
        test_clean_polished_subtitle_text,
        test_needs_chinese_translation,
        test_parse_translate_batch_output,
        test_extract_timeline_section,
        test_cross_language_display_split_monotonic,
        test_build_zh_srt_entries_from_texts_uses_origin_times,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"passed {len(tests)} tests")


if __name__ == "__main__":
    main()
