# VR Subtitle Test Metrics

- Run: `refactor_smoke_20250625`
- Date: 2026-06-25 14:04:00

## Summary

| Clip | Audio s | ASR s | ASR RTF | Segments | Refined | Timing | p50 | p95 | max | >10s | >30s | LLM s | ASR SRT | ZH SRT | ASR entries | ZH entries |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| vr_savr_799_sample.wav | 180.0 | 11.01 | 0.061 | 13 | 13 | char_timestamp | 12.0 | 13.9 | 14.2 | 8 | 0 | 48.37 | `results/srt/vr_savr_799_sample.asr.srt` | `results/srt/vr_savr_799_sample.zh.srt` | 38 | 32 |

## vr_savr_799_sample.wav

- Raw ASR segments: 13
- Refined segments: 13
- ASR SRT: `results/srt/vr_savr_799_sample.asr.srt` (38 entries)
- Chinese SRT: `results/srt/vr_savr_799_sample.zh.srt` (32 entries)
- Timing confidence mix: high=13
- LLM chunks: 1
