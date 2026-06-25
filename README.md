# SenseVoice 本地语音理解

**分支说明**

| 分支 | ASR 后端 | 说明 |
|------|----------|------|
| **`main`** | `official`（FunASR / CUDA） | mag GPU 测试、字幕/转写主线；**不含** SenseVoice.cpp |
| **`mac`** | `cpp`（SenseVoice.cpp + Metal） | Mac 本地开发；仓库内 vendor `SenseVoice.cpp/` |

Mac 上请 `git checkout mac`；`main` 上的 cpp/Metal 辅助脚本已归档到 [`archive/mac/`](archive/mac/)。

本 README 以下以 **`main` / `official`** 为准。

项目结构（详见 [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)）：

| 目录 | 内容 |
|------|------|
| `python/sense_voice/` | 库：所有共享逻辑 |
| `scripts/` | 扁平 CLI 入口（见 [`scripts/README.md`](scripts/README.md)） |
| `benchmark/` | LLM benchmark 代码 + 数据 + 结论 |
| `tests/` | 无 GPU 冒烟测试 |
| `reports/` | 字幕 / 转写运行产物 |
| `archive/` | 已归档实验（pyannote / mac-cpp / vad） |

## Linux GPU 官方包（main）

```bash
pixi install
pixi run install-gpu

pixi run sv test_voice_clips/sunflower.mp3 \
  --backend official \
  --device cuda:0 \
  -l zh
```

默认官方模型是 `iic/SenseVoiceSmall`。也可以用环境变量或参数覆盖：

```bash
SENSE_VOICE_BACKEND=official SENSE_VOICE_DEVICE=cuda:0 pixi run sv your-audio.wav
pixi run sv your-audio.wav --backend official --device cuda:0 --model iic/SenseVoiceSmall
```

## macOS / SenseVoice.cpp

请使用 **`mac` 分支**（含 `SenseVoice.cpp/`）。`main` 上的构建/下载脚本已归档在
[`archive/mac/`](archive/mac/)（`build.sh`、`download_model.py`、`MAC.md`），仅供参考。

## 本地 LLM Benchmark

Benchmark 会执行：

1. SenseVoice ASR
2. 解析 SenseVoice 标签，生成结构化时间线
3. 本地 Ollama LLM 中文润色
3. 英文翻译
4. 质量自评

使用官方 GPU ASR 和本地 `qwen3.5:latest`：

```bash
pixi run benchmark -- \
  --asr-backend official \
  --asr-device cuda:0 \
  --model qwen3.5:latest \
  --language zh
```

可以为不同步骤配置不同 Ollama 模型：

```bash
pixi run benchmark -- \
  --asr-backend official \
  --asr-device cuda:0 \
  --polish-model qwen3.5:latest \
  --translate-model qwen3.5:latest \
  --assess-model qwen3.5:latest \
  --profile finance \
  --language zh
```

benchmark 代码、数据和结论都在 [`benchmark/`](benchmark/)；默认报告输出到 `benchmark/reports/voice_llm_benchmark.md`。

## VR / 视频音轨 Benchmark

先把视频或 VR 文件提取成 benchmark 用的 16 kHz mono WAV：

```bash
pixi run extract-audio -- \
  /path/to/KAVR-or-other-vr-file.mp4 \
  test_voice_clips/vr_sample.wav \
  --duration 180
```

然后用 VR prompt profile 和本地 NSFW LLM：

```bash
pixi run benchmark -- \
  --clip test_voice_clips/vr_sample.wav \
  --report benchmark/reports/vr_audio_benchmark.md \
  --asr-backend official \
  --asr-device cuda:0 \
  --model nsfw-local:27b \
  --profile vr \
  --language ja \
  --chunk-chars 1200
```

`profile=vr` 会保留时间线、SenseVoice 标签和音频事件，不会把内容改写成无时间戳散文。

## Python 接口

```python
import sys
sys.path.insert(0, "python")

from sense_voice import SenseVoice

sv = SenseVoice(backend="official", device="cuda:0", language="zh")
print(sv.transcribe("test_voice_clips/sunflower.mp3"))
```

Mac C++ 示例见 `mac` 分支。

## 环境变量

| 变量 | 说明 |
|------|------|
| `SENSE_VOICE_BACKEND` | `official`（main 默认）或 `cpp`（mac 分支） |
| `SENSE_VOICE_DEVICE` | 官方后端设备，例如 `cuda:0` 或 `cpu` |
| `SENSE_VOICE_MODEL` | 官方模型名或 C++ GGUF 模型路径 |
| `SENSE_VOICE_BIN` | C++ 可执行文件路径（仅 `cpp` 后端） |
| `SENSE_VOICE_CPP_ROOT` | C++ 源码目录（可选 clone 到 `reference/SenseVoice.cpp`） |
