# VR Subtitle Test Metrics

- Run: `kavr_part2`
- Date: 2026-06-24 16:05:47

## Summary

| Clip | Audio s | ASR s | ASR RTF | Segments | Refined | Timing | p50 | p95 | max | >10s | >30s | LLM s | ASR SRT | ZH SRT | ASR entries | ZH entries |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|
| vr_kavr500_part2.wav | 2210.5 | 17.28 | 0.008 | 172 | 172 | char_timestamp | 11.9 | 14.3 | 14.7 | 120 | 0 | 343.11 | `results/srt/vr_kavr500_part2.asr.srt` | `results/srt/vr_kavr500_part2.zh.srt` | 430 | 381 |

## vr_kavr500_part2.wav

- Raw ASR segments: 172
- Refined segments: 172
- ASR SRT: `results/srt/vr_kavr500_part2.asr.srt` (430 entries)
- Chinese SRT: `results/srt/vr_kavr500_part2.zh.srt` (381 entries)
- Timing confidence mix: high=172
- LLM chunks: 3
