# mac 分支：SenseVoice.cpp 本地 ASR

`mac` 分支在仓库内 **vendor `SenseVoice.cpp/`**，用于 macOS Apple Silicon + Metal（或本地 CPU）跑 `cpp` 后端。

`main` 分支已移除 `SenseVoice.cpp`，默认使用 **FunASR `official`**（mag / Linux GPU）。

## 使用本分支

```bash
git checkout mac
pixi install
pixi run build          # 编译 SenseVoice.cpp → build/bin/sense-voice-main
pixi run download-model # GGUF 模型

pixi run sv models/asr_example_zh.wav --backend cpp
pixi run test-srt       # 无需 GPU
```

默认环境变量：`SENSE_VOICE_BACKEND=cpp`（`transcribe.py` 默认）。

## 与 main 同步

```bash
git checkout mac
git merge main          # 合并字幕/转写等业务改动
# 保留 SenseVoice.cpp/，不要从 main 侧删除该目录
git push origin mac
```

## 路径约定

| 项 | mac 分支 |
|----|----------|
| C++ 源码 | `SenseVoice.cpp/`（在 git 内） |
| 可执行文件 | `SenseVoice.cpp/build/bin/sense-voice-main` |
| GGUF 模型 | `models/sense-voice-small-fp16.gguf` |

可选参考 clone（不提交）：`reference/KrillinAI` 等，见 `.gitignore`。
