# TODO 索引

仓库结构与产品线划分见 [`.agent/ARCHITECTURE.md`](.agent/ARCHITECTURE.md)，开发规范见 [`.agent/RULE.md`](.agent/RULE.md)。

## 目录速览

| 目录 | 内容 |
|------|------|
| `.agent/` | Agent 文档：架构、规范、分轨 TODO |
| `python/sense_voice/` | 库：ASR、音频、LLM、diarize、SRT、transcript |
| `scripts/` | CLI 入口（扁平，见 [`scripts/README.md`](scripts/README.md)） |
| `scripts/tests/` | 无 GPU 冒烟测试 |
| `data/` | 本地音频（`vr` / `recording`） |
| `results/` | 字幕 / 转写运行产物（本地 only，不进 Git） |
| `benchmark/` | LLM benchmark 脚本与报告（本地 only，不进 Git） |
| `docs/` | 技术备忘（非 Agent 入口） |
| `archive/` | 已归档实验（pyannote、mac/cpp、vad） |

## 分轨 TODO

| 轨道 | 文件 | 用途 |
|------|------|------|
| **Core** | [`.agent/TODO-core.md`](.agent/TODO-core.md) | ASR、音频、LLM 公共底层 |
| **Subtitle** | [`.agent/TODO-subtitle.md`](.agent/TODO-subtitle.md) | 字幕时间轴、SRT、翻译、显示切分 |
| **Transcript** | [`.agent/TODO-transcript.md`](.agent/TODO-transcript.md) | 说话人转写、polish、电话/微信语音 |

## 快速判断改哪份 TODO

- 改 `transcribe.py`、VAD、字符时间戳、`sv.py` → **Core**
- 改 SRT、对齐、断句、烧录时间轴、KAVR/VR → **Subtitle**
- 改说话人分离、按人切分、转写 md、电话润色 → **Transcript**
