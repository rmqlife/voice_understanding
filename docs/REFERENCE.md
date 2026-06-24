# 外部参考仓库（不提交 git）

`reference/` 目录在 `.gitignore` 中，用于本地 clone 对照或可选依赖。

```bash
mkdir -p reference

# 字幕时间轴设计参考（只读）
git clone https://github.com/krillinai/KrillinAI reference/KrillinAI

# 可选：main 上本地编译 cpp 后端（推荐 Mac 直接用 mac 分支）
git clone https://github.com/lovemefan/SenseVoice.cpp reference/SenseVoice.cpp
pixi run build   # 产物：reference/SenseVoice.cpp/build/bin/sense-voice-main
```

| 路径 | 用途 | 是否在 main git |
|------|------|-----------------|
| `reference/KrillinAI` | KrillinAI 字幕 pipeline 对照 | 否 |
| `reference/SenseVoice.cpp` | 可选 C++ ASR 编译 | 否 |
| `SenseVoice.cpp/`（仓库根） | **仅 `mac` 分支** vendor | mac 分支是 |
