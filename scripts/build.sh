#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/SenseVoice.cpp/build"
JOBS="$(sysctl -n hw.ncpu 2>/dev/null || echo 4)"

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

cmake -DGGML_METAL=ON -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release -j "$JOBS"

echo ""
echo "Build complete: $BUILD_DIR/bin/sense-voice-main"
