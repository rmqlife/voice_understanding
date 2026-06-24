"""Speaker turn detection for transcript pipeline."""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from .audio import ffprobe_duration
from .models import FUNASR_DIARIZE_MODEL, FUNASR_SPK_MODEL
from .transcribe import _ms_to_seconds

DiarizeMethod = Literal["auto", "funasr", "pyannote", "ffmpeg-alternate", "vad"]


@dataclass
class SpeakerTurn:
    speaker: str
    start: float
    end: float
    text: str = ""
    name: str = ""

    def display_label(self) -> str:
        return self.name or self.speaker

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "speaker": self.speaker,
            "start": self.start,
            "end": self.end,
            "text": self.text,
        }
        if self.name:
            payload["name"] = self.name
        return payload


def _detect_speech_regions(
    audio_path: Path,
    *,
    silence_duration: float = 0.35,
    noise_db: int = -35,
    min_region_s: float = 0.25,
) -> list[tuple[float, float]]:
    """Return speech regions as (start, end) using ffmpeg silencedetect."""
    total = ffprobe_duration(audio_path)
    if total is None or total <= 0:
        return []

    proc = subprocess.run(
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
    silence_intervals: list[tuple[float, float]] = []
    current_start: float | None = None
    for line in proc.stderr.splitlines():
        if "silence_start:" in line:
            try:
                current_start = float(line.split("silence_start:")[-1].strip())
            except ValueError:
                current_start = None
        elif "silence_end:" in line and current_start is not None:
            match = re.search(r"silence_end:\s*([0-9.]+)", line)
            if match:
                silence_intervals.append((current_start, float(match.group(1))))
            current_start = None

    if not silence_intervals:
        return [(0.0, total)]

    regions: list[tuple[float, float]] = []
    cursor = 0.0
    for silence_start, silence_end in silence_intervals:
        if silence_start > cursor:
            regions.append((cursor, silence_start))
        cursor = max(cursor, silence_end)
    if cursor < total:
        regions.append((cursor, total))

    return [
        (start, end)
        for start, end in regions
        if end - start >= min_region_s
    ]


def _merge_close_regions(
    regions: list[tuple[float, float]],
    *,
    gap_s: float = 0.45,
) -> list[tuple[float, float]]:
    if not regions:
        return []
    merged: list[tuple[float, float]] = [regions[0]]
    for start, end in regions[1:]:
        prev_start, prev_end = merged[-1]
        if start - prev_end <= gap_s:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))
    return merged


def diarize_ffmpeg_alternate(
    audio_path: str | Path,
    *,
    silence_duration: float = 0.35,
    noise_db: int = -35,
    min_region_s: float = 0.35,
    merge_gap_s: float = 0.45,
) -> list[SpeakerTurn]:
    """ffmpeg silencedetect + alternating labels. Debug baseline only — not speaker ID."""
    regions = _detect_speech_regions(
        Path(audio_path),
        silence_duration=silence_duration,
        noise_db=noise_db,
        min_region_s=min_region_s,
    )
    regions = _merge_close_regions(regions, gap_s=merge_gap_s)
    turns: list[SpeakerTurn] = []
    for index, (start, end) in enumerate(regions):
        turns.append(
            SpeakerTurn(
                speaker=f"SPEAKER_{index % 2:02d}",
                start=start,
                end=end,
            )
        )
    return turns


def diarize_funasr(
    audio_path: str | Path,
    *,
    device: str = "cuda:0",
) -> list[SpeakerTurn]:
    """FunASR paraformer + cam++ speaker labels when available."""
    try:
        from funasr import AutoModel
    except ImportError as exc:
        raise RuntimeError(
            "FunASR diarization requires pixi run install-gpu on mag"
        ) from exc

    model = AutoModel(
        model=FUNASR_DIARIZE_MODEL,
        vad_model="fsmn-vad",
        punc_model="ct-punc-c",
        spk_model=FUNASR_SPK_MODEL,
        device=device,
        disable_update=True,
    )
    result = model.generate(input=str(audio_path), batch_size_s=300)
    turns: list[SpeakerTurn] = []
    if not result:
        return turns

    item = result[0] if isinstance(result[0], dict) else {}
    sentence_info = item.get("sentence_info")
    if not isinstance(sentence_info, list):
        return turns

    for sent in sentence_info:
        if not isinstance(sent, dict):
            continue
        text = str(sent.get("text", "")).strip()
        start_ms = sent.get("start")
        end_ms = sent.get("end")
        if start_ms is None or end_ms is None:
            continue
        start = _ms_to_seconds(start_ms)
        end = _ms_to_seconds(end_ms)
        if start is None or end is None:
            continue
        speaker = sent.get("spk")
        if speaker is None:
            speaker = sent.get("speaker")
        speaker_label = f"SPEAKER_{int(speaker):02d}" if speaker is not None else "SPEAKER_00"
        turns.append(
            SpeakerTurn(
                speaker=speaker_label,
                start=start,
                end=end,
            )
        )
    return turns


