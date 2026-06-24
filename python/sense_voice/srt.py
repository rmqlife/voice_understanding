"""SRT formatting and display-oriented splitting."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .timestamps import Word, match_sentence_timestamp

SrtEntry = tuple[float, float, str]
SRT_LINE_PATTERN = re.compile(
  r"^\s*(?:[-*]\s*)?\[(?P<start>[^\]-]+)-(?P<end>[^\]]+)\]\s*(?P<text>.+?)\s*$"
)


def srt_timestamp(seconds: float) -> str:
  millis = int(round(max(0.0, seconds) * 1000))
  hours, remainder = divmod(millis, 3_600_000)
  minutes, remainder = divmod(remainder, 60_000)
  secs, millis = divmod(remainder, 1000)
  return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def parse_time_label(label: str) -> float | None:
  label = label.strip().replace(",", ".")
  if not label or "?" in label:
    return None
  parts = label.split(":")
  try:
    if len(parts) == 1:
      return float(parts[0])
    if len(parts) == 2:
      minutes, seconds = parts
      return int(minutes) * 60 + float(seconds)
    if len(parts) == 3:
      hours, minutes, seconds = parts
      return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
  except ValueError:
    return None
  return None


def parse_srt_entries(polished: str) -> list[SrtEntry]:
  entries: list[SrtEntry] = []
  for line in polished.splitlines():
    match = SRT_LINE_PATTERN.match(line)
    if not match:
      continue
    start = parse_time_label(match.group("start"))
    end = parse_time_label(match.group("end"))
    text = match.group("text").strip()
    text = re.sub(r"^tags:\s*.*?\|\s*text:\s*", "", text).strip()
    if start is None or end is None or end <= start or not text:
      continue
    entries.append((start, end, text))
  return entries


def write_srt(path: Path, entries: list[SrtEntry]) -> None:
  blocks: list[str] = []
  for idx, (start, end, text) in enumerate(entries, start=1):
    blocks.append(
      "\n".join(
        [
          str(idx),
          f"{srt_timestamp(start)} --> {srt_timestamp(end)}",
          text,
        ]
      )
    )
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text("\n\n".join(blocks) + ("\n" if blocks else ""), encoding="utf-8")


def _words_in_range(words: list[Word], start: float, end: float) -> list[Word]:
  return [
    word
    for word in words
    if float(word.get("end", 0)) > start and float(word.get("start", 0)) < end
  ]


def _split_text_chunks(text: str, max_chars: int) -> list[str]:
  text = text.strip()
  if not text:
    return []
  if len(text) <= max_chars:
    return [text]

  chunks: list[str] = []
  cursor = 0
  while cursor < len(text):
    chunk = text[cursor : cursor + max_chars]
    if cursor + max_chars < len(text):
      split_at = max(chunk.rfind(" "), chunk.rfind("，"), chunk.rfind("、"))
      if split_at > max_chars // 3:
        chunk = chunk[: split_at + 1]
    chunk = chunk.strip()
    if chunk:
      chunks.append(chunk)
    cursor += max(1, len(chunk))
  return chunks


def split_entry_by_words(
  start: float,
  end: float,
  text: str,
  words: list[Word],
  *,
  max_chars: int,
  max_duration: float,
) -> list[SrtEntry]:
  duration = end - start
  if duration <= max_duration and len(text) <= max_chars:
    return [(start, end, text)]

  range_words = _words_in_range(words, start, end)
  chunks = _split_text_chunks(text, max_chars)
  if len(chunks) <= 1:
    if duration > max_duration and range_words:
      mid = len(range_words) // 2
      split_time = float(range_words[mid].get("start", (start + end) / 2))
      return [
        (start, split_time, text[: len(text) // 2].strip() or text),
        (split_time, end, text[len(text) // 2 :].strip() or text),
      ]
    return [(start, end, text)]

  entries: list[SrtEntry] = []
  cursor = 0
  last_end = start
  for chunk in chunks:
    chunk_start, chunk_end = match_sentence_timestamp(chunk, range_words or words, last_end)
    if chunk_start is None or chunk_end is None:
      ratio = len(chunk) / max(1, sum(len(c) for c in chunks))
      chunk_start = last_end
      chunk_end = min(end, last_end + duration * ratio)
    entries.append((chunk_start, chunk_end, chunk))
    last_end = chunk_end
    cursor += len(chunk)

  if entries:
    entries[0] = (start, entries[0][1], entries[0][2])
    entries[-1] = (entries[-1][0], end, entries[-1][2])
  return entries


def split_entries_for_display(
  entries: list[SrtEntry],
  words: list[Word],
  *,
  max_chars: int = 12,
  max_duration: float = 6.0,
) -> list[SrtEntry]:
  output: list[SrtEntry] = []
  for start, end, text in entries:
    output.extend(
      split_entry_by_words(
        start,
        end,
        text,
        words,
        max_chars=max_chars,
        max_duration=max_duration,
      )
    )
  return output


def segments_to_entries(segments: list[dict[str, Any]]) -> list[SrtEntry]:
  entries: list[SrtEntry] = []
  for segment in segments:
    start = segment.get("start")
    end = segment.get("end")
    text = str(segment.get("text", "")).strip()
    if start is None or end is None or not text:
      continue
    start_f = float(start)
    end_f = float(end)
    if end_f <= start_f:
      continue
    entries.append((start_f, end_f, text))
  return entries
