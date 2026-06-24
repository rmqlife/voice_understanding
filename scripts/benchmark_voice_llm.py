#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.audio import ffprobe_duration, max_timestamp_seconds  # noqa: E402
from sense_voice.llm import (  # noqa: E402
    assess_prompt,
    build_llm_input,
    chunk_text,
    generate_by_chunk,
    ollama_generate,
    polish_prompt,
    resolve_llm_timeline_mode,
    stop_ollama_models,
    translate_prompt,
)
from sense_voice.segments import (  # noqa: E402
    format_timeline,
    parse_asr_segments,
    segment_duration_stats,
)

DEFAULT_CLIP = ROOT / "test_voice_clips" / "sunflower.mp3"
DEFAULT_CLIPS = ROOT / "test_voice_clips"
DEFAULT_REPORT = ROOT / "reports" / "benchmark" / "voice_llm_benchmark.md"
DEFAULT_MODEL = "qwen3:1.7b"


def run_asr(
    audio: Path,
    language: str,
    *,
    backend: str,
    device: str | None,
    model: str | None,
) -> tuple[str, str, float | None, float, str, dict[str, object]]:
    cmd = [
        "pixi",
        "run",
        "python",
        "scripts/sv.py",
        str(audio),
        "--quiet",
        "-l",
        language,
        "--backend",
        backend,
        "--output-format",
        "json",
    ]
    if device:
        cmd.extend(["--device", device])
    if model:
        cmd.extend(["--model", model])
    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        raise RuntimeError(f"ASR failed for {audio.name}:\n{proc.stderr}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return proc.stdout.strip(), proc.stdout.strip(), None, elapsed, proc.stderr.strip(), {}
    return (
        str(payload.get("text", "")).strip(),
        str(payload.get("raw", "")).strip(),
        payload.get("audio_seconds"),
        elapsed,
        proc.stderr.strip(),
        payload,
    )


def md_code(text: str) -> str:
    return "```text\n" + text.strip() + "\n```"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--clips",
        type=Path,
        default=None,
        help="Directory of audio files (default: test_voice_clips/)",
    )
    parser.add_argument(
        "--clip",
        type=Path,
        default=DEFAULT_CLIP,
        help="Single benchmark audio file (used when --clips is not set)",
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Default Ollama model for all LLM steps")
    parser.add_argument("--polish-model", default=None, help="Ollama model for transcript polishing")
    parser.add_argument("--translate-model", default=None, help="Ollama model for English translation")
    parser.add_argument("--assess-model", default=None, help="Ollama model for quality assessment")
    parser.add_argument(
        "--profile",
        choices=["finance", "vr", "generic", "subtitle"],
        default="finance",
        help="Prompt profile for transcript cleanup",
    )
    parser.add_argument("--language", default="zh", help="ASR language (default: zh)")
    parser.add_argument(
        "--asr-backend",
        choices=["cpp", "official"],
        default="cpp",
        help="ASR backend for `pixi run sv`",
    )
    parser.add_argument(
        "--asr-device",
        default=None,
        help="Official backend device, e.g. cuda:0",
    )
    parser.add_argument(
        "--asr-model",
        default=None,
        help="ASR model path/name override",
    )
    parser.add_argument("--chunk-chars", type=int, default=900, help="Max transcript chars per LLM call")
    parser.add_argument(
        "--skip-translate",
        action="store_true",
        help="Skip English translation (VR ja->zh polish only)",
    )
    parser.add_argument(
        "--skip-assess",
        action="store_true",
        help="Skip model self-assessment",
    )
    parser.add_argument(
        "--llm-timeline",
        choices=["full", "compact"],
        default=None,
        help="Timeline format sent to polish LLM; default compact for vr profile",
    )
    parser.add_argument(
        "--srt-dir",
        type=Path,
        default=None,
        help="Optional directory for Chinese SRT files generated from polished timelines",
    )
    args = parser.parse_args()
    polish_model = args.polish_model or args.model
    translate_model = args.translate_model or args.model
    assess_model = args.assess_model or args.model
    llm_timeline_mode = resolve_llm_timeline_mode(args.profile, args.llm_timeline)

    audio_files = sorted(
        p for p in args.clips.iterdir() if p.suffix.lower() in {".mp3", ".aac", ".wav", ".m4a", ".flac"}
    ) if args.clips else [args.clip]
    if not audio_files:
        raise SystemExit(f"No audio files found in {args.clips or args.clip.parent}")
    if not args.clips and not args.clip.is_file():
        raise SystemExit(f"Benchmark clip not found: {args.clip}")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    for audio in audio_files:
        print(f"Processing {audio.name}", flush=True)
        stop_ollama_models([polish_model, translate_model, assess_model])
        asr_text, raw, result_audio_seconds, asr_seconds, stderr, asr_payload = run_asr(
            audio,
            args.language,
            backend=args.asr_backend,
            device=args.asr_device,
            model=args.asr_model,
        )
        audio_seconds = (
            float(result_audio_seconds)
            if result_audio_seconds is not None
            else max_timestamp_seconds(raw) or ffprobe_duration(audio)
        )
        segments = parse_asr_segments(raw, asr_text, audio_seconds, asr_payload=asr_payload)
        duration_stats = segment_duration_stats(segments)
        timeline = format_timeline(segments)
        llm_input = build_llm_input(
            segments,
            timeline,
            llm_timeline=llm_timeline_mode,
            drop_language_artifacts=args.profile == "finance",
        )
        chunks = chunk_text(llm_input, args.chunk_chars)

        polished, polish_seconds = generate_by_chunk(
            polish_model,
            chunks,
            lambda chunk: polish_prompt(chunk, args.profile),
        )
        srt_path = None
        srt_entries = 0
        asr_srt_path = None
        asr_srt_entries = 0
        words = asr_payload.get("words") if isinstance(asr_payload.get("words"), list) else []
        if args.srt_dir:
            sys.path.insert(0, str(ROOT / "python"))
            from sense_voice.srt import write_srt
            from sense_voice.subtitle import build_asr_srt_entries, build_zh_srt_entries

            args.srt_dir.mkdir(parents=True, exist_ok=True)
            asr_srt_path = args.srt_dir / f"{audio.stem}.asr.srt"
            srt_path = args.srt_dir / f"{audio.stem}.zh.srt"
            asr_entries = build_asr_srt_entries(segments, words)
            write_srt(asr_srt_path, asr_entries)
            asr_srt_entries = len(asr_entries)
            zh_entries = build_zh_srt_entries(polished, segments, words)
            write_srt(srt_path, zh_entries)
            srt_entries = len(zh_entries)
        if args.skip_translate:
            english = ""
            translate_seconds = 0.0
        else:
            polished_chunks = chunk_text(polished, args.chunk_chars)
            english, translate_seconds = generate_by_chunk(
                translate_model,
                polished_chunks,
                translate_prompt,
            )
        if args.skip_assess:
            assessment = ""
            assess_seconds = 0.0
        else:
            assessment, assess_seconds = ollama_generate(
                assess_model,
                assess_prompt(
                    llm_input,
                    polished,
                    english,
                    args.profile,
                    include_english=not args.skip_translate,
                ),
            )

        rows.append(
            {
                "file": audio.name,
                "size_mb": audio.stat().st_size / 1024 / 1024,
                "audio_seconds": audio_seconds,
                "asr_seconds": asr_seconds,
                "asr_rtf": asr_seconds / audio_seconds if audio_seconds else None,
                "raw_chars": len(llm_input),
                "timeline_chars": len(timeline),
                "segments": len(segments),
                "timing_source": str(asr_payload.get("timing_source", "unknown")),
                "duration_p50": duration_stats["p50"],
                "duration_p95": duration_stats["p95"],
                "duration_max": duration_stats["max"],
                "duration_over_10s": duration_stats["over_10s"],
                "duration_over_30s": duration_stats["over_30s"],
                "chunks": len(chunks),
                "polished_chars": len(polished),
                "srt_path": srt_path,
                "asr_srt_path": asr_srt_path,
                "srt_entries": srt_entries,
                "asr_srt_entries": asr_srt_entries,
                "english_chars": len(english),
                "polish_seconds": polish_seconds,
                "translate_seconds": translate_seconds,
                "assess_seconds": assess_seconds,
                "stderr": stderr,
                "raw": raw,
                "timeline": timeline,
                "llm_input": llm_input,
                "polished": polished,
                "english": english,
                "assessment": assessment,
            }
        )

    total_asr = sum(float(r["asr_seconds"]) for r in rows)
    total_polish = sum(float(r["polish_seconds"]) for r in rows)
    total_translate = sum(float(r["translate_seconds"]) for r in rows)
    total_audio = sum(float(r["audio_seconds"] or 0) for r in rows)

    lines: list[str] = []
    lines.append("# Voice Clip Local LLM Benchmark")
    lines.append("")
    lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- ASR: `{args.asr_backend}` via `pixi run sv`")
    if args.asr_device:
        lines.append(f"- ASR device: `{args.asr_device}`")
    if args.asr_model:
        lines.append(f"- ASR model: `{args.asr_model}`")
    lines.append(f"- ASR language: `{args.language}`")
    lines.append(f"- Prompt profile: `{args.profile}`")
    lines.append(f"- LLM timeline format: `{llm_timeline_mode}`")
    if args.srt_dir:
        lines.append(f"- Chinese SRT output: `{args.srt_dir}`")
    lines.append(f"- Polish LLM: `{polish_model}` via Ollama local API")
    if args.skip_translate:
        lines.append("- English translation: skipped")
    else:
        lines.append(f"- Translate LLM: `{translate_model}` via Ollama local API")
    if args.skip_assess:
        lines.append("- Self-assessment: skipped")
    else:
        lines.append(f"- Assess LLM: `{assess_model}` via Ollama local API")
    lines.append(f"- LLM chunk size: {args.chunk_chars} chars")
    if args.clips:
        lines.append(f"- Source directory: `{args.clips}`")
    else:
        lines.append(f"- Benchmark clip: `{args.clip}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Files processed: {len(rows)}")
    lines.append(f"- Approx. audio duration: {total_audio:.1f}s")
    lines.append(f"- Total ASR wall time: {total_asr:.2f}s")
    lines.append(f"- Total polish wall time: {total_polish:.2f}s")
    if not args.skip_translate:
        lines.append(f"- Total English translation wall time: {total_translate:.2f}s")
    lines.append("")
    lines.append("## Benchmark Table")
    lines.append("")
    if llm_timeline_mode == "compact":
        lines.append("| File | Size MB | Audio s | ASR s | ASR RTF | Segments | LLM chars | Timeline chars | Chunks | Polish s" + ("" if args.skip_translate else " | Translate s") + " |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:" + ("" if args.skip_translate else ":---") + "|")
    elif args.skip_translate:
        lines.append("| File | Size MB | Audio s | ASR s | ASR RTF | Segments | LLM chars | Chunks | Polish s |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    else:
        lines.append("| File | Size MB | Audio s | ASR s | ASR RTF | Segments | LLM chars | Chunks | Polish s | Translate s |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        if llm_timeline_mode == "compact":
            row = "| {file} | {size_mb:.2f} | {audio_seconds:.1f} | {asr_seconds:.2f} | {asr_rtf:.3f} | {segments} | {raw_chars} | {timeline_chars} | {chunks} | {polish_seconds:.2f}".format(
                file=str(r["file"]).replace("|", "\\|"),
                size_mb=float(r["size_mb"]),
                audio_seconds=float(r["audio_seconds"] or 0),
                asr_seconds=float(r["asr_seconds"]),
                asr_rtf=float(r["asr_rtf"] or 0),
                segments=int(r["segments"]),
                raw_chars=int(r["raw_chars"]),
                timeline_chars=int(r["timeline_chars"]),
                chunks=int(r["chunks"]),
                polish_seconds=float(r["polish_seconds"]),
            )
            if not args.skip_translate:
                row += " | {translate_seconds:.2f}".format(translate_seconds=float(r["translate_seconds"]))
            lines.append(row + " |")
        elif args.skip_translate:
            lines.append(
                "| {file} | {size_mb:.2f} | {audio_seconds:.1f} | {asr_seconds:.2f} | {asr_rtf:.3f} | {segments} | {raw_chars} | {chunks} | {polish_seconds:.2f} |".format(
                    file=str(r["file"]).replace("|", "\\|"),
                    size_mb=float(r["size_mb"]),
                    audio_seconds=float(r["audio_seconds"] or 0),
                    asr_seconds=float(r["asr_seconds"]),
                    asr_rtf=float(r["asr_rtf"] or 0),
                    segments=int(r["segments"]),
                    raw_chars=int(r["raw_chars"]),
                    chunks=int(r["chunks"]),
                    polish_seconds=float(r["polish_seconds"]),
                )
            )
        else:
            lines.append(
                "| {file} | {size_mb:.2f} | {audio_seconds:.1f} | {asr_seconds:.2f} | {asr_rtf:.3f} | {segments} | {raw_chars} | {chunks} | {polish_seconds:.2f} | {translate_seconds:.2f} |".format(
                    file=str(r["file"]).replace("|", "\\|"),
                    size_mb=float(r["size_mb"]),
                    audio_seconds=float(r["audio_seconds"] or 0),
                    asr_seconds=float(r["asr_seconds"]),
                    asr_rtf=float(r["asr_rtf"] or 0),
                    segments=int(r["segments"]),
                    raw_chars=int(r["raw_chars"]),
                    chunks=int(r["chunks"]),
                    polish_seconds=float(r["polish_seconds"]),
                    translate_seconds=float(r["translate_seconds"]),
                )
            )
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    lines.append(f"- `{args.asr_backend}` ASR completed for all selected clips.")
    if args.skip_translate:
        lines.append(f"- `{polish_model}` handled ja->zh transcript cleanup only.")
    else:
        lines.append(f"- `{polish_model}` handled transcript cleanup; `{translate_model}` handled English translation.")
    if not args.skip_assess:
        lines.append(f"- `{assess_model}` handled self-assessment.")
    lines.append("- The LLM input is now a structured timeline with coarse or exact segment times plus SenseVoice tags where available.")
    lines.append("- Best current direction: keep ASR language pinned when known, process long recordings in chunks, and keep domain-specific prompt profiles separate.")
    lines.append("")

    for idx, r in enumerate(rows, start=1):
        lines.append(f"## {idx}. {r['file']}")
        lines.append("")
        lines.append("### Metrics")
        lines.append("")
        lines.append(f"- Size: {float(r['size_mb']):.2f} MB")
        lines.append(f"- Approx. audio duration: {float(r['audio_seconds'] or 0):.1f}s")
        lines.append(f"- ASR wall time: {float(r['asr_seconds']):.2f}s")
        lines.append(f"- Structured ASR segments: {int(r['segments'])}")
        lines.append(f"- ASR timing source: `{r['timing_source']}`")
        lines.append(
            f"- Segment duration p50/p95/max: {float(r['duration_p50']):.1f}s / "
            f"{float(r['duration_p95']):.1f}s / {float(r['duration_max']):.1f}s"
        )
        lines.append(
            f"- Segments >10s / >30s: {int(r['duration_over_10s'])} / {int(r['duration_over_30s'])}"
        )
        lines.append(f"- LLM input chars: {int(r['raw_chars'])}")
        if r["srt_path"]:
            lines.append(f"- Chinese SRT: `{r['srt_path']}` ({int(r['srt_entries'])} entries)")
        if llm_timeline_mode == "compact":
            lines.append(f"- Full timeline chars: {int(r['timeline_chars'])}")
        lines.append(f"- Polish wall time: {float(r['polish_seconds']):.2f}s")
        if not args.skip_translate:
            lines.append(f"- Translation wall time: {float(r['translate_seconds']):.2f}s")
        if r["stderr"]:
            warning_lines = [line for line in str(r["stderr"]).splitlines() if "Input buffer exhausted" in line or "Invalid data" in line]
            if warning_lines:
                lines.append(f"- Decode warnings: {len(warning_lines)} ffmpeg warning lines")
        lines.append("")
        lines.append("### Chinese Polished")
        lines.append("")
        lines.append(md_code(str(r["polished"])))
        lines.append("")
        if not args.skip_translate:
            lines.append("### English Translation")
            lines.append("")
            lines.append(md_code(str(r["english"])))
            lines.append("")
        if not args.skip_assess:
            lines.append("### Model Self-Assessment")
            lines.append("")
            lines.append(md_code(str(r["assessment"])))
            lines.append("")
        if llm_timeline_mode == "compact":
            lines.append("### LLM Input Timeline")
            lines.append("")
            lines.append(md_code(str(r["llm_input"])))
            lines.append("")
        lines.append("### Structured ASR Timeline")
        lines.append("")
        lines.append(md_code(str(r["timeline"])))
        lines.append("")
        lines.append("### Raw ASR Payload")
        lines.append("")
        lines.append(md_code(str(r["raw"])))
        lines.append("")

    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.report}", flush=True)


if __name__ == "__main__":
    main()
