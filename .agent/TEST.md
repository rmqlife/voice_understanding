# 测试规范

所有测试在 mag 本机执行：`cd /home/rmqlife/work/voice_understanding`。

## 测试音频（`data/`）

| 目录 | 内容 | 示例 |
|------|------|------|
| `data/vr/` | VR 长样例 | `vr_kavr500_part3.wav`、`vr_savr_799_sample.wav` |
| `data/recording/` | 录音/电话 | `sunflower.mp3`、`微信录音 耿瑞香_*.aac` |

从 NFS 跑 VR 字幕全流程（`jav/#finished`，不拷贝 mp4）：

```bash
# 全流程：抽音轨 → 字幕 → 回写 NFS
pixi run add-subtitle -- --video /path/to/video.mp4
```

## 无 GPU 冒烟测试

改 SRT/时间轴/转写拼装逻辑后先跑：

```bash
pixi run test-srt          # 字幕切分与时间戳（推荐每次必跑）
pixi run test-transcript   # 转写 turn 拼装
pixi run test              # 小样 ASR（需 GPU + official 依赖）
```

脚本位置：`scripts/tests/`。

## VR 字幕测试（主验收）

与时间轴、润色、SRT 烧录相关的改动，跑完整管线：

```bash
pixi run vr-subtitle-test -- \
  --clip data/vr/vr_savr_799_sample.wav \
  --report results/subtitle/metrics/<run_label>_subtitle_metrics.md \
  --run-label <run_label> \
  --asr-backend official --asr-device cuda:0 \
  --polish-model nsfw-local:27b \
  --language ja \
  --profile vr \
  --chunk-chars 3000 \
  --llm-timeline compact \
  2>&1 | tee results/subtitle/logs/<run_label>_subtitle_run.log
```

批量 KAVR：

```bash
pixi run vr-subtitle-test -- \
  --clips data/vr --name-filter kavr \
  --report results/subtitle/metrics/kavr_p0_subtitle_metrics.md \
  --run-label kavr_p0 \
  --asr-backend official --asr-device cuda:0 \
  --polish-model nsfw-local:27b \
  --language ja
```

快速验证（跳过 LLM）：

```bash
pixi run vr-subtitle-test -- \
  --clip data/recording/微信录音\ 耿瑞香_20250326090128_45748064860651968.aac \
  --skip-polish --language zh \
  --report results/subtitle/metrics/geng_skip_polish_metrics.md
```

### 必须产出

| 产物 | 默认路径 | 检查点 |
|------|----------|--------|
| ASR SRT | `results/srt/<clip>.asr.srt` | 时间切分、原文 |
| 中文 SRT | `results/srt/<clip>.zh.srt` | 润色与烧录行宽 |
| 指标 MD | `results/subtitle/metrics/<run>_subtitle_metrics.md` | 耗时、segments、p50/p95、>10s/>30s |
| 指标 JSON | 同上 `.json` | 机器可读对比 |
| 运行日志 | `results/subtitle/logs/<run>_subtitle_run.log` | 排错（`tee` 可选） |

指标至少包含：**音频时长、ASR/LLM 耗时、segment 数、timing_source、时长分位数、SRT 条数**。

## 转写测试

见 [`.agent/TODO-transcript.md`](TODO-transcript.md)。

```bash
pixi run transcript-test -- \
  --clip "data/recording/微信录音 耿瑞香_20250326090128_45748064860651968.aac" \
  --diarize-method funasr \
  --asr-backend official --asr-device cuda:0 \
  --language zh \
  --polish-model nsfw-local:27b \
  --run-label geng_ruixiang_p1 \
  --report results/transcript/geng_ruixiang_p1_metrics.md \
  2>&1 | tee results/transcript/logs/geng_ruixiang_p1_run.log
```

产物：`results/transcript/<clip>.md` + `.json`（与 `results/srt/` 分开）。

## `results/` 布局

```
results/
├── srt/                    # .asr.srt + .zh.srt
├── subtitle/
│   ├── metrics/            # vr-subtitle-test 指标
│   └── logs/
└── transcript/             # 转写 md/json + 指标
    └── logs/
```

详表见本地 `results/README.md`（不进 Git）。

## 改哪条线跑什么

| 改动范围 | 最少测试 |
|----------|----------|
| `srt.py`、`subtitle.py`、`timestamps.py` | `test-srt` + `vr-subtitle-test` |
| `transcript.py`、`diarize.py` | `test-transcript` + `transcript-test` |
| `transcribe.py`、`asr_cli.py`、`sv.py` | `test` 或 `sv` 小样 + 受影响产品线的完整测试 |
| 仅文档 / 注释 | 相关冒烟测试（如有） |

## 决策记录

- 长 VR（20min+）全量在 mag 跑；小样用 `vr_savr_799_sample.wav`（~3min）做快速回归。
- 每个验收 clip 产出 **`.asr.srt` + `.zh.srt`** 一对。
- 满意后再决定是否把某次本地 `results/` 报告留存备份（见 [`GIT.md`](GIT.md)）。
