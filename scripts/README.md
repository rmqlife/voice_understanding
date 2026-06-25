# scripts/

扁平结构：每个文件是一个 CLI 入口。`pixi run <task>` 映射见根目录 [`pixi.toml`](../pixi.toml)。
公共逻辑（ASR、LLM、SRT、diarize 等）都在库 [`python/sense_voice/`](../python/sense_voice/)，脚本只做参数解析 + 调库。

| 脚本 | pixi task | 产品线 | 用途 |
|------|-----------|--------|------|
| `sv.py` | `sv` | Core | 单文件/批量 ASR → text 或 json |
| `extract_audio.py` | `extract-audio` | Core | 从视频/音频抽 16 kHz mono WAV |
| `vr_subtitle_test.py` | `vr-subtitle-test` | Subtitle | **主验收**：ASR 指标 + `.asr.srt` + `.zh.srt` |
| `publish_vr_srt.py` | `publish-vr-srt` | Subtitle | 把 SRT 拷到 NFS/gvfs 视频旁 |
| `transcript_test.py` | `transcript-test` | Transcript | 说话人 diarization + ASR + polish → md/json |
| `download_transcript_models.py` | `download-transcript-models` | Transcript | 预下载 FunASR 说话人模型 |
| `sync_vr_audio.py` | `sync-vr-audio` | Sync | 从 NFS/gvfs VR 视频抽 WAV |
| `sync_from_mag.sh` | `sync-reports-from-mag` | Sync | 从 `rmqlife-mag` 拉 `reports/` |

相关目录：

- [`benchmark/`](../benchmark/) — LLM benchmark 代码 + 数据 + 结论（自成一体）
- [`tests/`](../tests/) — 无 GPU 冒烟测试（`pixi run test` / `test-srt` / `test-transcript`）
- [`archive/`](../archive/) — 已归档的实验代码与报告（pyannote、mac/cpp、vad 等）
