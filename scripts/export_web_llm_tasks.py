#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from benchmark_voice_llm import ROOT, normalize_asr_text


DEFAULT_CLIPS = ROOT / "test_voice_clips"
DEFAULT_OUT = ROOT / "reports" / "web_llm_tasks"


WEB_PROMPT = """你是资深中文编辑。下面是一段中文电话或聊天录音的 ASR 转写文本，可能存在错字、断句错误、语气词、重复、语言误识别和专有名词误识别。

请把它整理成一份自然、通顺、适合保存的中文记录。

要求：
- 保留所有实质信息，不要摘要，不要新增事实。
- 删除无意义寒暄、卡顿、填充词和重复确认，例如“嗯、呃、啊、就是、然后、对对对”等。
- 把散乱口语改成完整自然的中文句子；必要时重排语序、合并重复句、补足主谓宾。
- 做全文一致性校对：同一对象前后有不同写法时，选择上下文中更可信的写法；不能确定时保留原文。
- 明显语言误识别的日语/英语短词，如果只是“啊、嗯、是、好”等语气或确认的误判，直接删除。
- 电话沟通可整理为对话纪要；能判断说话人时使用简洁说话人标签，不能判断时使用自然段。
- 不要输出翻译、评分、解释或修改说明。
- 只输出润色后的中文正文。

ASR 原文：
```text
{transcript}
```
"""


def run_asr(audio: Path, language: str) -> str:
    proc = subprocess.run(
        ["pixi", "run", "sv", str(audio), "--quiet", "-l", language],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"ASR failed for {audio.name}:\n{proc.stderr}")
    return proc.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips", type=Path, default=DEFAULT_CLIPS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--language", default="zh")
    args = parser.parse_args()

    audio_files = sorted(
        p for p in args.clips.iterdir()
        if p.suffix.lower() in {".mp3", ".aac", ".wav", ".m4a", ".flac"}
    )
    args.out.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# Web LLM Task Pack",
        "",
        f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- ASR language: `{args.language}`",
        "- Suggested web models: Qwen web, Kimi, Gemini",
        "",
        "## Files",
        "",
    ]

    for idx, audio in enumerate(audio_files, start=1):
        raw = run_asr(audio, args.language)
        transcript = normalize_asr_text(raw)
        stem = f"{idx:02d}_{audio.stem}"
        task_path = args.out / f"{stem}.md"
        raw_path = args.out / f"{stem}.raw_asr.md"
        prompt = WEB_PROMPT.format(transcript=transcript)
        task_path.write_text(prompt, encoding="utf-8")
        raw_path.write_text("```text\n" + raw + "\n```\n", encoding="utf-8")
        index_lines.append(f"- [{audio.name}]({task_path.name})")

    index_lines.extend(
        [
            "",
            "## How To Use",
            "",
            "1. Open a web LLM chat, such as Qwen, Kimi, or Gemini.",
            "2. Paste one `.md` task file into the chat.",
            "3. Save the answer next to the task file as `.polished.md`.",
            "4. Compare providers on readability, filler-word removal, factual preservation, and whether uncertain names are handled cautiously.",
            "",
            "## Current Best Bet",
            "",
            "- Use local SenseVoice with `-l zh` for ASR.",
            "- Use this task prompt with a strong web LLM for final Chinese polishing when privacy allows.",
            "- Keep local Ollama for private drafts and quick iteration.",
        ]
    )
    (args.out / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Wrote web LLM task pack to {args.out}")


if __name__ == "__main__":
    main()
