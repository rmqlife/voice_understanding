#!/usr/bin/env python3
"""VR subtitle test: ASR metrics + ASR-timeline SRT + LLM Chinese SRT."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))

import benchmark_voice_llm as bvl  # noqa: E402
from sense_voice.audio import ffprobe_duration, max_timestamp_seconds  # noqa: E402
from sense_voice.llm import build_llm_input, chunk_text, generate_by_chunk, polish_prompt, stop_ollama_models  # noqa: E402
from sense_voice.segments import format_timeline, parse_asr_segments, segment_duration_stats  # noqa: E402
from sense_voice.srt import write_srt  # noqa: E402
from sense_voice.subtitle import build_asr_srt_entries, build_zh_srt_entries  # noqa: E402


DEFAULT_SRT_DIR = ROOT / "reports" / "srt"
DEFAULT_REPORT = ROOT / "reports" / "vr_subtitle_test_metrics.md"


def render_metrics_report(rows: list[dict[str, object]], *, run_label: str) -> str:
    lines = [
        "# VR Subtitle Test Metrics",
        "",
        f"- Run: `{run_label}`",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Summary",
        "",
        "| Clip | Audio s | ASR s | ASR RTF | Segments | Refined | Timing | p50 | p95 | max | >10s | >30s | LLM s | ASR SRT | ZH SRT | ASR entries | ZH entries |",
        "|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {clip} | {audio:.1f} | {asr:.2f} | {rtf:.3f} | {segments} | {refined} | {timing} | "
            "{p50:.1f} | {p95:.1f} | {max:.1f} | {over10} | {over30} | {llm:.2f} | "
            "`{asr_srt}` | `{zh_srt}` | {asr_entries} | {zh_entries} |".format(
                clip=str(row["clip"]).replace("|", "\\|"),
                audio=float(row["audio_seconds"] or 0),
                asr=float(row["asr_seconds"]),
                rtf=float(row["asr_rtf"] or 0),
                segments=int(row["raw_segments"]),
                refined=int(row["segments"]),
                timing=str(row["timing_source"]),
                p50=float(row["duration_p50"]),
                p95=float(row["duration_p95"]),
                max=float(row["duration_max"]),
                over10=int(row["duration_over_10s"]),
                over30=int(row["duration_over_30s"]),
                llm=float(row["polish_seconds"]),
                asr_srt=row["asr_srt_rel"],
                zh_srt=row["zh_srt_rel"],
                asr_entries=int(row["asr_srt_entries"]),
                zh_entries=int(row["zh_srt_entries"]),
            )
        )
    lines.append("")
    for row in rows:
        lines.extend(
            [
                f"## {row['clip']}",
                "",
                f"- Raw ASR segments: {int(row['raw_segments'])}",
                f"- Refined segments: {int(row['segments'])}",
                f"- ASR SRT: `{row['asr_srt_rel']}` ({int(row['asr_srt_entries'])} entries)",
                f"- Chinese SRT: `{row['zh_srt_rel']}` ({int(row['zh_srt_entries'])} entries)",
                f"- Timing confidence mix: {row['timing_confidence']}",
                f"- LLM chunks: {int(row['chunks'])}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def process_clip(
    audio: Path,
    *,
    language: str,
    asr_backend: str,
    asr_device: str | None,
    asr_model: str | None,
    polish_model: str,
    chunk_chars: int,
    llm_timeline: str,
    profile: str,
    srt_dir: Path,
    skip_polish: bool,
) -> dict[str, object]:
    stop_ollama_models([polish_model])
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
        else max_timestamp_seconds(raw) or ffprobe_duration(audio)
    )
    segments = parse_asr_segments(raw, asr_text, audio_seconds, asr_payload=asr_payload)
    raw_segments = len(segments)
    words = asr_payload.get("words") if isinstance(asr_payload.get("words"), list) else []
    duration_stats = segment_duration_stats(segments)
    timeline = format_timeline(segments)
    llm_input = build_llm_input(
        segments,
        timeline,
        llm_timeline=llm_timeline,
        drop_language_artifacts=False,
    )
    chunks = chunk_text(llm_input, chunk_chars)

    stem = audio.stem
    asr_srt_path = srt_dir / f"{stem}.asr.srt"
    zh_srt_path = srt_dir / f"{stem}.zh.srt"
    asr_entries = build_asr_srt_entries(segments, words)
    write_srt(asr_srt_path, asr_entries)

    polish_seconds = 0.0
    polished = ""
    if skip_polish:
        zh_entries = asr_entries
        write_srt(zh_srt_path, zh_entries)
    else:
        polished, polish_seconds = generate_by_chunk(
            polish_model,
            chunks,
            lambda chunk: polish_prompt(chunk, profile),
        )
        zh_entries = build_zh_srt_entries(polished, segments, words)
        write_srt(zh_srt_path, zh_entries)

    confidence_counts: dict[str, int] = {}
    for segment in segments:
        key = str(segment.get("timing_confidence") or "unknown")
        confidence_counts[key] = confidence_counts.get(key, 0) + 1

    return {
        "clip": audio.name,
        "audio_seconds": audio_seconds,
        "asr_seconds": asr_seconds,
        "asr_rtf": asr_seconds / audio_seconds if audio_seconds else None,
        "raw_segments": raw_segments,
        "segments": len(segments),
        "timing_source": str(asr_payload.get("timing_source", "unknown")),
        "duration_p50": duration_stats["p50"],
        "duration_p95": duration_stats["p95"],
        "duration_max": duration_stats["max"],
        "duration_over_10s": duration_stats["over_10s"],
        "duration_over_30s": duration_stats["over_30s"],
        "polish_seconds": polish_seconds,
        "chunks": len(chunks),
        "asr_srt_rel": asr_srt_path.relative_to(ROOT).as_posix(),
        "zh_srt_rel": zh_srt_path.relative_to(ROOT).as_posix(),
        "asr_srt_entries": len(asr_entries),
        "zh_srt_entries": len(zh_entries),
        "timing_confidence": ", ".join(f"{k}={v}" for k, v in sorted(confidence_counts.items())),
        "stderr": stderr,
        "polished_preview": polished[:2000],
    }


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
    if args.clip:
        return list(args.clip)
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="VR subtitle test with ASR/ZH SRT and metrics report")
    parser.add_argument("--clip", type=Path, action="append", default=[], help="Audio clip (repeatable)")
    parser.add_argument("--clips", type=Path, default=None, help="Directory of audio clips")
    parser.add_argument(
        "--name-filter",
        default="kavr",
        help="When using --clips, only process files whose name contains this substring",
    )
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--srt-dir", type=Path, default=DEFAULT_SRT_DIR)
    parser.add_argument("--run-label", default="vr_subtitle_test")
    parser.add_argument("--language", default="ja")
    parser.add_argument("--profile", choices=["vr", "subtitle"], default="vr")
    parser.add_argument("--asr-backend", choices=["cpp", "official"], default="official")
    parser.add_argument("--asr-device", default=None)
    parser.add_argument("--asr-model", default=None)
    parser.add_argument("--polish-model", default="nsfw-local:27b")
    parser.add_argument("--chunk-chars", type=int, default=3000)
    parser.add_argument("--llm-timeline", choices=["full", "compact"], default="compact")
    parser.add_argument("--skip-polish", action="store_true", help="Skip LLM; duplicate ASR SRT as .zh.srt")
    args = parser.parse_args()

    audio_files = collect_clips(args)
    if not audio_files and args.clip:
        audio_files = list(args.clip)
    if not audio_files:
        raise SystemExit("No audio clips found. Use --clip and/or --clips.")

    args.srt_dir.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)

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
                polish_model=args.polish_model,
                chunk_chars=args.chunk_chars,
                llm_timeline=args.llm_timeline,
                profile=args.profile,
                srt_dir=args.srt_dir,
                skip_polish=args.skip_polish,
            )
        )

    report_text = render_metrics_report(rows, run_label=args.run_label)
    args.report.write_text(report_text, encoding="utf-8")
    json_path = args.report.with_suffix(".json")
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.report}", flush=True)
    print(f"Wrote {json_path}", flush=True)


if __name__ == "__main__":
    main()
