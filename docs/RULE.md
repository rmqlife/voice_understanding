# 开发规范

本仓库的默认工作流：**本地（Mac）改代码 → push 到 GitHub → mag 拉取并跑 GPU 测试 → 把 reports/SRT 回传本地审阅**。

## 机器分工

| 环境 | 主机 | 用途 |
|------|------|------|
| 本地开发 | Mac (`sense-voice/`) | 写代码；**ASR 用 `mac` 分支 cpp 或 mag 上测 official** |
| GPU 测试 | `rmqlife-mag` | 官方 SenseVoice ASR（`cuda:0`）、Ollama（`nsfw-local:27b`）、长音频样例 |

**分支**：`main` = FunASR official（mag）；`mac` = SenseVoice.cpp + Metal（`main` 上 cpp 辅助脚本归档在 [`archive/mac/`](../archive/mac/)）。

mag 上的仓库路径：

```text
/home/rmqlife/work/voice_understanding
```

远程 Git 仓库：

```text
git@github.com:rmqlife/voice_understanding.git
```

默认分支：`main`。

## Git 流程

### 日常开发（本地 → 云端 → mag）

1. 在 Mac 上完成改动并自测（能跑的逻辑尽量本地先过）。
2. 若 mag 上有未 push 的独有改动，先合并或挑有用的部分到本地，**避免 push 后覆盖 mag 上更好的实现**。
3. 提交并 push：

```bash
git add <相关文件>
git commit -m "简短说明 why"
git push origin main
```

4. 在 mag 上同步：

```bash
ssh rmqlife-mag 'cd /home/rmqlife/work/voice_understanding && git pull origin main'
```

5. 在 mag 上跑测试（见下文）。
6. 测试产物回传本地（见「结果回传」）。

### 提交原则

- **只在需要同步或用户明确要求时 commit**；不要随手提交半成品。
- 提交信息写 **why**，一两句即可；focus 在目的，不是文件清单。
- 不要提交：`reference/`、`mag/`、大模型、长音频、密钥（见 `.gitignore`）。
- 不要 `git push --force` 到 `main`。
- 不要改 git config、不要 skip hooks。

### mag 上有本地未跟踪改动时

mag 曾出现过仅存在于机器上的文件（如 `mag/vr_audio_sync/`、`scripts/sync_vr_audio.py`）。处理顺序：

1. 先 `git stash push -u` 或把有用改动拷到本地合并进 `main`。
2. 再 `git pull`。
3. 长期应纳入仓库的脚本/文档，应在 **Mac 上改完 push**；仅机器本地的数据目录保持 ignore。

## 不要进 Git 的内容

`.gitignore` 已包含：

- `reference/` — 外部参考（KrillinAI、可选 SenseVoice.cpp clone），见 [`docs/REFERENCE.md`](docs/REFERENCE.md)
- `SenseVoice.cpp/` — **仅 `mac` 分支** vendor；`main` 已删除
- `mag/` — mag 机器上的同步缓存、大音频等。
- `test_voice_clips/*` — 长 VR 测试音频（仓库内只保留 `sunflower.mp3` 作小样）。
- `models/`、`reference/SenseVoice.cpp/build/`、`.pixi/` 等构建与模型产物。

大音频、benchmark 结果如需共享：**放 mag 或 reports 回传**，不要直接 commit 进仓库（除非用户明确要求归档某次报告）。

## 测试与产物规范

### 转写测试（`docs/TODO-transcript.md`）

```bash
cd /home/rmqlife/work/voice_understanding

pixi run transcript-test -- \
  --clip "test_voice_clips/微信录音 耿瑞香_20250326090128_45748064860651968.aac" \
  --diarize-method funasr \
  --asr-backend official --asr-device cuda:0 \
  --language zh \
  --polish-model nsfw-local:27b \
  --run-label geng_ruixiang_p1 \
  --report reports/transcript/geng_ruixiang_p1_metrics.md \
  2>&1 | tee reports/transcript/logs/geng_ruixiang_p1_run.log
```

产物：`reports/transcript/<clip>.md` + `.json`（与 `reports/srt/` 分开）。

### VR 字幕测试（推荐入口）

每次与字幕时间轴相关的改动，在 mag 上跑：

