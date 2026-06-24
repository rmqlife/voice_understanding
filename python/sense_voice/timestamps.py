"""Align subtitle sentences to character/word timestamps (KrillinAI-style)."""

from __future__ import annotations

import re
import string
import unicodedata
from typing import Any

Word = dict[str, Any]
TimedSentence = dict[str, Any]

_PUNCT_AND_SPACE = set(string.punctuation) | {" ", "\t", "\n", "\r"}


def clean_base_text(text: str) -> str:
  cleaned: list[str] = []
  for char in text:
    if char in _PUNCT_AND_SPACE:
      continue
    if unicodedata.category(char).startswith("P") or unicodedata.category(char).startswith("Z"):
      continue
    if unicodedata.category(char).startswith("S"):
      continue
    cleaned.append(char)
  return "".join(cleaned)


def build_full_text(words: list[Word]) -> str:
  return "".join(str(word.get("text", "")) for word in words if word.get("text"))


def find_all_matches(needle: str, haystack: str) -> list[int]:
  needle_run = list(needle)
  haystack_run = list(haystack)
  if not needle_run or not haystack_run:
    return []
  matches: list[int] = []
  limit = len(haystack_run) - len(needle_run)
  for index in range(max(0, limit) + 1):
    if haystack_run[index : index + len(needle_run)] == needle_run:
      matches.append(index)
  return matches


def calculate_timestamps_by_char_index(
  start_char_index: int,
  end_char_index: int,
  words: list[Word],
  last_ts: float,
) -> tuple[float | None, float | None]:
  result_start: float | None = None
  result_end: float | None = None
  current_char_index = 0

  for word in words:
    text = str(word.get("text", ""))
    if not text:
      continue
    clean = clean_base_text(text)
    word_len = len(clean)
    if word_len == 0:
      continue

    word_start_index = current_char_index
    word_end_index = current_char_index + word_len

    if result_start is None and word_end_index > start_char_index:
      start = float(word.get("start", 0))
      if start >= last_ts:
        result_start = start

    if word_start_index < end_char_index:
      end = float(word.get("end", 0))
      if end >= last_ts:
        result_end = end

    if word_start_index >= end_char_index:
      break
    current_char_index = word_end_index

  if (
    result_start is None
    or result_end is None
    or result_start < last_ts
    or result_start >= result_end
  ):
    return None, None
  return result_start, result_end


def fuzzy_match_sentence(
  sentence: str,
  words: list[Word],
  last_ts: float,
) -> tuple[float | None, float | None]:
  clean_sentence = clean_base_text(sentence)
  if not clean_sentence:
    return None, None

  sentence_chars = set(clean_sentence)
  matched: list[Word] = []
  for word in words:
    if float(word.get("start", 0)) < last_ts:
      continue
    word_chars = set(clean_base_text(str(word.get("text", ""))))
    if sentence_chars & word_chars:
      matched.append(word)

  if not matched:
    for word in words:
      word_chars = set(clean_base_text(str(word.get("text", ""))))
      if sentence_chars & word_chars:
        matched.append(word)

  if not matched:
    return None, None

  start = float(matched[0].get("start", 0))
  end = float(matched[-1].get("end", 0))
  if start < last_ts:
    start = last_ts
  if end <= start:
    end = start + 1.0
  return start, end


def match_sentence_timestamp(
  sentence: str,
  words: list[Word],
  last_ts: float,
) -> tuple[float | None, float | None]:
  if not sentence or not words:
    return None, None

  whisper_full = build_full_text(words)
  if not whisper_full:
    return None, None

  clean_sentence = clean_base_text(sentence)
  clean_whisper = clean_base_text(whisper_full)
  if not clean_sentence:
    return None, None

  matches = find_all_matches(clean_sentence, clean_whisper)
  if not matches:
    return fuzzy_match_sentence(clean_sentence, words, last_ts)

  best_start: float | None = None
  best_end: float | None = None
  for start_char_index in matches:
    end_char_index = start_char_index + len(clean_sentence)
    start, end = calculate_timestamps_by_char_index(
      start_char_index,
      end_char_index,
      words,
      last_ts,
    )
    if start is None or end is None:
      continue
    if start >= last_ts:
      return start, end
    if best_start is None or start > best_start:
      best_start, best_end = start, end

  if best_start is not None and best_end is not None:
    return best_start, best_end
  return fuzzy_match_sentence(clean_sentence, words, last_ts)


class TimestampGenerator:
  """Generate monotonic timestamps for subtitle sentences."""

  def __init__(self, *, min_duration: float = 0.2) -> None:
    self.min_duration = min_duration

  def generate(
    self,
    sentences: list[str],
    words: list[Word],
    *,
    ts_offset: float = 0.0,
  ) -> list[TimedSentence]:
    last_end = 0.0
    results: list[TimedSentence] = []

    for index, sentence in enumerate(sentences, start=1):
      text = sentence.strip()
      if not text:
        continue
      start, end = match_sentence_timestamp(text, words, last_end)
      if start is None or end is None:
        start = last_end
        end = last_end + self.min_duration
      if start < last_end:
        start = last_end
      if end <= start:
        end = start + max(self.min_duration, 1.0)

      results.append(
        {
          "index": index,
          "text": text,
          "start": start + ts_offset,
          "end": end + ts_offset,
          "timing_confidence": "high" if end > start else "low",
        }
      )
      if end - start < 5:
        last_end = end

    return results

  def align_segment_dicts(
    self,
    segments: list[dict[str, Any]],
    words: list[Word],
  ) -> list[dict[str, Any]]:
    last_end = 0.0
    aligned: list[dict[str, Any]] = []
    for segment in segments:
      text = str(segment.get("text", "")).strip()
      if not text:
        continue
      start, end = match_sentence_timestamp(text, words, last_end)
      updated = dict(segment)
      if start is not None and end is not None:
        updated["start"] = start
        updated["end"] = end
        updated["timing_confidence"] = "high"
        if end - start < 5:
          last_end = end
      aligned.append(updated)
    return aligned
