# SenseVoice 本地部署

基于 [SenseVoice.cpp](https://github.com/RapidAI/SenseVoice.cpp) 的本地语音识别，使用 Apple Metal 硬件加速。

## 前置要求

- macOS Apple Silicon
- [pixi](https://pixi.sh/)（已安装）

## 一键部署

```bash
# 1. 安装依赖环境
pixi install

# 2. 编译 C++ 引擎（Metal 加速）
pixi run build

# 3. 下载模型（约 470MB fp16）
pixi run download-model

# 4. 测试
pixi run test
```

## CLI 转写（推荐）

```bash
# wav / mp3 均可，默认带时间戳和标点
pixi run sv models/asr_example_zh.wav
pixi run sv your-audio.mp3

# 输出示例：
# [0.96-5.18] 欢迎大家来体验...
#
# 音频 5.5s | 处理 0.4s | RTF 0.076
```

## 底层命令行

```bash
./SenseVoice.cpp/build/bin/sense-voice-main \
  -m models/sense-voice-small-fp16.gguf \
  models/asr_example_zh.wav \
  -t 4
```

## Python 接口

```python
import sys
sys.path.insert(0, "python")

from sense_voice import SenseVoice

sv = SenseVoice(use_gpu=True)  # Metal GPU 加速
text = sv.transcribe("models/asr_example_zh.wav")
print(text)
```

或在 pixi 环境中：

```bash
pixi run python -c "
import sys; sys.path.insert(0, 'python')
from sense_voice import SenseVoice
print(SenseVoice().transcribe('models/asr_example_zh.wav'))
"
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `SENSE_VOICE_MODEL` | 模型路径，默认 `models/sense-voice-small-fp16.gguf` |
| `SENSE_VOICE_BIN` | 可执行文件路径，默认 `SenseVoice.cpp/build/bin/sense-voice-main` |
