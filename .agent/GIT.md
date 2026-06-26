# Git 规范

开发与测试均在 mag 本机；改完、验过后直接在本仓库 commit / push。

## 仓库信息

```text
路径:   /home/rmqlife/work/voice_understanding
远程:   git@github.com:rmqlife/voice_understanding.git
分支:   main（FunASR official）
```

## 提交流程

1. 确认相关测试已通过（见 [`TEST.md`](TEST.md)）。
2. 只 stage 与本次改动相关的文件。
3. 提交并推送：

```bash
git add <相关文件>
git commit -m "简短说明 why"
git push origin main
```

多人或多机协作时，开工前先 `git pull`，避免覆盖他人提交。

## 提交原则

- **只在需要留存或用户明确要求时 commit**；不提交半成品。
- 提交信息写 **why**，一两句即可。
- 不要 `git push --force` 到 `main`。
- 不要改 `git config`、不要 skip hooks（`--no-verify` 等）。

## 不要进 Git 的内容

`.gitignore` 已覆盖，提交前再确认：

| 路径 | 说明 |
|------|------|
| `reference/` | 外部参考克隆（KrillinAI 等），见 [`.agent/REFERENCE.md`](REFERENCE.md) |
| `SenseVoice.cpp/` | 仅 `mac` 分支 vendor；`main` 无 |
| `data/vr/*` | VR 长音频（保留 `data/vr/.gitkeep`） |
| `data/recording/*` | 录音样例（仅 `sunflower.mp3` 可跟踪） |
| `models/`、`.pixi/` | 模型权重、pixi 环境 |
| `*.wav`、`*.aac`、大部分 `*.mp3` | 大媒体文件 |
| `results/` | 字幕 / 转写运行产物（SRT、指标、日志） |
| `benchmark/` | LLM benchmark 脚本与报告 |

`results/`、`benchmark/` 整目录不进 Git；产物留在本机，多机用 `sync-results-from-mag` 或各自本地跑。

## pull 时有本地未提交改动

```bash
git stash push -u -m "wip"
git pull
git stash pop
```

有冲突时先解决再继续开发；长期有用的脚本/配置应合入 `main`，一次性数据留在 `data/` / `results/` 并保持 ignore。

## 分支说明

| 分支 | 用途 |
|------|------|
| `main` | mag GPU、字幕/转写主线（本规范默认） |
| `mac` | SenseVoice.cpp + Metal 本地 ASR |

在 `main` 上不要引入 SenseVoice.cpp vendor；Mac 专用脚本见 `archive/mac/`。
