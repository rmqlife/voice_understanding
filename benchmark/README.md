# benchmark/

LLM benchmark **代码 + 数据 + 结论** 放在一起，自成一体。

```
benchmark/
├── benchmark_voice_llm.py      # 入口（pixi run benchmark）
├── benchmark_translate_llm.py  # ja→zh 翻译模型对比（ASR SRT 输入）
└── reports/                    # 历史结论报告
    ├── voice_llm_benchmark.md
    ├── translate_benchmark_kavr506_cd1.md
    └── vr_audio_benchmark*.md
```

ASR 通过 `sense_voice.asr_cli.run_asr`（即 `pixi run sv` 同一条 CLI 路径）拿结果，再跑本地 Ollama 润色/翻译/自评。

```bash
pixi run benchmark -- \
  --clip data/vr/vr_sample.wav \
  --report benchmark/reports/vr_audio_benchmark.md \
  --asr-backend official --asr-device cuda:0 \
  --model nsfw-local:27b --profile vr --language ja
```

默认报告输出到 `benchmark/reports/voice_llm_benchmark.md`。

**翻译模型对比**（`nsfw-local:27b` vs `huihui_ai/qwen3.5-abliterated:27b`，输入已有 `.asr.srt`）：

```bash
pixi run python benchmark/benchmark_translate_llm.py
```

默认用 `results/srt/KAVR-506-伊藤舞雪__KAVR-506-CD1.asr.srt`，报告写到 `benchmark/reports/translate_benchmark_kavr506_cd1.md`。

> 字幕主验收用 `pixi run vr-subtitle-test`（产出 SRT + 指标）；benchmark 适合做完整 LLM 长报告对比。
