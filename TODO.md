# TODO 索引

本仓库按产品线分轨管理待办，详见 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)。

| 轨道 | 文件 | 用途 |
|------|------|------|
| **Core** | [`docs/TODO-core.md`](docs/TODO-core.md) | ASR、音频、LLM 公共底层 |
| **Subtitle** | [`docs/TODO-subtitle.md`](docs/TODO-subtitle.md) | 字幕时间轴、SRT、翻译、显示切分 |
| **Transcript** | [`docs/TODO-transcript.md`](docs/TODO-transcript.md) | 说话人转写、polish、电话/微信语音 |
| **Mac cpp** | [`docs/MAC.md`](docs/MAC.md) | `mac` 分支 SenseVoice.cpp 后端 |
| **参考 clone** | [`docs/REFERENCE.md`](docs/REFERENCE.md) | `reference/` 外部仓库 |

## 快速判断改哪份 TODO

- 改 `transcribe.py`、VAD、字符时间戳、`sv.py` → **Core**
- 改 SRT、对齐、断句、烧录时间轴、KAVR/VR → **Subtitle**
- 改说话人分离、按人切分、转写 md、电话润色 → **Transcript**

开发规范与工作流见 [`RULE.md`](RULE.md)。
