"""ARCHIVED pyannote diarization (snapshot for reference, not imported).

Experiment conclusion (2026-06-24): pyannote/speaker-diarization-3.1 performed on
par with the FunASR cam++ path for our clips and is not the main route. Code kept
here for reproducibility only. To revive, copy these functions back into
`python/sense_voice/diarize.py`, restore `PYANNOTE_DIARIZE_MODEL` /
`_load_pyannote_pipeline` in `models.py`, and `pip install pyannote.audio` with a
valid `HF_TOKEN`.
"""

from __future__ import annotations

from pathlib import Path

from sense_voice.diarize import SpeakerTurn


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
        from pyannote.audio import Pipeline  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "pyannote.audio is not installed. Install manually: pip install pyannote.audio"
        ) from exc

    PYANNOTE_DIARIZE_MODEL = "pyannote/speaker-diarization-3.1"

    def _load_pyannote_pipeline(model_id: str, tok: str):
        from pyannote.audio import Pipeline

        try:
            return Pipeline.from_pretrained(model_id, token=tok)
        except TypeError:
            return Pipeline.from_pretrained(model_id, use_auth_token=tok)

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
