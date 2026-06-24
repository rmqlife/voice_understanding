# 字幕时间轴改进 TODO

参考实现：`reference/KrillinAI`（Whisper 词级时间戳 + 文本对齐）

## 问题诊断

当前 pipeline（`scripts/benchmark_voice_llm.py` → `python/sense_voice/transcribe.py`）的 SRT/时间线存在两类典型问题：

1. **单条字幕持续时间过长**（例如 `[12:14.3-12:51.6]` 约 37s，实际口语只有几秒）
2. **切分点不准**（VAD 段边界与语义句边界不对齐；LLM 润色后时间戳未重对齐）

### 根因

| 环节 | 现状 | 后果 |
|------|------|------|
| ASR 时间粒度 | official 后端未开 `output_timestamp=True`；`merge_length_s=15` 把 VAD 段合并到最长 15s+ | 一条 segment 覆盖整段 VAD 静音切分，不是一句话 |
| segment 解析 | `parse_asr_segments` 按 SenseVoice tag 组切分；无时间戳时按**字符比例**摊满全音频 | 时间完全失真，且长句占满大段时间窗 |
| 文本整理 | LLM 润色/合并/删词，但**沿用输入时间戳** | 润色后条目数、文本长度都变了，时间轴仍是旧的 |
| 缺少对齐层 | 没有 KrillinAI 的 `TimestampGenerator`（文本 ↔ 词级时间戳回对齐） | 无法在整理后重新计算 start/end |
| 无 SRT 导出 | 只输出 Markdown timeline，无时长上限、无行内二次切分 | 无法直接用于烧录字幕 |

### 实测样例（`reports/vr_audio_benchmark*.md`）

- `[12:14.3-12:51.6]`：37s，ASR 原文是一大段口语粘连
- `[11:00.3-11:34.3]`：34s
- `[02:57.2-03:26.6]`：29s
- 对比：短 VAD 段如 `[14:40.9-14:41.4]` 仅 0.5s，说明**不是全局时钟坏了，是 segment 粒度太粗**

---

## KrillinAI 做法摘要（值得借鉴）

整体是 **「先文本、后时间」** 两阶段，而不是把 VAD 段时间直接当最终字幕时间：

```
音频
  → 静音/能量切长段 (GetSplitPoints)
  → ASR（Whisper，带 Word{Text, Start, End, Num}）
  → 按标点 + 最大句长 + LLM 拆句/翻译（不带时间戳）
  → TimestampGenerator：把每句原文对齐回词级时间轴
  → 超长句按 MaxWordOneLine 再切显示行（short_origin_mixed_srt）
  → 写出 SRT
```

关键模块（`reference/KrillinAI/internal/service/`）：

- `audio2subtitle.go`：主流程；先写无时间戳 SRT，再 `generateSrtWithTimestamps`
- `timestamps.go`：`BaseLanguageMatcher.matchSentenceByStringAlignment`
  - 合并 Whisper 词文本 → 清理标点 → 在全文里找句子位置 → 映射到词 start/end
  - `lastEndTime` 单调递增，防止重叠；最短 1s
- `splitTextAndTranslateV2` / `splitTranslateItem`：标点拆句 + LLM 递归拆长句 + 双语对齐拆条
- `split_audio.go`：在固定时长附近找**能量最低**点切音频，避免硬切词语中间

---

## 改进路线（按优先级）

### P0 — 拿到更细的时间戳（不依赖 LLM）

- [x] **official 后端开启 `output_timestamp=True`**
  - 修改 `python/sense_voice/transcribe.py` `_transcribe_official`
  - 解析 `res[0]["timestamp"]` 和/或 `res[0]["sentence_info"]`（`start`/`end` 为 ms）
  - JSON 输出增加 `words: [{text, start, end}]` 和 `sentences: [...]`
- [x] **收紧 VAD 合并参数**（先 A/B 对比）
  - `merge_length_s`: 15 → 6
  - `vad_kwargs.max_single_segment_time`: 30000 → 12000
  - 目标：ASR segment 中位时长 < 8s
- [x] **废弃或降级字符比例 fallback**
  - `parse_asr_segments` 里 `audio_seconds * chars / total_chars` 仅作 `confidence=low` 占位
  - 无真实时间戳时明确告警，不用于 SRT 烧录

### P1 — 文本与时间解耦 + 回对齐（KrillinAI 核心）

- [x] **新增 `python/sense_voice/timestamps.py`**
  - 移植 `BaseLanguageMatcher` 逻辑（CJK 按字符、英文按词）
  - 输入：`words[]` + `sentences[]`（润色前的原文句）
  - 输出：每句 `{start, end}`，带 `last_end` 单调约束
- [x] **新增 `python/sense_voice/subtitle.py`**
  - 标点拆句（`。！？!?\.`）+ `max_sentence_chars`（默认 40，中文按加权字符）
  - 超长句：规则切分优先；支持 LLM JSON `align` 的 `origin_part` / `translated_part`
- [x] **润色后重对齐**
  - `build_zh_srt_entries`：用原文锚点 `realign_polished_entries` 回对齐词级时间轴
  - 解析 LLM JSON align 块时走 `build_entries_from_alignments`

- [x] **`python/sense_voice/srt.py`**
  - 标准 SRT 写出（`HH:MM:SS,mmm`）
  - 单条最大显示时长（默认 6s）和最大字数（默认 12 字/行）
  - 超长句二次切分：`split_entries_for_display`

- [x] **长音频静音切分**（可选，>10min）
  - `get_silence_split_points()`：`ffmpeg silencedetect` 在目标时长附近找切点

- [x] **VR / subtitle profile**
  - `vr`：保持 1:1 时间线条目
  - 新增 `subtitle` profile：只做断句/去口癖，专门服务 SRT

---

## 验收标准

以 `test_voice_clips/vr_kavr500_part3.wav`（或同类 20min+ 样本）为基准：

| 指标 | 现状（粗估） | 目标 |
|------|-------------|------|
| segment 时长 p95 | ~30s | < 8s |
| 单条 > 30s 数量 | 多条 | 0 |
| 单条 > 10s 占比 | 高 | < 5% |
| 相邻条间隙 | 常有大段空白或重叠 | 单调、间隙 < 0.5s 或明确静音标记 |

人工抽检：随机 20 条字幕，起止时间与听感对齐率 > 90%。

---

## 参考文件索引

| 本项目 | KrillinAI 对照 |
|--------|----------------|
| `python/sense_voice/transcribe.py` | `pkg/whispercpp/transcription.go` |
| `scripts/benchmark_voice_llm.py` `parse_asr_segments` | `internal/service/audio2subtitle.go` |
| （待建）`python/sense_voice/timestamps.py` | `internal/service/timestamps.go` |
| `python/sense_voice/srt.py` | `pkg/util/subtitle.go`, `generateSrtWithTimestamps` |
| `scripts/benchmark_voice_llm.py` `polish_prompt` | `splitTextAndTranslateV2`, `splitTranslateItem` |
