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

| 模块 / 入口 | 职责 |
|------|------|
| `transcribe.py` | SenseVoice / FunASR，字符时间戳，segment 解析 |
| `asr_cli.py` | `run_asr()`：经 `scripts/sv.py` 子进程跑 ASR（benchmark / 测试共用） |
| `llm.py` | Ollama 润色 / 翻译 / 自评、分块、prompt profile |
| `audio.py` · `segments.py` · `models.py` | 音频时长、segment 解析、模型缓存路径 |
| `scripts/sv.py` | CLI：单文件/批量 ASR → text/json |
| `scripts/extract_audio.py` | 抽 16k mono |

### 2. Subtitle — 字幕 / 翻译

| 模块 / 入口 | 职责 |
|------|------|
| `timestamps.py` | 文本 ↔ 字符时间轴对齐 |
| `subtitle.py` | 拆句、refine、润色后重对齐 |
| `srt.py` | SRT 读写、显示行切分 |
| `scripts/vr_subtitle_test.py` | VR/KAVR 字幕测试入口（主验收） |
| `benchmark/benchmark_voice_llm.py` | `vr` / `subtitle` profile，完整 LLM benchmark（本地 only） |
| `TODO-subtitle.md` | 字幕线待办 |

### 3. Transcript — 转写 / polish

| 模块 / 入口 | 职责 |
|------|------|
| `python/sense_voice/diarize.py` | 说话人分离 / turn 检测（FunASR cam++ 主路径，ffmpeg-alternate 仅 debug） |
| `python/sense_voice/transcript.py` | turn → 文本块，同说话人合并，导出 md/json |
| `python/sense_voice/speaker_names.py` | 可选 LLM 说话人命名 |
| `scripts/transcript_test.py` | 微信录音 / 电话样例测试 |
| `TODO-transcript.md` | 转写线待办 |

## 转写线预期 pipeline（草案）

```
音频 (aac/wav)
  → extract_audio（如需）
  → diarization → [{speaker_id, start, end}, …]
  → 按 turn 切片 ASR（或全量 ASR + 按时间归属说话人）
  → 合并同一 speaker 相邻 turn（可选）
  → LLM polish（transcript profile）
  → 写出 results/transcript/<clip>.md + .json
```

**不需要**：`split_entries_for_display`、润色后 `realign_polished_entries`、双轨 SRT。

**说话人选型**：FunASR cam++ 为主路径；pyannote 对比实验已归档到 `archive/pyannote/`（结论：相当，非主路径）。

## 脚本入口（pixi tasks）

| Task | 产品线 | 说明 |
|------|--------|------|
| `pixi run sv` | Core | 纯 ASR |
| `pixi run add-subtitle` | Subtitle | NFS mp4 → SRT → 回写 |
| `pixi run vr-subtitle-test` | Subtitle | SRT + 指标（主验收） |
| `pixi run transcript-test` | Transcript | 说话人转写 + polish |

## 仓库结构

```
python/sense_voice/   库：所有共享逻辑
scripts/              扁平 CLI 入口（见 scripts/README.md）
scripts/tests/        无 GPU 冒烟测试
data/                 本地音频（data/vr、data/recording）
results/              字幕 / 转写运行产物（本地 only，不进 Git）
benchmark/            LLM benchmark（本地 only，不进 Git）
tasks/                批量 task.toml（本地 only，不进 Git）
.agent/               架构、规范、分轨 TODO（Agent 文档）
docs/                 技术备忘（非 Agent 入口）
archive/              已归档实验（pyannote / mac-cpp / vad）
```

**约定**：脚本之间不互相 import；共享逻辑一律下沉到 `python/sense_voice/`（如 `run_asr` 在 `asr_cli.py`）。

## TODO 管理

| 文件 | 范围 |
|------|------|
| [`TODO.md`](../TODO.md)（根目录） | **索引**，指向 `.agent/` 下三份分轨 TODO |
| `TODO-core.md` | ASR、音频、LLM 公共能力、代码整理 |
| `TODO-subtitle.md` | 时间轴、SRT、翻译、显示切分 |
| `TODO-transcript.md` | 说话人分离、转写、polish 导出 |

## 样例音频复用

| 目录 | 字幕线 | 转写线 |
|------|--------|--------|
| `data/vr/vr_kavr500_part3.wav` | 主验收（长视频、翻译） | 一般不适用（无说话人标签需求） |
| `data/recording/微信录音 耿瑞香_*.aac` | 中文断句 / 时间轴 | **主验收**（电话、多人、polish） |
| `data/recording/微信录音 景宜_*.aac` | 可选 | 转写 A/B |
| `data/recording/talk_to_mom.aac` | 可选 | 转写 |
