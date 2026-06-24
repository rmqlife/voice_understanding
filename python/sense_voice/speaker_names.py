"""Optional LLM speaker naming for transcript export."""

from __future__ import annotations

import json
import re

from .diarize import SpeakerTurn


def collect_speaker_samples(turns: list[SpeakerTurn], *, max_chars: int = 400) -> dict[str, str]:
    samples: dict[str, str] = {}
    for turn in turns:
        if turn.speaker in samples:
            continue
        text = turn.text.strip()
        if text:
            samples[turn.speaker] = text[:max_chars]
    return samples


def speaker_name_prompt(samples: dict[str, str]) -> str:
    blocks = [f"{speaker}:\n{text}" for speaker, text in samples.items()]
    return f"""/no_think
根据以下电话/微信对话各说话人样本，为每个 SPEAKER_xx 起一个简短中文称呼（2-6字），例如「业主」「物业」「同事」「妻子」。
只输出 JSON 对象，键为原始 speaker id，值为称呼。不要解释。

样本：
{chr(10).join(blocks)}
"""


def parse_speaker_names(response: str) -> dict[str, str]:
    match = re.search(r"\{[^{}]*\}", response, re.DOTALL)
    if not match:
        return {}
    try:
        payload = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    return {str(key): str(value).strip() for key, value in payload.items() if value}


def apply_speaker_names(turns: list[SpeakerTurn], names: dict[str, str]) -> list[SpeakerTurn]:
    updated: list[SpeakerTurn] = []
    for turn in turns:
        updated.append(
            SpeakerTurn(
                speaker=turn.speaker,
                start=turn.start,
                end=turn.end,
                text=turn.text,
                name=names.get(turn.speaker, turn.name),
            )
        )
    return updated
