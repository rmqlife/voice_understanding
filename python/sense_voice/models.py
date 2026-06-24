"""Model cache paths and warm-up helpers."""

from __future__ import annotations

import os
from pathlib import Path

# FunASR / ModelScope ASR + diarization
SENSEVOICE_MODEL = "iic/SenseVoiceSmall"
FUNASR_DIARIZE_MODEL = (
    "iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
)
FUNASR_SPK_MODEL = "iic/speech_campplus_sv_zh-cn_16k-common"

# pyannote (optional; requires HF_TOKEN + accept model terms)
PYANNOTE_DIARIZE_MODEL = "pyannote/speaker-diarization-3.1"


def modelscope_cache_dir() -> Path:
    return Path(os.environ.get("MODELSCOPE_CACHE", Path.home() / ".cache" / "modelscope"))


def huggingface_cache_dir() -> Path:
    hf_home = os.environ.get("HF_HOME")
    if hf_home:
        return Path(hf_home)
    return Path.home() / ".cache" / "huggingface"


def warm_funasr_asr(*, device: str = "cuda:0") -> None:
    from funasr import AutoModel

    AutoModel(
        model=SENSEVOICE_MODEL,
        trust_remote_code=False,
        vad_model="fsmn-vad",
        device=device,
        disable_update=True,
    )


def warm_funasr_diarize(*, device: str = "cuda:0") -> None:
    from funasr import AutoModel

    AutoModel(
        model=FUNASR_DIARIZE_MODEL,
        vad_model="fsmn-vad",
        punc_model="ct-punc-c",
        spk_model=FUNASR_SPK_MODEL,
        device=device,
        disable_update=True,
    )


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
