"""Run ASR through the `sv.py` CLI in a subprocess.

Keeping ASR in a separate process isolates the heavy FunASR import from the
benchmark/test harnesses and lets them reuse the exact same CLI path users run.
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SV_SCRIPT = REPO_ROOT / "scripts" / "sv.py"


def run_asr(
    audio: Path,
    language: str,
    *,
    backend: str,
    device: str | None = None,
    model: str | None = None,
    chunk_seconds: float | None = None,
    repo_root: Path = REPO_ROOT,
    sv_script: Path = SV_SCRIPT,
) -> tuple[str, str, float | None, float, str, dict[str, object]]:
    """Return (text, raw, audio_seconds, wall_seconds, stderr, json_payload)."""
    audio = Path(audio).expanduser().resolve()
    cmd = [
        "pixi",
        "run",
        "python",
        str(sv_script),
        str(audio),
        "--quiet",
        "-l",
        language,
        "--backend",
        backend,
        "--output-format",
        "json",
    ]
    if device:
        cmd.extend(["--device", device])
    if model:
        cmd.extend(["--model", model])
    if chunk_seconds is not None:
        cmd.extend(["--chunk-seconds", str(chunk_seconds)])

    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        raise RuntimeError(f"ASR failed for {audio.name}:\n{proc.stderr}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.stdout.strip(), proc.stdout.strip(), None, elapsed, proc.stderr.strip(), {}
    return (
        str(payload.get("text", "")).strip(),
        str(payload.get("raw", "")).strip(),
        payload.get("audio_seconds"),
        elapsed,
        proc.stderr.strip(),
        payload,
    )
