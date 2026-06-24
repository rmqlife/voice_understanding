# Core 公共底层 TODO

ASR、音频预处理、LLM 调用——**字幕线与转写线共用**。功能归属判断：若两条线都会用，放 Core；若只服务烧录时间轴，放 Subtitle；若只服务说话人转写，放 Transcript。

## 现状

- [x] SenseVoice official 后端 + `output_timestamp=True`
- [x] 字符时间戳解析（含 ms/秒混合格式修复）
- [x] `scripts/sv.py` JSON 输出（`sentences`, `words`, `timing_source`）
- [x] VAD 参数调优（`merge_length_s=6`）
- [x] `scripts/extract_audio.py`

## P0 — 代码整理（减少 duplicate）

- [x] **抽出 `python/sense_voice/llm.py`**
- [x] **统一 segment 解析** → `python/sense_voice/segments.py`
- [x] **统一音频时长** → `python/sense_voice/audio.py`

## P1 — ASR 能力

- [x] 长音频分块 ASR + 拼接（`get_silence_split_points` + `extract_audio_segment` 接入 `transcribe.py`，默认 600s）
- [x] `sv.py` 支持批量目录（`--clips`）、进度日志（`[i/n]`）
- [x] 文档化 backend：见 [`REFERENCE.md`](REFERENCE.md)

## P2 — 模型与部署

- [x] mag 上模型缓存路径约定 → [`docs/MODELS.md`](MODELS.md) + `python/sense_voice/models.py`
- [x] 说话人模型预下载 → `pixi run download-transcript-models`

## 验收

- `pixi run sv <audio> -l zh --backend official --output-format json` 稳定返回 `words` + `sentences`
- `pixi run sv --clips test_voice_clips` 批量带进度
- 字幕 / 转写脚本均只通过 Core API 调 ASR，不重复实现解析逻辑
- Mac 本地：`pixi run test-srt` + `pixi run test-transcript` 通过（无 GPU）
