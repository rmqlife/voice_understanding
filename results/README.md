# results/ 目录说明

测试产物输出目录，路径见 [`.agent/TEST.md`](../.agent/TEST.md)。

## 目录结构

```
results/
├── README.md              ← 本文件
├── srt/                   ← 字幕烧录用（.asr.srt + .zh.srt）
├── subtitle/
│   ├── metrics/           ← vr-subtitle-test 指标 .md + .json
│   └── logs/              ← 运行 tee 日志
└── transcript/            ← 转写线 md/json + 指标
    └── logs/              ← 运行 tee 日志
```

> LLM benchmark 报告在 [`benchmark/reports/`](../benchmark/reports/)。

## srt/

命名规则：`<作品目录>__<mp4 文件名去扩展名>.{asr,zh}.srt`（`vr_sources.local_wav_path` 生成）。

| 文件 | 来源 |
|------|------|
| `vr_kavr500_part{2,3}.{asr,zh}.srt` | KAVR VR 字幕测试 |
| `vr_savr_799_sample.{asr,zh}.srt` | SAVR 样例 |
| `KAVR-506-伊藤舞雪__KAVR-506-CD*.{asr,zh}.srt` | VR 批量字幕（`tasks/vr_batch.toml`） |
| `DSVR-2001-*`、`MDVR-426-*`、`SAVR-*`、`VRKM-*` 等 | 同上 |
| `微信录音 耿瑞香_*.srt` | 中文断句 / 时间轴测试 |

## subtitle/metrics/

| 文件 | 说明 |
|------|------|
| `kavr_p0_subtitle_metrics.*` | P0 字符时间戳 |
| `kavr_p1_subtitle_metrics.*` | P1 拆句 + 重对齐 |
| `geng_ruixiang_zh_subtitle_metrics.*` | 耿瑞香 v1（无润色） |
| `geng_ruixiang_zh_p2_*` | P2 显示切分 |
| `geng_ruixiang_zh_p2b_*` | P2b 无禁切词表、无 6s 切分 |
| `refactor_smoke_20250625.*` | 字幕模块重构冒烟 |

## transcript/

| 文件 | 说明 |
|------|------|
| `<clip>.md` / `<clip>.json` | 按说话人转写正文 |
| `*_metrics.md` | `transcript-test --report` 指标 |
| `logs/*_run.log` | mag 运行日志 |

## 跑新测试

```bash
# 指标验收
pixi run vr-subtitle-test -- \
  --clip data/vr/vr_kavr500_part3.wav \
  --report results/subtitle/metrics/<run_name>_subtitle_metrics.md \
  --run-label <run_name> \
  --asr-backend official --asr-device cuda:0 \
  --language ja \
  2>&1 | tee results/subtitle/logs/<run_name>_subtitle_run.log

# 生产流水线（NFS mp4 → SRT → 回写）
pixi run add-subtitle -- --video /path/to/video.mp4 --language ja --profile vr
```
