# Translate Model Benchmark (ja → zh)

- Date: 2026-06-26 09:37:15
- ASR SRT: `results/srt/KAVR-506-伊藤舞雪__KAVR-506-CD1.asr.srt`
- Segments: 269
- Prompt profile: `vr`
- Chunk size: 80 segments / LLM call
- Models: `nsfw-local:27b`, `huihui_ai/qwen3.5-abliterated:27b`

## Summary

| Model | Wall s | Filled | Empty | Kana left | Untranslated | Bracket tags | Meta commentary | Mixed ja/zh |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| nsfw-local:27b | 425.9 | 265 | 4 | 0 | 0 | 0 | 0 | 0 |
| huihui_ai/qwen3.5-abliterated:27b | 683.3 | 263 | 6 | 0 | 0 | 0 | 0 | 0 |

## Metric Notes

- **Kana left**: output still contains Japanese kana (likely incomplete translation).
- **Untranslated**: `needs_chinese_translation()` still true (kana-heavy or meta).
- **Bracket tags**: `[停顿]` / `[不可辨语音]` etc. in output.
- **Meta commentary**: ASR uncertainty notes like “可能是…误识别”.
- **Mixed ja/zh**: both kana and Chinese in the same line.

## Head-to-head

- Entries with different output: 228 / 269
- Output SRT A: `benchmark/reports/translate_benchmark_kavr506_cd1/KAVR-506-伊藤舞雪__KAVR-506-CD1.nsfw-local_27b.zh.srt`
- Output SRT B: `benchmark/reports/translate_benchmark_kavr506_cd1/KAVR-506-伊藤舞雪__KAVR-506-CD1.huihui_ai_qwen3.5-abliterated_27b.zh.srt`

### Sample differences (first 20)

#### Entry 1

- ASR: 。こんにちは
- `nsfw-local:27b`: 今天请多指教。
- `huihui_ai/qwen3.5-abliterated:27b`: 今天请多关照。

#### Entry 2

- ASR: 今日はよろしくお願いします や
- `nsfw-local:27b`: 今天请多关照呀
- `huihui_ai/qwen3.5-abliterated:27b`: 今天很高兴见到大家

#### Entry 3

- ASR: でもすごいですね
- `nsfw-local:27b`: 不过真是令人惊叹。
- `huihui_ai/qwen3.5-abliterated:27b`: 真是令人惊叹。

#### Entry 5

- ASR: て 中に思ついてる。
- `nsfw-local:27b`: 里面竟然如此配置。
- `huihui_ai/qwen3.5-abliterated:27b`: 里面设施如此完备。

#### Entry 6

- ASR: しこんな 豪華 な 部屋
- `nsfw-local:27b`: 竟然如此豪华的房间。
- `huihui_ai/qwen3.5-abliterated:27b`: 如此豪华的房间。

#### Entry 7

- ASR: まで、いや、私、
- `nsfw-local:27b`: 直到……不，我，
- `huihui_ai/qwen3.5-abliterated:27b`: 没想到，我……

#### Entry 8

- ASR: プライベート サウナー
- `nsfw-local:27b`: 私人桑拿房
- `huihui_ai/qwen3.5-abliterated:27b`: 私人桑拿房。

#### Entry 9

- ASR: 初めて なん ですよ、
- `nsfw-local:27b`: 是第一次体验，
- `huihui_ai/qwen3.5-abliterated:27b`: 这是我第一次来。

#### Entry 10

- ASR: そもそも サウナじ。
- `nsfw-local:27b`: 说起来，桑拿……
- `huihui_ai/qwen3.5-abliterated:27b`: 说起桑拿。

#### Entry 11

- ASR: あんまり 行っ た こと
- `nsfw-local:27b`: 不太常去。
- `huihui_ai/qwen3.5-abliterated:27b`: 我很少去。

#### Entry 12

- ASR: なく て、
- `nsfw-local:27b`: 所以，
- `huihui_ai/qwen3.5-abliterated:27b`: 所以……

#### Entry 13

- ASR: いろいろ 教え て ほしく
- `nsfw-local:27b`: 希望多多指导，
- `huihui_ai/qwen3.5-abliterated:27b`: 希望您能多多指教。

#### Entry 14

- ASR: て お 願い し ま
- `nsfw-local:27b`: 拜托了。
- `huihui_ai/qwen3.5-abliterated:27b`: 拜托您了。

#### Entry 15

- ASR: す。あ、
- `nsfw-local:27b`: 了。啊，
- `huihui_ai/qwen3.5-abliterated:27b`: 是，啊，

#### Entry 16

- ASR: プライベートサウナー専門の根っぱしさんな
- `nsfw-local:27b`: 是专门负责私人桑拿的根叶先生吧。
- `huihui_ai/qwen3.5-abliterated:27b`: 原来您是专门从事私人桑拿服务的根场先生啊。

