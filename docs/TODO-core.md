# Core 公共底层 TODO

ASR、音频预处理、LLM 调用——**字幕线与转写线共用**。功能归属判断：若两条线都会用，放 Core；若只服务烧录时间轴，放 Subtitle；若只服务说话人转写，放 Transcript。

## 现状

- [x] SenseVoice official 后端 + `output_timestamp=True`
- [x] 字符时间戳解析（含 ms/秒混合格式修复）
- [x] `scripts/sv.py` JSON 输出（`sentences`, `words`, `timing_source`）
- [x] VAD 参数调优（`merge_length_s=6`）
- [x] `scripts/extract_audio.py`

## P0 — 代码整理（减少 duplicate）

- [ ] **抽出 `python/sense_voice/llm.py`**
  - 从 `benchmark_voice_llm.py` 迁：`ollama_generate`, `chunk_text`, `generate_by_chunk`, `stop_ollama_models`
  - `polish_prompt` 按 profile 留各产品入口调用，或拆 `llm/prompts.py`
- [ ] **统一 segment 解析**
  - `parse_asr_segments` 目前在 `benchmark_voice_llm.py`；应迁入 `transcribe.py` 或 `sense_voice/segments.py`
- [ ] **统一音频时长**
  - `ffprobe_duration` / `max_timestamp_seconds` 抽到 `sense_voice/audio.py`

## P1 — ASR 能力

- [ ] 长音频分块 ASR + 拼接（`get_silence_split_points` 接入 `transcribe`）
- [ ] `sv.py` 支持批量目录、进度日志
- [ ] 文档化 backend：`official`（main/mag）vs `cpp`（`mac` 分支），见 [`REFERENCE.md`](REFERENCE.md)

## P2 — 模型与部署

- [ ] mag 上模型缓存路径约定（`~/.cache/modelscope`）
- [ ] 可选：说话人相关模型预下载（为 Transcript 线做准备，见 `TODO-transcript.md`）

## 验收

- `pixi run sv <audio> -l zh --backend official --output-format json` 稳定返回 `words` + `sentences`
- 字幕 / 转写脚本均只通过 Core API 调 ASR，不重复实现解析逻辑