```bash
cd /home/rmqlife/work/voice_understanding

pixi run vr-subtitle-test -- \
  --clips test_voice_clips --name-filter kavr \
  --report reports/subtitle/metrics/kavr_p0_subtitle_metrics.md \
  --run-label <简短标签> \
  --asr-backend official --asr-device cuda:0 \
  --polish-model nsfw-local:27b \
  --language ja \
  --chunk-chars 3000 \
  --llm-timeline compact
```

**每次测试必须产出：**

| 产物 | 路径 | 用途 |
|------|------|------|
| ASR 时间轴 SRT | `reports/srt/<clip>.asr.srt` | 检查时间切分是否准确（原文） |
| 中文 SRT | `reports/srt/<clip>.zh.srt` | 检查润色与烧录效果 |
| 指标报告 | `reports/subtitle/metrics/<run>_subtitle_metrics.md` | 耗时、segments、p50/p95、>10s/>30s |
| JSON 指标 | `reports/subtitle/metrics/<run>_subtitle_metrics.json` | 机器可读、便于对比 |
| 运行日志 | `reports/subtitle/logs/<run>_subtitle_run.log` | 排错（可选 `tee`） |

指标报告至少包含：**audio 时长、ASR/LLM wall time、segment 数、timing_source、p50/p95/max、>10s/>30s 条数、SRT 条目数**。

完整 LLM benchmark 仍可用：

```bash
pixi run benchmark -- --clip ... --report benchmark/reports/... --srt-dir reports/srt ...
```

### 结果回传（mag → Mac）

测试结束后 **必须** 把 `reports/` 拉回本地审阅：

```bash
# Mac 上
pixi run sync-reports-from-mag
```

等价于：

```bash
rsync -avz rmqlife-mag:/home/rmqlife/work/voice_understanding/reports/ ./reports/
```

环境变量可覆盖：

- `MAG_HOST`（默认 `rmqlife-mag`）
- `MAG_REPO`（默认 `/home/rmqlife/work/voice_understanding`）

用户确认 SRT 质量满意后，再决定是否把报告 commit 进仓库。

## 代码与架构约定

### 字幕时间轴（参考 KrillinAI，见 `TODO.md`）

- 思路：**先文本、后时间** — ASR 拿细粒度时间戳 → 拆句/润色 → 再对齐回时间轴。
- 官方 ASR：`output_timestamp=True`，字符级 `words` + `timestamp` 对齐 tag 组（`char_timestamp`）。
- 不要用「按字符比例摊满全音频」的时间轴做 SRT 烧录；仅作 `timing_confidence=low` 占位。
- 改进路线与验收标准以 **`docs/TODO-subtitle.md`** 为准；转写线见 **`docs/TODO-transcript.md`**；公共底层见 **`docs/TODO-core.md`**。架构说明：**`docs/ARCHITECTURE.md`**。

### 参考实现

- KrillinAI 克隆在 `reference/KrillinAI/`（不提交），对照 `internal/service/timestamps.go`、`audio2subtitle.go`。
- 新功能优先扩展现有脚本：`transcribe.py`、`benchmark_voice_llm.py`、`vr_subtitle_test.py`。

### 代码风格

- **最小 diff**：只改与任务相关的文件。
- 匹配周边命名与结构；不引入一层就行的多余抽象。
- 注释只写非显而易见的业务/算法逻辑。
- 除非用户要求，不扩写无关 README/文档。

## 常用命令速查

```bash
# 本地
pixi run sv <audio> --backend official --device cuda:0 -l ja --output-format json
pixi run sync-reports-from-mag

# mag
ssh rmqlife-mag
cd /home/rmqlife/work/voice_understanding && git pull
pixi run vr-subtitle-test -- --clips test_voice_clips --name-filter kavr ...
```

## 决策记录（当前约定）

- **本地改、mag 测**：不在 Mac 上跑 27 分钟 VR 全量 benchmark，除非用户明确要求。
- **一个 KAVR 样例**：mag 上目前常见 `test_voice_clips/vr_kavr500_part3.wav`；每个 clip 产出 `.asr.srt` + `.zh.srt` 一对。
- **合并 mag 脚本**：mag 上验证过的 benchmark 能力应先合入 `main` 再 push，避免两端行为不一致。
