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


def stop_ollama_models(models: list[str]) -> None:
    for model in sorted({m for m in models if m}):
        subprocess.run(
            ["ollama", "stop", model],
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=30,
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
    if profile == "subtitle":
        return f"""/no_think
你是字幕断句编辑。下面是从 ASR 得到的时间线，请整理成适合烧录的中文字幕。

要求：
- 保留时间线结构；每条输入必须对应一条输出，禁止合并、拆分或重排条目。
- 只删除口癖、重复、明显识别噪声；不要改写语义，不要扩写。
- 输出主体为中文；原文为外语时做直译式翻译，保持简短。
- 时间戳必须与输入完全一致，格式为 `- [开始-结束] 中文字幕文本`。
- 呻吟/笑声/喘息/背景音乐/不可辨语音写进 text，例如“[喘息]”“[笑声]”。
- 输出 Markdown：`## Timeline` + 时间线条目 + `## Notes`（仅 ASR 不确定点）。

ASR 时间线：
{text}
"""

    if profile == "vr":
        return f"""/no_think
你是一个音频场景整理助手。下面是来自 VR/成人视频音轨的 ASR 时间线，可能包含亲密或露骨成人内容。

要求：
- 保留时间线结构，不要把内容改写成无时间戳的散文。
- 只整理可从音频文本判断的信息，不要补写画面、人物关系或事实。
- 删除重复口癖、卡顿和无意义识别噪声。
- 输出主体必须是中文；如果原文是日文、英文或其他语言，请翻译成自然中文。
- 每个输入时间线条目都必须在输出中有对应条目；不能省略末尾片段。
- 不要合并、拆分或重排时间线条目；输出条目数要尽量与输入一致，便于生成 SRT。
- 如果识别结果是呻吟、笑声、喘息、背景音乐或不可辨语音，把描述写进 text，例如“[喘息]”“[笑声]”“[背景音乐]”“[不可辨语音]”。
- 不要做道德评价，不要扩写情色描写。
- 输出 Markdown，包含：
  1. `## Timeline`
  2. 时间线条目，格式必须为 `- [开始-结束] 中文字幕文本`（不要输出 lang/emotion/type 等 tags）
  3. `## Notes`，只列出 ASR 不确定点和明显噪声。

ASR 时间线（每行格式为 `[开始-结束] 原文`）：
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


def assess_prompt(
    raw: str,
    polished: str,
    english: str,
    profile: str,
    *,
    include_english: bool,
) -> str:
    if profile == "vr":
        work_type = "VR/成人视频时间线整理"
    elif profile == "subtitle":
        work_type = "VR/字幕断句整理"
    elif include_english:
        work_type = "ASR 转写 -> 中文润色 -> 英文翻译"
    else:
        work_type = "ASR 转写 -> 中文润色"
    english_section = f"\n英文翻译：\n{english}\n" if include_english else ""
    english_score = "\n2. 英文翻译质量评分：1-5" if include_english else ""
    return f"""/no_think
请评估下面一次“{work_type}”的本地处理结果。

请输出：
1. 中文润色质量评分：1-5{english_score}
3. 主要问题
4. 是否适合直接用于工作记录

ASR 原文：
{raw}

中文润色：
{polished}
{english_section}"""


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


def parse_asr_segments(
    raw: str,
    text: str,
    audio_seconds: float | None,
    *,
    asr_payload: dict[str, object] | None = None,
) -> list[dict[str, object]]:
    segments: list[dict[str, object]] = []
    timing_source = str((asr_payload or {}).get("timing_source", ""))

    structured = (asr_payload or {}).get("sentences")
    if isinstance(structured, list) and structured:
        for item in structured:
            if isinstance(item, dict) and item.get("text"):
                segments.append(dict(item))
        if segments:
            return segments

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
                    segment["timing_confidence"] = "high"
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
                        "timing_confidence": "high",
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
                "timing_confidence": None,
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
            segment["timing_confidence"] = "low"

    words = (asr_payload or {}).get("words")
    if isinstance(words, list) and words and segments:
        try:
            sys.path.insert(0, str(ROOT / "python"))
            from sense_voice.subtitle import refine_segments

            segments = refine_segments(segments, words)
        except Exception:
            pass

    if timing_source and segments and all(segment.get("timing_confidence") is None for segment in segments):
        for segment in segments:
            segment["timing_confidence"] = "medium" if timing_source != "none" else None

    return segments


def segment_duration_stats(segments: list[dict[str, object]]) -> dict[str, float | int]:
    durations: list[float] = []
    for segment in segments:
        start = segment.get("start")
        end = segment.get("end")
        if start is None or end is None:
            continue
        duration = float(end) - float(start)
        if duration > 0:
            durations.append(duration)
    if not durations:
        return {
            "count": len(segments),
            "timed_count": 0,
            "p50": 0.0,
            "p95": 0.0,
            "max": 0.0,
            "over_10s": 0,
            "over_30s": 0,
        }
    durations.sort()
    p50 = durations[len(durations) // 2]
    p95 = durations[max(0, int(len(durations) * 0.95) - 1)]
    return {
        "count": len(segments),
        "timed_count": len(durations),
        "p50": p50,
        "p95": p95,
        "max": max(durations),
        "over_10s": sum(1 for value in durations if value > 10),
        "over_30s": sum(1 for value in durations if value > 30),
    }


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


def format_timeline_compact(segments: list[dict[str, object]]) -> str:
    """Timestamp + text only; leaner LLM input and SRT-friendly."""
    lines: list[str] = []
    for segment in segments:
        start = seconds_label(segment.get("start"))
        end = seconds_label(segment.get("end"))
        lines.append(f"[{start}-{end}] {segment['text']}")
    return "\n".join(lines)


def resolve_llm_timeline_mode(profile: str, llm_timeline: str | None) -> str:
    if llm_timeline:
        return llm_timeline
    return "compact" if profile in {"vr", "subtitle"} else "full"


def build_llm_input(
    segments: list[dict[str, object]],
    timeline: str,
    *,
    llm_timeline: str,
    drop_language_artifacts: bool,
) -> str:
    if llm_timeline == "compact":
        return format_timeline_compact(segments)
    return normalize_asr_text(timeline, drop_language_artifacts=drop_language_artifacts)


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


SRT_LINE_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?\[(?P<start>[^\]-]+)-(?P<end>[^\]]+)\]\s*(?P<text>.+?)\s*$"
)


def parse_time_label(label: str) -> float | None:
    label = label.strip().replace(",", ".")
    if not label or "?" in label:
        return None
    parts = label.split(":")
    try:
        if len(parts) == 1:
            return float(parts[0])
        if len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    except ValueError:
        return None
    return None


def srt_timestamp(seconds: float) -> str:
    millis = int(round(max(0.0, seconds) * 1000))
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def parse_srt_entries(polished: str) -> list[tuple[float, float, str]]:
    entries: list[tuple[float, float, str]] = []
    for line in polished.splitlines():
        match = SRT_LINE_PATTERN.match(line)
        if not match:
            continue
        start = parse_time_label(match.group("start"))
        end = parse_time_label(match.group("end"))
        text = match.group("text").strip()
        text = re.sub(r"^tags:\s*.*?\|\s*text:\s*", "", text).strip()
        if start is None or end is None or end <= start or not text:
            continue
        entries.append((start, end, text))
    return entries


def write_srt(path: Path, entries: list[tuple[float, float, str]]) -> None:
    blocks: list[str] = []
    for idx, (start, end, text) in enumerate(entries, start=1):
        blocks.append(
            "\n".join(
                [
                    str(idx),
                    f"{srt_timestamp(start)} --> {srt_timestamp(end)}",
                    text,
                ]
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(blocks) + ("\n" if blocks else ""), encoding="utf-8")


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
