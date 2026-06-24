#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_HOST="${MAG_HOST:-rmqlife-mag}"
REMOTE_DIR="${MAG_REPO:-/home/rmqlife/work/voice_understanding}"

rsync -avz "${REMOTE_HOST}:${REMOTE_DIR}/reports/" "${ROOT}/reports/"

echo "Synced reports from ${REMOTE_HOST}:${REMOTE_DIR}/reports/ -> ${ROOT}/reports/"
