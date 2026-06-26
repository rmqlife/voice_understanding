#!/usr/bin/env bash
# Repolish all .asr.srt → .zh.srt and publish to /mnt/fnos/jav/#finished
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
LOG="results/subtitle/logs/repolish_v2_20250625.log"
rm -f data/.subtitle_gpu.lock
echo "batch start $(date -Is)" >> "$LOG"
exec pixi run vr-subtitle-test -- \
  --repolish-only --repolish-asr --name-filter "" \
  --chunk-segments 80 --continue-on-error --publish \
  >> "$LOG" 2>&1
