#!/usr/bin/env bash
# Pull reports/ (and optional mag/vr wav cache) from rmqlife-mag.
set -euo pipefail
MAG_HOST="${MAG_HOST:-rmqlife-mag}"
MAG_REPO="${MAG_REPO:-/home/rmqlife/work/voice_understanding}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
rsync -avz "${MAG_HOST}:${MAG_REPO}/reports/" "${ROOT}/reports/"
if [[ "${SYNC_MAG_WAV:-}" == "1" ]]; then
  rsync -avz "${MAG_HOST}:${MAG_REPO}/mag/vr_audio_sync/" "${ROOT}/mag/vr_audio_sync/"
fi
echo "Synced reports/ from ${MAG_HOST}"
