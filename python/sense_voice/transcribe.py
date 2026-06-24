"""Python wrappers for local SenseVoice backends."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BIN = ROOT / "SenseVoice.cpp" / "build" / "bin" / "sense-voice-main"
DEFAULT_MODEL = ROOT / "models" / "sense-voice-small-fp16.gguf"
DEFAULT_OFFICIAL_MODEL = "iic/SenseVoiceSmall"
DEFAULT_MERGE_LENGTH_S = 6
DEFAULT_MAX_SINGLE_SEGMENT_MS = 12_000

TAG_PATTERN = re.compile(r"<\|[^|]+\|>")
TAG_GROUP_PATTERN = re.compile(r"((?:<\|[^|]+\|>)+)([^<]*)")
TIMESTAMP_PATTERN = re.compile(r"^\[[\d.\-]+\]\s*")
LANG_TAGS = {"zh", "en", "yue", "ja", "ko", "nospeech"}
SPEECH_TAGS = {"Speech", "Applause", "BGM", "Laughter", "Event"}
ITN_TAGS = {"withitn", "woitn"}


def strip_tags(text: str) -> str:
    """Remove SenseVoice special tokens and optional timestamp prefix."""
    text = TIMESTAMP_PATTERN.sub("", text)
    return TAG_PATTERN.sub("", text).strip()


def _ms_to_seconds(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number > 1000:
        return number / 1000.0
    return number


def _parse_tagged_chunks(text: str) -> list[dict[str, Any]]:
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
                "timing_confidence": None,
            }
        )
    return segments


def _allocate_time_ranges(
    start: float,
    end: float,
    segments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not segments:
        return segments
    if end <= start:
        for segment in segments:
            segment["start"] = start
            segment["end"] = end
            segment["timing_confidence"] = "low"
        return segments

    total_chars = sum(max(1, len(str(segment["text"]))) for segment in segments)
    cursor = start
    duration = end - start
    for index, segment in enumerate(segments):
        if index == len(segments) - 1:
            segment["start"] = cursor
            segment["end"] = end
        else:
            chunk_duration = duration * max(1, len(str(segment["text"]))) / total_chars
            segment["start"] = cursor
            segment["end"] = cursor + chunk_duration
            cursor += chunk_duration
        segment["timing_confidence"] = "medium"
    return segments


def _segments_from_timed_text(
    text: str,
    start: float | None,
    end: float | None,
    *,
    timing_confidence: str,
) -> list[dict[str, Any]]:
    chunks = _parse_tagged_chunks(text)
    if not chunks:
        clean = strip_tags(text)
        if not clean:
            return []
        return [
            {
                "start": start,
                "end": end,
                "lang": None,
                "type": None,
                "itn": None,
                "emotion": None,
                "text": clean,
                "timing_confidence": timing_confidence,
            }
        ]

    if start is not None and end is not None:
        return _allocate_time_ranges(start, end, chunks)
    for chunk in chunks:
        chunk["timing_confidence"] = timing_confidence
    return chunks


def _words_from_timestamp(text: str, timestamp: Any) -> list[dict[str, Any]]:
    if not isinstance(timestamp, list) or not timestamp:
        return []

    readable = strip_tags(text).replace(" ", "")
    chars = list(readable)
    if not chars:
        return []

    words: list[dict[str, Any]] = []
    for index, item in enumerate(timestamp):
        if index >= len(chars):
            break
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        start = _ms_to_seconds(item[0])
        end = _ms_to_seconds(item[1])
        if start is None or end is None:
            continue
        words.append(
            {
                "text": chars[index],
                "start": start,
                "end": end,
            }
        )
    return words


def _build_char_timings(words: list[Any], timestamp: list[Any]) -> list[dict[str, Any]]:
    timings: list[dict[str, Any]] = []
    for index, char in enumerate(words):
        if index >= len(timestamp):
            break
        item = timestamp[index]
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        start = _ms_to_seconds(item[0])
        end = _ms_to_seconds(item[1])
        if start is None or end is None:
            continue
        timings.append(
            {
                "text": str(char),
                "start": start,
                "end": end,
            }
        )
    return timings


def _normalize_chars(text: str) -> str:
    return re.sub(r"\s+", "", strip_tags(text))


def _find_char_span(haystack: str, needle: str, start: int) -> tuple[int, int] | None:
    if not needle:
        return None
    index = haystack.find(needle, start)
    if index < 0:
        return None
    return index, index + len(needle)


def _segments_from_char_timings(text: str, char_timings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not char_timings:
        return []

    char_stream = "".join(item["text"] for item in char_timings)
    segments: list[dict[str, Any]] = []
    cursor = 0

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
        normalized = _normalize_chars(segment_text)
        if not normalized:
            continue
        span = _find_char_span(char_stream, normalized, cursor)
        if span is None:
            span = _find_char_span(char_stream, normalized, 0)
        if span is None:
            segments.append(
                {
                    "start": None,
                    "end": None,
                    "lang": lang,
                    "type": speech_type,
                    "itn": itn,
                    "emotion": ",".join(emotions) if emotions else None,
                    "text": strip_tags(segment_text),
                    "timing_confidence": "low",
                }
            )
            continue

        begin, end = span
        segments.append(
            {
                "start": char_timings[begin]["start"],
                "end": char_timings[end - 1]["end"],
                "lang": lang,
                "type": speech_type,
                "itn": itn,
                "emotion": ",".join(emotions) if emotions else None,
                "text": strip_tags(segment_text),
                "timing_confidence": "high",
            }
        )
        cursor = end

    if segments:
        return segments

    normalized = _normalize_chars(text)
    if normalized:
        span = _find_char_span(char_stream, normalized, 0)
        if span:
            begin, end = span
            return [
                {
                    "start": char_timings[begin]["start"],
                    "end": char_timings[end - 1]["end"],
                    "lang": None,
                    "type": None,
                    "itn": None,
                    "emotion": None,
                    "text": strip_tags(text),
                    "timing_confidence": "high",
                }
            ]
    return []


def extract_official_segments(result: list[Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    """Parse FunASR SenseVoice output into timed segments and optional word spans."""
    if not result:
        return [], [], "none"

    item = result[0] if isinstance(result[0], dict) else {}
    words = item.get("words")
    timestamp = item.get("timestamp")
    if isinstance(words, list) and isinstance(timestamp, list) and words and timestamp:
        char_timings = _build_char_timings(words, timestamp)
        segments = _segments_from_char_timings(str(item.get("text", "")), char_timings)
        if segments:
            return segments, char_timings, "char_timestamp"

    sentence_info = item.get("sentence_info")
    if isinstance(sentence_info, list) and sentence_info:
        segments: list[dict[str, Any]] = []
        words: list[dict[str, Any]] = []
        for sent in sentence_info:
            if not isinstance(sent, dict):
                continue
            start = _ms_to_seconds(sent.get("start"))
            end = _ms_to_seconds(sent.get("end"))
            text = str(sent.get("text", ""))
            segments.extend(
                _segments_from_timed_text(
                    text,
                    start,
                    end,
                    timing_confidence="high",
                )
            )
            words.extend(_words_from_timestamp(text, sent.get("timestamp")))
        if segments:
            return segments, words, "sentence_info"

    timestamp = item.get("timestamp")
    words = _words_from_timestamp(str(item.get("text", "")), timestamp)
    if words:
        start = words[0]["start"]
        end = words[-1]["end"]
        segments = _segments_from_timed_text(
            str(item.get("text", "")),
            start,
            end,
            timing_confidence="high",
        )
        if segments:
            return segments, words, "timestamp"

    segments = _segments_from_timed_text(
        str(item.get("text", "")),
        None,
        None,
        timing_confidence="tag_only",
    )
    if segments:
        return segments, words, "tag_only"
    return [], words, "none"


def get_audio_duration(path: str | Path) -> float:
    """Return audio duration in seconds via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())


