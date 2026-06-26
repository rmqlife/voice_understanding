#!/usr/bin/env bash
# Pull results/ (and optional data/vr cache) from rmqlife-mag.
set -euo pipefail
MAG_HOST="${MAG_HOST:-rmqlife-mag}"
MAG_REPO="${MAG_REPO:-/home/rmqlife/work/voice_understanding}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
rsync -avz "${MAG_HOST}:${MAG_REPO}/results/" "${ROOT}/results/"
if [[ "${SYNC_MAG_WAV:-}" == "1" ]]; then
  rsync -avz "${MAG_HOST}:${MAG_REPO}/data/vr/" "${ROOT}/data/vr/"
fi
echo "Synced results/ from ${MAG_HOST}"
