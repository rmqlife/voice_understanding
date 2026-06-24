# 字幕时间轴改进 TODO

> 产品线：**Subtitle**（字幕 / 翻译）。公共 ASR 见 [`TODO-core.md`](TODO-core.md)；说话人转写见 [`TODO-transcript.md`](TODO-transcript.md)。架构总览：[`ARCHITECTURE.md`](ARCHITECTURE.md)。

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

## P2 — 中文显示切分质量（耿瑞香样例暴露）

### 现象（`reports/srt/微信录音 耿瑞香_*.asr.srt`，无润色，`--skip-polish`）

| 条目 | 问题 | 听感上应是什么 |
|------|------|----------------|
| 84–85 | `…这帮王八` / `蛋吗？` | 「这帮王八蛋吗？」一句，词被拦腰切断 |
| 89–90 | `…说说说说` / `，`（0 时长） | 逗号应留在上一句末尾，不应单独成行 |
| 93–94 | `…跟他联系` / `呢，` | 「跟他联系呢，」一句，语气词 `呢` 被剥到下一行 |

同类问题在全文件里多次出现（如 `他都没有他都没有派` / `人，`）。

### 根因（`python/sense_voice/srt.py`）

显示切分在 **refine 之后** 对每条 segment 做 `max_chars=12` / `max_duration=6s` 二次切分，逻辑过于粗糙：

1. **12 字硬切，中文几乎无安全边界**
   - `_split_text_chunks` 只在空格、`，`、`、` 处回退；中文口语无空格。
   - 窗口满 12 字仍无标点时 **按 index 硬砍** →「王八|蛋吗？」。

2. **孤立标点 chunk（已复现路径）**
   - 父文本如 `你要我正在我正在跟他联系呢，我刚才…`（>12 字）。
   - 第一窗 12 字 → `…跟他联系`；余下 `呢，我刚才…`。
   - 第二窗 `呢，我刚才跟他联系` 中 `rfind('，')==0` → chunk 仅为 `，`，时长 ≈ 0。

3. **时长兜底切分也不看语义**
   - `split_entry_by_words` 在 ≤12 字但 >6s 时用 `text[len(text)//2]` 对半砍，同样会切断词语。

4. **与 refine 层能力不匹配**
   - `subtitle.refine_segments` 已按 `。！？` + 加权 40 字拆 **语义句**；
   - 显示层又用 12 字盲切 **打碎语义句** → 标点、语气词、俚语词边界全丢。

5. **非润色问题**
   - 当前耿瑞香 `.zh.srt` 与 `.asr.srt` 相同；换 LLM 润色不能从根上修硬切，最多改个别 ASR 错字（如「我正在我正在」重复）。

### 改进方向（建议顺序）

- [x] **P2.1 标点/碎片行合并（快修）**
  - 切分后扫一遍：纯标点或 ≤1 字的 chunk 并入前一条（优先）或后一条。
  - `_split_text_chunks`：若 `split_at == 0`（窗以逗号开头），不要在此处切，继续向后找或扩大窗。

- [x] **P2.2 中文切分点优先级（核心）**
  - 在加权字数限制内按优先级找断点：`。！？` > `，；` > 语气词（`呢吗啊吧了`）；**无标点时不硬切**，宁可单行略长。
  - 显示行用加权长度（中文 2、英文 1），而非裸 `len()`。

- [x] **P2.3 时长切分**
  - 显示层默认 **不按秒数切**（`max_duration=None`）；segment 时间轴已约束上界。

- [x] **P2.4 参数**
  - `max_chars` 18（加权）；先拆语义句、再按标点拆显示行。

- [ ] **P2.5 可选：jieba 或规则分词**
  - 仅用于找切分点，不改 ASR 文本；长句切分前先 `cut` 再组包到 max_chars 内。

### P2 验收（耿瑞香 142s 样例）

| 检查项 | 目标 |
|--------|------|
| 词内切断（王八/蛋、派/人等） | 0 处 |
| 纯标点或 0 时长单行 | 0 处 |
| 语气词 `呢吗啊` 落单成行 | 0 处 |
| 显示行加权长度 p95 | ≤ 18，且无单条 > 6s（或配置上限） |
| 人工抽检 20 条 | 断句自然度 > 90% |

---

## 参考文件索引

| 本项目 | KrillinAI 对照 |
|--------|----------------|
| `python/sense_voice/transcribe.py` | `pkg/whispercpp/transcription.go` |
| `scripts/benchmark_voice_llm.py` `parse_asr_segments` | `internal/service/audio2subtitle.go` |
| （待建）`python/sense_voice/timestamps.py` | `internal/service/timestamps.go` |
| `python/sense_voice/srt.py` | `pkg/util/subtitle.go`, `generateSrtWithTimestamps` |
| `scripts/benchmark_voice_llm.py` `polish_prompt` | `splitTextAndTranslateV2`, `splitTranslateItem` |
