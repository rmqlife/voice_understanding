"""Load/write subtitle batch task lists (TOML)."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]


@dataclass
class SubtitleDefaults:
    language: str = "ja"
    profile: str = "vr"
    asr_backend: str = "official"
    asr_device: str = "cuda:0"
    asr_model: str | None = None
    asr_chunk_seconds: float | None = 0
    polish_model: str = "nsfw-local:27b"
    chunk_chars: int = 3000
    chunk_segments: int = 80
    llm_timeline: str = "compact"
    skip_existing: bool = True
    skip_polish: bool = False
    use_gpu_lock: bool = True
    wav_dir: str = "data/vr"
    srt_dir: str = "results/srt"
    mount: bool = False
    finished_root: str = ""


@dataclass
class SubtitleVideo:
    path: str
    enabled: bool = True
    note: str = ""


@dataclass
class SubtitleTask:
    label: str
    created: str
    defaults: SubtitleDefaults = field(default_factory=SubtitleDefaults)
    videos: list[SubtitleVideo] = field(default_factory=list)

    def enabled_videos(self) -> list[SubtitleVideo]:
        return [video for video in self.videos if video.enabled]


def _toml_bool(value: bool) -> str:
    return "true" if value else "false"


def _toml_str(value: str | None) -> str:
    if value is None:
        return '""'
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def write_subtitle_task(path: Path, task: SubtitleTask) -> None:
    """Write task.toml (hand-formatted; no extra TOML writer dependency)."""
    defaults = task.defaults
    lines = [
        f"# Subtitle batch task — generated {task.created}",
        f'label = {_toml_str(task.label)}',
        f"created = {_toml_str(task.created)}",
        "",
        "[defaults]",
        f"language = {_toml_str(defaults.language)}",
        f"profile = {_toml_str(defaults.profile)}",
        f"asr_backend = {_toml_str(defaults.asr_backend)}",
        f"asr_device = {_toml_str(defaults.asr_device)}",
        f"asr_model = {_toml_str(defaults.asr_model)}",
        f"asr_chunk_seconds = {defaults.asr_chunk_seconds if defaults.asr_chunk_seconds is not None else 0}",
        f"polish_model = {_toml_str(defaults.polish_model)}",
        f"chunk_chars = {defaults.chunk_chars}",
        f"chunk_segments = {defaults.chunk_segments}",
        f'llm_timeline = {_toml_str(defaults.llm_timeline)}',
        f"skip_existing = {_toml_bool(defaults.skip_existing)}",
        f"skip_polish = {_toml_bool(defaults.skip_polish)}",
        f"use_gpu_lock = {_toml_bool(defaults.use_gpu_lock)}",
        f"wav_dir = {_toml_str(defaults.wav_dir)}",
        f"srt_dir = {_toml_str(defaults.srt_dir)}",
        f"mount = {_toml_bool(defaults.mount)}",
        f"finished_root = {_toml_str(defaults.finished_root)}",
        "",
    ]
    for video in task.videos:
        lines.extend(
            [
                "[[videos]]",
                f"path = {_toml_str(video.path)}",
                f"enabled = {_toml_bool(video.enabled)}",
            ]
        )
        if video.note:
            lines.append(f"note = {_toml_str(video.note)}")
        lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def load_subtitle_task(path: Path, *, repo_root: Path | None = None) -> SubtitleTask:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    defaults_raw = raw.get("defaults", {})
    defaults = SubtitleDefaults(**_coerce_defaults(defaults_raw))
    videos: list[SubtitleVideo] = []
    for item in raw.get("videos", []):
        if not isinstance(item, dict):
            continue
        path_value = str(item.get("path", "")).strip()
        if not path_value:
            continue
        videos.append(
            SubtitleVideo(
                path=path_value,
                enabled=bool(item.get("enabled", True)),
                note=str(item.get("note", "")).strip(),
            )
        )
    if not videos:
        raise ValueError(f"no videos in task file: {path}")
    return SubtitleTask(
        label=str(raw.get("label", path.stem)),
        created=str(raw.get("created", "")),
        defaults=defaults,
        videos=videos,
    )


def _coerce_defaults(raw: dict[str, Any]) -> dict[str, Any]:
    fields = {item.name for item in SubtitleDefaults.__dataclass_fields__.values()}  # type: ignore[attr-defined]
    out: dict[str, Any] = {}
    for key, value in raw.items():
        if key in fields:
            if key == "asr_chunk_seconds" and value in {"", None}:
                out[key] = None
                continue
            out[key] = value
    return out


def video_has_srt(
    video: Path,
    *,
    finished_root: Path,
    wav_dir: Path,
    srt_dir: Path,
) -> bool:
    from .vr_sources import local_wav_path

    stem = local_wav_path(video, finished_root, wav_dir).stem
    asr_srt = srt_dir / f"{stem}.asr.srt"
    zh_srt = srt_dir / f"{stem}.zh.srt"
    return asr_srt.is_file() and zh_srt.is_file()


def new_task_from_videos(
    videos: list[Path],
    *,
    label: str,
    defaults: SubtitleDefaults | None = None,
    finished_root: Path | None = None,
    wav_dir: Path | None = None,
    srt_dir: Path | None = None,
    disable_completed: bool = True,
) -> SubtitleTask:
    defaults = defaults or SubtitleDefaults()
    wav_dir = wav_dir or Path(defaults.wav_dir)
    srt_dir = srt_dir or Path(defaults.srt_dir)
    ordered = sorted(videos, key=lambda path: path.as_posix().casefold())
    entries: list[SubtitleVideo] = []
    for path in ordered:
        resolved = path.resolve()
        completed = (
            disable_completed
            and finished_root is not None
            and video_has_srt(
                resolved,
                finished_root=finished_root,
                wav_dir=wav_dir,
                srt_dir=srt_dir,
            )
        )
        entries.append(
            SubtitleVideo(
                path=str(resolved),
                enabled=not completed,
                note="srt exists" if completed else "",
            )
        )
    return SubtitleTask(
        label=label,
        created=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        defaults=defaults,
        videos=entries,
    )


def task_summary(task: SubtitleTask) -> dict[str, Any]:
    enabled = task.enabled_videos()
    return {
        "label": task.label,
        "created": task.created,
        "videos_total": len(task.videos),
        "videos_enabled": len(enabled),
        "videos_disabled": len(task.videos) - len(enabled),
        "defaults": asdict(task.defaults),
        "paths": [video.path for video in enabled],
    }


def print_task_summary(task: SubtitleTask) -> None:
    print(json.dumps(task_summary(task), ensure_ascii=False, indent=2))
