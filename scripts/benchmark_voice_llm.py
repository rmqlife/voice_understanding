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
DEFAULT_CLIP = ROOT / "test_voice_clips" / "sunflower.mp3"
DEFAULT_CLIPS = ROOT / "test_voice_clips"
DEFAULT_REPORT = ROOT / "reports" / "voice_llm_benchmark.md"
DEFAULT_MODEL = "qwen3:1.7b"
KANA_PATTERN = re.compile(r"[\u3040-\u30ff]")
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")
TAG_GROUP_PATTERN = re.compile(r"((?:<\|[^|]+\|>)+)([^<]*)")
CPP_TIMELINE_PATTERN = re.compile(r"^\[(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]\s*(.*)$")
LANG_TAGS = {"zh", "en", "yue", "ja", "ko", "nospeech"}
SPEECH_TAGS = {"Speech", "Applause", "BGM", "Laughter", "Event"}
ITN_TAGS = {"withitn", "woitn"}


def run_asr(
    audio: Path,
    language: str,
    *,
    backend: str,
    device: str | None,
    model: str | None,
) -> tuple[str, str, float | None, float, str]:
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
        return proc.stdout.strip(), proc.stdout.strip(), None, elapsed, proc.stderr.strip()
    return (
        str(payload.get("text", "")).strip(),
        str(payload.get("raw", "")).strip(),
        payload.get("audio_seconds"),
        elapsed,
        proc.stderr.strip(),
    )


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


def polish_prompt(text: str, profile: str) -> str:
    if profile == "vr":
        return f"""/no_think
你是一个音频场景整理助手。下面是来自 VR/成人视频音轨的 ASR 时间线，可能包含亲密或露骨成人内容。

要求：
- 保留时间线结构，不要把内容改写成无时间戳的散文。
- 只整理可从音频文本判断的信息，不要补写画面、人物关系或事实。
- 保留关键台词、语气、情绪标签和明显音效；删除重复口癖、卡顿和无意义识别噪声。
- 输出主体必须是中文；如果原文是日文、英文或其他语言，请翻译成自然中文。
- 每个输入时间线条目都必须在输出中有对应条目；不能省略末尾片段。
- 如果识别结果是呻吟、笑声、喘息、背景音乐或不可辨语音，用中性标签描述，例如“[喘息]”“[笑声]”“[背景音乐]”“[不可辨语音]”。
- 不要做道德评价，不要扩写情色描写。
- 输出 Markdown，包含：
  1. `## Timeline`
  2. 时间线条目，格式为 `- [开始-结束] tags: ... | text: ...`
  3. `## Notes`，只列出 ASR 不确定点和明显噪声。

ASR 时间线：
{text}
"""

    if profile == "generic":
        return f"""/no_think
你是一个转写整理助手。请把下面带时间线和标签的 ASR 文本整理成可读记录。

要求：
- 保留时间线。
- 保留原意，不扩写事实。
- 删除卡顿、重复、明显识别噪声。
- 保留重要标签，例如语言、情绪、音频事件。
- 输出 Markdown，优先使用时间线条目。

ASR 时间线：
{text}
"""

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
- 保留重要时间线和标签；如果整理为纪要，可在段落前保留大致时间范围。
- 输出润色后的正文，不要解释。

ASR 时间线：
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


