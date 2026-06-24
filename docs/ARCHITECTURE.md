# 架构：三层产品线

同一仓库（`voice_understanding` / `sense-voice`），**一个 pixi 环境、一套 ASR 底层**，上层按用途拆成三条线。不要拆成三个 Git 仓库——现阶段共享代码太多，拆 repo 只会增加同步成本。

## 两条上游任务的本质区别

| 维度 | 字幕 / 翻译 | 电话 / 会议转写 |
|------|-------------|-----------------|
| 核心问题 | **什么时候显示什么字**（烧录时间轴） | **谁说了什么**（说话人 + 文本） |
| 切分轴 | 时间 + 语义句 + 显示行宽 | **说话人 turn**（可合并同一人连续段） |
| 时间精度 | 字符级对齐，回对齐润色 | 可选粗时间（turn 起止），**不追求 SRT 精度** |
| 典型输出 | `.srt`（`.asr` + `.zh`） | `.md` / `.json`（`Speaker A: …`） |
| LLM 角色 | 翻译、断句、去口癖，**必须回对齐时间** | 纠错、分段、摘要，**不改时间轴** |
| 关键模块 | `timestamps`, `subtitle`, `srt` | `diarize`（待建）, `transcript`（待建） |

```
                    ┌─────────────────────────────────────┐
                    │  1. Core（公共底层）                  │
                    │  transcribe · audio · llm · models  │
                    └──────────────┬──────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
     │ 2. Subtitle    │  │ 3. Transcript  │  │ (future)       │
     │ 字幕 / 翻译     │  │ 转写 / polish   │  │ realtime / …   │
     │ timestamps     │  │ diarization    │  │                │
     │ srt · subtitle │  │ speaker turns  │  │                │
     └────────────────┘  └────────────────┘  └────────────────┘
```

## 当前代码归属（现状 → 目标）

### 1. Core — `python/sense_voice/` 公共部分

| 现状 | 职责 |
|------|------|
| `transcribe.py` | SenseVoice / FunASR，字符时间戳，segment 解析 |
| `scripts/sv.py` | CLI：单文件 ASR → text/json |
| `scripts/extract_audio.py` | 抽 16k mono |
| `scripts/benchmark_voice_llm.py` 中 `run_asr`, `ollama_*`, `chunk_text` | LLM 与 ASR 胶水（**待抽到 `llm.py`**） |
| `models/`, `pixi.toml` | 模型与运行环境 |
| `reference/SenseVoice.cpp` | 可选 C++ 后端（**`mac` 分支 vendor 在根 `SenseVoice.cpp/`**） |

### 2. Subtitle — 字幕 / 翻译

| 现状 | 职责 |
|------|------|
| `timestamps.py` | 文本 ↔ 字符时间轴对齐 |
| `subtitle.py` | 拆句、refine、润色后重对齐 |
| `srt.py` | SRT 读写、显示行切分 |
| `scripts/vr_subtitle_test.py` | VR/KAVR 字幕测试入口 |
| `scripts/benchmark_voice_llm.py` | `vr` / `subtitle` profile，benchmark + SRT |
| `docs/TODO-subtitle.md` | 字幕线待办 |

### 3. Transcript — 转写 / polish（**新功能，尚未实现**）

| 规划 | 职责 |
|------|------|
| `python/sense_voice/diarize.py`（待建） | 说话人分离 / turn 检测 |
| `python/sense_voice/transcript.py`（待建） | turn → 文本块，同说话人合并，导出 md/json |
| `scripts/transcript_test.py`（待建） | 微信录音 / 电话样例测试 |
| LLM `transcript` profile | 纠错、口语整理，**不带时间戳 prompt** |
| `docs/TODO-transcript.md` | 转写线待办 |

## 转写线预期 pipeline（草案）

```
音频 (aac/wav)
  → extract_audio（如需）
  → diarization → [{speaker_id, start, end}, …]
  → 按 turn 切片 ASR（或全量 ASR + 按时间归属说话人）
  → 合并同一 speaker 相邻 turn（可选）
  → LLM polish（transcript profile）
  → 写出 reports/transcript/<clip>.md + .json
```

**不需要**：`split_entries_for_display`、润色后 `realign_polished_entries`、双轨 SRT。

**可能需要**：FunASR 说话人模型 / pyannote / 3D-Speaker 选型（见 `TODO-transcript.md` P0）。

## 脚本入口（pixi tasks）

| Task | 产品线 | 说明 |
|------|--------|------|
| `pixi run sv` | Core | 纯 ASR |
| `pixi run vr-subtitle-test` | Subtitle | SRT + 指标 |
| `pixi run benchmark` | Subtitle（主） | LLM benchmark，可带 `--srt-dir` |
| `pixi run transcript-test` | Transcript | **待建** |

## TODO 管理

| 文件 | 范围 |
|------|------|
| `docs/TODO-core.md` | ASR、音频、LLM 公共能力、代码整理 |
| `docs/TODO-subtitle.md` | 时间轴、SRT、翻译、显示切分 |
| `docs/TODO-transcript.md` | 说话人分离、转写、polish 导出 |
| `TODO.md`（根目录） | **索引**，指向以上三份 |

## 物理拆包节奏（建议）

1. **现在**：文档 + 分轨 TODO（不移动代码，避免大 diff）
2. **下一波**：从 `benchmark_voice_llm.py` 抽出 `sense_voice/llm.py`；根 `TODO.md` 已迁到 `docs/`
3. **转写 P0 验证后**：新增 `diarize.py` / `transcript.py`，**不要**塞进 `subtitle.py`
4. **稳定后可选**：`python/sense_voice/subtitle/` 子包 — 仅当 import 混乱时再做

## 样例音频复用

| 目录 | 字幕线 | 转写线 |
|------|--------|--------|
| `vr_kavr500_part3.wav` | 主验收（长视频、翻译） | 一般不适用（无说话人标签需求） |
| `微信录音 耿瑞香_*.aac` | 中文断句 / 时间轴 | **主验收**（电话、多人、polish） |
| `微信录音 景宜_*.aac` | 可选 | 转写 A/B |
| `talk_to_mom.aac` | 可选 | 转写 |
