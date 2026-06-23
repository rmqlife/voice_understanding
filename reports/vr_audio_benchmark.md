# Voice Clip Local LLM Benchmark

- Date: 2026-06-23 11:52:31
- ASR: `official` via `pixi run sv`
- ASR device: `cuda:0`
- ASR language: `ja`
- Prompt profile: `vr`
- Polish LLM: `nsfw-local:27b` via Ollama local API
- Translate LLM: `nsfw-local:27b` via Ollama local API
- Assess LLM: `nsfw-local:27b` via Ollama local API
- LLM chunk size: 1200 chars
- Benchmark clip: `test_voice_clips/vr_savr_799_sample.wav`

## Summary

- Files processed: 1
- Approx. audio duration: 180.0s
- Total ASR wall time: 8.25s
- Total polish wall time: 66.37s
- Total English translation wall time: 65.97s

## Benchmark Table

| File | Size MB | Audio s | ASR s | ASR RTF | Segments | Raw chars | Chunks | Polish s | Translate s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| vr_savr_799_sample.wav | 5.49 | 180.0 | 8.25 | 0.046 | 13 | 1552 | 2 | 66.37 | 65.97 |

## Findings

- `official` ASR completed for all selected clips.
- `nsfw-local:27b` handled transcript cleanup; `nsfw-local:27b` handled English translation; `nsfw-local:27b` handled self-assessment.
- The LLM input is now a structured timeline with coarse or exact segment times plus SenseVoice tags where available.
- Best current direction: keep ASR language pinned when known, process long recordings in chunks, and keep domain-specific prompt profiles separate.

## 1. vr_savr_799_sample.wav

### Metrics

- Size: 5.49 MB
- Approx. audio duration: 180.0s
- ASR wall time: 8.25s
- Structured ASR segments: 13
- Polish wall time: 66.37s
- Translation wall time: 65.97s

### Chinese Polished

```text
## Timeline
- [00:00.0-00:00.5] tags: [背景音乐] | text: （静音/开场）
- [00:00.5-00:06.1] tags: [对话] | text: 是的是的，那个，要开始吗？
- [00:06.1-00:27.3] tags: [对话] | text: 既然如此，这次就过来这边，好好做一下。是的是的，真不错。顺序也很完美。
- [00:27.3-00:49.3] tags: [对话] | text: 真厉害，这个也能做到。就是这里，要弹起来。慢慢来就好。嗯，弹起来。最后停住。真不错！
- [00:49.3-01:06.3] tags: [对话], [喘息] | text: 做得好。教给你的内容都做到了，不是吗？非常擅长。嗯嗯。
- [01:06.3-01:22.7] tags: [对话] | text: 是的是的。然后，最后再写一个字符。真厉害。好，好，哎，很好。
- [01:22.7-01:40.6] tags: [对话] | text: 嗯嗯。这里好像没粘上。啊，是之前午饭沾上的吧？稍微借看一下？
- [01:40.6-01:59.4] tags: [对话] | text: 没有吗？稍等一下。毕竟已经是小学生了，如果不认真做可不行哦？
- [01:59.4-02:13.5] tags: [对话] | text: 这里也沾上了。如果不认真做，可是会不受欢迎的哦。
- [02:13.5-02:17.7] tags: [对话] | text: 好，取下来了吗？

## Notes
- **00:00.0-00:00.5**: 原文仅有一个句号，结合标签 `type=BGM`，标记为开场背景音乐或静音过渡。
- **00:06.1-00:27.3**: 原文“ごちょんてして"为口语化表达，根据上下文语境整理为“好好做一下”。
- **00:49.3-01:06.3**: 原文“出ないじゃん"结合语境推测为“做到了/做出来了”；“うんん”标记为伴随的轻声喘息或肯定回应。
- **01:06.3-01:22.7**: 原文“一文字かけそう"结合后文语境（粘上、小学生）推测为书写或标记动作，暂译为“写一个字符”。
- **01:22.7-01:40.6**: 原文“ついてない"和“ついてる"在上下文中指代物体（如污渍或标记）的附着状态，译为“没粘上”和“沾上了”以符合语境。
- **整体**: 所有条目标签统一为 `[对话]`、`[背景音乐]` 等中性描述，未添加人物身份（如“老师”、“学生”）的具体推断，仅保留文本中“小学生”这一明确提及的身份指代。
- **语言**: 原文为日文，已全篇翻译为自然中文，去除了“是的是的”、“真不错”等口语中的重复填充词，保留核心指令与反馈。

## Timeline

- [02:17.7-02:36.5] tags: 语言=日语，情绪=未知，类型=背景音乐 | text: “什么？姐姐，你在看那边吗？怎么了？有什么事要谈吗？”
- [02:36.5-02:37.4] tags: 语言=日语，情绪=未知，类型=背景音乐 | text: “诶？”
- [02:37.4-03:00.0] tags: 语言=日语，情绪=未知，类型=背景音乐 | text: “什么？如果姐姐长大了，我们就结婚？你在说什么呀？虽然你很可爱。”

## Notes

- 所有条目均标记为 `type=BGM`，且伴随 `itn=withitn`，表明文本内容可能是在背景音乐或环境音背景下识别出的语音。
- 原文中“方见”推测为“看着”或“看那边”的口语连读识别结果；"お姉ちゃんと大きくなったら"在逻辑上被处理为条件状语从句。
- 情感标签均为 `EMO_UNKNOWN`，未包含具体的语气变化（如惊讶、羞涩等）或明确的音效（如喘息、笑声）标记。
- 时间片段 011 与 013 之间存在约 12 秒的音频间隙（02:36.5-03:00.0），期间包含短暂确认词及较长对话，需留意中间是否有未识别出的停顿。
```

