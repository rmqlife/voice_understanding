# 开发规范

开发与 GPU 测试均在 **mag** 本机完成，无 Mac ↔ mag 同步流程。

Agent 文档目录：**`.agent/`**（本文件及下方索引均在仓库根目录 `.agent/` 下）。

| 文档 | 内容 |
|------|------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | 三层产品线、代码归属、仓库结构 |
| [`GIT.md`](GIT.md) | 提交、分支、不要进 Git 的内容 |
| [`TEST.md`](TEST.md) | 冒烟测试、字幕/转写验收、产物路径 |
| [`TODO-core.md`](TODO-core.md) | ASR、音频、LLM 公共底层 |
| [`TODO-subtitle.md`](TODO-subtitle.md) | 字幕时间轴、SRT、翻译 |
| [`TODO-transcript.md`](TODO-transcript.md) | 说话人转写、polish |
| [`MODELS.md`](MODELS.md) | 模型缓存与预下载 |
| [`REFERENCE.md`](REFERENCE.md) | 外部参考仓库 |

## 环境

| 项 | 值 |
|----|-----|
| 工作目录 | `/home/rmqlife/work/voice_understanding` |
| 远程仓库 | `git@github.com:rmqlife/voice_understanding.git` |
| 默认分支 | `main`（FunASR official，`cuda:0`） |
| 本地 LLM | Ollama，常用 `nsfw-local:27b` |

`mac` 分支含 SenseVoice.cpp + Metal；`main` 上 cpp 脚本已归档在 [`archive/mac/`](../archive/mac/)。

## 目录约定

| 目录 | 用途 |
|------|------|
| `.agent/` | Agent / 开发规范、架构、TODO（本目录） |
| `python/sense_voice/` | 库：ASR、LLM、SRT、diarize 等 |
| `scripts/` | CLI 入口；冒烟测试在 `scripts/tests/` |
| `data/vr/` | VR 测试音频（gitignore，本地保留） |
| `data/recording/` | 录音/电话样例（仓库内仅跟踪 `sunflower.mp3`） |
| `results/` | 字幕 / 转写运行产物（本地 only，不进 Git） |
| `benchmark/` | LLM benchmark（本地 only，不进 Git） |
| `tasks/` | 批量 `*.toml`（本地 only，不进 Git） |
| `docs/` | 技术备忘（`fbank_lfr_cmvn_feature.md`、`wav-to-srt.html` 等） |

## 日常流程

1. 在 mag 上改代码。
2. 无 GPU 改动先跑 `pixi run test-srt`（及必要时 `test-transcript`）。
3. 字幕/转写相关改动跑完整验收（见 [`TEST.md`](TEST.md)）。
4. 满意后按 [`GIT.md`](GIT.md) 提交 push。

## 代码与架构约定

### 字幕时间轴

- 思路：**先文本、后时间** — ASR 字符时间戳 → 拆句/润色 → 重对齐回时间轴。
- 官方 ASR：`output_timestamp=True`，`char_timestamp` 为主时间源。
- 不用「按字符比例摊满全音频」做 SRT 烧录；仅作 `timing_confidence=low` 占位。
- 字幕线验收标准：[`TODO-subtitle.md`](TODO-subtitle.md)；转写：[`TODO-transcript.md`](TODO-transcript.md)；底层：[`TODO-core.md`](TODO-core.md)。

### 参考实现

- KrillinAI 在 `reference/KrillinAI/`（不提交），对照 `timestamps.go`、`audio2subtitle.go`。
- 新功能优先扩展现有模块与脚本，不平行造轮子。

### 代码风格

- **最小 diff**：只改与任务相关的文件。
- 匹配周边命名与结构；避免多余抽象。
- 注释只写非显而易见的逻辑。
- 除非用户要求，不扩写无关文档。

## 常用命令

```bash
cd /home/rmqlife/work/voice_understanding

pixi run sv data/recording/sunflower.mp3 --backend official --device cuda:0 -l zh
pixi run test-srt
pixi run vr-subtitle-test -- --clip data/vr/vr_savr_799_sample.wav --asr-backend official --asr-device cuda:0
```

完整测试说明见 [`TEST.md`](TEST.md)。
