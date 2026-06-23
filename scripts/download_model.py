#!/usr/bin/env python3
"""Download SenseVoice GGUF model and sample audio from Hugging Face."""

from pathlib import Path

from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"
REPO_ID = "lovemefan/sense-voice-gguf"

FILES = [
    "sense-voice-small-fp16.gguf",
    "asr_example_zh.wav",
]


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    for filename in FILES:
        dest = MODELS_DIR / filename
        if dest.exists():
            print(f"Already exists: {dest}")
            continue

        print(f"Downloading {filename} ...")
        path = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            local_dir=str(MODELS_DIR),
        )
        print(f"Saved to {path}")

    print(f"\nModels ready in {MODELS_DIR}")


if __name__ == "__main__":
    main()
