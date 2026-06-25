"""ARCHIVED pyannote model cache helpers (snapshot for reference, not imported).

See archive/pyannote/diarize_pyannote.py for context. Restore these into
`python/sense_voice/models.py` to revive the pyannote path.
"""

from __future__ import annotations

import os

PYANNOTE_DIARIZE_MODEL = "pyannote/speaker-diarization-3.1"


def _load_pyannote_pipeline(model_id: str, token: str):
    from pyannote.audio import Pipeline

    try:
        return Pipeline.from_pretrained(model_id, token=token)
    except TypeError:
        return Pipeline.from_pretrained(model_id, use_auth_token=token)


def warm_pyannote(*, hf_token: str | None = None) -> None:
    token = hf_token or os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        raise RuntimeError("HF_TOKEN is required to download pyannote models")

    _load_pyannote_pipeline(PYANNOTE_DIARIZE_MODEL, token)
