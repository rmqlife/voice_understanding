# Transcript 转写 / Polish TODO

**目标**：电话、微信语音等多人对话 → **按说话人**整理成可读文稿。不烧录字幕，不追求毫秒级时间轴。

样例：`test_voice_clips/微信录音 耿瑞香_*.aac`、`景宜_*.aac`、`talk_to_mom.aac`

## 与字幕线的边界

| 做 | 不做 |
|----|------|
| 说话人 turn 切分 | SRT / `split_entries_for_display` |
| 同一人连续句合并 | 润色后字符时间回对齐 |
| 全文 / 分段 polish | 翻译（除非单独开 profile） |
| 可选粗时间（turn 起止） | 帧级字幕对齐 |

## P0 — 技术选型与 spike

- [ ] **说话人分离方案对比**（mag 上小样本）
  - A: FunASR / ModelScope 说话人相关 pipeline
  - B: pyannote.audio
  - C: 仅 VAD + 能量切 turn（无 diarization，两人对话先手动标）
  - 验收：耿瑞香 142s 样本能分出 ≥2 个 speaker turn 序列（允许标 `SPEAKER_00`）
- [ ] **输出格式约定**
  ```markdown
  ## 说话人 A
  文本段落…

  ## 说话人 B
  文本段落…
  ```
  机器可读：`reports/transcript/<clip>.json` → `[{speaker, start?, end?, text}]`

## P1 — 最小 pipeline

- [ ] `python/sense_voice/diarize.py` — turn 列表 `{speaker, start, end}`
- [ ] `python/sense_voice/transcript.py`
  - 按 turn 调 ASR（或全量 ASR + 时间归属）
  - `merge_adjacent_turns(same_speaker=True)`
  - `write_transcript_md` / `write_transcript_json`
- [ ] `scripts/transcript_test.py` + `pixi run transcript-test`
- [ ] LLM **`transcript` profile**（`llm.py` / prompts）
  - 去口癖、纠错、分段；**输入输出均不带 SRT 时间戳**
  - 保持 speaker 标签不变

## P2 — Polish 质量

- [ ] 耿瑞香 / 景宜样本人工抽检：说话人归属准确率、文本可读性
- [ ] 可选：说话人命名（LLM 根据内容猜「物业」「业主」— 低优先级）
- [ ] 可选：会议纪要摘要（单独 profile，不混入 transcript）

## P3 — 与字幕线复用

- [ ] 同一段录音：字幕线出 SRT，转写线出 md — **两条命令、两种报告目录**
  - `reports/srt/` vs `reports/transcript/`
- [ ] Core ASR 只跑一次时的缓存接口（避免双线测试重复 GPU）

## 验收标准（耿瑞香 142s）

| 指标 | 目标 |
|------|------|
| 说话人 turn 数 | 与听感一致（允许 2–4 人） |
| 同一人一句话被拆到两个 speaker | 明显错误 < 5% |
| polish 后文本 | 无大面积 ASR 粘连，段落可读 |
| 产出 | `reports/transcript/<clip>.md` + `.json` |
