# VR Subtitle TODO

- [x] Keep VR app and orchestration under `vr_subtitle/`.
- [x] Reuse the main repo `../python/sense_voice` modules for ASR, audio, LLM, SRT, task parsing, and NFS helpers.
- [x] Provide local pixi tasks for CLI and web entry points.
- [x] Add a web app to scan/select videos and stream job progress.
- [x] Move existing WAV/SRT outputs into local cache paths and make processing cache-first.

- [x] Let the web app type/scan a folder path in the browser window.
- [x] Add a cron-friendly task runner for `/mnt/fnos/jav/#finished` using default settings every 6 hours.
- [x] Verify a generated `tasks/*.toml` batch can run end-to-end in dry-run mode.


# Done: benchmark one WAV and apply the best speed/quality setting.

- Report: `BENCHMARK_REPORT.md`
- Benchmark clip: `data/vr/_smoke_MANX-024-C.wav`
- Applied default: official ASR chunking disabled with `asr_chunk_seconds = 0`
