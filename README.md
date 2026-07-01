# SenseVoice 本地语音理解

**分支说明**

| 分支 | ASR 后端 | 说明 |
|------|----------|------|
| **`main`** | `official`（FunASR / CUDA） | mag GPU 测试、字幕/转写主线；**不含** SenseVoice.cpp |
| **`mac`** | `cpp`（SenseVoice.cpp + Metal） | Mac 本地开发；仓库内 vendor `SenseVoice.cpp/` |

Mac 上请 `git checkout mac`；`main` 上的 cpp/Metal 辅助脚本已归档到 [`archive/mac/`](archive/mac/)。

本 README 以下以 **`main` / `official`** 为准。

## 三条产品线

同一仓库、一套 ASR 底层，上层按用途拆成三条线（详见 [`.agent/ARCHITECTURE.md`](.agent/ARCHITECTURE.md)）：

| 产品线 | 核心问题 | 典型输出 | 主入口 |
|--------|----------|----------|--------|
| **Core** | 音频 → 文本 | text / json | `pixi run sv` |
| **Subtitle** | 什么时候显示什么字 | `.asr.srt` + `.zh.srt` | `pixi run add-subtitle` / `vr-subtitle-test` |
| **Transcript** | 谁说了什么 | `.md` / `.json` | `pixi run transcript-test` |

## 项目结构

| 目录 | 内容 |
|------|------|
| `.agent/` | Agent 文档：架构、规范、测试与分轨 TODO |
| `python/sense_voice/` | 库：ASR、音频、LLM、SRT、字幕、转写 |
| `scripts/` | 扁平 CLI 入口（见 [`scripts/README.md`](scripts/README.md)） |
| `scripts/tests/` | 无 GPU 冒烟测试 |
| `tasks/` | 字幕批量任务 `*.toml`（本地生成，不进 Git） |
| `data/` | 本地音频：`data/vr`（VR）、`data/recording`（录音/电话） |
| `results/` | 字幕 / 转写运行产物（**本地 only**，不进 Git） |
| `benchmark/` | LLM benchmark 脚本与报告（**本地 only**，不进 Git） |
| `docs/` | 技术备忘（`wav-to-srt.html` 等，非 Agent 入口） |
| `archive/` | 已归档实验（pyannote / mac-cpp / vad） |

## Linux GPU 官方包（main）

```bash
pixi install
pixi run install-gpu

pixi run sv data/recording/sunflower.mp3 \
  --backend official \
  --device cuda:0 \
  -l zh
```

默认官方模型是 `iic/SenseVoiceSmall`。也可以用环境变量或参数覆盖：

```bash
SENSE_VOICE_BACKEND=official SENSE_VOICE_DEVICE=cuda:0 pixi run sv your-audio.wav
pixi run sv your-audio.wav --backend official --device cuda:0 --model iic/SenseVoiceSmall
```

## VR 字幕流水线（Subtitle）

NFS `jav/#finished` 下的 VR mp4 → 本地 WAV → ASR + 日文→中文翻译 → SRT 回写 NFS。

```bash
# 单文件全流程（日文 ASR + LLM 翻译，默认 profile=vr）
pixi run add-subtitle -- \
  --video "/mnt/fnos/jav/#finished/SAVR-xxx/SAVR-xxx.mp4" \
  --language ja --profile vr

# 扫描 #finished 批量处理（跳过已有 SRT）
pixi run add-subtitle -- --scan-finished --skip-existing

# 推荐：生成 task.toml 后逐个跑（可编辑、断点续跑）
pixi run gen-subtitle-task -- --scan-finished --name-filter vr -o tasks/vr_batch.toml
pixi run run-subtitle-task -- tasks/vr_batch.toml
pixi run run-subtitle-task -- tasks/vr_batch.toml --from 5 --continue-on-error
```

分步调试：`--extract-only` / `--subtitle-only` / `--publish-only` / `--repolish-only`。

GPU 上 ASR 与 Ollama LLM 通过 `gpu.py` 文件锁串行（`data/.subtitle_gpu.lock`），避免显存争抢。

字幕指标验收：

```bash
pixi run vr-subtitle-test -- \
  --clip data/vr/vr_kavr500_part3.wav \
  --report results/subtitle/metrics/kavr_part3_subtitle_metrics.md \
  --asr-backend official --asr-device cuda:0 \
  --language ja
```

产物默认写到本地 `results/`（不进 Git）。详细流程见 [`.agent/TODO-subtitle.md`](.agent/TODO-subtitle.md)。

## 转写线（Transcript）

微信录音 / 电话样例：说话人分离 + ASR + polish → md/json。

```bash
pixi run transcript-test -- \
  --clip "data/recording/微信录音 耿瑞香_20250326090128_45748064860651968.aac" \
  --report results/transcript/geng_ruixiang_p1_metrics.md \
  --asr-backend official --asr-device cuda:0
```

## 冒烟测试

改 SRT / 时间轴 / 转写逻辑后先跑无 GPU 测试：

```bash
pixi run test-srt
pixi run test-transcript
pixi run test-vr-sources
pixi run test-subtitle-task
```

规范见 [`.agent/TEST.md`](.agent/TEST.md)。

## macOS / SenseVoice.cpp

请使用 **`mac` 分支**（含 `SenseVoice.cpp/`）。`main` 上的构建/下载脚本已归档在
[`archive/mac/`](archive/mac/)（`build.sh`、`download_model.py`、`MAC.md`），仅供参考。

## Python 接口

```python
import sys
sys.path.insert(0, "python")

from sense_voice import SenseVoice

sv = SenseVoice(backend="official", device="cuda:0", language="zh")
print(sv.transcribe("data/recording/sunflower.mp3"))
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
| `VR_JAV_ROOT` | 已挂载的 NFS/gvfs VR 根路径 |
| `VR_NFS_HOST` | NFS 主机（默认 `192.168.1.188`） |

## 开发文档

| 文件 | 用途 |
|------|------|
| [`TODO.md`](TODO.md) | 分轨 TODO 索引 |
| [`.agent/ARCHITECTURE.md`](.agent/ARCHITECTURE.md) | 三层产品线架构 |
| [`.agent/RULE.md`](.agent/RULE.md) | 开发规范 |
| [`.agent/TEST.md`](.agent/TEST.md) | 测试规范与产物路径 |
| [`.agent/GIT.md`](.agent/GIT.md) | 提交与协作规范 |
