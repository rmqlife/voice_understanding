# Voice Clip Local LLM Benchmark

- Date: 2026-06-23 14:22:02
- ASR: `official` via `pixi run sv`
- ASR device: `cuda:0`
- ASR language: `ja`
- Prompt profile: `vr`
- Polish LLM: `nsfw-local:27b` via Ollama local API
- English translation: skipped
- Self-assessment: skipped
- LLM chunk size: 3000 chars
- Benchmark clip: `test_voice_clips/vr_kavr500_part3.wav`

## Summary

- Files processed: 1
- Approx. audio duration: 1619.1s
- Total ASR wall time: 12.34s
- Total polish wall time: 412.68s

## Benchmark Table

| File | Size MB | Audio s | ASR s | ASR RTF | Segments | Raw chars | Chunks | Polish s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| vr_kavr500_part3.wav | 49.41 | 1619.1 | 12.34 | 0.008 | 119 | 13848 | 5 | 412.68 |

## Findings

- `official` ASR completed for all selected clips.
- `nsfw-local:27b` handled ja->zh transcript cleanup only.
- The LLM input is now a structured timeline with coarse or exact segment times plus SenseVoice tags where available.
- Best current direction: keep ASR language pinned when known, process long recordings in chunks, and keep domain-specific prompt profiles separate.

## 1. vr_kavr500_part3.wav

### Metrics

- Size: 49.41 MB
- Approx. audio duration: 1619.1s
- ASR wall time: 12.34s
- Structured ASR segments: 119
- Polish wall time: 412.68s

### Chinese Polished

