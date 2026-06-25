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
