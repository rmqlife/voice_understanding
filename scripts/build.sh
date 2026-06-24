#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/SenseVoice.cpp/build"
JOBS="$(sysctl -n hw.ncpu 2>/dev/null || nproc 2>/dev/null || echo 4)"
SYSTEM="$(uname -s)"

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

if [[ "$SYSTEM" == "Darwin" ]]; then
  cmake -DGGML_METAL=ON -DCMAKE_BUILD_TYPE=Release ..
elif command -v nvidia-smi >/dev/null 2>&1; then
  cmake -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release ..
else
  cmake -DCMAKE_BUILD_TYPE=Release ..
fi
cmake --build . --config Release -j "$JOBS"

echo ""
echo "Build complete: $BUILD_DIR/bin/sense-voice-main"
