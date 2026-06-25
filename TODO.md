# TODO 索引

仓库结构与产品线划分见 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)，开发规范见 [`docs/RULE.md`](docs/RULE.md)。

## 目录速览

| 目录 | 内容 |
|------|------|
| `python/sense_voice/` | 库：ASR、音频、LLM、diarize、SRT、transcript |
| `scripts/` | CLI 入口（扁平，见 [`scripts/README.md`](scripts/README.md)） |
| `benchmark/` | LLM benchmark 代码 + 数据 + 结论 |
| `tests/` | 无 GPU 冒烟测试 |
| `reports/` | 字幕 / 转写运行产物（从 mag 回传） |
| `docs/` | 架构、规范、分轨 TODO |
| `archive/` | 已归档实验（pyannote、mac/cpp、vad） |

## 分轨 TODO

| 轨道 | 文件 | 用途 |
|------|------|------|
| **Core** | [`docs/TODO-core.md`](docs/TODO-core.md) | ASR、音频、LLM 公共底层 |
| **Subtitle** | [`docs/TODO-subtitle.md`](docs/TODO-subtitle.md) | 字幕时间轴、SRT、翻译、显示切分 |
| **Transcript** | [`docs/TODO-transcript.md`](docs/TODO-transcript.md) | 说话人转写、polish、电话/微信语音 |

## 快速判断改哪份 TODO

- 改 `transcribe.py`、VAD、字符时间戳、`sv.py` → **Core**
- 改 SRT、对齐、断句、烧录时间轴、KAVR/VR → **Subtitle**
- 改说话人分离、按人切分、转写 md、电话润色 → **Transcript**
