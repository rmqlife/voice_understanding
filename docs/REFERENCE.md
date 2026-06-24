# 外部参考仓库（不提交 git）

`reference/` 目录在 `.gitignore` 中，用于本地 clone 对照或可选依赖。

```bash
mkdir -p reference

# 字幕时间轴设计参考（只读）
git clone https://github.com/krillinai/KrillinAI reference/KrillinAI

# 可选：main 上本地编译 cpp 后端（推荐 Mac 直接用 mac 分支）
git clone https://github.com/lovemefan/SenseVoice.cpp reference/SenseVoice.cpp
pixi run build   # 产物：reference/SenseVoice.cpp/build/bin/sense-voice-main
```

| 路径 | 用途 | 是否在 main git |
|------|------|-----------------|
| `reference/KrillinAI` | KrillinAI 字幕 pipeline 对照 | 否 |
| `reference/SenseVoice.cpp` | 可选 C++ ASR 编译 | 否 |
| `SenseVoice.cpp/`（仓库根） | **仅 `mac` 分支** vendor | mac 分支是 |

## ASR Backend 选择

| Backend | 分支 / 机器 | 说明 |
|---------|-------------|------|
| `official` | `main`、mag | FunASR `iic/SenseVoiceSmall`，CUDA，`output_timestamp=True` |
| `cpp` | `mac` 分支 | SenseVoice.cpp GGUF + Metal；`main` 上需 `reference/SenseVoice.cpp` 可选编译 |

```bash
# mag / main（默认 official）
pixi run sv audio.wav -l zh --backend official --device cuda:0 --output-format json

# Mac cpp（checkout mac 分支）
pixi run sv audio.wav -l zh --backend cpp
```

环境变量：`SENSE_VOICE_BACKEND`、`SENSE_VOICE_DEVICE`、`SENSE_VOICE_MODEL`。
