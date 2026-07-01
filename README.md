# VR Subtitle

Small local pipeline for VR mp4 subtitles:

`mp4 on NAS -> local WAV -> ASR SRT -> Chinese SRT -> SRT next to mp4`

The code is intentionally flat. Runtime CLIs live in `scripts/`; reusable logic lives in
`python/sense_voice/`; docs, tests, and local data live in `doc/`, `test/`, and `data/`.

## Layout

| Path | Purpose |
|---|---|
| `app.py` | stdlib web UI for scanning videos and starting one subtitle job |
| `scripts/` | CLI entry points for the VR subtitle pipeline |
| `python/sense_voice/` | ASR, audio, GPU lock, LLM, SRT, task, and VR path helpers |
| `data/vr/` | local extracted WAV cache |
| `data/tasks/` | generated batch task TOML |
| `results/srt/` | generated `.asr.srt` and `.zh.srt` files |
| `doc/` | notes and benchmark report |
| `test/` | no-GPU smoke tests |

## Setup

```bash
pixi install
pixi run install-gpu
```

`install-gpu` installs the CUDA FunASR stack used by the official SenseVoice backend.

Useful environment variables:

| Variable | Default |
|---|---|
| `VR_SUBTITLE_SCAN_FOLDER` | `/mnt/fnos/jav/#finished` |
| `VR_SUBTITLE_HOST` | `127.0.0.1` |
| `VR_SUBTITLE_PORT` | `8765` |
| `VR_JAV_ROOT` | auto-detected gvfs/NFS mount |

## Run

```bash
# Web UI
pixi run web

# Single video
pixi run add-subtitle -- \
  --video "/mnt/fnos/jav/#finished/SAVR-xxx/SAVR-xxx.mp4"

# Generate and run a batch
pixi run gen-subtitle-task -- \
  --folder "/mnt/fnos/jav/#finished" \
  --name-filter vr \
  -o data/tasks/vr_batch.toml
pixi run run-subtitle-task -- data/tasks/vr_batch.toml --continue-on-error

# Cron-friendly scan + run
pixi run cron-subtitle-batch -- --continue-on-error

# Repolish from existing ASR SRT
pixi run add-subtitle -- \
  --video "/mnt/fnos/jav/#finished/SAVR-xxx/SAVR-xxx.mp4" \
  --repolish-only
```

The pipeline is cache-first:

- existing `results/srt/<stem>.zh.srt` publishes cached subtitles;
- existing `results/srt/<stem>.asr.srt` skips ASR and runs translation only;
- existing `data/vr/<stem>.wav` skips extraction;
- `--force` recomputes requested stages.

## Test

```bash
pixi run test
```

The smoke test compiles entry points and checks task generation, cache decisions, web job locking, SRT duration caps, and VR path handling without requiring GPU inference.
