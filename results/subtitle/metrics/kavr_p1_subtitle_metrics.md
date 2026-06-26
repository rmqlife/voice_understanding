# VR Subtitle Test Metrics

- Run: `kavr_p1_refine_realign`
- Date: 2026-06-24 11:32:52

## Summary

| Clip | Audio s | ASR s | ASR RTF | Segments | Refined | Timing | p50 | p95 | max | >10s | >30s | LLM s | ASR SRT | ZH SRT | ASR entries | ZH entries |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| vr_kavr500_part3.wav | 1619.1 | 18.02 | 0.011 | 122 | 122 | char_timestamp | 12.0 | 14.3 | 14.8 | 81 | 0 | 373.13 | `results/srt/vr_kavr500_part3.asr.srt` | `results/srt/vr_kavr500_part3.zh.srt` | 374 | 256 |

## vr_kavr500_part3.wav

- Raw ASR segments: 122
- Refined segments: 122
- ASR SRT: `results/srt/vr_kavr500_part3.asr.srt` (374 entries)
- Chinese SRT: `results/srt/vr_kavr500_part3.zh.srt` (256 entries)
- Timing confidence mix: high=122
- LLM chunks: 2
