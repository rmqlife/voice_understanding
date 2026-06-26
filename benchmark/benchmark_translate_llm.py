#!/usr/bin/env python3
"""Compare ja->zh subtitle translation quality across local Ollama models."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

BENCH_DIR = Path(__file__).resolve().parent
ROOT = BENCH_DIR.parent
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.llm import (  # noqa: E402
    AUDIO_EVENT_TAG_PATTERN,
    KANA_PATTERN,
    META_COMMENTARY_PATTERN,
    assess_prompt,
    generate_polished_texts_by_segment_chunks,
    needs_chinese_translation,
    ollama_generate,
    stop_ollama_models,
)
from sense_voice.srt import read_srt_file, write_srt  # noqa: E402
from sense_voice.subtitle import build_zh_srt_entries_from_texts  # noqa: E402


def analyze_texts(texts: list[str]) -> dict[str, object]:
    total = len(texts)
    empty = sum(1 for text in texts if not text.strip())
    kana_left = sum(1 for text in texts if text.strip() and KANA_PATTERN.search(text))
    untranslated = sum(1 for text in texts if text.strip() and needs_chinese_translation(text))
    bracket_tags = sum(1 for text in texts if AUDIO_EVENT_TAG_PATTERN.search(text))
    meta = sum(1 for text in texts if META_COMMENTARY_PATTERN.search(text))
    mixed = sum(
        1
        for text in texts
        if text.strip() and KANA_PATTERN.search(text) and re.search(r"[\u4e00-\u9fff]", text)
    )
    return {
        "total": total,
        "empty": empty,
        "kana_left": kana_left,
        "untranslated": untranslated,
        "bracket_tags": bracket_tags,
        "meta_commentary": meta,
        "mixed_ja_zh": mixed,
        "filled": total - empty,
    }


def sample_pairs(
    segments: list[dict[str, object]],
    texts: list[str],
    *,
    limit: int = 12,
) -> list[tuple[int, str, str]]:
    rows: list[tuple[int, str, str]] = []
    for index, (segment, text) in enumerate(zip(segments, texts, strict=False)):
        origin = str(segment.get("text", "")).strip()
        polished = text.strip()
        if not origin:
            continue
        if not polished or KANA_PATTERN.search(polished) or META_COMMENTARY_PATTERN.search(polished):
            rows.append((index + 1, origin, polished))
        if len(rows) >= limit:
            break
    return rows


def md_code(text: str) -> str:
    return "```text\n" + text.strip() + "\n```"


def run_model(
    model: str,
    segments: list[dict[str, object]],
    *,
    profile: str,
    chunk_segments: int,
) -> tuple[list[str], float, dict[str, object]]:
    stop_ollama_models([model])
    texts, seconds = generate_polished_texts_by_segment_chunks(
        model,
        segments,
        profile,
        max_segments=chunk_segments,
    )
    metrics = analyze_texts(texts)
    metrics["seconds"] = seconds
    return texts, seconds, metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare ja->zh subtitle models on an ASR SRT")
    parser.add_argument(
        "--asr-srt",
        type=Path,
        default=ROOT / "results" / "srt" / "KAVR-506-伊藤舞雪__KAVR-506-CD1.asr.srt",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=["nsfw-local:27b", "huihui_ai/qwen3.5-abliterated:27b"],
    )
    parser.add_argument("--profile", choices=["vr", "subtitle"], default="vr")
    parser.add_argument("--chunk-segments", type=int, default=80)
    parser.add_argument(
        "--report",
        type=Path,
        default=BENCH_DIR / "reports" / "translate_benchmark_kavr506_cd1.md",
    )
    parser.add_argument("--out-dir", type=Path, default=BENCH_DIR / "reports" / "translate_benchmark_kavr506_cd1")
    parser.add_argument("--assess-model", default=None, help="Optional model for comparative assessment")
    args = parser.parse_args()

    asr_srt = args.asr_srt.resolve()
    if not asr_srt.is_file():
        raise SystemExit(f"ASR SRT not found: {asr_srt}")

    entries = read_srt_file(asr_srt.read_text(encoding="utf-8"))
    segments = [
        {"start": start, "end": end, "text": text, "origin_text": text}
        for start, end, text in entries
    ]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []
    for model in args.models:
        print(f"Running {model} ...", flush=True)
        texts, seconds, metrics = run_model(
            model,
            segments,
            profile=args.profile,
            chunk_segments=args.chunk_segments,
        )
        stem = asr_srt.name[: -len(".asr.srt")]
        safe_name = re.sub(r"[^\w.\-]+", "_", model)
        zh_path = args.out_dir / f"{stem}.{safe_name}.zh.srt"
        zh_entries = build_zh_srt_entries_from_texts(texts, segments, [])
        write_srt(zh_path, zh_entries)
        results.append(
            {
                "model": model,
                "texts": texts,
                "metrics": metrics,
                "zh_path": zh_path,
            }
        )
        print(f"  done in {seconds:.1f}s -> {zh_path}", flush=True)

    assessment = ""
    if args.assess_model and len(results) == 2:
        left, right = results
        left_samples = "\n".join(
            f"- [{idx}] ASR: {origin}\n  ZH: {text or '(empty)'}"
            for idx, origin, text in sample_pairs(segments, left["texts"], limit=8)
        )
        right_samples = "\n".join(
            f"- [{idx}] ASR: {origin}\n  ZH: {text or '(empty)'}"
            for idx, origin, text in sample_pairs(segments, right["texts"], limit=8)
        )
        prompt = assess_prompt(
            f"Model A ({left['model']}):\n{left_samples}\n\nModel B ({right['model']}):\n{right_samples}",
            "",
            "",
            "vr",
            include_english=False,
        )
        assessment, _ = ollama_generate(args.assess_model, prompt.replace("请评估下面一次", "请对比下面两次"))

    lines: list[str] = []
    lines.append("# Translate Model Benchmark (ja → zh)")
    lines.append("")
    lines.append(f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- ASR SRT: `{asr_srt.relative_to(ROOT).as_posix()}`")
    lines.append(f"- Segments: {len(segments)}")
    lines.append(f"- Prompt profile: `{args.profile}`")
    lines.append(f"- Chunk size: {args.chunk_segments} segments / LLM call")
    lines.append(f"- Models: {', '.join(f'`{m}`' for m in args.models)}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        "| Model | Wall s | Filled | Empty | Kana left | Untranslated | Bracket tags | Meta commentary | Mixed ja/zh |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in results:
        m = row["metrics"]
        lines.append(
            "| {model} | {seconds:.1f} | {filled} | {empty} | {kana} | {untranslated} | {tags} | {meta} | {mixed} |".format(
                model=str(row["model"]).replace("|", "\\|"),
                seconds=float(m["seconds"]),
                filled=int(m["filled"]),
                empty=int(m["empty"]),
                kana=int(m["kana_left"]),
                untranslated=int(m["untranslated"]),
                tags=int(m["bracket_tags"]),
                meta=int(m["meta_commentary"]),
                mixed=int(m["mixed_ja_zh"]),
            )
        )
    lines.append("")
    lines.append("## Metric Notes")
    lines.append("")
    lines.append("- **Kana left**: output still contains Japanese kana (likely incomplete translation).")
    lines.append("- **Untranslated**: `needs_chinese_translation()` still true (kana-heavy or meta).")
    lines.append("- **Bracket tags**: `[停顿]` / `[不可辨语音]` etc. in output.")
    lines.append("- **Meta commentary**: ASR uncertainty notes like “可能是…误识别”.")
    lines.append("- **Mixed ja/zh**: both kana and Chinese in the same line.")
    lines.append("")

    if len(results) == 2:
        left, right = results
        left_texts = left["texts"]
        right_texts = right["texts"]
        diffs: list[tuple[int, str, str, str]] = []
        for index, (segment, l_text, r_text) in enumerate(
            zip(segments, left_texts, right_texts, strict=False), start=1
        ):
            origin = str(segment.get("text", "")).strip()
            if not origin:
                continue
            if l_text.strip() != r_text.strip():
                diffs.append((index, origin, l_text.strip(), r_text.strip()))
        lines.append("## Head-to-head")
        lines.append("")
        lines.append(f"- Entries with different output: {len(diffs)} / {len(segments)}")
        lines.append(f"- Output SRT A: `{left['zh_path'].relative_to(ROOT).as_posix()}`")
        lines.append(f"- Output SRT B: `{right['zh_path'].relative_to(ROOT).as_posix()}`")
        lines.append("")

        lines.append("### Sample differences (first 20)")
        lines.append("")
        for index, origin, l_text, r_text in diffs[:20]:
            lines.append(f"#### Entry {index}")
            lines.append("")
            lines.append(f"- ASR: {origin}")
            lines.append(f"- `{left['model']}`: {l_text or '(empty)'}")
            lines.append(f"- `{right['model']}`: {r_text or '(empty)'}")
            lines.append("")

    for row in results:
        lines.append(f"## Problem samples — `{row['model']}`")
        lines.append("")
        samples = sample_pairs(segments, row["texts"], limit=15)
        if not samples:
            lines.append("- No obvious problem samples in the first pass.")
        else:
            for index, origin, text in samples:
                lines.append(f"- **[{index}]** ASR: {origin}")
                lines.append(f"  - ZH: {text or '(empty)'}")
        lines.append("")

    if assessment:
        lines.append("## Comparative assessment")
        lines.append("")
        lines.append(md_code(assessment))
        lines.append("")

  # Recommendation section based on metrics
    if len(results) == 2:
        left, right = results
        lm, rm = left["metrics"], right["metrics"]

        def score(m: dict[str, object]) -> tuple[int, float]:
            penalty = (
                int(m["kana_left"]) * 3
                + int(m["untranslated"]) * 3
                + int(m["bracket_tags"]) * 2
                + int(m["meta_commentary"]) * 4
                + int(m["mixed_ja_zh"]) * 2
            )
            return penalty, float(m["seconds"])

        l_score, r_score = score(lm), score(rm)
        if l_score < r_score:
            winner = left["model"]
            reason = "fewer translation-quality penalties"
        elif r_score < l_score:
            winner = right["model"]
            reason = "fewer translation-quality penalties"
        elif float(lm["seconds"]) <= float(rm["seconds"]):
            winner = left["model"]
            reason = "tie on quality metrics, faster"
        else:
            winner = right["model"]
            reason = "tie on quality metrics, faster"

        lines.append("## Recommendation")
        lines.append("")
        lines.append(f"- **Preferred model**: `{winner}` ({reason}).")
        lines.append(
            "- Use the penalty table above as the primary signal; spot-check sample differences for fluency."
        )
        lines.append("")

    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.report}", flush=True)


if __name__ == "__main__":
    main()
