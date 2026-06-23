"""Python wrapper around the sense-voice-main CLI binary."""

from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BIN = ROOT / "SenseVoice.cpp" / "build" / "bin" / "sense-voice-main"
DEFAULT_MODEL = ROOT / "models" / "sense-voice-small-fp16.gguf"

TAG_PATTERN = re.compile(r"<\|[^|]+\|>")
TIMESTAMP_PATTERN = re.compile(r"^\[[\d.\-]+\]\s*")


def strip_tags(text: str) -> str:
    """Remove SenseVoice special tokens and optional timestamp prefix."""
    text = TIMESTAMP_PATTERN.sub("", text)
    return TAG_PATTERN.sub("", text).strip()


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

    @property
    def rtf(self) -> float:
        if self.audio_seconds <= 0:
            return 0.0
        return self.process_seconds / self.audio_seconds


class SenseVoice:
    """Local SenseVoice speech recognition via the C++ binary."""

    def __init__(
        self,
        model_path: str | Path | None = None,
        bin_path: str | Path | None = None,
        threads: int = 4,
        use_gpu: bool = True,
        language: str = "auto",
        use_itn: bool = True,
    ) -> None:
        self.model_path = Path(
            model_path or os.environ.get("SENSE_VOICE_MODEL", DEFAULT_MODEL)
        )
        self.bin_path = Path(
            bin_path or os.environ.get("SENSE_VOICE_BIN", DEFAULT_BIN)
        )
        self.threads = threads
        self.use_gpu = use_gpu
        self.language = language
        self.use_itn = use_itn

    def _build_cmd(self, audio_path: str | Path) -> list[str]:
        if not self.bin_path.is_file():
            raise FileNotFoundError(
                f"sense-voice-main not found at {self.bin_path}. "
                "Run: pixi run build"
            )
        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Model not found at {self.model_path}. "
                "Run: pixi run download-model"
            )

        cmd = [
            str(self.bin_path),
            "-m",
            str(self.model_path),
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

    def transcribe(
        self,
        audio_path: str | Path,
        *,
        raw: bool = False,
        with_timestamps: bool = True,
    ) -> str | TranscriptionResult:
        """Transcribe a WAV file. Returns plain text by default."""
        audio_seconds = get_audio_duration(audio_path)
        started = time.perf_counter()
        result = subprocess.run(
            self._build_cmd(audio_path),
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
            )
        return clean