```text
## Timeline

- [00:00.0-00:20.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 真可惜啊，也让我们的身体感到舒适吧。看，放进去吧。
- [00:20.4-00:25.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊，已经进去了。
- [00:25.5-00:31.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 原本腰部反复运动，真厉害。
- [00:31.1-00:45.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 厉害厉害，已经累了吧。触碰到深处，感觉很好。
- [00:45.3-01:00.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 发出了声音，似乎感觉很舒适。啊，那里很舒服。
- [01:00.0-01:19.3] tags: lang=ja, emotion=HAPPY, type=Speech | text: 因为充满了疲惫感，忍不住触碰，正在摇晃，真害羞，真厉害。
- [01:19.3-01:32.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 电视的，大家的手都很温暖，正在进行亲密行为。
- [01:32.3-01:59.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊啊啊，很舒服。这边也希望有所改变吧？啊，是的，哥哥也很舒服。啊啊，真高兴。
- [01:59.4-02:12.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊啊，请更紧密地贴近，变得如此激烈。
- [02:12.5-02:16.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 变得非常激烈。
- [02:16.4-02:29.5] tags: lang=ja, emotion=HAPPY, type=Speech | text: 非常激烈，如此让人心情舒畅，感觉真不错。
- [02:29.5-02:31.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 好的。
- [02:31.1-02:43.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 完全不希望停止，内部兴奋，面部表情明显。
- [02:43.0-02:50.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊，要来了，要来了，要来了。
- [02:50.4-02:57.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 好的，已经进去了，真是。
- [02:57.2-03:26.6] tags: lang=ja, emotion=HAPPY, type=Speech | text: 是啊，真舒服，非常舒服。正在颤抖，身体紧紧收缩，真是如此。还可以继续吧。雪代小姐，我们开始吧。
- [03:26.6-03:36.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 请也让我的身体感到舒适。
- [03:36.3-03:40.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 充满地跟随。
- [03:40.8-03:56.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 进去得很深，真厉害。非常坚硬，非常坚硬。啊啊，真厉害。
- [03:56.6-04:13.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 那里非常舒服，糟糕，非常舒服，确实如此。
- [04:13.0-04:32.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 一直触碰到深处，非常触碰到。那里很坚硬。啊，就是那里，真舒服。
- [04:32.9-04:50.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 嗯，逐渐变得激烈，真厉害。那种状态，吐息的样子看得很清楚。
- [04:50.4-05:06.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 嗯，那种感觉真厉害。那里很舒服，糟糕，看，请让我更舒适一些。
- [05:06.8-05:27.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 糟糕，那种感觉要来了，就是那里，不行。请安静，那种感觉要来了。等等，要来了，要来了。啊，要来了。
- [05:27.2-05:36.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 变得非常颤抖，真厉害。

## Notes

- **ASR 不确定点**：
  - 条目 007 ("テレビの みんなの手あたかい")：原文识别为“电视”和“大家的手很温暖”，但在成人场景语境下，"テレビ"可能是"テレビ" (电视) 或特定人名的误识，"手あたかい" (手很温暖) 指代不明。
  - 条目 016 ("ゆきちゃん交退しよ")：原文"交退"可能是"交尾" (交配/性行为) 或"交代" (轮流) 的识别误差，"ゆきちゃん" (雪代/小雪) 为人名或昵称。
  - 条目 020 ("そういっちゃい")：原文句尾结构不完整，可能是"そういっちゃいます" (确实如此) 的截断或口语省略。
  - 条目 022 ("気持ち吐ってる")："吐ってる" (正在吐出/呼吸) 可能指代喘息或体液流动的声音描述。
- **明显噪声与识别特征**：
  - 多条目 (如 003, 005, 009, 011) 中存在明显的日语助词脱落或口语化重复（如"すごい"多次出现），已进行通顺化处理。
  - 条目 012 ("かい") 和条目 015 ("すの") 为极短片段，可能是对话中的确认词或连接词的独立识别。
  - 整体文本中未包含明显的非语音标签（如 [笑声]、[喘息]），所有条目均标记为 Speech，表明该时间段内语音识别为主要内容。

## Timeline

- [05:36.8-06:07.4] tags: 情绪=愉悦，类型=语音 | text: 啊、好舒服，这种感觉真棒。要是能再紧贴着哥哥，让腰动起来就好了，真是停不下来呢。
- [06:07.4-06:11.9] tags: 情绪=未知，类型=语音 | text: 好舒服，太棒了。
- [06:11.9-06:30.0] tags: 情绪=未知，类型=语音 | text: 啊、好舒服，啊、好棒。是在动那个舒服的地方吗？
- [06:30.0-06:47.0] tags: 情绪=未知，类型=语音 | text: 是啊，好舒服。要多多摩擦哦，这样会很舒服的。
- [06:47.0-06:57.8] tags: 情绪=未知，类型=语音 | text: 那个……说得太害羞了，这种感觉真让人舒服。
- [06:57.8-07:04.0] tags: 情绪=未知，类型=语音 | text: 好激烈，不行，那里太敏感了。
- [07:04.0-07:27.2] tags: 情绪=愉悦，类型=语音 | text: 啊啊啊、好棒，啊、好舒服。这种感觉真棒，太舒服了。视线好像都移开了呢。
- [07:27.2-07:45.3] tags: 情绪=未知，类型=语音 | text: 我已经忍不住了。毕竟我们两个人的感觉都这么好。
- [07:45.3-08:13.1] tags: 情绪=未知，类型=语音 | text: 因为，这个阴茎很舒服哦。一直触碰让我感到好舒服。看，也让我来感受！
- [08:13.1-08:21.0] tags: 情绪=未知，类型=语音 | text: 抬起来，抬起来，已经进去了。
- [08:21.0-08:27.8] tags: 情绪=未知，类型=语音 | text: 啊，太紧绷了，情况不妙。
- [08:27.8-08:38.5] tags: 情绪=未知，类型=语音 | text: 好厉害，竟然变得这么湿润？
- [08:38.5-08:41.9] tags: 情绪=未知，类型=语音 | text: 一下子就到了深处。
- [08:41.9-09:03.5] tags: 情绪=未知，类型=语音 | text: 啊，明明已经出来了，却还有这种感觉。啊，哥哥难道有绝顶的能力吗？
- [09:03.5-09:10.3] tags: 情绪=未知，类型=语音 | text: 不行了，太敏感了。
- [09:10.3-09:28.4] tags: 情绪=愉悦，类型=语音 | text: 情况不妙了，好舒服，太舒服了。还没结束，还要继续，继续，继续，继续。
- [09:28.4-09:45.3] tags: 情绪=未知，类型=语音 | text: 稍微有点太棒了。好有活力，动作幅度真大，一直在动呢。
- [09:45.3-10:12.0] tags: 情绪=愉悦，类型=语音 | text: 不行了，已经忍不住了。啊，哥哥好舒服，既然这么紧绷，应该还能再出来一些吧。
- [10:12.0-10:41.4] tags: 情绪=愉悦，类型=语音 | text: 嗯，看，可以哦，还没结束呢。在说着可以哦。要怎么做呢？要释放出来了吗？也请给到我的身体里，哥哥的精华。
- [10:41.4-10:52.1] tags: 情绪=未知，类型=语音 | text: 啊，对，好舒服。太棒了，不行了，不行了。
- [10:52.1-11:10.8] tags: 情绪=未知，类型=语音 | text: 好舒服，一起走吧。不行了，不行了，要去了，要去了，要去了，要去了，要去了，要去了。
- [11:10.8-11:16.5] tags: 情绪=未知，类型=语音 | text: 感觉好激烈，真舒服。
- [11:16.5-11:21.0] tags: 情绪=未知，类型=语音 | text: 动得好，太棒了。
- [11:21.0-11:29.5] tags: 情绪=未知，类型=语音 | text: 看来已经释放了很多呢。
- [11:29.5-11:48.2] tags: 情绪=愉悦，类型=语音 | text: 啊，看，好棒。浓度很高，出来了很多呢。又释放了很多，真是辛苦你了。

## Notes

- **ASR 不确定点与噪声**：
    - **05:36.8 片段**：原文“腰してまらないね”存在断句模糊，可能意为“让腰部动起来停不下来”或“腰部动作让人停不下来”，此处按语意连贯整理。
    - **06:11.9 片段**：“いとこかがってるの”中“いとこ”（表姐妹）一词在上下文中可能为“いいとこ”（好地方）或“気持ちいいとこ”的识别偏差，暂按原文语义“那个舒服的地方”处理。
    - **06:47.0 片段**：“激しいだメそこだメそ”中“だメ”为“ダメ”（不行/受不了）的常见识别变体，已统一修正为“不行/敏感”。
    - **07:45.3 片段**：“おちんちん”为日语口语中对男性生殖器的通俗称呼，已译为“阴茎”以保持文本的成人语境专业性。
    - **08:41.9 片段**：“絶縁”（绝缘）在此语境下极可能为“絶頂”（高潮/绝顶）的同音误识，已根据上下文逻辑修正为“绝顶的能力”。
    - **09:45.3 片段**：“カビカしね”可能为“カビカビ”（活跃/有活力）或特定拟声词的识别噪声，结合“动いてる"（在动）语境，整理为“动作幅度大/有活力”。
    - **10:41.4 片段**：“出しちゃう”在成人语境中通常指射精/释放，已译为“释放出来”和“精华”以明确指代。
    - **11:29.5 片段**：“濃なたくさん”中“濃た”可能指“浓厚”，结合后文“出たね”，整理为描述体液浓度与量。

## Timeline

- [11:48.2-12:08.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 真是黏糊糊的，太棒了。不过看起来还是很硬挺呢，看来还能继续，对吧？
- [12:08.6-12:13.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 我们再做多一点吧。
- [12:13.7-12:47.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 接下来由我们让您感觉更舒适，客户您就保持原样休息吧。真是厉害呢。
- [12:47.6-13:14.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 又变得这样了，而且再次变大了。衣服都要撑破了，这阴茎真是惊人。
- [13:14.2-13:39.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 这边的乳头也反应了，变得好温暖。连乳头都已经变得硬挺起来了呢。
- [13:39.1-13:52.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 又展现出很舒服的样子，真是可爱呢。
- [13:52.2-13:56.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 真是惊人的湿润。
- [13:56.1-14:31.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 已经察觉到了，真是厉害，精力依然旺盛。这样的话应该很快就能开始了，那我也立刻为您准备吧。
- [14:31.2-14:40.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 请您保持不动，不要动。
- [14:40.9-14:41.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Breath | text: [轻微喘息]
- [14:41.4-14:49.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 呼，全都打开了呢。
- [14:49.3-15:04.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 感觉如何？舒服吗？竟然又变得这么坚硬。
- [15:04.6-15:26.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 客户您真是精力过人呢，您听这声音，咕叽咕叽的，不正是这样吗。
- [15:26.1-15:33.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 可以听到很多湿润的声音呢。
- [15:33.5-15:35.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 对吧。
- [15:35.8-15:45.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 跳动得很有力，真是惊人，更加紧致了。
- [15:45.4-16:14.8] tags: lang=ja, emotion=HAPPY, type=Speech | text: 那个看起来要深入到底呢。真是棒极了。看，看得见吧。我的下体已经全部将其接纳进去了。
- [16:14.8-16:26.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊，太棒了，这里简直舒服极了。
- [16:26.1-16:35.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 不行了，我似乎快要到达了。
- [16:35.2-16:43.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 表情真不错，稍微有点太舒服了。
- [16:43.7-16:48.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 腰停不下来，啊，真是的。
- [16:48.8-17:09.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 这边也很可爱呢。感觉舒服吗？我会让您感觉更舒服，啊。
- [17:09.7-17:17.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 请感受这份细微的脉动，稍等一下。
- [17:17.1-17:24.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 已经非常湿润了，真是惊人。
- [17:24.5-17:26.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Breath | text: [应声]

## Notes

- **ASR 不确定点**：
  - 条目 054 中“服ふかついちゃうんで"推测为“衣服（fuku）撑破（fukatsu/hihatsu）”，语境中确认为衣物紧绷。
  - 条目 057“ガちい"结合上下文推测为“ガッツリ”（扎实/湿润）或“ガッチリ"（坚硬），此处根据前文“乳首”及后文“元気”译为“湿润”或“坚实”，保留原意中“惊人”的感叹语气。
  - 条目 063“こいつの音としてますよ"中“こいつ"可能指代前文提到的身体部位，“音として"可能为“音がして"（发出声音），译为“您听这声音”以确保通顺。
  - 条目 064“ちな音"推测为“しな音”或“チン（阴茎）音”，结合上下文指代摩擦产生的湿润声响。
  - 条目 066“クリクリ"指跳动或收缩，“たた"可能为“触れ”或感叹词，译为“跳动有力”及“紧致”。
  - 条目 073“ちクス"推测为“チクッ"（刺痛/悸动）或“チクッ"（细微声响），结合“感じて"译为“细微的脉动”。
  - 条目 074“マ足く"推测为“マズク"或“マメク"（频繁/湿润），结合语境译为“非常湿润”。

- **明显噪声**：
  - 条目 060 和 075 识别为 `Breath` 且文本为空或仅有简短应声，已标记为中性标签。
  - 部分条目（如 051, 054, 058）中存在日语口语助词较多（如"～ね"、"～よ"、"～ちゃって"），整理时已尽量保留语气但去除冗余口癖。
  - 条目 065“ですか。”为简短确认，可能伴随点头或轻微动作，文本保留其确认语气。

## Timeline
- [17:26.2-17:51.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 里面在剧烈颤抖，是不是太大了？来看看。我也做过，这次换我和您一起吧。
- [17:51.6-18:01.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 这次轮到我了，也请您尽快体验一下。
- [18:01.3-18:06.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 要进去了哦。
- [18:06.3-18:09.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 进去了。
- [18:09.2-18:31.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊，很舒服。一直保持着很硬的状态，真是厉害，真的非常坚硬呢。
- [18:31.8-18:49.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 感觉非常棒，发出的声音也很淫靡。哥哥您也一定很舒服吧？
- [18:49.9-19:08.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 请变得更加舒服吧。看这表情，真是让人无法忍耐呢。
- [19:08.1-19:13.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊，很舒服。
- [19:13.1-19:17.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 非常剧烈。
- [19:17.1-19:48.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 感觉非常舒服，真是令人苦恼。太棒了，声音好大。好棒，好棒，好棒，非常舒服。
- [19:48.2-19:48.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: [不可辨语音]
- [19:48.8-20:10.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 完全没有停止，您依然硬邦邦的，一点都没变呢。真厉害，哥哥，好棒。
- [20:10.9-20:26.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 您的表情也渐渐放松下来了，感觉舒服吗？
- [20:26.2-20:48.3] tags: lang=ja, emotion=HAPPY, type=Speech | text: 真可爱，我也觉得非常舒服。快要到达顶点，正在激烈地流淌。
- [20:48.3-20:53.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 身体在微微颤抖。
- [20:53.3-21:09.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 很舒服呢。大家都在看，我也想要进去了。
- [21:09.2-21:13.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 要交换位置吗？
- [21:13.7-21:25.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 真厉害，竟然还保持着这种状态呢。
- [21:25.1-21:41.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 那么接下来由我进去，请好好看着逐渐充盈的样子。
- [21:41.5-21:51.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 进去了，进去了，甚至感动得流泪了。
- [21:51.7-21:58.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 怎么样？很舒服吧。
- [21:58.5-22:14.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 被骑在上面，因为太兴奋而无法停止，真是奇妙呢。
- [22:14.3-22:30.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 这边也来触碰一下吗？我们会将一切全部汲取出来哦。
- [22:30.7-22:42.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 抬起来，看起来那样，请把表情再展现得更清楚一些。
- [22:42.6-22:50.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 有感觉到吗？想看得更清楚些。

## Notes
- **条目 086 (19:48.2-19:48.8)**: 原文识别结果仅为句号“。”，无实质语音内容，标记为不可辨语音。
- **条目 085 (19:17.1-19:48.2)**: 包含大量重复感叹词及口癖（如“すっごい”“あだメいく”），整理时已合并为流畅语句，但保留了高频重复的情感表达。
- **条目 080 & 087**: 原文中“硬”“ガチガチ”等词汇重复出现，保留了以体现持续的生理状态描述。
- **条目 084**: 原文“そごいきたる”识别可能存在轻微断句误差，结合上下文译为“非常剧烈”，指代声音或动作强度。
- **条目 095**: 原文“熊まで泣いちゃった”中“熊”字结合语境可能为“感”或“感动”的识别偏差，但依据“只整理可从音频文本判断的信息”原则，暂保留字面含义或理解为特定感叹，译文侧重“感动流泪”的语意。
- **通用**: 所有条目中的 `EMO_UNKNOWN` 表示 ASR 未明确标注具体情绪（如喜悦、紧张等），仅保留 `HAPPY` (条目 089) 的明确标签。

## Timeline

- [22:50.0-23:15.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 越来越舒服了，啊，太棒了。这……不行了，要来了。啊，太棒了，好，来了。
- [23:15.4-23:21.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 今天可能是最大的一次。
- [23:21.7-23:30.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 还觉得不够，就再来一点点。
- [23:30.7-23:48.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 就是这样吗？让我们看看。应该还能继续吧，对吧？
- [23:48.8-24:01.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 让我感觉更舒服。真不错啊，真让人心情愉悦。
- [24:01.3-24:15.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 里面的量正在增加，请保持这个节奏继续。
- [24:15.4-24:25.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 动得更剧烈了，正在持续进行。
- [24:25.1-24:30.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 非常激烈。怎么了？
- [24:30.7-24:42.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 快要到了。请释放出来，也请让我感受。
- [24:42.6-24:51.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 不，不行，不行，要出来了。
- [24:51.7-25:04.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 我们一起到达了。有很多呢，感觉怎么样？
- [25:04.1-25:05.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 是？
- [25:05.3-25:23.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 啊，没想到能出来这么多。确实释放了很多呢，出来了很多吧？
- [25:23.4-25:31.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 清爽地结束了。太厉害了。
- [25:31.3-25:42.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 美味，非常美味。特别是现在还在持续流出。
- [25:42.6-26:00.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 这确实是精液，附着在我身上。已经流了很多，量非常充足。
- [26:00.2-26:19.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 真厉害，精液很美味。即使已经释放了很多，竟然还能持续流出这么优质的精液。
- [26:19.4-26:50.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 之前到底积蓄了多少呢。清理工作做得很好，真是不错。接下来可以集中精神，准备进行剪辑了。那么……
- [26:50.0-26:59.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech | text: 我们继续剪辑的后续部分吧。

## Notes

1. **ASR 识别模糊点**：
   - 条目 106 (24:01.3-24:15.4)：原文文本“ってますよ中本がとざいま増えてわそのままついてと”存在较多断句和助词识别误差，已根据上下文语境优化为通顺的陈述句，但具体指代对象（如“中本”可能为“内部”或特定名词）保留中性描述。
   - 条目 107 (24:15.4-24:25.1)：原文“動くなったこしてるよ”存在动词变形识别问题，已修正为“动得更剧烈了，正在持续进行”以符合逻辑。
   - 条目 116 (25:42.6-26:00.2)：原文“これにたん私精しかついてますよ”包含明显的识别噪声（如“たん”、“精し”），已结合后续条目中明确的“精液”语境进行整合翻译。

2. **噪声处理**：
   - 所有条目中的重复语气词（如“あ”、“いや”、“ダメ”的多次出现）已保留以体现情绪节奏，但去除了无意义的填充词卡顿。
   - 条目 112 (25:04.1-25:05.3) 原文“れ？”较短，可能为确认性疑问词或上一句的尾音延伸，已按独立短句处理。

3. **内容性质说明**：
   - 文本中多次出现“精液”、“释放”、“美味”、“内部”等词汇，表明场景涉及成人生理互动，翻译时已采用中性且直接的解剖学术语对应词汇，未添加额外修饰。
```

