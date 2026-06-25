# Voice Clip Local LLM Benchmark

- Date: 2026-06-23 14:52:20
- ASR: `official` via `pixi run sv`
- ASR device: `cuda:0`
- ASR language: `ja`
- Prompt profile: `vr`
- LLM timeline format: `compact`
- Polish LLM: `nsfw-local:27b` via Ollama local API
- English translation: skipped
- Self-assessment: skipped
- LLM chunk size: 3000 chars
- Benchmark clip: `test_voice_clips/vr_kavr500_part3.wav`

## Summary

- Files processed: 1
- Approx. audio duration: 1619.1s
- Total ASR wall time: 11.36s
- Total polish wall time: 208.73s

## Benchmark Table

| File | Size MB | Audio s | ASR s | ASR RTF | Segments | LLM chars | Timeline chars | Chunks | Polish s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| vr_kavr500_part3.wav | 49.41 | 1619.1 | 11.36 | 0.007 | 119 | 5120 | 13848 | 2 | 208.73 |

## Findings

- `official` ASR completed for all selected clips.
- `nsfw-local:27b` handled ja->zh transcript cleanup only.
- The LLM input is now a structured timeline with coarse or exact segment times plus SenseVoice tags where available.
- Best current direction: keep ASR language pinned when known, process long recordings in chunks, and keep domain-specific prompt profiles separate.

## 1. vr_kavr500_part3.wav

### Metrics

- Size: 49.41 MB
- Approx. audio duration: 1619.1s
- ASR wall time: 11.36s
- Structured ASR segments: 119
- LLM input chars: 5120
- Full timeline chars: 13848
- Polish wall time: 208.73s

### Chinese Polished

