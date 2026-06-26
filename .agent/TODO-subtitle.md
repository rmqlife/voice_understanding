# 字幕设计 TODO

NFS VR 字幕流水线（`192.168.1.188` / `atop-nuc-fnos.local` → gvfs `jav/#finished`）。

## 流程（已实现）

对每个 VR mp4（`scripts/add_subtitle.sh` 或 `pixi run add-subtitle`）：

1. **抽音轨**：ffmpeg 直读 NFS mp4（不拷贝视频）→ `data/vr/<stem>.wav`
2. **生成字幕**：ASR + LLM 润色 → `results/srt/<stem>.{asr,zh}.srt`
3. **回写**：SRT 复制到 mp4 同目录（gvfs 用 `copyfile`）

核心模块：

| 模块 | 职责 |
|------|------|
| `python/sense_voice/vr_sources.py` | 挂载检测、`#finished` 扫描、VR mp4 过滤、本地路径 |
| `scripts/sync_vr_audio.py` | 仅抽 WAV（`--scan-finished` / `--input`） |
| `scripts/add_subtitle.py` | 三步合一；支持 `--extract-only` / `--subtitle-only` / `--publish-only` |
| `scripts/gen_subtitle_task.py` | 扫描或指定 mp4 → 写出 `task.toml` |
| `scripts/run_subtitle_task.py` | 读取 `task.toml`，逐个跑全流程 |
| `scripts/add_subtitle.sh` | `pixi run add-subtitle` 薄封装 |

## 常用命令

```bash
cd /home/rmqlife/work/voice_understanding

# 列出 #finished 下匹配的 VR mp4
pixi run sync-vr-audio -- --scan-finished --name-filter MANX --list-only

# 单文件全流程（**不要**加 --skip-polish，否则 .zh.srt 只是日文原文副本）
pixi run add-subtitle -- \
  --video "/run/user/.../SAVR-xxx/SAVR-xxx.mp4" \
  --language ja --profile vr

# 批量（#finished 下所有 VR mp4）
pixi run add-subtitle -- --scan-finished --skip-existing

# 推荐：先生成 task.toml，再逐个处理（可编辑列表、断点续跑）
pixi run gen-subtitle-task -- --scan-finished --name-filter vr -o tasks/vr_batch.toml
pixi run run-subtitle-task -- tasks/vr_batch.toml
pixi run run-subtitle-task -- tasks/vr_batch.toml --from 5 --continue-on-error

# 分步调试
pixi run add-subtitle -- --video <mp4> --extract-only
pixi run add-subtitle -- --video <mp4> --subtitle-only --skip-polish
pixi run add-subtitle -- --video <mp4> --publish-only
```

环境变量：`VR_JAV_ROOT`（已挂载根路径）、`VR_NFS_HOST`（默认 `192.168.1.188`）、`VR_NFS_SERVER_NAME`（默认 `atop-nuc-fnos.local`）。

## 验收

- [x] `pixi run test-vr-sources` — 路径与 VR 过滤
- [x] 流水线冒烟：抽音轨 → SRT → 回写（曾用 `MANX-024-C` + `--skip-polish` 测通路，**非 VR 样例**）
- [ ] 用真实 VR mp4（SAVR/KAVR/…）跑完整流程（含 LLM 日文→中文，**无** `--skip-polish`）
- [ ] `--scan-finished` 批量跑完 `#finished`

测试规范见 [`.agent/TEST.md`](TEST.md)。

## 批量运行（task.toml）

1. **生成任务文件**（列出具体 mp4 path，可按需手工编辑 `enabled = false` 跳过条目）：

```bash
pixi run gen-subtitle-task -- --scan-finished --name-filter vr -o tasks/vr_batch.toml
# 或指定文件
pixi run gen-subtitle-task -- --video "/run/user/.../SAVR-xxx.mp4" -o tasks/one.toml
```

2. **按列表逐个处理**：

```bash
pixi run run-subtitle-task -- tasks/vr_batch.toml
# 从第 5 条继续；单条失败不中断
pixi run run-subtitle-task -- tasks/vr_batch.toml --from 5 --continue-on-error
```

`task.toml` 结构：`[defaults]` 为 ASR/LLM 参数，`[[videos]]` 每行一个 `path`（须位于 `jav/#finished` 下）。生成时按路径字母序排列；`results/srt/` 中已有 `.asr.srt` + `.zh.srt` 的条目会标为 `enabled = false`（`note = "srt exists"`），`run-subtitle-task` 会跳过。

日志可重定向：`pixi run run-subtitle-task -- tasks/vr_batch.toml >> results/subtitle/logs/vr_batch.log 2>&1`