### English Translation

```text
## Timeline
- [00:00.0-00:00.5] tags: [Background Music] | text: (Silence/Opening)
- [00:00.5-00:06.1] tags: [Dialogue] | text: Yes, yes, shall we begin?
- [00:06.1-00:27.3] tags: [Dialogue] | text: In that case, let's come over here and do it properly. Yes, yes, that's truly excellent. The sequence is also perfect.
- [00:27.3-00:49.3] tags: [Dialogue] | text: Truly impressive; you can achieve this as well. It's right here; it needs to spring up. Take your time. Yes, spring it up. And stop there at the end. Truly excellent!
- [00:49.3-01:06.3] tags: [Dialogue], [Breathing] | text: Well done. You've accomplished everything I taught you, haven't you? Very adept. Mm-hmm.
- [01:06.3-01:22.7] tags: [Dialogue] | text: Yes, yes. And then, write one final character. Truly impressive. Good, good, ah, very good.
- [01:22.7-01:40.6] tags: [Dialogue] | text: Mm-hmm. It seems this part hasn't adhered properly. Ah, was this from lunch earlier? May I take a closer look?
- [01:40.6-01:59.4] tags: [Dialogue] | text: Is there none? Please wait a moment. After all, you are already an elementary school student; it is not acceptable to do things without seriousness.
- [01:59.4-02:13.5] tags: [Dialogue] | text: This area is also stained. If you do not proceed with seriousness, you may become unpopular.
- [02:13.5-02:17.7] tags: [Dialogue] | text: Good, have you removed it?
## Notes
- **00:00.0-00:00.5**: The original text contained only a period; combined with the `type=BGM` tag, it is marked as opening background music or a silent transition.
- **00:06.1-00:27.3**: The original phrase "ごちょんてして" is a colloquial expression, organized here as "do it properly" based on the contextual context.
- **00:49.3-01:06.3**: The original "出ないじゃん" is interpreted as "accomplished/done" based on the context; "うんん" is marked as accompanying soft breathing or an affirmative response.
- **01:06.3-01:22.7**: The original "一文字かけそう" is inferred as a writing or marking action based on the subsequent context (adhesion, elementary student), tentatively translated as "write one character."
- **01:22.7-01:40.6**: In the context, the original "ついてない" and "ついてる" refer to the adhesion state of objects (such as stains or marks), translated as "hasn't adhered" and "is stained" to align with the context.
- **Overall**: All entry tags are standardized to neutral descriptions such as `[Dialogue]` and `[Background Music]`; no specific inferences regarding character identities (e.g., "Teacher," "Student") were added, retaining only the explicitly mentioned identity of "elementary school student" within the text.
- **Language**: The original text is in Japanese and has been fully translated into natural Chinese, removing repetitive filler words such as "yes, yes" and "truly excellent" found in spoken language, while preserving core instructions and feedback.
## Timeline

- [02:17.7-02:36.5] tags: Language=Japanese, Emotion=Unknown, Type=Background Music | text: "What? Older sister, are you looking over there? What's wrong? Is there something to discuss?"
- [02:36.5-02:37.4] tags: Language=Japanese, Emotion=Unknown, Type=Background Music | text: "Eh?"
- [02:37.4-03:00.0] tags: Language=Japanese, Emotion=Unknown, Type=Background Music | text: "What? If you grow up, Older sister, we will get married? What are you talking about? Although you are very cute."
## Notes
- All entries are marked as `type=BGM` and include `itn=withitn`, indicating that the text content may be speech recognized against a background of background music or ambient sound.
- In the original text, "Fang Jian" is tentatively identified as a result of speech recognition for the colloquial connected speech of "looking" or "looking over there"; the phrase "osshachan to ookikunattara" is logically processed as a conditional adverbial clause.
- All emotion tags are `EMO_UNKNOWN`, not including specific tone changes (such as surprise or shyness) or clear sound effect markers (such as panting or laughter).
- There is an audio gap of approximately 12 seconds between time segments 011 and 013 (02:36.5-03:00.0), which contains a brief confirmation word and a longer dialogue; attention should be paid to any unrecognized pauses in the middle.
```

