# scripts/

扁平结构：每个文件是一个 CLI 入口。`pixi run <task>` 映射见根目录 [`pixi.toml`](../pixi.toml)。
公共逻辑（ASR、LLM、SRT、diarize 等）都在库 [`python/sense_voice/`](../python/sense_voice/)，脚本只做参数解析 + 调库。

| 脚本 | pixi task | 产品线 | 用途 |
|------|-----------|--------|------|
| `sv.py` | `sv` | Core | 单文件/批量 ASR → text 或 json |
| `extract_audio.py` | `extract-audio` | Core | 从视频/音频抽 16 kHz mono WAV |
| `add_subtitle.py` | `add-subtitle` | Subtitle | NFS VR mp4 → WAV → SRT → 回写 NFS |
| `gen_subtitle_task.py` | `gen-subtitle-task` | Subtitle | 扫描或指定 mp4 → 写出 `task.toml` |
| `run_subtitle_task.py` | `run-subtitle-task` | Subtitle | 读取 `task.toml`，逐个跑全流程 |
| `vr_subtitle_test.py` | `vr-subtitle-test` | Subtitle | **指标验收**：ASR + `.asr.srt` + `.zh.srt` |
| `publish_vr_srt.py` | `publish-vr-srt` | Subtitle | 把 SRT 拷到 NFS/gvfs 视频旁 |
| `transcript_test.py` | `transcript-test` | Transcript | 说话人 diarization + ASR + polish → md/json |
| `download_transcript_models.py` | `download-transcript-models` | Transcript | 预下载 FunASR 说话人模型 |
| `scripts/tests/` | `test` / `test-srt` / `test-transcript` / `test-vr-sources` | Test | 无 GPU 冒烟测试 |

相关目录：

- [`benchmark/`](../benchmark/) — LLM benchmark（本地 only，不进 Git）
- [`results/`](../results/) — 运行产物 SRT / 指标 / 日志（本地 only，不进 Git）
- [`tasks/`](../tasks/) — 批量任务 `*.toml`（本地生成，不进 Git）
- [`scripts/tests/`](tests/) — 无 GPU 冒烟测试
- [`data/`](../data/) — 本地音频：`data/vr`（VR）、`data/recording`（录音/电话）
- [`archive/`](../archive/) — 已归档的实验代码（pyannote、mac/cpp、vad 等）
