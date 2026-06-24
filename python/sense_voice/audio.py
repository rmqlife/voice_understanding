"""Audio duration and timestamp helpers."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def extract_audio_segment(
    audio_path: str | Path,
    start: float,
    end: float,
    output_path: str | Path,
) -> Path:
    """Extract [start, end) as 16 kHz mono WAV."""
    duration = max(0.01, float(end) - float(start))
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-ss",
            str(max(0.0, start)),
            "-i",
            str(audio_path),
            "-t",
            str(duration),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(output_path),
        ],
        check=True,
    )
    return output_path


def ffprobe_duration(path: str | Path) -> float | None:
    """Return media duration in seconds, or None if ffprobe fails."""
    proc = subprocess.run(
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
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return None
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return None


def get_audio_duration(path: str | Path) -> float:
    """Return media duration in seconds; raises on failure."""
    duration = ffprobe_duration(path)
    if duration is None:
        raise RuntimeError(f"ffprobe could not read duration for {path}")
    return duration


def max_timestamp_seconds(text: str) -> float | None:
    """Largest end time from `[start-end]` markers in ASR text."""
    matches = re.findall(r"\[(?:\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]", text)
    if not matches:
        return None
    return max(float(value) for value in matches)
