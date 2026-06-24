"""Subtitle sentence splitting and post-LLM realignment."""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Any

from .srt import SrtEntry, parse_srt_entries, split_entries_for_display
from .timestamps import TimestampGenerator, Word, match_sentence_timestamp

SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?\.])\s*")
CLAUSE_SPLIT_RE = re.compile(r"(?<=[，、,；;])\s*")
JSON_ALIGN_PATTERN = re.compile(r"\{[\s\S]*\"align\"[\s\S]*\}", re.MULTILINE)

DEFAULT_MAX_SENTENCE_CHARS = 40
DEFAULT_MAX_SEGMENT_DURATION = 8.0
DEFAULT_MAX_SRT_CHARS = 18
DEFAULT_MAX_SRT_DURATION = None


def calc_weighted_length(text: str) -> float:
    total = 0.0
    for char in text:
        if unicodedata.category(char).startswith("L"):
            total += 2.0 if ord(char) > 0x2E80 else 1.0
        else:
            total += 1.0
    return total


def split_sentences(text: str, *, max_weight: float = DEFAULT_MAX_SENTENCE_CHARS) -> list[str]:
    text = text.strip()
    if not text:
        return []

    parts = [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]
    if not parts:
        parts = [text]

    sentences: list[str] = []
    for part in parts:
        if calc_weighted_length(part) <= max_weight:
            sentences.append(part)
            continue
        clauses = [chunk.strip() for chunk in CLAUSE_SPLIT_RE.split(part) if chunk.strip()]
        if not clauses:
            clauses = [part]
        buffer = ""
        for clause in clauses:
            candidate = f"{buffer}{clause}" if buffer else clause
            if calc_weighted_length(candidate) <= max_weight:
                buffer = candidate
                continue
            if buffer:
                sentences.append(buffer)
            if calc_weighted_length(clause) <= max_weight:
                buffer = clause
            else:
                sentences.extend(_split_by_weight(clause, max_weight))
                buffer = ""
        if buffer:
            sentences.append(buffer)
    return sentences


def _split_by_weight(text: str, max_weight: float) -> list[str]:
    chunks: list[str] = []
    current = ""
    for char in text:
        candidate = current + char
        if calc_weighted_length(candidate) > max_weight and current:
            chunks.append(current)
            current = char
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def refine_segments(
    segments: list[dict[str, Any]],
    words: list[Word],
    *,
    max_sentence_chars: float = DEFAULT_MAX_SENTENCE_CHARS,
    max_duration: float = DEFAULT_MAX_SEGMENT_DURATION,
) -> list[dict[str, Any]]:
    """Split long ASR segments by punctuation and re-align to char timestamps."""
    if not words:
        return [_with_origin_text(segment) for segment in segments]

    refined: list[dict[str, Any]] = []
    last_end = 0.0
    for segment in segments:
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        start = segment.get("start")
        end = segment.get("end")
        duration = float(end) - float(start) if start is not None and end is not None else 0.0
        needs_split = duration > max_duration or calc_weighted_length(text) > max_sentence_chars

        if not needs_split:
            refined.append(_with_origin_text(segment))
            if end is not None:
                last_end = max(last_end, float(end))
            continue

        for sentence in split_sentences(text, max_weight=max_sentence_chars):
            start_ts, end_ts = match_sentence_timestamp(sentence, words, last_end)
            child = dict(segment)
            child["text"] = sentence
            child["origin_text"] = sentence
            if start_ts is not None and end_ts is not None:
                child["start"] = start_ts
                child["end"] = end_ts
                child["timing_confidence"] = "high"
                last_end = end_ts
            refined.append(child)
    return refined


def _with_origin_text(segment: dict[str, Any]) -> dict[str, Any]:
    updated = dict(segment)
    updated.setdefault("origin_text", str(segment.get("text", "")))
    return updated


def _nearest_origin_segment(
    start: float,
    origin_segments: list[dict[str, Any]],
) -> dict[str, Any] | None:
    best: dict[str, Any] | None = None
    best_distance = float("inf")
    for segment in origin_segments:
        seg_start = segment.get("start")
        if seg_start is None:
            continue
        distance = abs(float(seg_start) - start)
        if distance < best_distance:
            best_distance = distance
            best = segment
    return best


