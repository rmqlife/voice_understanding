# archive/

试过、但当前主线不再使用的代码与报告。保留在仓库里方便复现，**不参与 pipeline**，不被 `python/sense_voice` 或 `scripts/` import。

| 目录 | 内容 | 归档原因 |
|------|------|----------|
| `pyannote/` | `diarize_pyannote.py`、`models_pyannote.py` 快照 + 对比报告 | 实验结论：与 FunASR cam++ 相当，非主路径（见 `docs/TODO-transcript.md`） |
| `reports/` | `diarize_compare.*`、`geng_ruixiang_vad_*` | vad / diarize 对比实验产物 |
| `mac/` | `build.sh`、`download_model.py`、`MAC.md` | SenseVoice.cpp / Metal 仅 `mac` 分支用，`main` 不需要 |

## 如何复活 pyannote

1. 把 `pyannote/diarize_pyannote.py` 的函数拷回 `python/sense_voice/diarize.py`，并在 `DiarizeMethod`、`diarize()` 里加回 `pyannote` 分支。
2. 把 `pyannote/models_pyannote.py` 拷回 `python/sense_voice/models.py`。
3. `pip install pyannote.audio`，设置 `HF_TOKEN` 并接受模型条款。
