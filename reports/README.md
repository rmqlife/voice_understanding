# reports/ 目录说明

测试产物从 mag 拉回本地后放这里（`pixi run sync-reports-from-mag`）。**默认不进 git**。

## 目录结构

```
reports/
├── README.md              ← 本文件
├── srt/                   ← 字幕烧录用（.asr.srt + .zh.srt）
├── subtitle/
│   ├── metrics/           ← vr-subtitle-test 指标 .md + .json
│   └── logs/              ← 运行 tee 日志
├── benchmark/             ← LLM benchmark 长报告
├── transcript/            ← 转写线 md/json + 指标
│   └── logs/              ← 运行 tee 日志
├── web_llm_tasks/         ← mac 分支 Web LLM 任务导出（可选）
```

## srt/

| 文件 | 来源 |
|------|------|
| `vr_kavr500_part3.{asr,zh}.srt` | KAVR VR 字幕测试 |
| `微信录音 耿瑞香_*.srt` | 中文断句 / 时间轴测试 |

## subtitle/metrics/

| 文件 | 说明 |
|------|------|
| `kavr_p0_subtitle_metrics.*` | P0 字符时间戳 |
| `kavr_p1_subtitle_metrics.*` | P1 拆句 + 重对齐 |
| `geng_ruixiang_zh_subtitle_metrics.*` | 耿瑞香 v1（无润色） |
| `geng_ruixiang_zh_p2_*` | P2 显示切分 |
| `geng_ruixiang_zh_p2b_*` | P2b 无禁切词表、无 6s 切分 |

## transcript/

| 文件 | 说明 |
|------|------|
| `<clip>.md` / `<clip>.json` | 按说话人转写正文 |
| `*_metrics.md` | `transcript-test --report` 指标 |
| `logs/*_run.log` | mag 运行日志 |

## benchmark/

| 文件 | 说明 |
|------|------|
| `vr_audio_benchmark.md` | VR 全量 benchmark |
| `vr_audio_benchmark_kavr500*.md` | KAVR500 各版本报告 |
| `voice_llm_benchmark.md` | 通用 voice+LLM benchmark |

## 在 mag 上跑新测试时

```bash
pixi run vr-subtitle-test -- \
  --clip test_voice_clips/....aac \
  --report reports/subtitle/metrics/<run_name>_subtitle_metrics.md \
  --run-label <run_name> \
  --asr-backend official --asr-device cuda:0 \
  --language zh --skip-polish \
  2>&1 | tee reports/subtitle/logs/<run_name>_subtitle_run.log
```

Mac 上：`pixi run sync-reports-from-mag`
