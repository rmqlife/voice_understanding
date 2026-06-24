# VR Subtitle Test Metrics

- Run: `kavr_part3`
- Date: 2026-06-24 15:59:24

## Summary

| Clip | Audio s | ASR s | ASR RTF | Segments | Refined | Timing | p50 | p95 | max | >10s | >30s | LLM s | ASR SRT | ZH SRT | ASR entries | ZH entries |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| vr_kavr500_part3.wav | 1619.1 | 16.66 | 0.010 | 122 | 122 | char_timestamp | 12.0 | 14.3 | 14.8 | 81 | 0 | 311.63 | `reports/srt/vr_kavr500_part3.asr.srt` | `reports/srt/vr_kavr500_part3.zh.srt` | 253 | 379 |

## vr_kavr500_part3.wav

- Raw ASR segments: 122
- Refined segments: 122
- ASR SRT: `reports/srt/vr_kavr500_part3.asr.srt` (253 entries)
- Chinese SRT: `reports/srt/vr_kavr500_part3.zh.srt` (379 entries)
- Timing confidence mix: high=122
- LLM chunks: 2
