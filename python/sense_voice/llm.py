"""Local LLM helpers (Ollama) and prompt profiles."""

from __future__ import annotations

import json
import re
import subprocess
import time
import urllib.request
from typing import Callable

KANA_PATTERN = re.compile(r"[\u3040-\u30ff]")
CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]")


def stop_ollama_models(models: list[str]) -> None:
    for model in sorted({item for item in models if item}):
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


def chunk_text(text: str, max_chars: int) -> list[str]:
    """Split text on line boundaries for manageable LLM calls."""
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


def generate_by_chunk(
    model: str,
    chunks: list[str],
    prompt_builder: Callable[[str], str],
) -> tuple[str, float]:
    outputs: list[str] = []
    total_seconds = 0.0
    for chunk in chunks:
        output, seconds = ollama_generate(model, prompt_builder(chunk))
        outputs.append(output)
        total_seconds += seconds
    return "\n\n".join(outputs).strip(), total_seconds


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

    if profile == "transcript":
        return f"""/no_think
你是电话/微信语音转写编辑。下面按时间顺序给出了多段 ASR 原文（每段含 Turn 编号与 SPEAKER 标签）。

要求：
- 保留每个 `## Turn N · SPEAKER_xx` 标题，不要合并、删减或重排 turn。
- 不要调换说话人标签；每条 turn 对应一条输出。
- 删除口癖、重复、明显识别噪声；修正错别字和标点。
- 把口语整理成可读段落，但不要摘要或删实质信息。
- 不要输出 SRT 格式；可保留标题里的粗时间范围。
- 输出 Markdown：每个 turn 一节，正文为自然中文段落。

ASR 分段原文：
{text}
"""

    if profile == "diary":
        return f"""/no_think
你是个人日记/语音备忘整理助手。下面是一段 ASR 转写（可能含 Turn 标题）。

要求：
- **尽量保留原意和所有实质信息**，不要摘要、不要扩写、不要添加新事实。
- 只做轻量整理：补标点、删明显口癖（嗯、呃、那个）、合并重复词。
- 专有名词（人名、项目名如 imitation/RL、林巧等）保持原样，不确定的不要改。
- 若输入有 `## Turn N` 标题，保留标题结构；单段则输出连贯段落。
- 语气保持第一人称日记口吻，不要改成正式公文。
- 输出润色后的 Markdown 正文，不要解释。

ASR 原文：
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
    elif profile == "transcript":
        work_type = "电话/微信语音转写整理"
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


def strip_timestamps(text: str) -> str:
    return re.sub(r"\[\d+(?:\.\d+)?-\d+(?:\.\d+)?\]\s*", "", text).strip()


def normalize_asr_text(text: str, *, drop_language_artifacts: bool = True) -> str:
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
    from .segments import format_timeline_compact

    if llm_timeline == "compact":
        return format_timeline_compact(segments)
    return normalize_asr_text(timeline, drop_language_artifacts=drop_language_artifacts)