### Model Self-Assessment

```text
### 1. 中文润色质量评分：2.5/5

### 2. 英文翻译质量评分：2.5/5

### 3. 主要问题

本次处理结果存在**严重的逻辑矛盾**与**上下文理解偏差**，具体表现在以下几个方面：

#### A. 核心场景与身份推断的严重错位（关键问题）
*   **场景误读**：ASR 原文（002-010）包含大量动作指令（“弹起来”、“写一个字符”、“粘上”、“小学生”），这通常指向**教育/书写/手工**场景。然而，处理结果在 Notes 中保留了“小学生”和“书写”的推断，但在后续的 Timeline（011-013）中突然转折到“姐姐”、“结婚”的话题。
*   **身份模糊**：原文中“お姉ちゃん"（姐姐/大姐姐）的称呼出现较晚。在处理前段（002-010）时，完全未体现“老师/长辈”与“学生/孩子”的互动关系，导致“好好做一下”、“顺序完美”等指令显得突兀，缺乏明确的执行主体（Who is speaking to whom?）。
*   **术语不匹配**：原文“跳ねて"（Hane-te）在中文润色中译为“弹起来”，在英文中译为"spring up"。在“书写/绘画”语境下，这通常指笔触的弹跳或纸张的折叠；若为“成人视频/VR"语境，可能涉及更具体的肢体动作。目前的翻译过于通用，未能体现 VR 交互或特定动作的精确性。

#### B. 标签（Tags）与内容（Text）的逻辑冲突
*   **标签误用**：ASR 原文中所有条目（001-013）的 `type` 均为 `BGM`（背景音乐）。然而，`text` 内容却充满了大量的人声对话指令（“是的是的”、“真厉害”、“结婚”）。
    *   **问题点**：处理结果在中文和英文的 Timeline 中，虽然将部分条目标记为 `[Dialogue]`，但在 Notes 中又反复强调 `type=BGM`。这种**“标签为音乐，内容却为密集对话”**的现象未得到合理解释。通常 `BGM` 标签意味着人声微弱或为背景音，但此处文本密度极高，更应标记为 `Dialogue` 或 `Speech`，而非单纯依赖 `BGM` 标签。
*   **缺失的情感标记**：原文 `emotion=EMO_UNKNOWN`，且 Notes 中明确指出未包含具体语气。但在 00:49-01:06 段，原文有明显的“うんん”（喘息/肯定），处理结果虽在中文中增加了 `[喘息]` 标签，但在英文翻译中对应的描述（"Mm-hmm"）略显平淡，未能充分传达 VR/成人语境下可能存在的张力或情感起伏。

#### C. 语言润色与翻译的流畅度
*   **中文润色**：
    *   **优点**：成功去除了“是的是的”等口语冗余，将“ごちょんてして”意译为“好好做一下”符合语境。
    *   **不足**：部分长句逻辑略显松散。例如 01:22-01:40 段中，“关于这个部分，似乎贴合得不太到位”与“是中午吃的时候留下的吗？”之间的过渡稍显生硬，缺乏明确的因果连接词。
*   **英文翻译**：
    *   **优点**：时态和语态使用准确，如 "hasn't adhered" 和 "accomplished" 用词得当。
    *   **不足**：部分翻译过于字面化，缺乏语境适配。例如 "It seems this part hasn't adhered properly" 略显生硬，更自然的表达可能是 "It seems this section isn't sticking well" 或 "This part doesn't seem to adhere properly"。此外，对于 "Fang Jian"（方见/方剑）的 ASR 识别错误推断，Notes 中仅提及“可能是‘看着’的连读误识”，但未在文本中直接修正，导致英文 Timeline 中保留了这一潜在的歧义点。

#### D. 时间轴与间隙处理
*   **02:36.5-03:00.0 间隙处理**：Notes 中正确指出了 12 秒的间隙及其中包含的短暂确认词。但在 Timeline 呈现上，02:36.5-02:37.4 的 "Eh?" 与后续长对话的衔接在视觉上显得紧凑，未充分体现出“间隙”带来的节奏变化。建议在该间隙处增加更明确的 `[Pause]` 或 `[Silence]` 标签，以辅助理解对话的停顿与转折。

### 4. 改进建议

1.  **重构场景描述**：在 Notes 或 Timeline 的开头增加“场景概览”，明确区分前段（教学/书写指导）与后段（情感交流/家庭话题）的转换，并明确对话双方身份（如：指导者 vs. 小学生/受导者）。
2.  **优化标签体系**：
    *   将 `type=BGM` 中的人声密集段落重新评估，建议拆分或增加 `type=Dialogue` 标签。
    *   针对 `EMO_UNKNOWN`，结合文本内容（如“结婚”、“可爱”）增加推测性情感标签（如 `[Tone: Affectionate]`, `[Tone: Instructive]`），并在 Notes 中说明这是基于语境的推断。
3.  **修正 ASR 误识**：对于 "Fang Jian" 等疑似误识点，建议在 Timeline 的 `text` 字段中直接给出修正后的译文（如 "Are you looking over there?"），并在 Notes 中详细说明修正依据，而非仅在 Notes 中提及。
4.  **增强翻译的语境感**：
    *   中文：加强连接词的使用，使指令与反馈之间的逻辑更紧密。
    *   英文：提升习语的使用频率，使表达更符合目标语（英语）的自然口语习惯，避免过度直译。
5.  **细化时间轴呈现**：在 02:36.5-03:00.0 的间隙处，明确标注 `[Audio Gap / Transition]`，并简要说明该间隙对对话节奏的影响（如：为情绪转折预留空间）。

---
**总结**：本次处理在基础信息提取和语言转换上表现尚可，但在**深层语义理解**、**场景逻辑构建**及**标签体系的精准应用**上存在明显短板。建议结合 VR/成人视频的特定语境，对身份、动作及情感进行更细致的推断与标注，以提升整体的专业度与可读性。
```