def _normalize_pyannote_label(label: str, mapping: dict[str, str]) -> str:
    if label not in mapping:
        mapping[label] = f"SPEAKER_{len(mapping):02d}"
    return mapping[label]


def _pyannote_annotation(output: object, *, exclusive: bool = False):
    """pyannote 4.x returns DiarizeOutput; 3.x returns Annotation directly."""
    if exclusive:
        annotation = getattr(output, "exclusive_speaker_diarization", None)
        if annotation is not None:
            return annotation
    annotation = getattr(output, "speaker_diarization", None)
    return output if annotation is None else annotation


def diarize_pyannote(
    audio_path: str | Path,
    *,
    device: str = "cuda:0",
    hf_token: str | None = None,
    exclusive: bool = False,
) -> list[SpeakerTurn]:
    """pyannote speaker-diarization-3.1. Requires HF_TOKEN and accepted model terms."""
    import os

    token = hf_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        raise RuntimeError(
            "pyannote diarization requires HF_TOKEN. "
            "Accept terms at https://huggingface.co/pyannote/speaker-diarization-3.1"
        )

    try:
        import torch
        from pyannote.audio import Pipeline
    except ImportError as exc:
        raise RuntimeError(
            "pyannote.audio is not installed. Run: pixi run install-diarize"
        ) from exc

    from .models import PYANNOTE_DIARIZE_MODEL, _load_pyannote_pipeline

    pipeline = _load_pyannote_pipeline(PYANNOTE_DIARIZE_MODEL, token)
    torch_device = torch.device(device if device.startswith("cuda") and torch.cuda.is_available() else "cpu")
    pipeline.to(torch_device)
    output = pipeline(str(audio_path))
    annotation = _pyannote_annotation(output, exclusive=exclusive)

    label_map: dict[str, str] = {}
    turns: list[SpeakerTurn] = []
    for segment, _, label in annotation.itertracks(yield_label=True):
        turns.append(
            SpeakerTurn(
                speaker=_normalize_pyannote_label(str(label), label_map),
                start=float(segment.start),
                end=float(segment.end),
            )
        )
    return sorted(turns, key=lambda turn: (turn.start, turn.end))


def diarize_vad_alternate(*args: object, **kwargs: object) -> list[SpeakerTurn]:
    """Deprecated alias for :func:`diarize_ffmpeg_alternate`."""
    return diarize_ffmpeg_alternate(*args, **kwargs)  # type: ignore[arg-type]


def diarize(
    audio_path: str | Path,
    *,
    method: DiarizeMethod = "auto",
    device: str = "cuda:0",
    pyannote_exclusive: bool = False,
) -> tuple[list[SpeakerTurn], str]:
    """Return speaker turns and the method actually used."""
    path = Path(audio_path)
    normalized = "ffmpeg-alternate" if method == "vad" else method

    if normalized == "ffmpeg-alternate":
        return diarize_ffmpeg_alternate(path), "ffmpeg-alternate"

    if normalized == "pyannote":
        label = "pyannote-exclusive" if pyannote_exclusive else "pyannote"
        return diarize_pyannote(path, device=device, exclusive=pyannote_exclusive), label

    if normalized == "funasr":
        return diarize_funasr(path, device=device), "funasr"

    try:
        turns = diarize_funasr(path, device=device)
        if turns and len({turn.speaker for turn in turns}) >= 1:
            return turns, "funasr"
    except Exception:
        pass

    return diarize_ffmpeg_alternate(path), "ffmpeg-alternate-fallback"
