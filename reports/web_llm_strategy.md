# Web LLM Chinese Polishing Strategy

## Goal

Use local SenseVoice for transcription, then use a web LLM only as a high-quality Chinese editor. The tool should produce a clean Chinese record from noisy ASR text, without translation, scoring, or sample-specific terminology rules.

## Workflow

1. Run local ASR with Chinese fixed: `pixi run sv audio --quiet -l zh`.
2. Remove obvious language-ID artifacts before sending text to an LLM.
3. Paste the generated polishing task into a web LLM such as Qwen, Kimi, or Gemini.
4. Save the returned Chinese polished text as the final draft.

## Prompt Principles

- Keep all substantive information.
- Do not summarize or add facts.
- Remove filler words, stutters, repeated confirmations, and obvious ASR noise.
- Rewrite loose spoken fragments into complete natural Chinese sentences.
- Use whole-document consistency only when the context clearly supports it.
- Preserve uncertain names or domain terms instead of guessing.
- Output only the polished Chinese text.

## Files

- Web prompt tasks: `reports/web_llm_tasks/*.md`
- Original ASR snapshots: `reports/web_llm_tasks/*.raw_asr.md`
- Web task exporter: `scripts/export_web_llm_tasks.py`

## Recommendation

Best practical solution right now:

- Private/local draft: SenseVoice `-l zh` + local Ollama.
- Better final Chinese text: SenseVoice `-l zh` + web LLM polishing prompt.
