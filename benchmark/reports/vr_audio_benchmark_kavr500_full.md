# Voice Clip Local LLM Benchmark

- Date: 2026-06-23 15:09:09
- ASR: `official` via `pixi run sv`
- ASR device: `cuda:0`
- ASR language: `ja`
- Prompt profile: `vr`
- LLM timeline format: `full`
- Polish LLM: `nsfw-local:27b` via Ollama local API
- English translation: skipped
- Self-assessment: skipped
- LLM chunk size: 3000 chars
- Benchmark clip: `test_voice_clips/vr_kavr500_part3.wav`

## Summary

- Files processed: 1
- Approx. audio duration: 1619.1s
- Total ASR wall time: 12.04s
- Total polish wall time: 322.77s

## Benchmark Table

| File | Size MB | Audio s | ASR s | ASR RTF | Segments | LLM chars | Chunks | Polish s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| vr_kavr500_part3.wav | 49.41 | 1619.1 | 12.04 | 0.007 | 119 | 13848 | 5 | 322.77 |

## Findings

- `official` ASR completed for all selected clips.
- `nsfw-local:27b` handled ja->zh transcript cleanup only.
- The LLM input is now a structured timeline with coarse or exact segment times plus SenseVoice tags where available.
- Best current direction: keep ASR language pinned when known, process long recordings in chunks, and keep domain-specific prompt profiles separate.

## 1. vr_kavr500_part3.wav

### Metrics

- Size: 49.41 MB
- Approx. audio duration: 1619.1s
- ASR wall time: 12.04s
- Structured ASR segments: 119
- LLM input chars: 13848
- Polish wall time: 322.77s

### Chinese Polished

