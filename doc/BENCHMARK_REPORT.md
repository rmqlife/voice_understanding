# VR Subtitle WAV Benchmark

Date: 2026-06-28

Benchmark clip: `data/vr/_smoke_MANX-024-C.wav`

- Duration: 120.0 seconds
- Hardware observed: NVIDIA GeForce RTX 4090, 24 GiB VRAM
- Scope: ASR + SRT generation with `--skip-polish`; LLM polish was excluded so the WAV processing speed comparison measures ASR behavior directly.
- Quality proxy: timing source, segment count, and generated SRT entry count. No reference transcript is available in this folder, so word-level accuracy could not be scored.

## Results

| Method | ASR seconds | RTF | Timing source | Segments | SRT entries | Result |
|---|---:|---:|---|---:|---:|---|
| official backend, CUDA, chunking disabled | 9.55 | 0.080 | `char_timestamp` | 6 | 5 | Best |
| official backend, CUDA, 60s chunks | 9.81 | 0.082 | `none` | 5 | 6 | Slower and worse timing metadata |
| official backend, CUDA, 30s chunks | 11.33 | 0.094 | `none` | 5 | 6 | Slower and worse timing metadata |
| official backend, CPU, chunking disabled | 12.87 | 0.107 | `char_timestamp` | 6 | 5 | Good fallback, slower |
| SenseVoice.cpp backend | n/a | n/a | n/a | n/a | n/a | Not installed: `reference/SenseVoice.cpp/build/bin/sense-voice-main` missing |

Raw benchmark outputs:

- `results/benchmark_official_cuda_nochunk.md`
- `results/benchmark_official_cuda_chunk60.md`
- `results/benchmark_official_cuda_chunk30.md`
- `results/benchmark_official_cpu_nochunk.md`

## Tested Improvements

1. Disable official-backend chunking.
   Result: fastest on the benchmark and preserved `char_timestamp` timing. This is the selected default.

2. Shorter official-backend chunks.
   Result: 30s and 60s chunks were slower on the sample and lost useful timing metadata. They may still be useful for very long files if memory pressure appears, but they are not the fastest default here.

3. CPU fallback.
   Result: valid output with the same timing metadata as CUDA, but about 35% slower than CUDA on this sample.

4. SenseVoice.cpp.
   Result: unavailable in this checkout, so it cannot be selected as the default without installing its binary and GGUF model.

## Applied Change

The VR subtitle pipeline now exposes `--asr-chunk-seconds` through the benchmark script, `add_subtitle.py`, and task TOML defaults. The default is `0`, which disables official-backend chunking and applies the fastest measured setting:

```bash
pixi run add-subtitle -- --video /path/to/video.mp4 --asr-chunk-seconds 0
```

Batch task files can also set:

```toml
[defaults]
asr_chunk_seconds = 0
```

## Notes

During benchmarking, `run_asr` also had a relative-path bug: it launched ASR from the repo root, so relative audio paths could be reported as missing. `run_asr` now resolves the audio path before starting the ASR subprocess.
