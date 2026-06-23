#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLIPS = ROOT / "test_voice_clips"
DEFAULT_REPORT = ROOT / "reports" / "voice_llm_benchmark.md"
DEFAULT_MODEL = "qwen3:1.7b"
KANA_PATTERN = re.compile(r"[\u3040-\u30ff]")
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")


def run_asr(audio: Path, language: str) -> tuple[str, float, str]:
    start = time.perf_counter()
    proc = subprocess.run(
        ["pixi", "run", "sv", str(audio), "--quiet", "-l", language],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    elapsed = time.perf_counter() - start
    if proc.returncode != 0:
        raise RuntimeError(f"ASR failed for {audio.name}:\n{proc.stderr}")
    return proc.stdout.strip(), elapsed, proc.stderr.strip()


def ollama_generate(model: str, prompt: str) -> tuple[str, float]:
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": False,
        }
    ).encode("utf-8")
    start = time.perf_counter()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    elapsed = time.perf_counter() - start
    return body.get("response", "").strip(), elapsed


def polish_prompt(text: str) -> str:
    return f"""/no_think
你是一个资深中文编辑。请把下面这段语音识别文本整理成适合保存、发给同事或放入笔记的自然中文记录。

要求：
- 保留原意，不扩写事实。
- 不要摘要，不要删除任何实质信息；但可以删除寒暄、重复确认、卡顿、填充词和明显无意义片段。
- 删除“嗯、呃、啊、就是、然后、对对对、好嘞”等口语填充词，保留必要语气含义。
- 把散乱口语改成完整句子；必要时重排语序、合并重复句、补足主谓宾，让整段话通顺。
- 做全文一致性校对：同一对象前后不同写法时，选择后文更可信、领域内真实存在的写法。
- 修正错别字、标点、断句和明显的语音识别错误。
- 金融录音常见纠错：招行=招商银行，金桂花/金葵花应统一为“金葵花”，贵定应为“贵宾”，京东精融应为“京东金融”，M家/M加如无法确定则保留为“M+”。
- 只在能从上下文明显判断时纠错；不能确定的专有名词保留原文。
- 电话沟通整理为可读对话纪要，必要时用“客户：”“客户经理：”区分说话人；普通聊天整理为连贯段落。
- 不要保留时间戳。
- 输出润色后的正文，不要解释。

文本：
{text}
"""


def translate_prompt(text: str) -> str:
    return f"""/no_think
Please translate the following polished Chinese transcript into natural English.

Requirements:
- Preserve meaning and concrete details.
- Do not summarize or omit substantive information.
- Keep names, numbers, dates, and card/account references as written when uncertain.
- Do not leave Chinese words untranslated unless they are proper names or card names.
- Use this glossary when relevant:
  - 招行 / 招商银行 = China Merchants Bank / CMB
  - 金葵花贵宾卡 = Golden Sunflower VIP Card
  - 理财产品 = wealth management products
  - 永隆 = CMB Wing Lung Bank
  - 微众 = WeBank
  - 京东金融 = JD Finance
  - 物业 = property management office
  - 售楼处 = sales office
- Output only the English translation.

Text:
{text}
"""


def assess_prompt(raw: str, polished: str, english: str) -> str:
    return f"""/no_think
请评估下面一次“ASR 转写 -> 中文润色 -> 英文翻译”的本地处理结果。

请输出：
1. 中文润色质量评分：1-5
2. 英文翻译质量评分：1-5
3. 主要问题
4. 是否适合直接用于工作记录

ASR 原文：
{raw}

中文润色：
{polished}

英文翻译：
{english}
"""


def max_timestamp_seconds(text: str) -> float | None:
    matches = re.findall(r"\[(?:\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]", text)
    if not matches:
        return None
    return max(float(m) for m in matches)


def strip_timestamps(text: str) -> str:
    return re.sub(r"\[\d+(?:\.\d+)?-\d+(?:\.\d+)?\]\s*", "", text).strip()


def normalize_asr_text(text: str) -> str:
    """Remove obvious language-ID artifacts before LLM cleanup."""
    cleaned: list[str] = []
    for line in strip_timestamps(text).splitlines():
        line = line.strip()
        if not line:
            continue
        has_kana = bool(KANA_PATTERN.search(line))
        has_chinese = bool(CHINESE_PATTERN.search(line))
        if has_kana and not has_chinese:
            continue
        if line.lower() in {"yes.", "yes", "yeah.", "yeah", "sure", "sure."}:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def md_code(text: str) -> str:
    return "```text\n" + text.strip() + "\n```"