### Structured ASR Timeline

```text
001. [00:00.0-00:20.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: う惜しくなっちゃった 私たちのことも気持ちよくして ほら、入れてあげて。
002. [00:20.4-00:25.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あった入っちゃた。
003. [00:25.5-00:31.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もと腰動返しすごい。
004. [00:31.1-00:45.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: すごいすごい疲れてますね 奥に当たって気持ちいい。
005. [00:45.3-01:00.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: こい声しちゃったい気持ちよさそう あそれ気持ちいい。
006. [01:00.0-01:19.3] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: いっぱい疲れてるから触っちゃうだでこ揺がちゃってる恥ずかしすごいい。
007. [01:19.3-01:32.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: テレビの みんなの手あたかい エッチでしうら。
008. [01:32.3-01:59.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あああ、気持ちい。こっちも変わってほしいんじゃないですかああねお兄さんも気持ちいいああ、嬉しい。
009. [01:59.4-02:12.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ああもっとついてきくなっちゃってとつすごのと。
010. [02:12.5-02:16.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 激いちゃって。
011. [02:16.4-02:29.5] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: 激しいめなで気持ち気持ちくしてもなんだ気持ち。
012. [02:29.5-02:31.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: かい。
013. [02:31.1-02:43.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ご全然ほし止まらないやい中興奮してる顔目。
014. [02:43.0-02:50.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あ、いくいくいくいくいく。
015. [02:50.4-02:57.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ごい入っちゃった すの。
016. [02:57.2-03:26.6] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: そうすごい気持ちよかったすごいビクビク持ち縦てガチガチなんだもん。まだいけますよね。ゆきちゃん交退しよ。
017. [03:26.6-03:36.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 私のことも気持ちよくしてください。
018. [03:36.3-03:40.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: いっぱいついて。
019. [03:40.8-03:56.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: すごい入ってるあガチガチガチすごいガチガチああ、すごい。
020. [03:56.6-04:13.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あそこすごい気持ちいいやばすごい気持ちいいそういっちゃい。
021. [04:13.0-04:32.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 奥まで当たってるすごく当ってる そこ硬い あ、そこだべああ気持ちいい。
022. [04:32.9-04:50.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ういだんだん悪くなってすごいそれ、気持ち吐ってるのよく見える。
023. [04:50.4-05:06.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: んそれすごあそこ気持ちやばほらもっと気持ちよくしてあげて。
024. [05:06.8-05:27.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: やばそれいくそこだめあ黙ってそれいっちゃうや待っていく行くいく あ行く。
025. [05:27.2-05:36.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: すごいビクビクしちゃっいったすご。
026. [05:36.8-06:07.4] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: あたいはいあ、すごいいああ、気持ちこれもれ気持ちいいんだなったらもっとくっついてお兄さんに腰してまらないね。
027. [06:07.4-06:11.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ご気持ちすごい。
028. [06:11.9-06:30.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ああ、気持ちいあああ、すごいああ、気持ちいいいとこかがってるの？
029. [06:30.0-06:47.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: わたって気持ちいいいいのいっぱい擦ってあげて気持ちいいされ。
030. [06:47.0-06:57.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: そそう言っちゃうてかしくなって気持ち。
031. [06:57.8-07:04.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 激しいだメそこだメそ。
032. [07:04.0-07:27.2] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: ああああ、すごああ、気持ちいい。気持ちいすごい気持ちいいすごよく見ちゃったっても。
033. [07:27.2-07:45.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 私我慢できないね私の交え二人ともすごい気持ちよさそうなんだもん。
034. [07:45.3-08:13.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: だって、このおちんちん気持ちいいんですよ 迷くまで当たってちめちゃ気持ちいい ほらね 私にも来て！
035. [08:13.1-08:21.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あげてあげて 入っちゃった。
036. [08:21.0-08:27.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あビンビンすぎ やばい。
037. [08:27.8-08:38.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: すご壊できた そんなに濡れちゃうのメ？
038. [08:38.5-08:41.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: きなり奥ま。
039. [08:41.9-09:03.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あ出してるのにまだこのああベべェなんてやばいよお兄さんって絶縁なんですかあ？
040. [09:03.5-09:10.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: だメてそご気持ち悪い 。
041. [09:10.3-09:28.4] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: やばいますねいて気持ちいいていっちゃうからまだいくくくくくいく。
042. [09:28.4-09:45.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ちっとすごいごい元気すごいカビカしねそんなに動いてるんです。
043. [09:45.3-10:12.0] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: ばいよもう我慢できないんじゃないああお兄さん気持ちいいこんなにビンビンなんだからまだ出るよね。
044. [10:12.0-10:41.4] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: うんほらいいよきってないいよって言ってくれてるよどうすんの？出しちゃうの？私の中にもちょうだい兄さんの。
045. [10:41.4-10:52.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ああそう、気持ちいいすごダめだダメだ。
046. [10:52.1-11:10.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ち気持ちいい一緒行こう だメだメいくいくいくいくいくいくいくいく。
047. [11:10.8-11:16.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 激し気持ちよさそう。
048. [11:16.5-11:21.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ってるよいばい。
049. [11:21.0-11:29.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: いっぱい出しちゃったんですね。
050. [11:29.5-11:48.2] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: あ見てすごい濃なたくさん出たねまたいっぱい出しちゃったんで、すね。
051. [11:48.2-12:08.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ドロドロ すごいでも、まだまだビンビンみたいだね まだまだできますよね。
052. [12:08.6-12:13.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もっとしましょう。
053. [12:13.7-12:47.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 次 は 私 たちが もっと 気持ち よく して あげ ます から、お 客 様は そのまま 寝 てて ください すごいね。
054. [12:47.6-13:14.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: またこんなになっちゃって また大きくなってる 服ふかついちゃうんで、すね すごいこのちんちん。
055. [13:14.2-13:39.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: こっちの乳首っちゃう すごい暖くなってますよ 乳首までピンピンになってきちゃいましたね。
056. [13:39.1-13:52.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: また気持ちよさそうな感じしてる こエっチなと。
057. [13:52.2-13:56.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: すごいガちい。
058. [13:56.1-14:31.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: わかっちゃったの すごい まだ元気なんですね これならもうすぐ入っちゃいそうですね じゃあ 早速私がいただいちゃおうかな 。
059. [14:31.2-14:40.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: お様はそのまま動かないでください。
060. [14:40.9-14:41.4] tags: lang=ja, emotion=EMO_UNKNOWN,Breath, itn=withitn | text: 。
061. [14:41.4-14:49.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ほ、全部開いちゃいましたよ。
062. [14:49.3-15:04.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: どうですか 気持ちいいですか またこんなに硬くなんて。
063. [15:04.6-15:26.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 本当に絶倫ですねお客様 こいつの音としてますよ ぐちゃぐちゃじゃないですか。
064. [15:26.1-15:33.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ちな音いっぱい聞こえます。
065. [15:33.5-15:35.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ですか。
066. [15:35.8-15:45.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: クリクリすごいたた もっとめちも。
067. [15:45.4-16:14.8] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: それすごい奥まで入りそう。すごいロいですよ。ほら、見えてます。全部飲み込んじゃってますよ、私のおまんこ。
068. [16:14.8-16:26.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あすごああここすっごはたって気持ちいい。
069. [16:26.1-16:35.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: こダメ 私、いっちゃいそうです。
070. [16:35.2-16:43.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: いい顔なすごちょっ気持ちよく。
071. [16:43.7-16:48.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 腰止まんないあす。
072. [16:48.8-17:09.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: こちが可愛いね 気持ちいいんですか もっともっと気持ちよく出しますねあら。
073. [17:09.7-17:17.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ちクスしてく感じて待って。
074. [17:17.1-17:24.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もうマ足くいったいすごい。
075. [17:24.5-17:26.2] tags: lang=ja, emotion=EMO_UNKNOWN,Breath, itn=withitn | text: うん。
076. [17:26.2-17:51.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 中で すごいビクついてる あまだ大きいですか 見て ナ 私もした 今度は 私としましょう。
077. [17:51.6-18:01.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 今度は私の番 も早く味わってみて。
078. [18:01.3-18:06.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 入れちゃいますね。
079. [18:06.3-18:09.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: いっちゃ。
080. [18:09.2-18:31.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あ、気持ちいい ずっと硬くてやばいやないかな すごい本当にずっと硬たいですねご。
081. [18:31.8-18:49.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 気持ちすごいいやらしい音してるすうお兄さんも気持ちいいでしょう？
082. [18:49.9-19:08.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もっと気持ちよくなってください たまらない顔してるがっち見しい。
083. [19:08.1-19:13.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ああ、気持ちいい。
084. [19:13.1-19:17.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: そごいきたる。
085. [19:17.1-19:48.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: めっち気持ちよくそうなていいの 悩ましい ますご こだめいきそう あだメいく あいくいく すっごい気持ちいい。
086. [19:48.2-19:48.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 。
087. [19:48.8-20:10.9] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 全然止まんない まだガチガチなお前全然変わんないよ すごいねお兄さんあいすご。
088. [20:10.9-20:26.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: こど顔もだんどんとらけてきちゃってね気持ちいいですか。
089. [20:26.2-20:48.3] tags: lang=ja, emotion=HAPPY, type=Speech, itn=withitn | text: 可わい私もめっちゃ気持ちいいです。かれいっちゃうよめっちゃまなく流れる激しい。
090. [20:48.3-20:53.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: てんだビクビクし。
091. [20:53.3-21:09.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 気持ちい ね みんなも見てた、私も入れたくなっちゃった。
092. [21:09.2-21:13.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 交代しましょう？
093. [21:13.7-21:25.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: すごい まだこんなになってるのいですね。
094. [21:25.1-21:41.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: じゃあ次は私が入れちゃうね ちゃんと生えていくところ見て。
095. [21:41.5-21:51.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 入った 入った 熊まで泣いちゃった。
096. [21:51.7-21:58.5] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: どうですか 気持ちいい。
097. [21:58.5-22:14.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 上に乗られて 時き取れないの興奮してるんだ 変対ですね。
098. [22:14.3-22:30.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: こっちも触っちゃうかな 私たちが全部搾り取っちゃいますよ。
099. [22:30.7-22:42.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 持ち さそうなと もっとその顔よく見せて。
100. [22:42.6-22:50.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 感じてるか、もっと見たい。
101. [22:50.0-23:15.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もっと気持ちよくなって あすごいこれ 後いやばいな やばい これいく あすごい はいいく。
102. [23:15.4-23:21.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: す今日一番大きいかも。
103. [23:21.7-23:30.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: まだ足りないから ちょっとだけ。
104. [23:30.7-23:48.8] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: さそうなか私たちに見せて まだまだできますよね うできるでしょ？
105. [23:48.8-24:01.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 気持ちよくさせて やらしい あ気持ちいだね。
106. [24:01.3-24:15.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ってますよ中本がとざいま増えてわそのままついてと。
107. [24:15.4-24:25.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もっともっと動くなったこしてるよ。
108. [24:25.1-24:30.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 激しい どうしたの？
109. [24:30.7-24:42.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: いきそう あなたに出して、私にもちなせし。
110. [24:42.6-24:51.7] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: なでダメダメダメダメいっちゃう。
111. [24:51.7-25:04.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 一緒に行っちゃったねいっぱいれたのあったか。
112. [25:04.1-25:05.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: れ？
113. [25:05.3-25:23.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: あどなかこんなに出たんだ いっぱい出しましたね いっぱい出てる？
114. [25:23.4-25:31.3] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: はッきりしま した すごい。
115. [25:31.3-25:42.6] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: 美味しい美味しい 特にいついちゃってる。
116. [25:42.6-26:00.2] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: これにたん私精しかついてますよ本どたれちゃっためちゃおうかな。
117. [26:00.2-26:19.4] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: ごい精子美味しいごいいっぱい出したのにこんなすごい精子まだ出るんだ。
118. [26:19.4-26:50.0] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: もうどんだけ溜ま ってたの いっぱいスッきーできてよかったですね これで集中して カットできま すね じゃ。
119. [26:50.0-26:59.1] tags: lang=ja, emotion=EMO_UNKNOWN, type=Speech, itn=withitn | text: カットの続きしていきましょうか。
```

