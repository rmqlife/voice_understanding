"""Python wrappers for local SenseVoice backends."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BIN = ROOT / "SenseVoice.cpp" / "build" / "bin" / "sense-voice-main"
DEFAULT_MODEL = ROOT / "models" / "sense-voice-small-fp16.gguf"
DEFAULT_OFFICIAL_MODEL = "iic/SenseVoiceSmall"

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
                vad_kwargs={"max_single_segment_time": 30000},
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
                merge_length_s=15,
            )
        process_seconds = time.perf_counter() - started

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