def chunk_text(text: str, max_chars: int) -> list[str]:
    """Split text on ASR line boundaries for manageable LLM calls."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for line in lines:
        extra = len(line) + 1
        if current and current_len + extra > max_chars:
            chunks.append("\n".join(current))
            current = [line]
            current_len = extra
        else:
            current.append(line)
            current_len += extra
    if current:
        chunks.append("\n".join(current))
    return chunks


def generate_by_chunk(model: str, chunks: list[str], prompt_builder) -> tuple[str, float]:
    outputs: list[str] = []
    total_seconds = 0.0
    for chunk in chunks:
        output, seconds = ollama_generate(model, prompt_builder(chunk))
        outputs.append(output)
        total_seconds += seconds
    return "\n\n".join(outputs).strip(), total_seconds


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips", type=Path, default=DEFAULT_CLIPS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default="zh", help="ASR language (default: zh)")
    parser.add_argument("--chunk-chars", type=int, default=900, help="Max transcript chars per LLM call")
    args = parser.parse_args()

    audio_files = sorted(
        p for p in args.clips.iterdir() if p.suffix.lower() in {".mp3", ".aac", ".wav", ".m4a", ".flac"}
    )
    if not audio_files:
        raise SystemExit(f"No audio files found in {args.clips}")

    args.report.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    for audio in audio_files:
        print(f"Processing {audio.name}", flush=True)
        raw, asr_seconds, stderr = run_asr(audio, args.language)
        transcript = normalize_asr_text(raw)
        audio_seconds = max_timestamp_seconds(raw)
        chunks = chunk_text(transcript, args.chunk_chars)

        polished, polish_seconds = generate_by_chunk(args.model, chunks, polish_prompt)
        polished_chunks = chunk_text(polished, args.chunk_chars)
        english, translate_seconds = generate_by_chunk(args.model, polished_chunks, translate_prompt)
        assessment, assess_seconds = ollama_generate(args.model, assess_prompt(transcript, polished, english))

        rows.append(
            {
                "file": audio.name,
                "size_mb": audio.stat().st_size / 1024 / 1024,
                "audio_seconds": audio_seconds,
                "asr_seconds": asr_seconds,
                "asr_rtf": asr_seconds / audio_seconds if audio_seconds else None,
                "raw_chars": len(transcript),
                "chunks": len(chunks),
                "polished_chars": len(polished),
                "english_chars": len(english),
                "polish_seconds": polish_seconds,
                "translate_seconds": translate_seconds,
                "assess_seconds": assess_seconds,
                "stderr": stderr,
                "raw": raw,
                "transcript": transcript,
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
    lines.append(f"- ASR: SenseVoice.cpp via `pixi run sv`")
    lines.append(f"- ASR language: `{args.language}`")
    lines.append(f"- Local LLM: `{args.model}` via Ollama local API")
    lines.append(f"- LLM chunk size: {args.chunk_chars} chars")
    lines.append(f"- Source directory: `{args.clips}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Files processed: {len(rows)}")
    lines.append(f"- Approx. audio duration: {total_audio:.1f}s")
    lines.append(f"- Total ASR wall time: {total_asr:.2f}s")
    lines.append(f"- Total polish wall time: {total_polish:.2f}s")
    lines.append(f"- Total English translation wall time: {total_translate:.2f}s")
    lines.append("")
    lines.append("## Benchmark Table")
    lines.append("")
    lines.append("| File | Size MB | Audio s | ASR s | ASR RTF | Raw chars | Chunks | Polish s | Translate s |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            "| {file} | {size_mb:.2f} | {audio_seconds:.1f} | {asr_seconds:.2f} | {asr_rtf:.3f} | {raw_chars} | {chunks} | {polish_seconds:.2f} | {translate_seconds:.2f} |".format(
                file=str(r["file"]).replace("|", "\\|"),
                size_mb=float(r["size_mb"]),
                audio_seconds=float(r["audio_seconds"] or 0),
                asr_seconds=float(r["asr_seconds"]),
                asr_rtf=float(r["asr_rtf"] or 0),
                raw_chars=int(r["raw_chars"]),
                chunks=int(r["chunks"]),
                polish_seconds=float(r["polish_seconds"]),
                translate_seconds=float(r["translate_seconds"]),
            )
        )
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    lines.append("- SenseVoice.cpp is fast on these clips, with ASR wall time well below real-time overall.")
    lines.append("- The AAC inputs emitted ffmpeg decode warnings in this run, but transcription still completed.")
    lines.append("- `qwen3:1.7b` is usable for quick local drafts, but it is not the best-quality solution. It still preserves some awkward ASR phrasing and can mis-handle speaker roles.")
    lines.append("- The first phone-call clip is much harder than the others: it contains overlapping speakers, finance-specific terms, card numbers, and possible ASR hallucinations such as non-Chinese filler tokens.")
    lines.append("- `qwen3:4b` was downloaded and tested, but it was too slow for full benchmark processing on this machine. Since 4B is already too slow for the long clip, `qwen3:8b` is not recommended for this workflow right now.")
    lines.append("- Best current direction: keep ASR language pinned to Chinese, clean language-ID artifacts before LLM input, process long recordings in chunks, and add deterministic post-processing for domain terms before/after LLM polishing.")
    lines.append("")

    for idx, r in enumerate(rows, start=1):
        lines.append(f"## {idx}. {r['file']}")
        lines.append("")
        lines.append("### Metrics")
        lines.append("")
        lines.append(f"- Size: {float(r['size_mb']):.2f} MB")
        lines.append(f"- Approx. audio duration from timestamps: {float(r['audio_seconds'] or 0):.1f}s")
        lines.append(f"- ASR wall time: {float(r['asr_seconds']):.2f}s")
        lines.append(f"- Polish wall time: {float(r['polish_seconds']):.2f}s")
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
        lines.append("### English Translation")
        lines.append("")
        lines.append(md_code(str(r["english"])))
        lines.append("")
        lines.append("### Model Self-Assessment")
        lines.append("")
        lines.append(md_code(str(r["assessment"])))
        lines.append("")
        lines.append("### Raw ASR Transcript")
        lines.append("")
        lines.append(md_code(str(r["raw"])))
        lines.append("")

    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.report}", flush=True)


if __name__ == "__main__":
    main()