```text
## Timeline
- [00:00.0-00:20.4] 真是可惜呢。请也让我们感到愉悦吧。来，请进入。
- [00:20.4-00:25.5] 啊，已经进去了。
- [00:25.5-00:31.1] 腰部反复摆动，非常厉害。
- [00:31.1-00:45.3] 非常厉害，看起来很疲惫呢。触碰深处，感觉真舒服。
- [00:45.3-01:00.0] 发出了这样的声音，看起来很愉悦。那确实很舒服。
- [01:00.0-01:19.3] 因为非常疲惫，所以忍不住触碰，身体摇晃得厉害，真害羞，非常棒。
- [01:19.3-01:32.3] 电视的，大家的手都很温暖，真是热情呢。
- [01:32.3-01:59.4] 啊啊啊，很舒服。这边是不是也希望改变一下呢？啊，是的，哥哥也很舒服。啊啊，真高兴。
- [01:59.4-02:12.5] 啊，再更靠近一些，变得非常激烈。
- [02:12.5-02:16.4] 变得非常激烈。
- [02:16.4-02:29.5] 非常激烈的，那种感觉，感觉真的很舒服，那种感觉。
- [02:29.5-02:31.1] 好的。
- [02:31.1-02:43.0] 完全希望不停，里面正兴奋着，看那张脸。
- [02:43.0-02:50.4] 啊，来了来了来了来了来了。
- [02:50.4-02:57.2] 啊，已经进去了，那个。
- [02:57.2-03:26.6] 是的，真舒服，非常舒服。身体颤抖，紧紧抓住，变得硬邦邦的。还可以继续呢。小雪，我们也一起进入吧。
- [03:26.6-03:36.3] 请也让我们感到愉悦。
- [03:36.3-03:40.8] 紧紧地跟随。
- [03:40.8-03:56.6] 进入了非常多，硬邦邦，非常硬邦邦，啊，非常厉害。
- [03:56.6-04:13.0] 那里非常舒服，糟糕，非常舒服，真是这样。
- [04:13.0-04:32.9] 一直触碰到深处，非常触碰，那里很硬。啊，就是那里，啊，很舒服。
- [04:32.9-04:50.4] 啊，越来越强烈，非常，那种，吐息的感觉很清晰。
- [04:50.4-05:06.8] 嗯，那个，非常，那里舒服，糟糕，来，让我们更愉悦一些吧。
- [05:06.8-05:27.2] 糟糕，那个，要去了，就是那里，不行，啊，请安静，那个，要去了，要去了，啊，要去了。
- [05:27.2-05:36.8] 变得非常颤抖，非常厉害。
- [05:36.8-06:07.4] 啊，是的，啊，非常舒服，啊，舒服，这也是，很舒服呢，既然这样，那就更靠近哥哥，腰部不停摆动呢。
- [06:07.4-06:11.9] 非常舒服。
- [06:11.9-06:30.0] 啊，舒服，啊啊啊，非常，啊，很舒服，是在那个地方吗？
- [06:30.0-06:47.0] 分开后很舒服，请多多摩擦，很舒服。
- [06:47.0-06:57.8] 是的，是啊，说起来，变得舒适了。
- [06:57.8-07:04.0] 非常激烈，就是那里，就是那里。
- [07:04.0-07:27.2] 啊啊啊，非常，啊，很舒服。舒服，非常舒服，非常，看起来很好。
- [07:27.2-07:45.3] 我无法忍耐呢。我的交融，两个人都看起来非常愉悦，真是这样。
- [07:45.3-08:13.1] 是的，这个阴茎真的很舒服呢。一直触碰到深处，真是舒服。来吧，也来我这里！
- [08:13.1-08:21.0] 请进入，已经进去了。
- [08:21.0-08:27.8] 啊，太紧绷了，糟糕。
- [08:27.8-08:38.5] 非常，能恢复过来。竟然变得这么湿润了吗？
- [08:38.5-08:41.9] 一下子深入深处。
- [08:41.9-09:03.5] 啊，已经出来了，但还有这个，啊啊，贝贝，真是糟糕，哥哥是绝伦的吗？
- [09:03.5-09:10.3] 就是那里，那个，真舒服。
- [09:10.3-09:28.4] 真是厉害，是的，很舒服，要去了，所以还要继续，继续，继续，继续，继续。
- [09:28.4-09:45.3] 非常厉害，非常，很有活力，非常厉害，真是这样，竟然动得这么厉害。
- [09:45.3-10:12.0] 糟糕，已经无法忍耐了不是吗？啊，哥哥真舒服，既然这么紧绷，应该还会出来吧。
- [10:12.0-10:41.4] 嗯，来，好的，还没结束呢，说着好的。怎么办？要出来了吗？也请给我，哥哥的，在我的里面。
- [10:41.4-11:00.3] 真是这样，哥哥，来，让我看看，哥哥，请在这里，这里，啊，好厉害，哥哥，请让我看看哥哥。
- [11:00.3-11:34.3] 哥哥，啊，请让我看看哥哥。哥哥，啊，好厉害，哥哥，请让我看看哥哥。
- [11:34.3-11:57.4] 啊，哥哥，好厉害，哥哥，请让我看看哥哥。
- [11:57.4-12:08.6] 哥哥，啊，好厉害，哥哥，请让我看看哥哥。
- [12:08.6-12:13.7] 请继续，也请让我们感到愉悦。
- [12:13.7-12:47.6] 接下来我们会让您更感到愉悦，请客人就这样躺好休息。真的很厉害呢。
- [12:47.6-13:14.2] 又变成了这样，又变大了，衣服都快撑破了，真是厉害的阴茎。
- [13:14.2-13:39.1] 这边的乳头也变成了这样，变得非常温暖了，乳头也变得硬挺起来了呢。
- [13:39.1-13:52.2] 又有了那种很舒服的感觉，真是可爱呢。
- [13:52.2-13:56.1] 真是厉害的声音。
- [13:56.1-14:31.2] 明白了呢，真是厉害，还很精神呢，这样的话应该很快就能进去了吧。那我先来品尝一下好了。
- [14:31.2-14:40.9] 客人请保持不动。
- [14:40.9-14:41.4] 。
- [14:41.4-14:49.3] 哇，全部张开了呢。
- [14:49.3-15:04.6] 怎么样，很舒服吗？又变得这么坚硬。
- [15:04.6-15:26.1] 客人真是绝伦呢，这个声音很美妙，咕叽咕叽的声音不是吗。
- [15:26.1-15:33.5] 听到了很多这样的声音。
- [15:33.5-15:35.8] 是吗。
- [15:35.8-15:45.4] 咔啦咔啦，非常，更加，非常。
- [15:45.4-16:14.8] 那真是厉害，感觉要进入深处了。非常柔软，看，都能看到，已经全部吞下我了呢。

## Timeline
- [16:14.8-16:26.1] 好厉害，这里，非常，感觉非常舒服。
- [16:26.1-16:35.2] 不行，我，快要到了。
- [16:35.2-16:43.7] 好漂亮，好厉害，稍微，很舒适。
- [16:43.7-16:48.8] 腰停不下来，啊，好厉害。
- [16:48.8-17:09.7] 这里很可爱呢，感觉舒服吗？我会让你更加舒适，出来吧，哎呀。
- [17:09.7-17:17.1] 感觉有点害羞，感觉到了，请等一下。
- [17:17.1-17:24.5] 已经，很满足了，太棒了。
- [17:24.5-17:26.2] 嗯。
- [17:26.2-17:51.6] 在里面，好厉害，在颤抖呢，还不够大吗？看着，我也做了，这次，我和您一起做吧。
- [17:51.6-18:01.3] 这次轮到我了，也请快点品尝一下。
- [18:01.3-18:06.3] 要进去了哦。
- [18:06.3-18:09.2] 进去了。
- [18:09.2-18:31.8] 啊，好舒服，一直都很硬，真不得了，真的非常硬呢，好厉害。
- [18:31.8-18:49.9] 感觉好舒服，发出了很淫靡的声音，呼，哥哥也很舒服吧？
- [18:49.9-19:08.1] 请变得更加舒适，表情已经忍耐不住了，看起来很结实。
- [19:08.1-19:13.1] 啊，好舒服。
- [19:13.1-19:17.1] 好厉害，来了。
- [19:17.1-19:48.2] 非常舒适，这样好吗？真让人烦恼，好厉害，不行，快要去了，来了，来了，超级舒服。
- [19:48.2-19:48.8] [不可辨语音]
- [19:48.8-20:10.9] 完全停不下来，你还是那么坚硬，一点都没变呢，好厉害，哥哥好厉害。
- [20:10.9-20:26.2] 这张脸也渐渐红润起来了呢，感觉舒服吗？
- [20:26.2-20:48.3] 好可爱，我也非常舒服。快要来了，水流非常猛烈。
- [20:48.3-20:53.3] 正在，颤抖着。
- [20:53.3-21:09.2] 好舒服，嗯，大家也看着呢，我也很想进去了。
- [21:09.2-21:13.7] 要交换吗？
- [21:13.7-21:25.1] 好厉害，还是这样的状态呢。
- [21:25.1-21:41.5] 那么接下来轮到我要进去了，请好好看着慢慢进入的样子。
- [21:41.5-21:51.7] 进去了，进去了，连熊都感动得哭了。
- [21:51.7-21:58.5] 怎么样？好舒服。
- [21:58.5-22:14.3] 被骑在上面，因为兴奋所以取不下来，真是不可思议呢。
- [22:14.3-22:30.7] 这边也来触碰一下吗？我们会把全部都榨取出来哦。
- [22:30.7-22:42.6] 拿着，那个表情，请让我看得更清楚一点。
- [22:42.6-22:50.0] 感觉到了吗？想看得更清楚。
- [22:50.0-23:15.4] 变得更加舒服吧，啊好厉害，这个，后面，不行，不行，这个要去了，啊好厉害，好，去了。
- [23:15.4-23:21.7] 今天可能是最厉害的一次。
- [23:21.7-23:30.7] 还不够，所以再稍微一点。
- [23:30.7-23:48.8] 请向我们展示，还一直可以吧？可以做到吧？
- [23:48.8-24:01.3] 让您感到舒适，真淫靡，啊好舒服呢。
- [24:01.3-24:15.4] 正在里面，原本的状态增加了，就这样继续。
- [24:15.4-24:25.1] 更加，更加地动着，正在做着。
- [24:25.1-24:30.7] 很激烈，怎么了？
- [24:30.7-24:42.6] 快要去了，请您释放，也请让我感受。
- [24:42.6-24:51.7] 不行，不行，不行，不行，要去了。
- [24:51.7-25:04.1] 一起去到了呢，出来了那么多，有很多呢。
- [25:04.1-25:05.3] 了？
- [25:05.3-25:23.4] 啊，原来里面是这样的，出了很多呢，出了很多吗？
- [25:23.4-25:31.3] 呼，结束了，好厉害。
- [25:31.3-25:42.6] 美味，美味，特别是哪里都充满了。
- [25:42.6-26:00.2] 这个，我主要是精子，本来要滴落下来的，太棒了。
- [26:00.2-26:19.4] 好厉害，精液很美味，好厉害，出了这么多，还有这么棒的精液，还在流出。
- [26:19.4-26:50.0] 到底积攒了多少啊，充满了，做得很好呢，这样就可以集中处理了，可以剪辑了，那么。
- [26:50.0-26:59.1] 继续剪辑的部分吧。

## Notes
- **ASR 不确定点**：
  - [20:48.3-20:53.3] 原文“てんだビクビクし”中“てんだ”可能是“てる”或“てんだ”的误识，结合语境理解为“正在颤抖”。
  - [21:41.5-21:51.7] 原文“熊まで泣いちゃった”直译为“连熊都哭了”，在成人语境下可能指代某种特定反应或比喻，保留直译。
  - [24:01.3-24:15.4] 原文“ってますよ中本がとざいま増えてわそのままついてと”存在较多断句和识别噪声，整理时保留了核心语义“里面”、“原本状态”、“增加”、“继续”，去除了连接词的冗余。
- **明显噪声**：
  - 多处出现“すっご”、“すご”、“ご”等词汇的重复或截断，已在整理中合并为“好厉害”、“非常”等完整表达。
  - [19:48.2-19:48.8] 原文仅有一个句号，标记为不可辨语音或短暂停顿。
  - [25:04.1-25:05.3] 原文“れ？”为单字疑问，保留。
  - 部分条目中“気持ちいい”（舒服/舒适）高频出现，根据语境在翻译中微调为“舒服”、“舒适”或“好舒服”以避免单调，但核心词义保持一致。
```