def parse_transcript(stdout: str, *, with_timestamps: bool = True) -> str:
    """Parse CLI stdout into clean text, merging VAD segments."""
    segments: list[str] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("sense_voice") or line.startswith("system_info"):
            continue
        if line.startswith("main:") or "rtf is" in line:
            continue

        timestamp = ""
        if line.startswith("["):
            match = re.match(r"^(\[[\d.\-]+\])\s*(.*)$", line)
            if match:
                timestamp, line = match.group(1), match.group(2)

        text = strip_tags(line)
        if not text:
            continue

        if with_timestamps and timestamp:
            segments.append(f"{timestamp} {text}")
        else:
            segments.append(text)

    if with_timestamps:
        return "\n".join(segments)
    return "".join(segments)


@dataclass
class TranscriptionResult:
    raw: str
    text: str
    audio_seconds: float
    process_seconds: float
    sentences: list[dict[str, Any]] = field(default_factory=list)
    words: list[dict[str, Any]] = field(default_factory=list)
    timing_source: str = "none"

    @property
    def rtf(self) -> float:
        if self.audio_seconds <= 0:
            return 0.0
        return self.process_seconds / self.audio_seconds

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "raw": self.raw,
            "audio_seconds": self.audio_seconds,
            "process_seconds": self.process_seconds,
            "rtf": self.rtf,
            "sentences": self.sentences,
            "words": self.words,
            "timing_source": self.timing_source,
        }


