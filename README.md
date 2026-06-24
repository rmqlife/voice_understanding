# SenseVoice 本地语音理解

本仓库支持两套 ASR 后端：

- `official`: 官方 SenseVoice/FunASR Python 包，适合 Linux + NVIDIA GPU。
- `cpp`: SenseVoice.cpp GGUF 命令行，适合 macOS Apple Silicon + Metal，也可在 Linux 编译 CUDA/CPU。

## Linux GPU 官方包

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

## macOS SenseVoice.cpp

```bash
pixi install
pixi run build
pixi run download-model

pixi run sv models/asr_example_zh.wav --backend cpp
```

`scripts/build.sh` 会在 macOS 使用 `GGML_METAL=ON`，在 Linux NVIDIA 环境使用 `GGML_CUDA=ON`，否则构建 CPU 版本。

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

使用 macOS C++ 后端：

```bash
pixi run benchmark -- \
  --asr-backend cpp \
  --model qwen3.5:latest \
  --language zh
```

报告输出到 `reports/voice_llm_benchmark.md`。

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
  --report reports/vr_audio_benchmark.md \
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

sv_cpp = SenseVoice(backend="cpp", use_gpu=True)
print(sv_cpp.transcribe("models/asr_example_zh.wav"))
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `SENSE_VOICE_BACKEND` | `cpp` 或 `official`，默认 `cpp` |
| `SENSE_VOICE_DEVICE` | 官方后端设备，例如 `cuda:0` 或 `cpu` |
| `SENSE_VOICE_MODEL` | 官方模型名或 C++ GGUF 模型路径 |
| `SENSE_VOICE_BIN` | C++ 可执行文件路径，默认 `SenseVoice.cpp/build/bin/sense-voice-main` |