### LLM Input Timeline

```text
[00:00.0-00:20.4] う惜しくなっちゃった 私たちのことも気持ちよくして ほら、入れてあげて。
[00:20.4-00:25.5] あった入っちゃた。
[00:25.5-00:31.1] もと腰動返しすごい。
[00:31.1-00:45.3] すごいすごい疲れてますね 奥に当たって気持ちいい。
[00:45.3-01:00.0] こい声しちゃったい気持ちよさそう あそれ気持ちいい。
[01:00.0-01:19.3] いっぱい疲れてるから触っちゃうだでこ揺がちゃってる恥ずかしすごいい。
[01:19.3-01:32.3] テレビの みんなの手あたかい エッチでしうら。
[01:32.3-01:59.4] あああ、気持ちい。こっちも変わってほしいんじゃないですかああねお兄さんも気持ちいいああ、嬉しい。
[01:59.4-02:12.5] ああもっとついてきくなっちゃってとつすごのと。
[02:12.5-02:16.4] 激いちゃって。
[02:16.4-02:29.5] 激しいめなで気持ち気持ちくしてもなんだ気持ち。
[02:29.5-02:31.1] かい。
[02:31.1-02:43.0] ご全然ほし止まらないやい中興奮してる顔目。
[02:43.0-02:50.4] あ、いくいくいくいくいく。
[02:50.4-02:57.2] ごい入っちゃった すの。
[02:57.2-03:26.6] そうすごい気持ちよかったすごいビクビク持ち縦てガチガチなんだもん。まだいけますよね。ゆきちゃん交退しよ。
[03:26.6-03:36.3] 私のことも気持ちよくしてください。
[03:36.3-03:40.8] いっぱいついて。
[03:40.8-03:56.6] すごい入ってるあガチガチガチすごいガチガチああ、すごい。
[03:56.6-04:13.0] あそこすごい気持ちいいやばすごい気持ちいいそういっちゃい。
[04:13.0-04:32.9] 奥まで当たってるすごく当ってる そこ硬い あ、そこだべああ気持ちいい。
[04:32.9-04:50.4] ういだんだん悪くなってすごいそれ、気持ち吐ってるのよく見える。
[04:50.4-05:06.8] んそれすごあそこ気持ちやばほらもっと気持ちよくしてあげて。
[05:06.8-05:27.2] やばそれいくそこだめあ黙ってそれいっちゃうや待っていく行くいく あ行く。
[05:27.2-05:36.8] すごいビクビクしちゃっいったすご。
[05:36.8-06:07.4] あたいはいあ、すごいいああ、気持ちこれもれ気持ちいいんだなったらもっとくっついてお兄さんに腰してまらないね。
[06:07.4-06:11.9] ご気持ちすごい。
[06:11.9-06:30.0] ああ、気持ちいあああ、すごいああ、気持ちいいいとこかがってるの？
[06:30.0-06:47.0] わたって気持ちいいいいのいっぱい擦ってあげて気持ちいいされ。
[06:47.0-06:57.8] そそう言っちゃうてかしくなって気持ち。
[06:57.8-07:04.0] 激しいだメそこだメそ。
[07:04.0-07:27.2] ああああ、すごああ、気持ちいい。気持ちいすごい気持ちいいすごよく見ちゃったっても。
[07:27.2-07:45.3] 私我慢できないね私の交え二人ともすごい気持ちよさそうなんだもん。
[07:45.3-08:13.1] だって、このおちんちん気持ちいいんですよ 迷くまで当たってちめちゃ気持ちいい ほらね 私にも来て！
[08:13.1-08:21.0] あげてあげて 入っちゃった。
[08:21.0-08:27.8] あビンビンすぎ やばい。
[08:27.8-08:38.5] すご壊できた そんなに濡れちゃうのメ？
[08:38.5-08:41.9] きなり奥ま。
[08:41.9-09:03.5] あ出してるのにまだこのああベべェなんてやばいよお兄さんって絶縁なんですかあ？
[09:03.5-09:10.3] だメてそご気持ち悪い 。
[09:10.3-09:28.4] やばいますねいて気持ちいいていっちゃうからまだいくくくくくいく。
[09:28.4-09:45.3] ちっとすごいごい元気すごいカビカしねそんなに動いてるんです。
[09:45.3-10:12.0] ばいよもう我慢できないんじゃないああお兄さん気持ちいいこんなにビンビンなんだからまだ出るよね。
[10:12.0-10:41.4] うんほらいいよきってないいよって言ってくれてるよどうすんの？出しちゃうの？私の中にもちょうだい兄さんの。
[10:41.4-10:52.1] ああそう、気持ちいいすごダめだダメだ。
[10:52.1-11:10.8] ち気持ちいい一緒行こう だメだメいくいくいくいくいくいくいくいく。
[11:10.8-11:16.5] 激し気持ちよさそう。
[11:16.5-11:21.0] ってるよいばい。
[11:21.0-11:29.5] いっぱい出しちゃったんですね。
[11:29.5-11:48.2] あ見てすごい濃なたくさん出たねまたいっぱい出しちゃったんで、すね。
[11:48.2-12:08.6] ドロドロ すごいでも、まだまだビンビンみたいだね まだまだできますよね。
[12:08.6-12:13.7] もっとしましょう。
[12:13.7-12:47.6] 次 は 私 たちが もっと 気持ち よく して あげ ます から、お 客 様は そのまま 寝 てて ください すごいね。
[12:47.6-13:14.2] またこんなになっちゃって また大きくなってる 服ふかついちゃうんで、すね すごいこのちんちん。
[13:14.2-13:39.1] こっちの乳首っちゃう すごい暖くなってますよ 乳首までピンピンになってきちゃいましたね。
[13:39.1-13:52.2] また気持ちよさそうな感じしてる こエっチなと。
[13:52.2-13:56.1] すごいガちい。
[13:56.1-14:31.2] わかっちゃったの すごい まだ元気なんですね これならもうすぐ入っちゃいそうですね じゃあ 早速私がいただいちゃおうかな 。
[14:31.2-14:40.9] お様はそのまま動かないでください。
[14:40.9-14:41.4] 。
[14:41.4-14:49.3] ほ、全部開いちゃいましたよ。
[14:49.3-15:04.6] どうですか 気持ちいいですか またこんなに硬くなんて。
[15:04.6-15:26.1] 本当に絶倫ですねお客様 こいつの音としてますよ ぐちゃぐちゃじゃないですか。
[15:26.1-15:33.5] ちな音いっぱい聞こえます。
[15:33.5-15:35.8] ですか。
[15:35.8-15:45.4] クリクリすごいたた もっとめちも。
[15:45.4-16:14.8] それすごい奥まで入りそう。すごいロいですよ。ほら、見えてます。全部飲み込んじゃってますよ、私のおまんこ。
[16:14.8-16:26.1] あすごああここすっごはたって気持ちいい。
[16:26.1-16:35.2] こダメ 私、いっちゃいそうです。
[16:35.2-16:43.7] いい顔なすごちょっ気持ちよく。
[16:43.7-16:48.8] 腰止まんないあす。
[16:48.8-17:09.7] こちが可愛いね 気持ちいいんですか もっともっと気持ちよく出しますねあら。
[17:09.7-17:17.1] ちクスしてく感じて待って。
[17:17.1-17:24.5] もうマ足くいったいすごい。
[17:24.5-17:26.2] うん。
[17:26.2-17:51.6] 中で すごいビクついてる あまだ大きいですか 見て ナ 私もした 今度は 私としましょう。
[17:51.6-18:01.3] 今度は私の番 も早く味わってみて。
[18:01.3-18:06.3] 入れちゃいますね。
[18:06.3-18:09.2] いっちゃ。
[18:09.2-18:31.8] あ、気持ちいい ずっと硬くてやばいやないかな すごい本当にずっと硬たいですねご。
[18:31.8-18:49.9] 気持ちすごいいやらしい音してるすうお兄さんも気持ちいいでしょう？
[18:49.9-19:08.1] もっと気持ちよくなってください たまらない顔してるがっち見しい。
[19:08.1-19:13.1] ああ、気持ちいい。
[19:13.1-19:17.1] そごいきたる。
[19:17.1-19:48.2] めっち気持ちよくそうなていいの 悩ましい ますご こだめいきそう あだメいく あいくいく すっごい気持ちいい。
[19:48.2-19:48.8] 。
[19:48.8-20:10.9] 全然止まんない まだガチガチなお前全然変わんないよ すごいねお兄さんあいすご。
[20:10.9-20:26.2] こど顔もだんどんとらけてきちゃってね気持ちいいですか。
[20:26.2-20:48.3] 可わい私もめっちゃ気持ちいいです。かれいっちゃうよめっちゃまなく流れる激しい。
[20:48.3-20:53.3] てんだビクビクし。
[20:53.3-21:09.2] 気持ちい ね みんなも見てた、私も入れたくなっちゃった。
[21:09.2-21:13.7] 交代しましょう？
[21:13.7-21:25.1] すごい まだこんなになってるのいですね。
[21:25.1-21:41.5] じゃあ次は私が入れちゃうね ちゃんと生えていくところ見て。
[21:41.5-21:51.7] 入った 入った 熊まで泣いちゃった。
[21:51.7-21:58.5] どうですか 気持ちいい。
[21:58.5-22:14.3] 上に乗られて 時き取れないの興奮してるんだ 変対ですね。
[22:14.3-22:30.7] こっちも触っちゃうかな 私たちが全部搾り取っちゃいますよ。
[22:30.7-22:42.6] 持ち さそうなと もっとその顔よく見せて。
[22:42.6-22:50.0] 感じてるか、もっと見たい。
[22:50.0-23:15.4] もっと気持ちよくなって あすごいこれ 後いやばいな やばい これいく あすごい はいいく。
[23:15.4-23:21.7] す今日一番大きいかも。
[23:21.7-23:30.7] まだ足りないから ちょっとだけ。
[23:30.7-23:48.8] さそうなか私たちに見せて まだまだできますよね うできるでしょ？
[23:48.8-24:01.3] 気持ちよくさせて やらしい あ気持ちいだね。
[24:01.3-24:15.4] ってますよ中本がとざいま増えてわそのままついてと。
[24:15.4-24:25.1] もっともっと動くなったこしてるよ。
[24:25.1-24:30.7] 激しい どうしたの？
[24:30.7-24:42.6] いきそう あなたに出して、私にもちなせし。
[24:42.6-24:51.7] なでダメダメダメダメいっちゃう。
[24:51.7-25:04.1] 一緒に行っちゃったねいっぱいれたのあったか。
[25:04.1-25:05.3] れ？
[25:05.3-25:23.4] あどなかこんなに出たんだ いっぱい出しましたね いっぱい出てる？
[25:23.4-25:31.3] はッきりしま した すごい。
[25:31.3-25:42.6] 美味しい美味しい 特にいついちゃってる。
[25:42.6-26:00.2] これにたん私精しかついてますよ本どたれちゃっためちゃおうかな。
[26:00.2-26:19.4] ごい精子美味しいごいいっぱい出したのにこんなすごい精子まだ出るんだ。
[26:19.4-26:50.0] もうどんだけ溜ま ってたの いっぱいスッきーできてよかったですね これで集中して カットできま すね じゃ。
[26:50.0-26:59.1] カットの続きしていきましょうか。
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