#### Entry 17

- ASR: んですよね すごい いや、
- `nsfw-local:27b`: 真是厉害，不，
- `huihui_ai/qwen3.5-abliterated:27b`: 真是厉害，难怪……

#### Entry 18

- ASR: 全然予約取れなかったんで！
- `nsfw-local:27b`: 完全约不上！
- `huihui_ai/qwen3.5-abliterated:27b`: 因为完全约不到！

#### Entry 19

- ASR: すごい人気な方なんだなぁと思って びっく
- `nsfw-local:27b`: 原来人气这么高，
- `huihui_ai/qwen3.5-abliterated:27b`: 原来是非常受欢迎的人，真是让人惊讶。

#### Entry 20

- ASR: りしましたよ
- `nsfw-local:27b`: 真是大吃一惊。
- `huihui_ai/qwen3.5-abliterated:27b`: 做完了哦

#### Entry 21

- ASR: 今日はいろいろ教えてもらえ
- `nsfw-local:27b`: 今天希望能学到很多，
- `huihui_ai/qwen3.5-abliterated:27b`: 今天希望能学到很多东西。

## Problem samples — `nsfw-local:27b`

- **[222]** ASR: うん。。
  - ZH: (empty)
- **[224]** ASR: うし。。
  - ZH: (empty)
- **[257]** ASR: あ。。
  - ZH: (empty)
- **[258]** ASR: あ。。
  - ZH: (empty)

## Problem samples — `huihui_ai/qwen3.5-abliterated:27b`

- **[104]** ASR: も。
  - ZH: (empty)
- **[222]** ASR: うん。。
  - ZH: (empty)
- **[224]** ASR: うし。。
  - ZH: (empty)
- **[254]** ASR: う。。。。
  - ZH: (empty)
- **[257]** ASR: あ。。
  - ZH: (empty)
- **[258]** ASR: あ。。
  - ZH: (empty)

## Qualitative findings

### Speed

- `nsfw-local:27b`: **425.9 s** (~7.1 min) for 269 segments.
- `huihui_ai/qwen3.5-abliterated:27b`: **683.3 s** (~11.4 min) — **1.6× slower**.

### Known failure modes (from subtitle QA)

| Issue | `nsfw-local:27b` | `huihui_ai/qwen3.5-abliterated:27b` |
|---|---|---|
| Leftover Japanese kana | 0 | 0 |
| `[停顿]` / `[不可辨语音]` tags | 0 | 0 |
| ASR meta notes (“可能是…误识别”) | 0 | 0 |
| Partial skip (ASR text present, ZH empty) | 0 | 0 |
| Empty on filler-only lines | 4 | 6 |

Both models satisfy the current post-processing rules on this clip: no bracket tags, no kana residue, no explicit ASR commentary.

### Fluency & accuracy spot-check

- **Segment fidelity**: `nsfw-local:27b` tends to keep one short subtitle per ASR fragment (e.g. entry 19–20 split: “原来人气这么高，” / “真是大吃一惊。”). `huihui_ai/qwen3.5-abliterated:27b` sometimes merges or mis-assigns across fragments — entry 20 `りしましたよ` became **“做完了哦”** (clear mistranslation; should be surprise/“吓了一跳”), while `nsfw-local:27b` correctly rendered **“真是大吃一惊。”**
- **Register**: `huihui_ai/qwen3.5-abliterated:27b` often uses slightly more formal phrasing (“请多关照” vs “请多指教”, “拜托您了”); either is acceptable for VR dialogue.
- **Display SRT line count** (after `build_zh_srt_entries_from_texts` splitting): nsfw 256, qwen 285, production 237 — counts differ because of line-breaking, not missing segments.

### Notable mistranslations (qwen)

| Entry | ASR | `huihui_ai/qwen3.5-abliterated:27b` | `nsfw-local:27b` |
|---:|---|---|---|
| 2 | 今日はよろしくお願いします や | 今天很高兴见到大家 | 今天请多关照呀 |
| 20 | りしましたよ | 做完了哦 | 真是大吃一惊。 |

Entry 2 and 20 show qwen occasionally drifts from the spoken meaning when ASR fragments are short or split mid-phrase.

## Recommendation

- **Preferred model**: `nsfw-local:27b` — same automated quality score, **1.6× faster**, and fewer segment-alignment / mistranslation issues on spot-check.
- Keep `huihui_ai/qwen3.5-abliterated:27b` as an optional fallback if `nsfw-local:27b` is unavailable; quality is close on aggregate metrics but fluency errors are slightly more frequent on fragmented ASR lines.
- Re-run: `pixi run python benchmark/benchmark_translate_llm.py`
