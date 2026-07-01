"""SRT formatting and display-oriented splitting."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any

from .timestamps import Word, match_sentence_timestamp

SrtEntry = tuple[float, float, str]
SRT_LINE_PATTERN = re.compile(
  r"^\s*(?:[-*]\s*)?\[(?P<start>[^\]-]+)-(?P<end>[^\]]+)\]\s*(?P<text>.+?)\s*$"
)

STRONG_BREAK_CHARS = "。！？!?"
WEAK_BREAK_CHARS = "，、；,"
MODAL_END_CHARS = "呢吗啊吧了呀嘛"
DEFAULT_MAX_SRT_WEIGHT = 18.0
# None = do not split display lines by duration (segment timing already bounds entries).
DEFAULT_MAX_SRT_DURATION: float | None = None
MAX_FRAGMENT_MERGE_GAP = 1.0


def calc_weighted_length(text: str) -> float:
  total = 0.0
  for char in text:
    if unicodedata.category(char).startswith("L"):
      total += 2.0 if ord(char) > 0x2E80 else 1.0
    else:
      total += 1.0
  return total


def _char_weight(char: str) -> float:
  if unicodedata.category(char).startswith("L"):
    return 2.0 if ord(char) > 0x2E80 else 1.0
  return 1.0


def _split_priority(text: str, split_index: int) -> int:
  if split_index <= 0 or split_index >= len(text):
    return 0
  prev_char = text[split_index - 1]
  if prev_char in STRONG_BREAK_CHARS:
    return 50
  if prev_char in WEAK_BREAK_CHARS:
    return 40
  if prev_char in MODAL_END_CHARS:
    return 30
  if prev_char.isspace():
    return 10
  return 0


def _is_fragment_text(text: str) -> bool:
  stripped = text.strip()
  if not stripped:
    return True
  if all(
    unicodedata.category(char).startswith("P") or char.isspace()
    for char in stripped
  ):
    return True
  if calc_weighted_length(stripped) <= 4 and all(
    char in MODAL_END_CHARS or char in WEAK_BREAK_CHARS for char in stripped
  ):
    return True
  return False


def _is_tiny_tail_fragment(text: str) -> bool:
  """Short tail pieces with no sentence end (e.g. 地方, 业，) merge to previous line."""
  stripped = text.strip()
  if not stripped or calc_weighted_length(stripped) > 6:
    return False
  if stripped[-1] in STRONG_BREAK_CHARS:
    return False
  return True


def _can_merge_fragment(prev: SrtEntry, current: SrtEntry, *, max_gap: float = MAX_FRAGMENT_MERGE_GAP) -> bool:
  """Only merge display fragments that are temporally adjacent."""
  _prev_start, prev_end, _prev_text = prev
  start, end, _text = current
  if end <= start:
    return False
  return start - prev_end <= max_gap


def _find_best_split_index(text: str, max_weight: float, *, soft_overflow: float = 8.0) -> int | None:
  """Split only at punctuation/modal boundaries; never hard-cut mid-phrase."""
  if calc_weighted_length(text) <= max_weight:
    return None

  best_index: int | None = None
  best_priority = 0
  weight = 0.0
  limit = max_weight + soft_overflow

  for index, char in enumerate(text):
    weight += _char_weight(char)
    split_index = index + 1
    if weight > limit:
      break
    if weight > max_weight and _split_priority(text, split_index) == 0:
      continue
    priority = _split_priority(text, split_index)
    if priority > best_priority or (priority == best_priority and priority > 0):
      best_priority = priority
      best_index = split_index

  if best_index is not None and best_priority > 0:
    return best_index
  return None


def _split_text_chunks(text: str, max_weight: float) -> list[str]:
  text = text.strip()
  if not text:
    return []
  if calc_weighted_length(text) <= max_weight:
    return [text]

  chunks: list[str] = []
  cursor = 0
  while cursor < len(text):
    remainder = text[cursor:]
    split_index = _find_best_split_index(remainder, max_weight)
    if split_index is None:
      chunks.append(remainder)
      break
    chunk = remainder[:split_index]
    if not chunk.strip():
      cursor += max(1, split_index)
      continue
    chunks.append(chunk)
    cursor += split_index
  return chunks


def _attach_leading_punctuation(entries: list[SrtEntry]) -> list[SrtEntry]:
  if not entries:
    return entries

  output: list[SrtEntry] = []
  for start, end, text in entries:
    if output and text:
      lead = 0
      while lead < len(text) and text[lead] in WEAK_BREAK_CHARS + STRONG_BREAK_CHARS:
        lead += 1
      if 0 < lead < len(text):
        prev_start, prev_end, prev_text = output[-1]
        output[-1] = (prev_start, prev_end, prev_text + text[:lead])
        text = text[lead:]
        start = prev_end
    if text.strip():
      output.append((start, end, text))
  return output


def _merge_fragment_entries(entries: list[SrtEntry]) -> list[SrtEntry]:
  if not entries:
    return entries

  merged: list[SrtEntry] = []
  for start, end, text in entries:
    if (
      merged
      and (_is_fragment_text(text) or _is_tiny_tail_fragment(text))
      and _can_merge_fragment(merged[-1], (start, end, text))
    ):
      prev_start, prev_end, prev_text = merged[-1]
      merged[-1] = (prev_start, max(prev_end, end), prev_text + text)
      continue
    if not merged and _is_fragment_text(text):
      merged.append((start, end, text))
      continue
    if merged and _is_fragment_text(merged[-1][2]) and _can_merge_fragment(merged[-1], (start, end, text)):
      prev_start, prev_end, prev_text = merged[-1]
      merged[-1] = (prev_start, end, prev_text + text)
      continue
    merged.append((start, end, text))
  return _attach_leading_punctuation(merged)


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


def parse_srt_timestamp_label(label: str) -> float | None:
  label = label.strip()
  match = re.match(r"(\d+):(\d+):(\d+),(\d+)", label)
  if match:
    hours, minutes, seconds, millis = match.groups()
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis) / 1000
  return parse_time_label(label)


def read_srt_file(content: str) -> list[SrtEntry]:
  """Parse standard SRT blocks (index / timestamps / text)."""
  entries: list[SrtEntry] = []
  for block in re.split(r"\n\s*\n", content.strip()):
    lines = [line for line in block.strip().splitlines() if line.strip()]
    if len(lines) < 3:
      continue
    time_match = re.match(r"(.+?)\s*-->\s*(.+)", lines[1].strip())
    if not time_match:
      continue
    start = parse_srt_timestamp_label(time_match.group(1))
    end = parse_srt_timestamp_label(time_match.group(2))
    text = "\n".join(lines[2:]).strip()
    if start is None or end is None or end <= start or not text:
      continue
    entries.append((start, end, text))
  return entries


def reclean_srt_entries(entries: list[SrtEntry]) -> list[SrtEntry]:
  """Re-apply subtitle text cleaning (drop fillers, fix punctuation) without re-running LLM."""
  from .llm import clean_polished_subtitle_text

  cleaned: list[SrtEntry] = []
  for start, end, text in entries:
    new_text = clean_polished_subtitle_text(text)
    if new_text:
      cleaned.append((start, end, new_text))
  return cleaned


def parse_srt_entries(polished: str) -> list[SrtEntry]:
  entries: list[SrtEntry] = []
  for line in polished.splitlines():
    if line.strip().startswith("##"):
      break
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


def _split_entry_proportionally(
  start: float,
  end: float,
  chunks: list[str],
) -> list[SrtEntry]:
  duration = max(0.0, end - start)
  total_weight = sum(calc_weighted_length(chunk) for chunk in chunks)
  entries: list[SrtEntry] = []
  last_end = start
  for index, chunk in enumerate(chunks):
    if index == len(chunks) - 1:
      chunk_end = end
    else:
      ratio = calc_weighted_length(chunk) / max(1.0, total_weight)
      chunk_end = min(end, last_end + duration * ratio)
    if chunk_end <= last_end:
      chunk_end = min(end, last_end + 0.2)
    entries.append((last_end, chunk_end, chunk))
    last_end = chunk_end
  if entries:
    entries[0] = (start, entries[0][1], entries[0][2])
    entries[-1] = (entries[-1][0], end, entries[-1][2])
  return entries


def _cap_entry_duration(start: float, end: float, text: str, max_duration: float | None) -> SrtEntry:
  if max_duration is None or end - start <= max_duration:
    return (start, end, text)
  return (start, min(end, start + max_duration), text)


def _cap_entries_duration(entries: list[SrtEntry], max_duration: float | None) -> list[SrtEntry]:
  if max_duration is None:
    return entries
  return [_cap_entry_duration(start, end, text, max_duration) for start, end, text in entries]


def split_entry_by_words(
  start: float,
  end: float,
  text: str,
  words: list[Word],
  *,
  timing_text: str | None = None,
  max_chars: int | float = DEFAULT_MAX_SRT_WEIGHT,
  max_duration: float | None = DEFAULT_MAX_SRT_DURATION,
) -> list[SrtEntry]:
  max_weight = float(max_chars)
  duration = end - start
  within_duration = max_duration is None or duration <= max_duration
  if within_duration and calc_weighted_length(text) <= max_weight:
    return [(start, end, text)]

  range_words = _words_in_range(words, start, end)
  chunks = _split_text_chunks(text, max_weight)
  if len(chunks) <= 1:
    return [_cap_entry_duration(start, end, text, max_duration)]

  align_text = timing_text if timing_text is not None else text
  cross_language = timing_text is not None and timing_text.strip() != text.strip()
  if cross_language:
    return _cap_entries_duration(_merge_fragment_entries(_split_entry_proportionally(start, end, chunks)), max_duration)

  entries: list[SrtEntry] = []
  last_end = start
  for chunk in chunks:
    chunk_start, chunk_end = match_sentence_timestamp(chunk, range_words or words, last_end)
    if chunk_start is None or chunk_end is None:
      ratio = calc_weighted_length(chunk) / max(1.0, calc_weighted_length(text))
      chunk_start = last_end
      chunk_end = min(end, last_end + duration * ratio)
    entries.append((chunk_start, chunk_end, chunk))
    last_end = chunk_end

  if entries:
    entries[0] = (start, entries[0][1], entries[0][2])
    entries[-1] = (entries[-1][0], end, entries[-1][2])
  return _cap_entries_duration(_merge_fragment_entries(entries), max_duration)


def split_entries_for_display(
  entries: list[SrtEntry],
  words: list[Word],
  *,
  timing_texts: list[str] | None = None,
  max_chars: int | float = DEFAULT_MAX_SRT_WEIGHT,
  max_duration: float | None = DEFAULT_MAX_SRT_DURATION,
) -> list[SrtEntry]:
  output: list[SrtEntry] = []
  for index, (start, end, text) in enumerate(entries):
    timing_text = timing_texts[index] if timing_texts and index < len(timing_texts) else None
    output.extend(
      split_entry_by_words(
        start,
        end,
        text,
        words,
        timing_text=timing_text,
        max_chars=max_chars,
        max_duration=max_duration,
      )
    )
  return _cap_entries_duration(_attach_leading_punctuation(_merge_fragment_entries(output)), max_duration)


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
