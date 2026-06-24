"""ASR segment parsing and timeline formatting."""

from __future__ import annotations

import json
import re
from typing import Any

from .transcribe import strip_tags

TAG_GROUP_PATTERN = re.compile(r"((?:<\|[^|]+\|>)+)([^<]*)")
CPP_TIMELINE_PATTERN = re.compile(r"^\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]\s*(.*)$")
LANG_TAGS = {"zh", "en", "yue", "ja", "ko", "nospeech"}
SPEECH_TAGS = {"Speech", "Applause", "BGM", "Laughter", "Event"}
ITN_TAGS = {"withitn", "woitn"}


def parse_tagged_text(text: str) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for match in TAG_GROUP_PATTERN.finditer(text):
        tags = re.findall(r"<\|([^|]+)\|>", match.group(1))
        segment_text = match.group(2).strip()
        if not segment_text:
            continue
        lang = next((tag for tag in tags if tag in LANG_TAGS), None)
        speech_type = next((tag for tag in tags if tag in SPEECH_TAGS), None)
        itn = next((tag for tag in tags if tag in ITN_TAGS), None)
        emotions = [
            tag
            for tag in tags
            if tag not in LANG_TAGS and tag not in SPEECH_TAGS and tag not in ITN_TAGS
        ]
        segments.append(
            {
                "start": None,
                "end": None,
                "lang": lang,
                "type": speech_type,
                "itn": itn,
                "emotion": ",".join(emotions) if emotions else None,
                "text": strip_tags(segment_text),
            }
        )
    return segments


def parse_asr_segments(
    raw: str,
    text: str,
    audio_seconds: float | None,
    *,
    asr_payload: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    timing_source = str((asr_payload or {}).get("timing_source", ""))

    structured = (asr_payload or {}).get("sentences")
    if isinstance(structured, list) and structured:
        for item in structured:
            if isinstance(item, dict) and item.get("text"):
                segments.append(dict(item))
        if segments:
            return segments

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                segments.extend(parse_tagged_text(str(item.get("text", ""))))

    if not segments:
        for line in raw.splitlines():
            match = CPP_TIMELINE_PATTERN.match(line.strip())
            if not match:
                continue
            segment_text = match.group(3)
            tagged = parse_tagged_text(segment_text)
            if tagged:
                for segment in tagged:
                    segment["start"] = float(match.group(1))
                    segment["end"] = float(match.group(2))
                    segment["timing_confidence"] = "high"
                    segments.append(segment)
            else:
                segments.append(
                    {
                        "start": float(match.group(1)),
                        "end": float(match.group(2)),
                        "lang": None,
                        "type": None,
                        "itn": None,
                        "emotion": None,
                        "text": strip_tags(segment_text),
                        "timing_confidence": "high",
                    }
                )

    if not segments:
        chunks = re.split(r"(?<=[。！？!?\.])\s*", text)
        segments = [
            {
                "start": None,
                "end": None,
                "lang": None,
                "type": None,
                "itn": None,
                "emotion": None,
                "text": chunk.strip(),
                "timing_confidence": None,
            }
            for chunk in chunks
            if chunk.strip()
        ]

    if audio_seconds and segments and all(segment["start"] is None for segment in segments):
        total_chars = sum(max(1, len(str(segment["text"]))) for segment in segments)
        cursor = 0.0
        for segment in segments:
            duration = audio_seconds * max(1, len(str(segment["text"]))) / total_chars
            segment["start"] = cursor
            cursor += duration
            segment["end"] = min(audio_seconds, cursor)
            segment["timing_confidence"] = "low"

    words = (asr_payload or {}).get("words")
    if isinstance(words, list) and words and segments:
        try:
            from .subtitle import refine_segments

            segments = refine_segments(segments, words)
        except Exception:
            pass

    if timing_source and segments and all(segment.get("timing_confidence") is None for segment in segments):
        for segment in segments:
            segment["timing_confidence"] = "medium" if timing_source != "none" else None

    return segments


def segment_duration_stats(segments: list[dict[str, Any]]) -> dict[str, float | int]:
    durations: list[float] = []
    for segment in segments:
        start = segment.get("start")
        end = segment.get("end")
        if start is None or end is None:
            continue
        duration = float(end) - float(start)
        if duration > 0:
            durations.append(duration)
    if not durations:
        return {
            "count": len(segments),
            "timed_count": 0,
            "p50": 0.0,
            "p95": 0.0,
            "max": 0.0,
            "over_10s": 0,
            "over_30s": 0,
        }
    durations.sort()
    p50 = durations[len(durations) // 2]
    p95 = durations[max(0, int(len(durations) * 0.95) - 1)]
    return {
        "count": len(segments),
        "timed_count": len(durations),
        "p50": p50,
        "p95": p95,
        "max": max(durations),
        "over_10s": sum(1 for value in durations if value > 10),
        "over_30s": sum(1 for value in durations if value > 30),
    }


def seconds_label(seconds: float | None) -> str:
    if seconds is None:
        return "??:??"
    total_tenths = int(round(max(0.0, seconds) * 10))
    minutes, tenths = divmod(total_tenths, 600)
    sec = tenths / 10
    return f"{minutes:02d}:{sec:04.1f}"


def format_timeline(segments: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for idx, segment in enumerate(segments, start=1):
        start = seconds_label(segment.get("start"))
        end = seconds_label(segment.get("end"))
        tags = []
        for key in ("lang", "emotion", "type", "itn"):
            value = segment.get(key)
            if value:
                tags.append(f"{key}={value}")
        tag_text = ", ".join(tags) if tags else "none"
        lines.append(f"{idx:03d}. [{start}-{end}] tags: {tag_text} | text: {segment['text']}")
    return "\n".join(lines)


def format_timeline_compact(segments: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for segment in segments:
        start = seconds_label(segment.get("start"))
        end = seconds_label(segment.get("end"))
        lines.append(f"[{start}-{end}] {segment['text']}")
    return "\n".join(lines)