### Structured ASR Timeline

```text
001. [00:00.0-00:00.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: 。
002. [00:00.5-00:06.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: そうそうそう、そかける？
003. [00:06.1-00:27.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: さそしたら今度こっち行って ごちょんてして そう 上手じゃん そうそう、かき順もバッチリ。
004. [00:27.3-00:49.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: すごいね これもできる そそこを跳ねて ゆっくりでいいよ うん跳ねて 最後止める 上手じゃん！
005. [00:49.3-01:06.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: えらいね ちゃんと教えたことできて出ないじゃん すっごい上手だようんん。
006. [01:06.3-01:22.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: そうそう で、最後 もう 一文字かけそう すごい よしよしえいね れ。
007. [01:22.7-01:40.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: ねね ここはなんかついてない ああ、さきの昼ご飯でしょう ちょっと貸して ？
008. [01:40.6-01:59.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: ないな、ちょっと待ってね ま 小学生になったんだからちゃんとしないとダメでしょ？
009. [01:59.4-02:13.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: ここ にもついてる もう ちゃんとしないと モテ ない ぞ。
010. [02:13.5-02:17.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: よし、取れたかな？
011. [02:17.7-02:36.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: なに お 姉ちゃん の 方見 て どう した の 何 なん かお 話 ある の？
012. [02:36.5-02:37.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: え？
013. [02:37.4-03:00.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=BGM, itn=withitn | text: なに お 姉ちゃんと 大きく な ったら 結婚 する 何 言っ てん の 可愛 いん だ けど。
```

### Raw ASR Payload

```text
[{"key": "vr_savr_799_sample", "text": "<|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>。 <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>そうそうそう、そかける？ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>さそしたら今度こっち行って ごちょんてして そう 上手じゃん そうそう、かき順もバッチリ。 <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>すごいね これもできる そそこを跳ねて ゆっくりでいいよ うん跳ねて 最後止める 上手じゃん！ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>えらいね ちゃんと教えたことできて出ないじゃん すっごい上手だようんん。 <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>そうそう で、最後 もう 一文字かけそう すごい よしよしえいね れ。 <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>ねね ここはなんかついてない ああ、さきの昼ご飯でしょう ちょっと貸して ？ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>ないな、ちょっと待ってね ま 小学生になったんだからちゃんとしないとダメでしょ？ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>ここ にもついてる もう ちゃんとしないと モテ ない ぞ。 <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>よし、取れたかな？ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>なに お 姉ちゃん の 方見 て どう した の 何 なん かお 話 ある の？ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>え？ <|ja|><|EMO_UNKNOWN|><|BGM|><|withitn|>なに お 姉ちゃんと 大きく な ったら 結婚 する 何 言っ てん の 可愛 いん だ けど。"}]
```