```text
## Timeline

- [00:00.0-00:20.4] 太可惜了，也让我也感到愉悦吧。看，放进去。
- [00:20.4-00:25.5] 进来了，已经进去了。
- [00:25.5-00:31.1] 腰部反复运动，真厉害。
- [00:31.1-00:45.3] 太厉害了，看起来很疲惫呢。触碰到深处，感觉很舒服。
- [00:45.3-01:00.0] 声音都变得不同了，看起来感觉很好。是啊，很舒服。
- [01:00.0-01:19.3] 因为非常疲惫，所以触碰时都在颤抖，真可爱，太厉害了。
- [01:19.3-01:32.3] 电视的，大家的手都很温暖，真是亲密的时刻。
- [01:32.3-01:59.4] 啊，真舒服。这边也希望能有些变化呢。啊，哥哥也很舒服。啊，真高兴。
- [01:59.4-02:12.5] 啊，请更贴近一些。变得很紧密，非常厉害。
- [02:12.5-02:16.4] 变得很激烈。
- [02:16.4-02:29.5] 非常激烈，感觉非常舒畅，真是太舒服了。
- [02:29.5-02:31.1] 真棒。
- [02:31.1-02:43.0] 完全停不下来，非常兴奋，脸上的表情也很生动。
- [02:43.0-02:50.4] 啊，要来了，要来了，要来了，要来了，要来了。
- [02:50.4-02:57.2] 真棒，已经进去了，真是的。
- [02:57.2-03:26.6] 是啊，太舒服了，真厉害。身体都在颤抖，紧紧抓住，全身都僵硬了。应该还可以继续吧。雪子，我们来交换吧。
- [03:26.6-03:36.3] 也请让我感到愉悦。
- [03:36.3-03:40.8] 全部贴合在一起。
- [03:40.8-03:56.6] 深入进去了，全身僵硬，非常僵硬，啊，太厉害了。
- [03:56.6-04:13.0] 那里非常舒服，真是不得了，太舒服了，就这样继续吧。
- [04:13.0-04:32.9] 一直触碰到深处，非常深入，那里很坚硬。啊，就是那里，啊，很舒服。
- [04:32.9-04:50.4] 嗯，越来越强烈了，真是厉害。那份舒服的感觉溢出来了，看得很清楚。
- [04:50.4-05:06.8] 嗯，太厉害了，那里很舒服，真是不得了。看，请让我更愉悦一些。
- [05:06.8-05:27.2] 真是不得了，那里要来了，不行啊，请安静，那个要来了。等等，要来了，来了，来了，啊，来了。
- [05:27.2-05:36.8] 太厉害了，身体都在颤抖，真是非常厉害。

## Notes

- **识别不确定点**：
    - 条目 007（01:19.3）中“テレビの”（电视的）与上下文“手”及“エッチ”（亲密/爱抚）的连接略显生硬，可能是对背景环境音的误听或特定语境下的指代。
    - 条目 016（03:26.6）中“交退しよ”推测为“交换（交わる/交代）”相关的口误或识别偏差，根据上下文整理为“交换”。
    - 条目 019（03:56.6）中“ガチガチ”重复多次，已保留以体现语气的强调。
- **噪声处理**：
    - 原文中多处出现“あ”、“すごい”、“気持ちいい”等高频感叹词及口癖，已在翻译中通过句式调整自然融合，未做冗余重复。
    - 条目 022（04:32.9）中“気持ち吐ってる”推测为“気持ち（溢）ってる”（感觉满溢/流露）的语音识别偏差，按语境译为“舒服的感觉溢出来了”。
    - 条目 024（05:06.8）中“いくそこだめ”为快速连读，已拆解为逻辑通顺的短句。

## Timeline

- [05:36.8-06:07.4] 哎呀，真棒啊，好舒服。这也太舒服了，要是能再紧紧贴着你，哥哥，把腰抵过来吧，停不下来了呢。
- [06:07.4-06:11.9] 好舒服，真厉害。
- [06:11.9-06:30.0] 啊，好舒服，啊啊，好厉害啊，是不是那个地方好舒服？
- [06:30.0-06:47.0] 哇，好舒服，好舒服，帮我多摩擦一会儿，好舒服，这样就好。
- [06:47.0-06:57.8] 那个，不好意思，说着说着身体就变得更舒服了。
- [06:57.8-07:04.0] 好激烈，那里，那里，好厉害。
- [07:04.0-07:27.2] 啊啊啊，好厉害啊，好舒服。好舒服，真厉害，好舒服，好厉害，看得我都……
- [07:27.2-07:45.3] 我忍不住了呢，我和你们两个人，感觉都好舒服的样子。
- [07:45.3-08:13.1] 毕竟，这个阳具好舒服呢，一直抵着好舒服，你看，也来我这里吧！
- [08:13.1-08:21.0] 抬起来，抬起来，已经进入里面了。
- [08:21.0-08:27.8] 啊，太紧实了，不得了。
- [08:27.8-08:38.5] 好厉害，都这样了，会弄湿成这样吗？
- [08:38.5-08:41.9] 突然深入到了深处。
- [08:41.9-09:03.5] 啊，明明已经出来了，可是这个……啊啊，哥哥，这难道是绝缘的吗？
- [09:03.5-09:10.3] 那里，好舒服，有点奇怪的感觉。
- [09:10.3-09:28.4] 不得了，太舒服了，要出来了，还在继续，继续，继续。
- [09:28.4-09:45.3] 真的，好厉害，很有精神，一直动个不停呢。
- [09:45.3-10:12.0] 不行了，已经忍不住了，啊，哥哥好舒服，这么紧实，应该还没结束吧。
- [10:12.0-10:41.4] 嗯，你看，很好哦，还没结束哦，他也在说着呢。怎么办？要出来了吗？也要进到我身体里，把哥哥的给我吧。
- [10:41.4-10:52.1] 啊啊，是的，好舒服，好厉害，不行了，不行了。
- [10:52.1-11:10.8] 好舒服，一起走吧。不行了，不行了，要去了，要去了，要去了，要去了，要去了，要去了。
- [11:10.8-11:16.5] 好激烈，看起来好舒服。
- [11:16.5-11:21.0] 正在动着，好棒。
- [11:21.0-11:29.5] 已经全部释放出来了呢。
- [11:29.5-11:48.2] 啊，看，好厉害，好浓，出了好多呢。又释放了好多，真好。

## Notes

- **026**: 原文“腰してまらない”识别可能为“腰を擦って（こすって）まらない（止まらない）”的连读或误识，已按语意整理为“把腰抵过来吧，停不下来了呢”。
- **028**: 原文“いとこかがってるの”中“いとこ”可能是“いいとこ”（好地方）的误识，“かがってる”可能是“がってる”或“磨ってる”（摩擦），结合上下文处理为“是不是那个地方好舒服”。
- **030**: 原文“言っちゃうてかしくなって”中“かしく”可能为“硬しく”（变硬）或“甘しく”（变温柔）的误识，结合语境整理为“身体就变得更舒服了”。
- **031**: 原文“激しいだメそこだメそ”中“だメ”为“ダメ”（不行/受不了）的常见误识，“そ”为“そこ”（那里）的省略，已还原。
- **034**: 原文“迷くまで当たって”中“迷く”可能为“擦（こす）”或“触（さわ）”的误识，结合“当たって”处理为“一直抵着/摩擦”。
- **036**: 原文“ビンビンすぎ”意为“非常饱满/紧实”，翻译时保留了该状态描述。
- **037**: 原文“メ”在语境中极大概率为“ダメ”（DAME）的后半部分或感叹词，结合前后文处理为“会弄湿成这样吗？”。
- **039**: 原文“絶縁なんですかあ”在成人语境下极大概率为“連発”（连发/多次）或“絶え間ない”（不间断）的误识，但考虑到“绝緣”（绝缘）在口语中可能指代某种特定状态或误听，此处保留“绝缘”并标注为不确定点，也可能指“接连不断”。
- **040**: 原文“だメてそご気持ち悪い”中“だメ”为“ダメ”，“ご”可能为“ここ”（这里）或“そこ”（那里），结合语境整理为“那里，好舒服，有点奇怪的感觉”。
- **041**: 原文“やばいますねいて”中“やばい”后接“います”可能为重叠或误识，整理为“不得了，太舒服了”。
- **042**: 原文“カビカしね”可能为“カピカピ”（干燥）或“カクカ”（活跃/动）的误识，结合后文“そんなに動いてる”整理为“很有精神”。
- **049**: 原文“いっぱい出しちゃったんですね”中“出しちゃった”指“释放/排出”，在语境中明确指代高潮后的状态。

## Timeline
- [11:48.2-12:08.6] 粘稠得很，不过似乎还很坚挺，对吧？还能继续的。
- [12:08.6-12:13.7] 让我们再多做一些吧。
- [12:13.7-12:47.6] 接下来我们会让您感觉更舒适，请客人就这样躺着休息。真棒。
- [12:47.6-13:14.2] 又变成了这样，又变大了。衣服快要撑破了呢，真了不起，这个阴茎。
- [13:14.2-13:39.1] 这边的乳头也……变得好温暖。乳头也都变得硬挺起来了呢。
- [13:39.1-13:52.2] 又呈现出令人愉悦的感觉，好……这里。
- [13:52.2-13:56.1] 非常……紧致。
- [13:56.1-14:31.2] 明白了，真了不起，体力还很充沛呢。这样的话，似乎很快就能进入了。那么，我就立刻开始为您享用吧。
- [14:31.2-14:40.9] 请客人保持不动，不要动。
- [14:40.9-14:41.4] [呼吸]
- [14:41.4-14:49.3] 看，全部都打开了。
- [14:49.3-15:04.6] 感觉如何？舒服吗？又变得这么坚硬。
- [15:04.6-15:26.1] 客人真是精力充沛呢。这个声音听得出来吗？发出“咕啾咕啾”的声音呢。
- [15:26.1-15:33.5] 能听到很多这种声音。
- [15:33.5-15:35.8] 是这样吗？
- [15:35.8-15:45.4] 扑通扑通跳动得很厉害，心跳声非常大。
- [15:45.4-16:14.8] 那个要深入进去了呢。非常……湿润。看，能看见了吧。全部都被吞进去了，我的阴道。
- [16:14.8-16:26.1] 啊，好棒，啊，这里……非常舒服。
- [16:26.1-16:35.2] 不行，我好像要到了。
- [16:35.2-16:43.7] 表情真好，非常……好舒服。
- [16:43.7-16:48.8] 腰停不下来，啊，是。
- [16:48.8-17:09.7] 这个很可爱呢。感觉舒服吗？我会让您感觉更加舒适的。啊。
- [17:09.7-17:17.1] 感觉到紧致收缩了吗？请等待。
- [17:17.1-17:24.5] 已经……非常深了，太棒了。
- [17:24.5-17:26.2] [应声]

## Notes
- **051**: 原文"ドロドロ"（粘稠/浓稠）、"ビンビン"（坚挺/紧绷）为拟声叠词，保留其口语化特征。
- **054**: 原文"服ふかついちゃう"（衣服fuka-...），结合上下文推测为"服が破れそう"或"衣服快要撑破"的口语表达，翻译时处理为通顺的中文描述。
- **055**: 原文"乳首っちゃう"为口语省略表达，指乳头发生变化。
- **056**: 原文"こエっチなと"存在识别噪声，结合语境处理为"好……这里"，保留口语停顿感。
- **057**: 原文"すごいガちい"推测为"すごいがちい"或"すごいがっち"（紧致/结实），译为“非常紧致”。
- **060 & 075**: 标签包含 Breath，文本为标点或简短应声，按规范标注为"[呼吸]"和"[应声]"。
- **063**: 原文"こいつの音としてますよ"中"音として"推测为"音がしている"（发出声音）的口语变体。
- **064**: 原文"ちな音"结合上下文推测指代前文的摩擦声或心跳声，译为“这种声音”。
- **066**: 原文"クリクリ"（跳动/脉动）、"すごいたた"（心跳/扑通）、"もっとめちも"（非常/很厉害），均为拟声词及口语表达。
- **067**: 原文"ロい"推测为"ロイ"（湿润/润滑）或"ロイド"的口语发音，结合后文"全部飲み込んじゃってますよ"，译为“非常湿润”。
- **070**: 原文"いい顔なすごちょっ"存在断句和识别噪声，处理为“表情真好，非常……好舒服”。
- **071**: 原文"腰止まんないあす"推测为"腰が止まらない"（腰停不下来）及"あ、す（てい）"（啊，是），保留动作与应声。
- **073**: 原文"ちクス"推测为"キュッ"（收缩）或"チクッ"（刺痛/收缩感）的变体，结合语境译为“紧致收缩”。
- **074**: 原文"もうマ足くいったい"推测为"もう深くいった"（已经进去了很深处）及"すごい"，译为“已经……非常深了，太棒了”。

## Timeline

- [17:26.2-17:51.6] 里面在剧烈颤抖，还很大吗？看着吧，我也来一次。这次换我来吧。
- [17:51.6-18:01.3] 这次轮到我了，也请快点品尝一下。
- [18:01.3-18:06.3] 要进去了哦。
- [18:06.3-18:09.2] 进去了。
- [18:09.2-18:31.8] 啊，好舒服。一直都很硬，状态真棒呢，真的是非常坚硬。
- [18:31.8-18:49.9] 感觉非常舒服，发出了很淫靡的声音，哥哥您也应该很舒服吧？
- [18:49.9-19:08.1] 请变得更加舒服吧，您那难以抑制的表情真令人怜惜。
- [19:08.1-19:13.1] 啊，好舒服。
- [19:13.1-19:17.1] 真是太厉害了。
- [19:17.1-19:48.2] 感觉非常舒服，令人烦恼，太棒了，似乎要呻吟出来了，好舒服，真不错，真是超级舒服。
- [19:48.2-19:48.8] [不可辨语音]
- [19:48.8-20:10.9] 完全停不下来，您还一直硬邦邦的，完全没有变化呢，哥哥真厉害。
- [20:10.9-20:26.2] 您的表情也渐渐变得陶醉了呢，感觉舒服吗？
- [20:26.2-20:48.3] 可爱，我也觉得非常舒服。要开始剧烈地流淌出来了，真是令人怜惜。
- [20:48.3-20:53.3] 一直在颤抖。
- [20:53.3-21:09.2] 很舒服，大家也都看着呢，我也想要进入里面了。
- [21:09.2-21:13.7] 我们要交换一下吗？
- [21:13.7-21:25.1] 真是厉害，竟然还保持这样的状态呢。
- [21:25.1-21:41.5] 那么接下来由我进入，请好好看着进入的过程。
- [21:41.5-21:51.7] 进去了，进去了，连声音都变得有些哽咽了。
- [21:51.7-21:58.5] 感觉如何？很舒适吧。
- [21:58.5-22:14.3] 被骑在上面，似乎有些无法承受，因为正处于兴奋状态，真是相当特别呢。
- [22:14.3-22:30.7] 这边也想触碰一下，我们要将全部精华都汲取出来哦。
- [22:30.7-22:42.6] 持住，看起来很好，请让我更清楚地看到您的表情。
- [22:42.6-22:50.0] 有感觉吗？我想看得更仔细些。

## Notes

- **076**: 原文“あまだ”推测为“まだ”（还）的识别误差，结合上下文语境处理为“还很大吗”。
- **078**: 原文“入れちゃいますね”与079“いっちゃ”存在语意重叠，079可能是078动作开始时的短促反应，已分别保留。
- **080**: 原文“硬くてやばいやないかな”中“やばい”与“ない”结合，译为“状态真棒呢”，以符合口语逻辑。
- **082**: 原文“がっち見しい”推测为“がっしり”（结实）与“怜しい”（令人怜惜/可爱）的混合识别，译为“令人怜惜”以对应“顔”（表情）。
- **085**: 原文包含大量重叠感叹词（“すっごい”、“めっち”、“あだメいく”等），已整理为连贯的中文表达，去除了重复的“気持ちいい”冗余。
- **086**: 原文仅为标点符号，识别为[不可辨语音]。
- **089**: 原文“かれいっちゃうよ”推测为“かわい”（可爱）与“怜れ”（怜惜）的混合，结合“流れる激しい”译为“要开始剧烈地流淌出来了，真是令人怜惜”。
- **095**: 原文“熊まで泣いちゃった”中“熊”极大概率为“声”（声音）的识别错误，结合上下文译为“连声音都变得有些哽咽了”。
- **097**: 原文“変対ですね”推测为“変態ですね”（真是个性变态/特别的人）或“大変ですね”（真是辛苦/难得），结合语境保留“相当特别”的释义，避免过度推断具体形容词。
- **100**: 原文结尾较为简练，未做额外扩写。

## Timeline
- [22:50.0-23:15.4] 变得更舒服了，啊，太棒了，这……不行，太不行了。要去了，啊太棒了，好，来了。
- [23:15.4-23:21.7] 今天可能是最大的一次。
- [23:21.7-23:30.7] 因为还不够，所以来一点点就好。
- [23:30.7-23:48.8] 是这样吗？让我们看看。我们还能继续吧？可以吧？
- [23:48.8-24:01.3] 让你感到舒服，做得很好。啊，真舒服呢。
- [24:01.3-24:15.4] [不可辨语音] 里面正在增加，请保持原样继续。
- [24:15.4-24:25.1] 动得更厉害一点，做得很好。
- [24:25.1-24:30.7] 很激烈，怎么了？
- [24:30.7-24:42.6] 好像要去了。释放给我，也释放给我。
- [24:42.6-24:51.7] 不行不行不行，要出来了。
- [24:51.7-25:04.1] 一起去了呢。满满地释放了很多，很多吗？
- [25:04.1-25:05.3] 什么？
- [25:05.3-25:23.4] 啊，没想到会有这么多。释放了很多呢，正在释放很多吗？
- [25:23.4-25:31.3] 好了，结束了。太棒了。
- [25:31.3-25:42.6] 美味，很美味，特别是正在持续进行。
- [25:42.6-26:00.2] [不可辨语音] 我的精华附着在上面，全都流下来了，真是令人惊叹。
- [26:00.2-26:19.4] 太棒了，美味的精子，很好。释放了这么多，居然还有如此优质的精子持续流出。
- [26:19.4-26:50.0] 积攒了多少啊？做得很好，非常感谢。接下来集中处理，可以剪辑了。好的。
- [26:50.0-26:59.1] 继续剪辑的后续部分吧。

## Notes
- **ASR 不确定点**：
  - 条目 106 (24:01.3-24:15.4)：原文包含大量无法连通的词组（如“中本”、“本ど”），推测为对话重叠或呼吸声导致的识别断裂，已标记为 [不可辨语音] 并保留可辨部分。
  - 条目 110 (24:42.6-24:51.7)：“なで”开头部分语意不完整，结合上下文推断为“不行（ダメ）”前的语气助词或口误，已整理为连贯短句。
  - 条目 116 (25:42.6-26:00.2)：原文存在多处断句和重复音节（如“たん私精しか”），推测为说话者因情绪激动导致的语句重组，已按逻辑顺序整理。
- **明显噪声**：
  - 条目 101 和 110 中检测到多次“ダメ”（不行）和“いっちゃう”（要出来了）的重复，已删除冗余口癖，保留核心语义。
  - 条目 118 末尾“カットできま すね”中包含明显的停顿，已合并为流畅语句。
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
