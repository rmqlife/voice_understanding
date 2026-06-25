# Transcript 转写 / Polish TODO

**目标**：电话、微信语音等多人对话 → **按说话人、按时间顺序**整理成可读文稿。不烧录字幕，不追求毫秒级时间轴。

样例：`test_voice_clips/微信录音 耿瑞香_*.aac`、`景宜_*.aac`、`talk_to_mom.aac`

## 与字幕线的边界

| 做 | 不做 |
|----|------|
| 说话人 turn 切分（声纹 / cam++） | SRT / `split_entries_for_display` |
| 同一人**相邻** turn 合并 | 润色后字符时间回对齐 |
| 按时间线导出 turn | 把同 label 揉成两个大段落 |
| 全文 / 分段 polish | 翻译（除非单独开 profile） |
| 可选粗时间（turn 起止） | 帧级字幕对齐 |

## Diarization 方案（澄清命名）

| CLI `--diarize-method` | 实际用的 | 用途 |
|------------------------|----------|------|
| `funasr`（**默认主路径**） | FunASR `fsmn-vad` + `cam++` | 真·说话人 turn |
| `auto` | 同 `funasr`；失败才 fallback | 日常测试 |
| `ffmpeg-alternate` | **ffmpeg `silencedetect`** + 奇偶 `SPEAKER_00/01` | 仅 debug baseline，**不是 FunASR VAD** |

> `pyannote` 与废弃的 `vad` 别名已从 `main` 移除；pyannote 代码快照与对比报告见 [`archive/pyannote/`](../archive/pyannote/)。

**已有、不重复下载的 VAD：**

- `pixi run sv --backend official`：`transcribe.py` 里 FunASR `fsmn-vad`（**只服务 ASR 切句**）
- `diarize_funasr()`：同一套 `fsmn-vad` + `cam++`（**服务说话人**）
- `ffmpeg silencedetect`：仅 `ffmpeg-alternate` / `get_silence_split_points`（**不是模型**）

## P0 — spike 结论（耿瑞香 142s）

- [x] FunASR `cam++` 能出 ≥2 speaker（`geng_ruixiang_p0`：13 turns）
- [x] `ffmpeg-alternate` **不能**当 diarization（一人长段 + 多停顿 → 假两人 + 内容重复）
- [ ] **重跑验收**（pipeline 修完后）：`~1:52`「你要上班 / 上什么班呢」必须在**相邻两个 turn、两个 speaker**

## P1 — pipeline 修复

- [x] **去掉默认 `consolidate_turns_by_speaker`**（改为按时间线多 turn 导出；consolidate 仅 opt-in）
- [x] **`assign_segments_to_turns`：按重叠面积归属，每句只归一个 turn**
- [x] **导出格式带粗时间**：`## Turn N · SPEAKER_xx [mm:ss-mm:ss]`
- [x] **polish 按 turn 编号回写**（`## Turn N · …`）
- [x] **`vad` → `ffmpeg-alternate`**；默认 `--diarize-method funasr`
- [x] **mag 重跑耿瑞香**（`geng_ruixiang_p1`：funasr，6 turns / 2 speakers）
- [ ] **锚点 ~1:52 未达标**（三种 diarization 均失败，见下方 P2）
- [ ] **字级时间戳 + 短停顿二次切分**：ASR `words[]` 在 `，`/`？` 处拆句，再按 diarization 重叠重分配 speaker（耿瑞香 ~1:52 验收）

## P2 — 快问快答细切（耿瑞香锚点）

实验结论（2026-06-24）：funasr / pyannote / pyannote-exclusive 均把「你要上班」「上什么班呢」留在同一 Turn；ASR 字级仅间隔 ~1s，需 turn 内二次切分而非换 diarization 后端。

- [ ] `split_turns_on_word_pauses()`：turn 内按 `words[]` + 标点/停顿拆句
- [ ] 拆句后按时间重叠把子句重映射到 speaker（或相邻 turn 边界）
- [ ] 耿瑞香 ~1:52 锚点回归测试

## P2 — Polish 质量

- [x] `python/sense_voice/diarize.py`
- [x] `python/sense_voice/transcript.py`（待按上表修）
- [x] `scripts/transcript_test.py` + `pixi run transcript-test`
- [x] `pixi run test-transcript` 本地 smoke

## P1 — 已完成（上一轮）

- [ ] 耿瑞香 / 景宜人工抽检
- [x] **pyannote.audio 对比实验** — 结论：与 funasr 相当，不作为主路径（`compare-diarize` 脚本已移除）
- [x] **可选说话人命名** — `--name-speakers` + `speaker_names.py`
- [ ] 可选：会议纪要摘要（单独 profile）

## mag 测试命令

```bash
cd /home/rmqlife/work/voice_understanding
git pull   # 或 rsync 最新 python/scripts

# 主路径：FunASR cam++（不要用 vad / ffmpeg-alternate 验收）
pixi run transcript-test -- \
  --clip "test_voice_clips/微信录音 耿瑞香_20250326090128_45748064860651968.aac" \
  --diarize-method funasr \
  --asr-backend official --asr-device cuda:0 \
  --language zh --skip-polish \
  --run-label geng_ruixiang_p1 \
  --report reports/transcript/geng_ruixiang_p1_metrics.md \
  2>&1 | tee reports/transcript/logs/geng_ruixiang_p1_run.log

# pyannote 已归档（见 archive/pyannote/）；main 上 --diarize-method 仅 auto/funasr/ffmpeg-alternate

# 说话人命名（LLM）
pixi run transcript-test -- \
  --clip "test_voice_clips/微信录音 耿瑞香_....aac" \
  --name-speakers --name-speakers-model nsfw-local:27b \
  --skip-polish
```

Mac：`pixi run sync-reports-from-mag`

### pyannote（已归档）

实验结论见上文 P2。代码快照与对比报告在 [`archive/pyannote/`](../archive/pyannote/)；复现步骤见 [`archive/README.md`](../archive/README.md)。

### 说话人命名

```bash
pixi run transcript-test -- \
  --clip "test_voice_clips/微信录音 耿瑞香_....aac" \
  --name-speakers --name-speakers-model nsfw-local:27b \
  --skip-polish
```

## 验收标准（耿瑞香 142s）

| 指标 | 目标 |
|------|------|
| 主路径 | `funasr` / `auto`，不用 `ffmpeg-alternate` 判合格 |
| 锚点 ~1:52 | 「你要上班」与「上什么班呢」分属相邻 turn、不同 speaker |
| 同一句不重复出现在两个 speaker 大段 | 明显错误 < 5% |
| 产出 | `reports/transcript/<clip>.md` + `.json`（turn 按时间排序） |