### Raw ASR Payload

```text
[{"key": "vr_kavr500_part3", "text": "<|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>う惜しくなっちゃった 私たちのことも気持ちよくして ほら、入れてあげて。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あった入っちゃた。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もと腰動返しすごい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>すごいすごい疲れてますね 奥に当たって気持ちいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>こい声しちゃったい気持ちよさそう あそれ気持ちいい。 <|ja|><|HAPPY|><|Speech|><|withitn|>いっぱい疲れてるから触っちゃうだでこ揺がちゃってる恥ずかしすごいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>テレビの みんなの手あたかい エッチでしうら。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あああ、気持ちい。こっちも変わってほしいんじゃないですかああねお兄さんも気持ちいいああ、嬉しい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ああもっとついてきくなっちゃってとつすごのと。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>激いちゃって。 <|ja|><|HAPPY|><|Speech|><|withitn|>激しいめなで気持ち気持ちくしてもなんだ気持ち。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|> かい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ご全然ほし止まらないやい中興奮してる顔目。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あ、いくいくいくいくいく。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ごい入っちゃった すの。 <|ja|><|HAPPY|><|Speech|><|withitn|>そうすごい気持ちよかったすごいビクビク持ち縦てガチガチなんだもん。まだいけますよね。ゆきちゃん交退しよ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>私のことも気持ちよくしてください。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>いっぱいついて。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>すごい入ってるあガチガチガチすごいガチガチああ、すごい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あそこすごい気持ちいいやばすごい気持ちいいそういっちゃい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>奥まで当たってるすごく当ってる そこ硬い あ、そこだべああ気持ちいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ういだんだん悪くなってすごいそれ、気持ち吐ってるのよく見える。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>んそれすごあそこ気持ちやばほらもっと気持ちよくしてあげて。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>やばそれいくそこだめあ黙ってそれいっちゃうや待っていく行くいく あ行く。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>すごいビクビクしちゃっいったすご。 <|ja|><|HAPPY|><|Speech|><|withitn|>あたいはいあ、すごいいああ、気持ちこれもれ気持ちいいんだなったらもっとくっついてお兄さんに腰してまらないね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ご気持ちすごい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ああ、気持ちいあああ、すごいああ、気持ちいいいとこかがってるの？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>わたって気持ちいいいいのいっぱい擦ってあげて気持ちいいされ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>そそう言っちゃうてかしくなって気持ち。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>激しいだメそこだメそ。 <|ja|><|HAPPY|><|Speech|><|withitn|>ああああ、すごああ、気持ちいい。気持ちいすごい気持ちいいすごよく見ちゃったっても。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>私我慢できないね私の交え二人ともすごい気持ちよさそうなんだもん。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>だって、このおちんちん気持ちいいんですよ 迷くまで当たってちめちゃ気持ちいい ほらね 私にも来て！ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あげてあげて 入っちゃった。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あビンビンすぎ やばい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>すご壊できた そんなに濡れちゃうのメ？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>きなり奥ま。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あ出してるのにまだこのああベべェなんてやばいよお兄さんって絶縁なんですかあ？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>だメてそご気持ち悪い 。 <|ja|><|HAPPY|><|Speech|><|withitn|>やばいますねいて気持ちいいていっちゃうからまだいくくくくくいく。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ちっとすごいごい元気すごいカビカしねそんなに動いてるんです。 <|ja|><|HAPPY|><|Speech|><|withitn|>ばいよもう我慢できないんじゃないああお兄さん気持ちいいこんなにビンビンなんだからまだ出るよね。 <|ja|><|HAPPY|><|Speech|><|withitn|>うんほらいいよきってないいよって言ってくれてるよどうすんの？出しちゃうの？私の中にもちょうだい兄さんの。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ああそう、気持ちいいすごダめだダメだ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ち気持ちいい一緒行こう だメだメいくいくいくいくいくいくいくいく。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>激し気持ちよさそう。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ってるよいばい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>いっぱい出しちゃったんですね。 <|ja|><|HAPPY|><|Speech|><|withitn|>あ見てすごい濃なたくさん出たねまたいっぱい出しちゃったんで、すね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ドロドロ すごいでも、まだまだビンビンみたいだね まだまだできますよね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もっとしましょう。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>次 は 私 たちが もっと 気持ち よく して あげ ます から、お 客 様は そのまま 寝 てて ください すごいね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>またこんなになっちゃって また大きくなってる 服ふかついちゃうんで、すね すごいこのちんちん。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>こっちの乳首っちゃう すごい暖くなってますよ 乳首までピンピンになってきちゃいましたね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>また気持ちよさそうな感じしてる こエっチなと。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>すごいガちい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>わかっちゃったの すごい まだ元気なんですね これならもうすぐ入っちゃいそうですね じゃあ 早速私がいただいちゃおうかな 。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>お様はそのまま動かないでください。 <|ja|><|EMO_UNKNOWN|><|Breath|><|withitn|>。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ほ、全部開いちゃいましたよ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>どうですか 気持ちいいですか またこんなに硬くなんて。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>本当に絶倫ですねお客様 こいつの音としてますよ ぐちゃぐちゃじゃないですか。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ちな音いっぱい聞こえます。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ですか。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>クリクリすごいたた もっとめちも。 <|ja|><|HAPPY|><|Speech|><|withitn|>それすごい奥まで入りそう。すごいロいですよ。ほら、見えてます。全部飲み込んじゃってますよ、私のおまんこ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あすごああここすっごはたって気持ちいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>こダメ 私、いっちゃいそうです。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>いい顔なすごちょっ気持ちよく。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>腰止まんないあす。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>こちが可愛いね 気持ちいいんですか もっともっと気持ちよく出しますねあら。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ちクスしてく感じて待って。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もうマ足くいったいすごい。 <|ja|><|EMO_UNKNOWN|><|Breath|><|withitn|>うん。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>中で すごいビクついてる あまだ大きいですか 見て ナ 私もした 今度は 私としましょう。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>今度は私の番 も早く味わってみて。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>入れちゃいますね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>いっちゃ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あ、気持ちいい ずっと硬くてやばいやないかな すごい本当にずっと硬たいですねご。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>気持ちすごいいやらしい音してるすうお兄さんも気持ちいいでしょう？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もっと気持ちよくなってください たまらない顔してるがっち見しい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ああ、気持ちいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>そごいきたる。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>めっち気持ちよくそうなていいの 悩ましい ますご こだめいきそう あだメいく あいくいく すっごい気持ちいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>全然止まんない まだガチガチなお前全然変わんないよ すごいねお兄さんあいすご。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>こど顔もだんどんとらけてきちゃってね気持ちいいですか。 <|ja|><|HAPPY|><|Speech|><|withitn|>可わい私もめっちゃ気持ちいいです。かれいっちゃうよめっちゃまなく流れる激しい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>てんだビクビクし。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>気持ちい ね みんなも見てた、私も入れたくなっちゃった。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>交代しましょう？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>すごい まだこんなになってるのいですね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>じゃあ次は私が入れちゃうね ちゃんと生えていくところ見て。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>入った 入った 熊まで泣いちゃった。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>どうですか 気持ちいい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>上に乗られて 時き取れないの興奮してるんだ 変対ですね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>こっちも触っちゃうかな 私たちが全部搾り取っちゃいますよ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>持ち さそうなと もっとその顔よく見せて。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>感じてるか、もっと見たい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もっと気持ちよくなって あすごいこれ 後いやばいな やばい これいく あすごい はいいく。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>す今日一番大きいかも。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>まだ足りないから ちょっとだけ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>さそうなか私たちに見せて まだまだできますよね うできるでしょ？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>気持ちよくさせて やらしい あ気持ちいだね。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ってますよ中本がとざいま増えてわそのままついてと。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もっともっと動くなったこしてるよ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>激しい どうしたの？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>いきそう あなたに出して、私にもちなせし。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>なでダメダメダメダメいっちゃう。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>一緒に行っちゃったねいっぱいれたのあったか。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>れ？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>あどなかこんなに出たんだ いっぱい出しましたね いっぱい出てる？ <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>はッきりしま した すごい。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>美味しい美味しい 特にいついちゃってる。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>これにたん私精しかついてますよ本どたれちゃっためちゃおうかな。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>ごい精子美味しいごいいっぱい出したのにこんなすごい精子まだ出るんだ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>もうどんだけ溜ま ってたの いっぱいスッきーできてよかったですね これで集中して カットできま すね じゃ。 <|ja|><|EMO_UNKNOWN|><|Speech|><|withitn|>カットの続きしていきましょうか。"}]
```