def assess_prompt(raw: str, polished: str, english: str, profile: str) -> str:
    work_type = "VR/成人视频时间线整理" if profile == "vr" else "ASR 转写 -> 中文润色 -> 英文翻译"
    return f"""/no_think
请评估下面一次“{work_type}”的本地处理结果。

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


def seconds_label(seconds: float | None) -> str:
    if seconds is None:
        return "??:??"
    total_tenths = int(round(max(0.0, seconds) * 10))
    minutes, tenths = divmod(total_tenths, 600)
    sec = tenths / 10
    return f"{minutes:02d}:{sec:04.1f}"


def parse_tagged_text(text: str) -> list[dict[str, object]]:
    segments: list[dict[str, object]] = []
    for match in TAG_GROUP_PATTERN.finditer(text):
        tags = re.findall(r"<\|([^|]+)\|>", match.group(1))
        segment_text = match.group(2).strip()
        if not segment_text:
            continue
        lang = next((tag for tag in tags if tag in LANG_TAGS), None)
        speech_type = next((tag for tag in tags if tag in SPEECH_TAGS), None)
        itn = next((tag for tag in tags if tag in ITN_TAGS), None)
        emotions = [
            tag for tag in tags
            if tag not in LANG_TAGS and tag not in SPEECH_TAGS and tag not in ITN_TAGS
        ]
        segments.append(
            {
                "start": None,
                "end": None,
                "lang": lang,
                "type": speech_type,
                "itn": itn,
                "emotion": ",".join(emotions) if emotions else None,
                "text": strip_tags(segment_text),
            }
        )
    return segments


def parse_asr_segments(raw: str, text: str, audio_seconds: float | None) -> list[dict[str, object]]:
    segments: list[dict[str, object]] = []
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                segments.extend(parse_tagged_text(str(item.get("text", ""))))

    if not segments:
        for line in raw.splitlines():
            match = CPP_TIMELINE_PATTERN.match(line.strip())
            if not match:
                continue
            segment_text = match.group(3)
            tagged = parse_tagged_text(segment_text)
            if tagged:
                for segment in tagged:
                    segment["start"] = float(match.group(1))
                    segment["end"] = float(match.group(2))
                    segments.append(segment)
            else:
                segments.append(
                    {
                        "start": float(match.group(1)),
                        "end": float(match.group(2)),
                        "lang": None,
                        "type": None,
                        "itn": None,
                        "emotion": None,
                        "text": strip_tags(segment_text),
                    }
                )

    if not segments:
        chunks = re.split(r"(?<=[。！？!?\.])\s*", text)
        segments = [
            {
                "start": None,
                "end": None,
                "lang": None,
                "type": None,
                "itn": None,
                "emotion": None,
                "text": chunk.strip(),
            }
            for chunk in chunks
            if chunk.strip()
        ]

    if audio_seconds and segments and all(segment["start"] is None for segment in segments):
        total_chars = sum(max(1, len(str(segment["text"]))) for segment in segments)
        cursor = 0.0
        for segment in segments:
            duration = audio_seconds * max(1, len(str(segment["text"]))) / total_chars
            segment["start"] = cursor
            cursor += duration
            segment["end"] = min(audio_seconds, cursor)

    return segments


def format_timeline(segments: list[dict[str, object]]) -> str:
    lines: list[str] = []
    for idx, segment in enumerate(segments, start=1):
        start = seconds_label(segment.get("start"))
        end = seconds_label(segment.get("end"))
        tags = []
        for key in ("lang", "emotion", "type", "itn"):
            value = segment.get(key)
            if value:
                tags.append(f"{key}={value}")
        tag_text = ", ".join(tags) if tags else "none"
        lines.append(f"{idx:03d}. [{start}-{end}] tags: {tag_text} | text: {segment['text']}")
    return "\n".join(lines)


def max_timestamp_seconds(text: str) -> float | None:
    matches = re.findall(r"\[(?:\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)\]", text)
    if not matches:
        return None
    return max(float(m) for m in matches)


def ffprobe_duration(path: Path) -> float | None:
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return None
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return None


def strip_tags(text: str) -> str:
    return re.sub(r"<\|[^|]+\|>", "", text).strip()


def strip_timestamps(text: str) -> str:
    return re.sub(r"\[\d+(?:\.\d+)?-\d+(?:\.\d+)?\]\s*", "", text).strip()


def normalize_asr_text(text: str, *, drop_language_artifacts: bool = True) -> str:
    """Remove obvious language-ID artifacts before LLM cleanup."""
    cleaned: list[str] = []
    for line in strip_timestamps(text).splitlines():
        line = line.strip()
        if not line:
            continue
        has_kana = bool(KANA_PATTERN.search(line))
        has_chinese = bool(CHINESE_PATTERN.search(line))
        if drop_language_artifacts and has_kana and not has_chinese:
            continue
        if drop_language_artifacts and line.lower() in {"yes.", "yes", "yeah.", "yeah", "sure", "sure."}:
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
        choices=["finance", "vr", "generic"],
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
    args = parser.parse_args()
    polish_model = args.polish_model or args.model
    translate_model = args.translate_model or args.model
    assess_model = args.assess_model or args.model

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
        asr_text, raw, result_audio_seconds, asr_seconds, stderr = run_asr(
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
        segments = parse_asr_segments(raw, asr_text, audio_seconds)
        timeline = format_timeline(segments)
        transcript = normalize_asr_text(
            timeline,
            drop_language_artifacts=args.profile == "finance",
        )
        chunks = chunk_text(transcript, args.chunk_chars)

        polished, polish_seconds = generate_by_chunk(
            polish_model,
            chunks,
            lambda chunk: polish_prompt(chunk, args.profile),
        )
        polished_chunks = chunk_text(polished, args.chunk_chars)
        english, translate_seconds = generate_by_chunk(
            translate_model,
            polished_chunks,
            translate_prompt,
        )
        assessment, assess_seconds = ollama_generate(
            assess_model,
            assess_prompt(transcript, polished, english, args.profile),
        )

        rows.append(
            {
                "file": audio.name,
                "size_mb": audio.stat().st_size / 1024 / 1024,
                "audio_seconds": audio_seconds,
                "asr_seconds": asr_seconds,
                "asr_rtf": asr_seconds / audio_seconds if audio_seconds else None,
                "raw_chars": len(transcript),
                "segments": len(segments),
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
    lines.append(f"- ASR: `{args.asr_backend}` via `pixi run sv`")
    if args.asr_device:
        lines.append(f"- ASR device: `{args.asr_device}`")
    if args.asr_model:
        lines.append(f"- ASR model: `{args.asr_model}`")
    lines.append(f"- ASR language: `{args.language}`")
    lines.append(f"- Prompt profile: `{args.profile}`")
    lines.append(f"- Polish LLM: `{polish_model}` via Ollama local API")
    lines.append(f"- Translate LLM: `{translate_model}` via Ollama local API")
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
    lines.append(f"- Total English translation wall time: {total_translate:.2f}s")
    lines.append("")
    lines.append("## Benchmark Table")
    lines.append("")
    lines.append("| File | Size MB | Audio s | ASR s | ASR RTF | Segments | Raw chars | Chunks | Polish s | Translate s |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
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
    lines.append(f"- `{polish_model}` handled transcript cleanup; `{translate_model}` handled English translation; `{assess_model}` handled self-assessment.")
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
        lines.append("### Structured ASR Timeline")
        lines.append("")
        lines.append(md_code(str(r["transcript"])))
        lines.append("")
        lines.append("### Raw ASR Payload")
        lines.append("")
        lines.append(md_code(str(r["raw"])))
        lines.append("")

    args.report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.report}", flush=True)


if __name__ == "__main__":
    main()
