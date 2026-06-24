#!/usr/bin/env python3
"""Transcript test: diarization + ASR + optional polish → md/json."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))

import benchmark_voice_llm as bvl  # noqa: E402
from sense_voice.audio import ffprobe_duration, max_timestamp_seconds  # noqa: E402
from sense_voice.diarize import diarize  # noqa: E402
from sense_voice.llm import (  # noqa: E402
    chunk_text,
    generate_by_chunk,
    ollama_generate,
    polish_prompt,
    stop_ollama_models,
)
from sense_voice.speaker_names import (  # noqa: E402
    apply_speaker_names,
    collect_speaker_samples,
    parse_speaker_names,
    speaker_name_prompt,
)
from sense_voice.segments import parse_asr_segments  # noqa: E402
from sense_voice.transcript import (  # noqa: E402
    assign_segments_to_turns,
    build_transcript_llm_input,
    drop_empty_turns,
    merge_adjacent_turns,
    parse_polished_transcript,
    sort_turns,
    write_transcript_json,
    write_transcript_md,
)

DEFAULT_OUTPUT_DIR = ROOT / "reports" / "transcript"


def collect_clips(args: argparse.Namespace) -> list[Path]:
    if args.clips:
        files = sorted(
            p
            for p in args.clips.iterdir()
            if p.suffix.lower() in {".wav", ".mp3", ".m4a", ".flac", ".aac"}
        )
        if args.name_filter:
            files = [p for p in files if args.name_filter.lower() in p.name.lower()]
        return files
    return list(args.clip)


def process_clip(
    audio: Path,
    *,
    language: str,
    asr_backend: str,
    asr_device: str | None,
    asr_model: str | None,
    diarize_method: str,
    pyannote_exclusive: bool,
    polish_model: str | None,
    polish_profile: str,
    chunk_chars: int,
    skip_polish: bool,
    name_speakers_model: str | None,
    output_dir: Path,
    output_suffix: str,
    run_label: str,
) -> dict[str, object]:
    started = time.perf_counter()
    turns, diarize_used = diarize(
        audio,
        method=diarize_method,  # type: ignore[arg-type]
        device=asr_device or "cuda:0",
        pyannote_exclusive=pyannote_exclusive,
    )
    turns = merge_adjacent_turns(turns, same_speaker=True)

    asr_text, raw, result_audio_seconds, asr_seconds, stderr, asr_payload = bvl.run_asr(
        audio,
        language,
        backend=asr_backend,
        device=asr_device,
        model=asr_model,
    )
    audio_seconds = (
        float(result_audio_seconds)
        if result_audio_seconds is not None
        else max_timestamp_seconds(raw) or ffprobe_duration(audio) or 0.0
    )
    segments = parse_asr_segments(raw, asr_text, audio_seconds, asr_payload=asr_payload)
    turns = assign_segments_to_turns(turns, segments)
    turns = merge_adjacent_turns(turns, same_speaker=True, gap_s=1.5)
    turns = drop_empty_turns(sort_turns(turns))

    polish_seconds = 0.0
    if skip_polish or not polish_model:
        final_turns = turns
    else:
        stop_ollama_models([polish_model])
        llm_input = build_transcript_llm_input(turns)
        chunks = chunk_text(llm_input, chunk_chars)
        polished, polish_seconds = generate_by_chunk(
            polish_model,
            chunks,
            lambda chunk: polish_prompt(chunk, polish_profile),
        )
        final_turns = parse_polished_transcript(polished, turns)

    name_seconds = 0.0
    if name_speakers_model and final_turns:
        stop_ollama_models([name_speakers_model])
        samples = collect_speaker_samples(final_turns)
        if samples:
            named, name_seconds = ollama_generate(
                name_speakers_model,
                speaker_name_prompt(samples),
            )
            final_turns = apply_speaker_names(final_turns, parse_speaker_names(named))

    stem = audio.stem
    suffix = f"_{output_suffix}" if output_suffix else ""
    md_path = output_dir / f"{stem}{suffix}.md"
    json_path = output_dir / f"{stem}{suffix}.json"
    metadata = {
        "clip": audio.name,
        "run_label": run_label,
        "audio_seconds": audio_seconds,
        "asr_seconds": asr_seconds,
        "diarize_method": diarize_used,
        "asr_backend": asr_backend,
        "timing_source": str(asr_payload.get("timing_source", "unknown")),
        "speaker_count": len({turn.speaker for turn in final_turns}),
        "turn_count": len(final_turns),
        "polish_seconds": polish_seconds,
        "name_speakers_seconds": name_seconds,
        "wall_seconds": time.perf_counter() - started,
    }
    write_transcript_md(final_turns, md_path, title=audio.name)
    write_transcript_json(final_turns, json_path, metadata=metadata)

    return {
        "clip": audio.name,
        "audio_seconds": audio_seconds,
        "asr_seconds": asr_seconds,
        "diarize_method": diarize_used,
        "speaker_count": metadata["speaker_count"],
        "turn_count": metadata["turn_count"],
        "polish_seconds": polish_seconds,
        "md_path": md_path.relative_to(ROOT).as_posix(),
        "json_path": json_path.relative_to(ROOT).as_posix(),
        "stderr": stderr,
    }


def render_report(rows: list[dict[str, object]], *, run_label: str) -> str:
    lines = [
        "# Transcript Test",
        "",
        f"- Run: `{run_label}`",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        "| Clip | Audio s | ASR s | Diarize | Speakers | Turns | Polish s | MD | JSON |",
        "|---|---:|---:|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {clip} | {audio:.1f} | {asr:.2f} | {method} | {speakers} | {turns} | {polish:.2f} | `{md}` | `{json}` |".format(
                clip=str(row["clip"]).replace("|", "\\|"),
                audio=float(row["audio_seconds"] or 0),
                asr=float(row["asr_seconds"]),
                method=row["diarize_method"],
                speakers=int(row["speaker_count"]),
                turns=int(row["turn_count"]),
                polish=float(row["polish_seconds"]),
                md=row["md_path"],
                json=row["json_path"],
            )
        )
    lines.append("")
    for row in rows:
        lines.extend(
            [
                f"## {row['clip']}",
                "",
                f"- Diarization: `{row['diarize_method']}`",
                f"- Speakers: {int(row['speaker_count'])}",
                f"- Turns: {int(row['turn_count'])}",
                f"- Output: `{row['md_path']}`, `{row['json_path']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcript test: speaker turns + ASR + polish")
    parser.add_argument("--clip", type=Path, action="append", default=[], help="Audio clip (repeatable)")
    parser.add_argument("--clips", type=Path, default=None, help="Directory of audio clips")
    parser.add_argument("--name-filter", default="", help="Filter clip filenames")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report", type=Path, default=None, help="Optional metrics markdown report")
    parser.add_argument("--run-label", default="transcript_test")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--asr-backend", choices=["cpp", "official"], default="official")
    parser.add_argument("--asr-device", default="cuda:0")
    parser.add_argument("--asr-model", default=None)
    parser.add_argument(
        "--diarize-method",
        choices=["auto", "funasr", "pyannote", "ffmpeg-alternate", "vad"],
        default="funasr",
        help="funasr/pyannote/ffmpeg-alternate; vad is deprecated alias",
    )
    parser.add_argument("--polish-model", default="nsfw-local:27b")
    parser.add_argument(
        "--polish-profile",
        choices=["transcript", "diary", "generic"],
        default="transcript",
        help="LLM polish prompt profile (diary = light touch for voice memos)",
    )
    parser.add_argument(
        "--name-speakers",
        action="store_true",
        help="Use LLM to assign display names (业主/物业等) via --name-speakers-model",
    )
    parser.add_argument("--name-speakers-model", default=None)
    parser.add_argument(
        "--pyannote-exclusive",
        action="store_true",
        help="Use pyannote exclusive_speaker_diarization (no overlapping turns)",
    )
    parser.add_argument(
        "--output-suffix",
        default="",
        help="Append to output md/json stem to avoid overwriting (e.g. _pyannote_exclusive)",
    )
    parser.add_argument("--chunk-chars", type=int, default=6000)
    parser.add_argument("--skip-polish", action="store_true")
    args = parser.parse_args()
    name_speakers_model = None
    if args.name_speakers:
        name_speakers_model = args.name_speakers_model or args.polish_model

    audio_files = collect_clips(args)
    if not audio_files:
        raise SystemExit("No audio clips found. Use --clip and/or --clips.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for audio in audio_files:
        if not audio.is_file():
            raise SystemExit(f"Clip not found: {audio}")
        print(f"Processing {audio}", flush=True)
        rows.append(
            process_clip(
                audio,
                language=args.language,
                asr_backend=args.asr_backend,
                asr_device=args.asr_device,
                asr_model=args.asr_model,
                diarize_method=args.diarize_method,
                pyannote_exclusive=args.pyannote_exclusive,
                polish_model=None if args.skip_polish else args.polish_model,
                polish_profile=args.polish_profile,
                chunk_chars=args.chunk_chars,
                skip_polish=args.skip_polish,
                name_speakers_model=name_speakers_model,
                output_dir=args.output_dir,
                output_suffix=args.output_suffix,
                run_label=args.run_label,
            )
        )

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        report_text = render_report(rows, run_label=args.run_label)
        args.report.write_text(report_text, encoding="utf-8")
        json_report = args.report.with_suffix(".json")
        json_report.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {args.report}", flush=True)
        print(f"Wrote {json_report}", flush=True)

    for row in rows:
        print(f"Wrote {row['md_path']}", flush=True)
        print(f"Wrote {row['json_path']}", flush=True)


if __name__ == "__main__":
    main()
