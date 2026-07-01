"""Serialize subtitle GPU use: Ollama LLM vs FunASR on a single CUDA device."""

from __future__ import annotations

import fcntl
import os
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .llm import stop_all_ollama_models

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_LOCK_PATH = REPO_ROOT / "data" / ".subtitle_gpu.lock"

# FunASR official + VAD needs headroom; 27B Ollama needs ~20 GiB loaded plus graph headroom.
ASR_MIN_FREE_MIB = 6_000
OLLAMA_MIN_FREE_MIB = 20_000
OLLAMA_SETTLE_SEC = 3.0
GPU_WAIT_TIMEOUT_SEC = 180.0
GPU_POLL_INTERVAL_SEC = 2.0


def uses_cuda(device: str | None) -> bool:
    if not device:
        return False
    lowered = device.lower()
    return lowered != "cpu" and "cuda" in lowered


def nvidia_free_mib(device_index: int = 0) -> int | None:
    proc = subprocess.run(
        [
            "nvidia-smi",
            f"--id={device_index}",
            "--query-gpu=memory.free",
            "--format=csv,noheader,nounits",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    line = proc.stdout.strip().splitlines()
    if not line:
        return None
    try:
        return int(line[0].strip())
    except ValueError:
        return None


def wait_for_gpu_free(
    *,
    min_free_mib: int,
    timeout_sec: float = GPU_WAIT_TIMEOUT_SEC,
    poll_sec: float = GPU_POLL_INTERVAL_SEC,
    label: str = "GPU",
) -> None:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        free_mib = nvidia_free_mib()
        if free_mib is not None and free_mib >= min_free_mib:
            return
        time.sleep(poll_sec)
    free_mib = nvidia_free_mib()
    raise RuntimeError(
        f"{label}: timed out waiting for >= {min_free_mib} MiB free VRAM "
        f"(last reading: {free_mib} MiB)"
    )


def prepare_gpu_for_asr(*, device: str | None, polish_model: str | None) -> None:
    """Release Ollama and wait before loading FunASR on CUDA."""
    if not uses_cuda(device):
        return
    print("gpu: stop Ollama before ASR", flush=True)
    extras = [polish_model] if polish_model else []
    stop_all_ollama_models(extras)
    wait_for_gpu_free(min_free_mib=ASR_MIN_FREE_MIB, label="ASR")


def prepare_gpu_for_ollama(*, device: str | None) -> None:
    """Wait for ASR subprocess VRAM to drop before loading Ollama."""
    if not uses_cuda(device):
        return
    print("gpu: wait for VRAM after ASR", flush=True)
    wait_for_gpu_free(min_free_mib=OLLAMA_MIN_FREE_MIB, label="Ollama")
    if OLLAMA_SETTLE_SEC > 0:
        time.sleep(OLLAMA_SETTLE_SEC)


def release_gpu_after_polish(polish_model: str | None) -> None:
    """Unload Ollama so the next clip's ASR can use CUDA."""
    if not polish_model:
        return
    print(f"gpu: stop Ollama after polish ({polish_model})", flush=True)
    stop_all_ollama_models([polish_model])
    wait_for_gpu_free(min_free_mib=ASR_MIN_FREE_MIB, label="post-polish")


def _lock_holder_alive(path: Path) -> bool:
    try:
        pid_text = path.read_text(encoding="utf-8").strip()
        pid = int(pid_text)
    except (OSError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


@contextmanager
def subtitle_pipeline_lock(
    path: Path = DEFAULT_LOCK_PATH,
    *,
    blocking: bool = True,
) -> Iterator[None]:
    """Only one subtitle pipeline (batch or manual) may use GPU at a time."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not _lock_holder_alive(path):
        path.unlink(missing_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        flags = fcntl.LOCK_EX
        if not blocking:
            flags |= fcntl.LOCK_NB
        try:
            fcntl.flock(handle.fileno(), flags)
        except BlockingIOError as exc:
            raise RuntimeError(
                f"Another subtitle pipeline holds the GPU lock ({path}). "
                "Stop the other add-subtitle / subtitle-pipeline process first."
            ) from exc
        handle.write(f"{os.getpid()}\n")
        handle.flush()
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
