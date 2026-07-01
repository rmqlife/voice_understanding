# fbank_lfr_cmvn_feature.json 是什么？

仓库根目录下的 `fbank_lfr_cmvn_feature.json` 是 **FunASR / SenseVoice 官方 Python 后端**在跑 ASR 时自动写出的 **CMVN 特征统计文件**，不是手写的业务配置。

## 含义

| 部分 | 含义 |
|------|------|
| **fbank** | Filter Bank，梅尔滤波器组声学特征 |
| **lfr** | Low Frame Rate，降帧率（把多帧特征拼接，降低时间分辨率） |
| **cmvn** | Cepstral Mean and Variance Normalization，倒谱均值方差归一化 |

文件内容是一大段浮点数组：模型在推理时对声学特征做归一化用的 **mean/variance 向量**（与训练时统计一致）。

## 何时出现

使用 `pixi run sv ... --backend official` 或 `SenseVoice(backend="official")` 时，FunASR 可能在**当前工作目录**生成该文件。属于运行时缓存/中间产物。

## 要不要管

- **已在 `.gitignore`** — 不要提交进仓库。
- **可以删** — 下次跑 official ASR 会再生成；删了不影响源码。
- **与字幕/转写逻辑无关** — `python/sense_voice/` 和 `scripts/` 都不读这个文件；只有 FunASR 内部用。

## 与 SenseVoice.cpp 的关系

C++ 后端用编译进二进制的 CMVN（见 mac 分支 `SenseVoice.cpp/scripts/generate-cmvn.py` → `sense-voice-cmvn.h`），**不会**生成这个 JSON。该 JSON 是 **official 后端专用** 的产物。