class SenseVoice:
    """Local SenseVoice speech recognition.

    Backends:
    - cpp: SenseVoice.cpp GGUF binary, useful for macOS/Metal.
    - official: FunASR AutoModel, useful for CUDA GPU environments.
    """

    def __init__(
        self,
        model_path: str | Path | None = None,
        bin_path: str | Path | None = None,
        threads: int = 4,
        use_gpu: bool = True,
        language: str = "auto",
        use_itn: bool = True,
        backend: str | None = None,
        device: str | None = None,
        vad_model: str = "fsmn-vad",
        disable_update: bool = True,
        merge_length_s: float = DEFAULT_MERGE_LENGTH_S,
        max_single_segment_ms: int = DEFAULT_MAX_SINGLE_SEGMENT_MS,
    ) -> None:
        self.backend = (backend or os.environ.get("SENSE_VOICE_BACKEND", "cpp")).lower()
        if self.backend in {"cxx", "sensevoice.cpp", "sense-voice.cpp"}:
            self.backend = "cpp"
        if self.backend in {"funasr", "python"}:
            self.backend = "official"
        if self.backend not in {"cpp", "official"}:
            raise ValueError("backend must be 'cpp' or 'official'")

        default_model = (
            DEFAULT_OFFICIAL_MODEL if self.backend == "official" else DEFAULT_MODEL
        )
        self.model_path = model_path or os.environ.get("SENSE_VOICE_MODEL", default_model)
        self.bin_path = Path(
            bin_path or os.environ.get("SENSE_VOICE_BIN", DEFAULT_BIN)
        )
        self.threads = threads
        self.use_gpu = use_gpu
        self.language = language
        self.use_itn = use_itn
        self.device = device or os.environ.get(
            "SENSE_VOICE_DEVICE", "cuda:0" if use_gpu else "cpu"
        )
        self.vad_model = vad_model
        self.disable_update = disable_update
        self.merge_length_s = merge_length_s
        self.max_single_segment_ms = max_single_segment_ms
        self._official_model = None

    def _build_cpp_cmd(self, audio_path: str | Path) -> list[str]:
        if not self.bin_path.is_file():
            raise FileNotFoundError(
                f"sense-voice-main not found at {self.bin_path}. "
                "Run: pixi run build"
            )
        model_path = Path(self.model_path)
        if not model_path.is_file():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Run: pixi run download-model"
            )

        cmd = [
            str(self.bin_path),
            "-m",
            str(model_path),
            "-t",
            str(self.threads),
            "-l",
            self.language,
            "-np",
        ]
        if not self.use_gpu:
            cmd.append("-ng")
        if self.use_itn:
            cmd.append("-itn")
        cmd.append(str(audio_path))
        return cmd

    def _load_official_model(self):
        if self._official_model is not None:
            return self._official_model

        try:
            from funasr import AutoModel
        except ImportError as exc:
            raise RuntimeError(
                "The official SenseVoice backend requires FunASR. "
                "Run: pixi run install-gpu"
            ) from exc

        with redirect_stdout(sys.stderr):
            self._official_model = AutoModel(
                model=str(self.model_path),
                trust_remote_code=False,
                vad_model=self.vad_model,
                vad_kwargs={"max_single_segment_time": self.max_single_segment_ms},
                device=self.device,
                disable_update=self.disable_update,
            )
        return self._official_model

    def _transcribe_cpp(
        self,
        audio_path: str | Path,
        *,
        raw: bool,
        with_timestamps: bool,
        audio_seconds: float,
        started: float,
    ) -> str | TranscriptionResult:
        result = subprocess.run(
            self._build_cpp_cmd(audio_path),
            capture_output=True,
            text=True,
            check=False,
        )
        process_seconds = time.perf_counter() - started
        if result.returncode != 0:
            raise RuntimeError(
                f"sense-voice-main failed (exit {result.returncode}):\n"
                f"{result.stderr or result.stdout}"
            )

        clean = parse_transcript(result.stdout, with_timestamps=with_timestamps)
        raw_text = result.stdout.strip()
        if raw:
            return TranscriptionResult(
                raw=raw_text,
                text=clean,
                audio_seconds=audio_seconds,
                process_seconds=process_seconds,
                timing_source="cpp_vad",
            )
        return clean

    def _transcribe_official(
        self,
        audio_path: str | Path,
        *,
        raw: bool,
        audio_seconds: float,
        started: float,
    ) -> str | TranscriptionResult:
        model = self._load_official_model()
        with redirect_stdout(sys.stderr):
            result = model.generate(
                input=str(audio_path),
                cache={},
                language=self.language,
                use_itn=self.use_itn,
                batch_size_s=60,
                merge_vad=True,
                merge_length_s=self.merge_length_s,
                output_timestamp=True,
            )
        process_seconds = time.perf_counter() - started

        sentences, words, timing_source = extract_official_segments(result)

        texts: list[str] = []
        for item in result:
            if isinstance(item, dict):
                texts.append(str(item.get("text", "")))
        clean = "\n".join(text for text in texts if text).strip()
        try:
            from funasr.utils.postprocess_utils import rich_transcription_postprocess

            clean = rich_transcription_postprocess(clean)
        except Exception:
            clean = strip_tags(clean)

        raw_text = json.dumps(result, ensure_ascii=False, default=str)
        if raw:
            return TranscriptionResult(
                raw=raw_text,
                text=clean,
                audio_seconds=audio_seconds,
                process_seconds=process_seconds,
                sentences=sentences,
                words=words,
                timing_source=timing_source,
            )
        return clean

    def transcribe(
        self,
        audio_path: str | Path,
        *,
        raw: bool = False,
        with_timestamps: bool = True,
    ) -> str | TranscriptionResult:
        """Transcribe an audio file. Returns plain text by default."""
        audio_seconds = get_audio_duration(audio_path)
        started = time.perf_counter()
        if self.backend == "official":
            return self._transcribe_official(
                audio_path,
                raw=raw,
                audio_seconds=audio_seconds,
                started=started,
            )
        return self._transcribe_cpp(
            audio_path,
            raw=raw,
            with_timestamps=with_timestamps,
            audio_seconds=audio_seconds,
            started=started,
        )