def realign_polished_entries(
    polished_entries: list[SrtEntry],
    origin_segments: list[dict[str, Any]],
    words: list[Word],
) -> list[SrtEntry]:
    """Recompute subtitle times from origin text anchors; keep polished display text."""
    if not words or not polished_entries:
        return polished_entries

    last_end = 0.0
    realigned: list[SrtEntry] = []

    if len(polished_entries) == len(origin_segments):
        pairs = zip(polished_entries, origin_segments, strict=False)
    else:
        pairs = (
            (entry, _nearest_origin_segment(entry[0], origin_segments) or {"text": entry[2]})
            for entry in polished_entries
        )

    for (polished_start, polished_end, zh_text), origin in pairs:
        anchor = str(origin.get("origin_text") or origin.get("text") or zh_text)
        start, end = match_sentence_timestamp(anchor, words, last_end)
        if start is None or end is None:
            start, end = polished_start, polished_end
        if start < last_end:
            start = last_end
        if end <= start:
            end = start + 0.5
        realigned.append((start, end, zh_text))
        last_end = end
    return realigned


def parse_llm_alignments(polished: str) -> list[dict[str, str]] | None:
    match = JSON_ALIGN_PATTERN.search(polished)
    if not match:
        return None
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    align = payload.get("align")
    if not isinstance(align, list):
        return None
    rows: list[dict[str, str]] = []
    for item in align:
        if not isinstance(item, dict):
            continue
        origin = str(item.get("origin_part", "")).strip()
        translated = str(item.get("translated_part", "")).strip()
        if origin and translated:
            rows.append({"origin_part": origin, "translated_part": translated})
    return rows or None


def build_entries_from_alignments(
    alignments: list[dict[str, str]],
    words: list[Word],
) -> list[SrtEntry]:
    generator = TimestampGenerator()
    sentences = [row["origin_part"] for row in alignments]
    timed = generator.generate(sentences, words)
    entries: list[SrtEntry] = []
    for timed_row, align in zip(timed, alignments, strict=False):
        entries.append(
            (
                float(timed_row["start"]),
                float(timed_row["end"]),
                align["translated_part"],
            )
        )
    return entries


def build_zh_srt_entries(
    polished: str,
    origin_segments: list[dict[str, Any]],
    words: list[Word],
    *,
    max_chars: int = DEFAULT_MAX_SRT_CHARS,
    max_duration: float = DEFAULT_MAX_SRT_DURATION,
) -> list[SrtEntry]:
    alignments = parse_llm_alignments(polished)
    if alignments:
        entries = build_entries_from_alignments(alignments, words)
    else:
        entries = parse_srt_entries(polished)
        entries = realign_polished_entries(entries, origin_segments, words)
    return split_entries_for_display(
        entries,
        words,
        max_chars=max_chars,
        max_duration=max_duration,
    )


def build_asr_srt_entries(
    segments: list[dict[str, Any]],
    words: list[Word],
    *,
    max_chars: int = DEFAULT_MAX_SRT_CHARS,
    max_duration: float = DEFAULT_MAX_SRT_DURATION,
) -> list[SrtEntry]:
    from .srt import segments_to_entries

    refined = refine_segments(segments, words) if words else segments
    entries = segments_to_entries(refined)
    if not words:
        return entries
    return split_entries_for_display(
        entries,
        words,
        max_chars=max_chars,
        max_duration=max_duration,
    )


def get_silence_split_points(
    audio_path: str | Path,
    *,
    segment_duration: float = 600.0,
    silence_duration: float = 0.35,
    noise_db: int = -35,
) -> list[float]:
    """Find split points near fixed intervals using ffmpeg silencedetect."""
    audio_path = Path(audio_path)
    duration_proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        total_duration = float(duration_proc.stdout.strip())
    except ValueError:
        return [0.0]

    if total_duration <= segment_duration:
        return [0.0, total_duration]

    detect_proc = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            str(audio_path),
            "-af",
            f"silencedetect=noise={noise_db}dB:d={silence_duration}",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    silences: list[float] = []
    for line in detect_proc.stderr.splitlines():
        if "silence_start:" in line:
            try:
                silences.append(float(line.split("silence_start:")[-1].strip()))
            except ValueError:
                continue

    points = [0.0]
    target = segment_duration
    while target < total_duration:
        window = [value for value in silences if abs(value - target) <= 30.0]
        points.append(min(window, key=lambda value: abs(value - target)) if window else target)
        target += segment_duration
    points.append(total_duration)
    return sorted(set(points))
