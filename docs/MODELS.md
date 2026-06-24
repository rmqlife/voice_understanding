# 模型缓存与预下载

## 缓存路径（mag / Linux）

| 用途 | 环境变量 | 默认路径 |
|------|----------|----------|
| FunASR / ModelScope | `MODELSCOPE_CACHE` | `~/.cache/modelscope` |
| Hugging Face / pyannote | `HF_HOME` | `~/.cache/huggingface` |
| Hugging Face token | `HF_TOKEN` | — |

代码入口：`python/sense_voice/models.py` → `modelscope_cache_dir()` / `huggingface_cache_dir()`

## 预下载

```bash
# mag：ASR + FunASR cam++ diarization
pixi run download-transcript-models -- --device cuda:0

# 可选：pyannote（需先在 HF 接受模型条款并设置 HF_TOKEN）
export HF_TOKEN=...
pixi run install-diarize
pixi run download-transcript-models -- --pyannote
```

## 模型清单

| 模型 | 用途 | 后端 |
|------|------|------|
| `iic/SenseVoiceSmall` | ASR | `pixi run sv --backend official` |
| `iic/speech_seaco_paraformer_large_...` + `cam++` | 说话人 diarization | `transcript-test --diarize-method funasr` |
| `pyannote/speaker-diarization-3.1` | diarization 对比 | `compare-diarize` / `--diarize-method pyannote` |

## 长音频 ASR 分块

official 后端默认 `chunk_seconds=600`：超过 10 分钟在静音附近切分，逐块 ASR 后按时间偏移拼接。

```bash
pixi run sv long.wav --backend official --chunk-seconds 600
pixi run sv --clips test_voice_clips --name-filter kavr --backend official
```

`--chunk-seconds 0` 关闭分块。
