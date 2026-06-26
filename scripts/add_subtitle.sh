#!/usr/bin/env bash
# VR subtitle pipeline: NFS mp4 → data/vr WAV → results/srt → copy SRT beside mp4.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
exec pixi run add-subtitle -- "$@"
