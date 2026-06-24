#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CPP_ROOT="${SENSE_VOICE_CPP_ROOT:-$ROOT/reference/SenseVoice.cpp}"
BUILD_DIR="$CPP_ROOT/build"
JOBS="$(sysctl -n hw.ncpu 2>/dev/null || nproc 2>/dev/null || echo 4)"
SYSTEM="$(uname -s)"

if [[ ! -d "$CPP_ROOT" ]]; then
  echo "SenseVoice.cpp not found at: $CPP_ROOT" >&2
  echo "Mac with vendored copy: git checkout mac" >&2
  echo "Or clone for optional local build:" >&2
  echo "  git clone https://github.com/lovemefan/SenseVoice.cpp \"$CPP_ROOT\"" >&2
  exit 1
fi

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
