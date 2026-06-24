#!/usr/bin/env python3
"""Compare funasr vs pyannote diarization on sample clips."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.audio import ffprobe_duration  # noqa: E402
from sense_voice.diarize import diarize_funasr, diarize_pyannote  # noqa: E402
from sense_voice.transcript import sort_turns  # noqa: E402


def summarize_turns(turns: list) -> dict[str, object]:
    ordered = sort_turns(turns)
    return {
        "speaker_count": len({turn.speaker for turn in ordered}),
        "turn_count": len(ordered),
        "turns": [
            {
                "speaker": turn.speaker,
                "start": round(turn.start, 2),
                "end": round(turn.end, 2),
                "duration": round(turn.end - turn.start, 2),
            }
            for turn in ordered
        ],
    }


def render_report(rows: list[dict[str, object]], *, run_label: str) -> str:
    lines = [
        "# Diarization Compare",
        "",
        f"- Run: `{run_label}`",
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "| Clip | Audio s | funasr turns | funasr spk | pyannote turns | pyannote spk |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {clip} | {audio:.1f} | {ft} | {fs} | {pt} | {ps} |".format(
                clip=str(row["clip"]).replace("|", "\\|"),
                audio=float(row["audio_seconds"] or 0),
                ft=int(row["funasr_turns"]),
                fs=int(row["funasr_speakers"]),
                pt=row.get("pyannote_turns", "—"),
                ps=row.get("pyannote_speakers", "—"),
            )
        )
    lines.append("")
    for row in rows:
        lines.extend([f"## {row['clip']}", ""])
        lines.append("### funasr")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(row["funasr"], ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")
        if row.get("pyannote"):
            lines.append("### pyannote")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(row["pyannote"], ensure_ascii=False, indent=2))
            lines.append("```")
            lines.append("")
        if row.get("pyannote_error"):
            lines.append(f"### pyannote error\n\n`{row['pyannote_error']}`\n")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare funasr and pyannote diarization")
    parser.add_argument("--clip", type=Path, action="append", default=[])
    parser.add_argument("--clips", type=Path, default=None)
    parser.add_argument("--name-filter", default="")
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--report", type=Path, default=ROOT / "reports" / "transcript" / "diarize_compare.md")
    parser.add_argument("--run-label", default="diarize_compare")
    parser.add_argument("--skip-pyannote", action="store_true")
    args = parser.parse_args()

    if args.clips:
        files = sorted(
            path
            for path in args.clips.iterdir()
            if path.suffix.lower() in {".wav", ".mp3", ".m4a", ".flac", ".aac"}
        )
        if args.name_filter:
            files = [path for path in files if args.name_filter.lower() in path.name.lower()]
    else:
        files = list(args.clip)
    if not files:
        raise SystemExit("No clips found")

    rows: list[dict[str, object]] = []
    for audio in files:
        if not audio.is_file():
            raise SystemExit(f"Clip not found: {audio}")
        print(f"Comparing {audio.name}", flush=True)
        funasr_turns = diarize_funasr(audio, device=args.device)
        funasr_summary = summarize_turns(funasr_turns)
        row: dict[str, object] = {
            "clip": audio.name,
            "audio_seconds": ffprobe_duration(audio),
            "funasr": funasr_summary,
            "funasr_turns": funasr_summary["turn_count"],
            "funasr_speakers": funasr_summary["speaker_count"],
        }
        if not args.skip_pyannote:
            try:
                pyannote_turns = diarize_pyannote(audio, device=args.device)
                pyannote_summary = summarize_turns(pyannote_turns)
                row["pyannote"] = pyannote_summary
                row["pyannote_turns"] = pyannote_summary["turn_count"]
                row["pyannote_speakers"] = pyannote_summary["speaker_count"]
            except Exception as exc:
                row["pyannote_error"] = str(exc)
        rows.append(row)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(rows, run_label=args.run_label), encoding="utf-8")
    json_path = args.report.with_suffix(".json")
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.report}", flush=True)
    print(f"Wrote {json_path}", flush=True)


if __name__ == "__main__":
    main()
