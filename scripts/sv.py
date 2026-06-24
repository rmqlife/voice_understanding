#!/usr/bin/env python3
"""Transcribe audio (wav/mp3/...) to text."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from sense_voice import SenseVoice

WAV_EXTS = {".wav", ".wave"}
AUDIO_EXTS = {".wav", ".wave", ".mp3", ".m4a", ".flac", ".aac", ".ogg"}


def to_wav(src: Path) -> tuple[Path, bool]:
    """Return a 16kHz mono WAV path. Second value is whether caller should delete it."""
    if src.suffix.lower() in WAV_EXTS:
        return src, False

    tmp = Path(tempfile.mktemp(suffix=".wav"))
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(tmp),
        ],
        check=True,
    )
    return tmp, True


def collect_inputs(args: argparse.Namespace) -> list[Path]:
    if args.clips:
        files = sorted(
            path
            for path in args.clips.iterdir()
            if path.suffix.lower() in AUDIO_EXTS
        )
        if args.name_filter:
            files = [path for path in files if args.name_filter.lower() in path.name.lower()]
        return files
    return [Path(path) for path in args.audio]


def transcribe_one(
    src: Path,
    *,
    sv: SenseVoice,
    args: argparse.Namespace,
    index: int,
    total: int,
) -> None:
    if not src.is_file():
        print(f"[{index}/{total}] missing: {src}", file=sys.stderr)
        return

    print(f"[{index}/{total}] {src.name}", file=sys.stderr, flush=True)
    wav, cleanup = to_wav(src)
    try:
        result = sv.transcribe(
            wav,
            raw=True,
            with_timestamps=not args.no_timestamps,
        )
        if args.output_format == "json":
            payload = result.to_json_dict()
            payload["source"] = src.name
            print(json.dumps(payload, ensure_ascii=False), flush=True)
        else:
            print(f"### {src.name}", flush=True)
            print(result.text, flush=True)
            if index < total:
                print(flush=True)
        if not args.quiet:
            print(
                f"  audio {result.audio_seconds:.1f}s | "
                f"process {result.process_seconds:.1f}s | "
                f"rtf {result.rtf:.3f}",
                file=sys.stderr,
                flush=True,
            )
    finally:
        if cleanup:
            wav.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sv",
        description="Transcribe audio to text (wav, mp3, m4a, flac, ...)",
    )
    parser.add_argument(
        "audio",
        nargs="*",
        help="Input audio file(s). Omit when using --clips.",
    )
    parser.add_argument(
        "--clips",
        type=Path,
        default=None,
        help="Directory of audio files to transcribe in batch",
    )
    parser.add_argument(
        "--name-filter",
        default="",
        help="When using --clips, only process filenames containing this substring",
    )
    parser.add_argument(
        "--backend",
        choices=["cpp", "official"],
        default=None,
        help="ASR backend: cpp for SenseVoice.cpp, official for FunASR",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Official backend device, e.g. cuda:0 or cpu",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model path/name. Defaults to GGUF for cpp and iic/SenseVoiceSmall for official.",
    )
    parser.add_argument("-l", "--language", default="zh", help="Language (auto/zh/en/...)")
    parser.add_argument("-t", "--threads", type=int, default=4, help="CPU threads")
    parser.add_argument("--cpu", action="store_true", help="Disable Metal GPU")
    parser.add_argument(
        "--no-punct",
        action="store_true",
        help="Disable punctuation (ITN)",
    )
    parser.add_argument(
        "--no-timestamps",
        action="store_true",
        help="Hide VAD segment timestamps",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide timing summary",
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output plain text or machine-readable transcription result",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=float,
        default=None,
        help="Chunk long audio at silence boundaries (official backend). 0 disables.",
    )
    args = parser.parse_args()

    inputs = collect_inputs(args)
    if not inputs:
        print("no audio files found", file=sys.stderr)
        sys.exit(1)

    chunk_seconds = args.chunk_seconds
    if chunk_seconds is not None and chunk_seconds <= 0:
        chunk_seconds = None

    sv = SenseVoice(
        model_path=args.model,
        threads=args.threads,
        use_gpu=not args.cpu,
        language=args.language,
        use_itn=not args.no_punct,
        backend=args.backend,
        device=args.device,
        chunk_seconds=chunk_seconds,
    )

    total = len(inputs)
    for index, src in enumerate(inputs, start=1):
        transcribe_one(src, sv=sv, args=args, index=index, total=total)


if __name__ == "__main__":
    main()
