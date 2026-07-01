"""Transcript assembly: speaker turns + ASR text + export."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .diarize import SpeakerTurn
from .segments import seconds_label


TURN_HEADER_PATTERN = re.compile(
    r"^##\s*Turn\s+(?P<index>\d+)\s*·\s*(?P<speaker>.+?)(?:\s*\[(?P<start>[^\]]+)-(?P<end>[^\]]+)\])?\s*$"
)


def _overlap_seconds(
    turn_start: float,
    turn_end: float,
    seg_start: float,
    seg_end: float,
) -> float:
    return max(0.0, min(turn_end, seg_end) - max(turn_start, seg_start))


def sort_turns(turns: list[SpeakerTurn]) -> list[SpeakerTurn]:
    return sorted(turns, key=lambda turn: (turn.start, turn.end, turn.speaker))


def turn_header(turn: SpeakerTurn, *, index: int) -> str:
    start = seconds_label(turn.start)
    end = seconds_label(turn.end)
    return f"## Turn {index} · {turn.display_label()} [{start}-{end}]"


def consolidate_turns_by_speaker(turns: list[SpeakerTurn]) -> list[SpeakerTurn]:
    """Merge all turns from the same speaker into one block. Opt-in only — breaks dialogue order."""
    order: list[str] = []
    buckets: dict[str, list[SpeakerTurn]] = {}
    for turn in sort_turns(turns):
        if turn.speaker not in buckets:
            order.append(turn.speaker)
            buckets[turn.speaker] = []
        buckets[turn.speaker].append(turn)

    consolidated: list[SpeakerTurn] = []
    for speaker in order:
        group = buckets[speaker]
        texts = [turn.text.strip() for turn in group if turn.text.strip()]
        consolidated.append(
            SpeakerTurn(
                speaker=speaker,
                start=min(turn.start for turn in group),
                end=max(turn.end for turn in group),
                text="".join(texts),
            )
        )
    return consolidated


def assign_segments_to_turns(
    turns: list[SpeakerTurn],
    segments: list[dict[str, Any]],
) -> list[SpeakerTurn]:
    """Map each timed ASR segment to exactly one turn by maximum temporal overlap."""
    if not turns:
        return []

    assigned: list[SpeakerTurn] = [SpeakerTurn(speaker=t.speaker, start=t.start, end=t.end) for t in turns]
    bucket: list[list[tuple[float, str]]] = [[] for _ in turns]

    for segment in segments:
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        seg_start = segment.get("start")
        seg_end = segment.get("end")
        if seg_start is None or seg_end is None:
            continue
        seg_start_f = float(seg_start)
        seg_end_f = float(seg_end)
        if seg_end_f <= seg_start_f:
            continue

        best_index: int | None = None
        best_score = 0.0
        for index, turn in enumerate(turns):
            score = _overlap_seconds(turn.start, turn.end, seg_start_f, seg_end_f)
            if score > best_score:
                best_score = score
                best_index = index

        if best_index is None:
            midpoint = (seg_start_f + seg_end_f) / 2.0
            nearest_index = min(
                range(len(turns)),
                key=lambda index: abs(midpoint - (turns[index].start + turns[index].end) / 2.0),
            )
            best_index = nearest_index

        bucket[best_index].append((seg_start_f, text))

    for index, items in enumerate(bucket):
        items.sort(key=lambda item: item[0])
        assigned[index].text = "".join(text for _, text in items)
    return assigned


def merge_adjacent_turns(
    turns: list[SpeakerTurn],
    *,
    same_speaker: bool = True,
    gap_s: float = 1.0,
) -> list[SpeakerTurn]:
    if not turns:
        return []

    ordered = sort_turns(turns)
    merged: list[SpeakerTurn] = [SpeakerTurn(**ordered[0].to_dict())]
    for turn in ordered[1:]:
        prev = merged[-1]
        if same_speaker and turn.speaker == prev.speaker and turn.start - prev.end <= gap_s:
            prev.end = max(prev.end, turn.end)
            prev.text = f"{prev.text}{turn.text}".strip()
        else:
            merged.append(SpeakerTurn(**turn.to_dict()))
    return merged


def drop_empty_turns(turns: list[SpeakerTurn]) -> list[SpeakerTurn]:
    return [turn for turn in turns if turn.text.strip()]


def build_transcript_llm_input(turns: list[SpeakerTurn]) -> str:
    blocks: list[str] = []
    for index, turn in enumerate(drop_empty_turns(sort_turns(turns)), start=1):
        blocks.append(f"{turn_header(turn, index=index)}\n{turn.text.strip()}")
    return "\n\n".join(blocks)


def parse_polished_transcript(polished: str, turns: list[SpeakerTurn]) -> list[SpeakerTurn]:
    """Parse LLM output with `## Turn N · SPEAKER_xx` headers back onto turns."""
    ordered = drop_empty_turns(sort_turns(turns))
    sections: dict[int, str] = {}
    current_index: int | None = None
    buffer: list[str] = []

    for line in polished.splitlines():
        match = TURN_HEADER_PATTERN.match(line.strip())
        if match:
            if current_index is not None:
                sections[current_index] = "\n".join(buffer).strip()
            current_index = int(match.group("index"))
            buffer = []
        elif current_index is not None:
            buffer.append(line)
    if current_index is not None:
        sections[current_index] = "\n".join(buffer).strip()

    if not sections:
        return ordered

    updated: list[SpeakerTurn] = []
    for index, turn in enumerate(ordered, start=1):
        text = sections.get(index, turn.text)
        updated.append(
            SpeakerTurn(
                speaker=turn.speaker,
                start=turn.start,
                end=turn.end,
                text=text,
            )
        )
    return updated


def write_transcript_md(
    turns: list[SpeakerTurn],
    path: str | Path,
    *,
    title: str | None = None,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if title:
        lines.extend([f"# {title}", ""])

    for index, turn in enumerate(drop_empty_turns(sort_turns(turns)), start=1):
        lines.extend([turn_header(turn, index=index), "", turn.text.strip(), ""])
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_transcript_json(
    turns: list[SpeakerTurn],
    path: str | Path,
    *,
    metadata: dict[str, Any] | None = None,
) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = drop_empty_turns(sort_turns(turns))
    payload = {
        "turns": [turn.to_dict() for turn in ordered],
        "metadata": metadata or {},
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
