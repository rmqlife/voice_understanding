#!/usr/bin/env python3
"""VR subtitle pipeline: NFS mp4 -> local WAV -> SRT -> copy back next to mp4."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _paths import PROJECT_ROOT, add_main_paths

add_main_paths(include_scripts=True)

from sense_voice.audio import extract_wav_from_media  # noqa: E402
from sense_voice.vr_sources import (  # noqa: E402
    finished_dir,
    iter_finished_mp4s,
    local_wav_path,
    resolve_finished_video,
    resolve_jav_root,
)
from publish_vr_srt import publish_srt  # noqa: E402
from subtitle_pipeline import process_clip  # noqa: E402

DEFAULT_SRT_DIR = PROJECT_ROOT / "results" / "srt"


def add_subtitle_for_video(
    video: Path,
    *,
    finished_root: Path,
    wav_dir: Path,
    srt_dir: Path,
    skip_existing: bool,
    force: bool,
    extract_only: bool,
    subtitle_only: bool,
    publish_only: bool,
    start: str | None,
    duration: str | None,
    language: str,
    profile: str,
    asr_backend: str,
    asr_device: str | None,
    asr_model: str | None,
    asr_chunk_seconds: float | None,
    polish_model: str,
    chunk_chars: int,
    chunk_segments_size: int,
    llm_timeline: str,
    skip_polish: bool,
    use_gpu_lock: bool,
    dry_run: bool,
    repolish_only: bool = False,
    release_model_after: bool = True,
) -> dict[str, Path | str | list[Path]]:
    video = resolve_finished_video(video, finished_root=finished_root)
    wav_path = local_wav_path(video, finished_root, wav_dir)
    srt_stem = wav_path.stem
    asr_srt = srt_dir / f"{srt_stem}.asr.srt"
    zh_srt = srt_dir / f"{srt_stem}.zh.srt"

    if dry_run:
        print(f"video: {video}")
        print(f"wav:   {wav_path}")
        print(f"srt:   {srt_dir}/{srt_stem}.{{asr,zh}}.srt")
        return {"video": video, "wav": wav_path, "srt_stem": srt_stem}

    _ = skip_existing  # Compatibility flag; cache-first is the default unless --force is used.
    cache_first = not force
    if cache_first and not publish_only and not extract_only and not repolish_only:
        if zh_srt.is_file():
            print(f"cache hit translated srt {zh_srt}; publish cached files")
            published = publish_srt(video, srt_dir, srt_stem=srt_stem)
            return {
                "video": video,
                "wav": wav_path,
                "srt_stem": srt_stem,
                "cache": "translated",
                "published": published,
            }
        if asr_srt.is_file() and not skip_polish:
            print(f"cache hit asr srt {asr_srt}; translate only")
            repolish_only = True
            subtitle_only = True

    if not publish_only:
        if not subtitle_only or not wav_path.is_file():
            if cache_first and wav_path.is_file():
                print(f"cache hit wav {wav_path}; skip extraction")
            else:
                print(f"extract {video} -> {wav_path}", flush=True)
                extract_wav_from_media(video, wav_path, start=start, duration=duration)
        if extract_only:
            return {"video": video, "wav": wav_path, "srt_stem": srt_stem}

    if not publish_only:
        if not repolish_only and cache_first and asr_srt.is_file() and zh_srt.is_file():
            print(f"skip existing srt {srt_stem}")
        else:
            if not repolish_only and not wav_path.is_file():
                raise FileNotFoundError(f"wav not found: {wav_path}")
            if repolish_only and not asr_srt.is_file():
                raise FileNotFoundError(f"asr srt not found: {asr_srt}")
            print(f"subtitle {wav_path}" + (" (repolish)" if repolish_only else ""), flush=True)
            srt_dir.mkdir(parents=True, exist_ok=True)
            process_clip(
                wav_path,
                language=language,
                asr_backend=asr_backend,
                asr_device=asr_device,
                asr_model=asr_model,
                asr_chunk_seconds=asr_chunk_seconds,
                polish_model=polish_model,
                chunk_chars=chunk_chars,
                chunk_segments_size=chunk_segments_size,
                llm_timeline=llm_timeline,
                profile=profile,
                srt_dir=srt_dir,
                skip_polish=skip_polish,
                use_gpu_lock=use_gpu_lock,
                repolish_only=repolish_only,
                release_model_after=release_model_after,
            )

    print(f"publish -> {video.parent}", flush=True)
    published = publish_srt(video, srt_dir, srt_stem=srt_stem)
    return {"video": video, "wav": wav_path, "srt_stem": srt_stem, "published": published}


def main() -> None:
    parser = argparse.ArgumentParser(description="Add ASR/ZH subtitles for NFS VR mp4")
    parser.add_argument("--video", type=Path, action="append", default=[], help="Single mp4 (repeatable)")
    parser.add_argument("--scan-finished", action="store_true", help="Process VR mp4 under jav/#finished")
    parser.add_argument("--name-filter", default=None)
    parser.add_argument("--all-mp4", action="store_true")
    parser.add_argument("--mount", action="store_true", help="gio mount smb://192.168.1.188/jav")
    parser.add_argument("--finished-root", type=Path, default=None, help="Folder used as the mp4 scan/cache root")
    parser.add_argument("--wav-dir", type=Path, default=PROJECT_ROOT / "data" / "vr")
    parser.add_argument("--srt-dir", type=Path, default=DEFAULT_SRT_DIR)
    parser.add_argument("--skip-existing", action="store_true", help="Compatibility flag; cache-first is the default")
    parser.add_argument("--force", action="store_true", help="Ignore cached WAV/SRT and recompute requested stages")
    parser.add_argument("--extract-only", action="store_true")
    parser.add_argument("--subtitle-only", action="store_true")
    parser.add_argument("--publish-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--start", default=None)
    parser.add_argument("--duration", default=None, help="Limit ffmpeg extract")
    parser.add_argument("--language", default="ja")
    parser.add_argument("--profile", choices=["vr", "subtitle"], default="vr")
    parser.add_argument("--asr-backend", choices=["cpp", "official"], default="official")
    parser.add_argument("--asr-device", default="cuda:0")
    parser.add_argument("--asr-model", default=None)
    parser.add_argument("--asr-chunk-seconds", type=float, default=0, help="Official backend chunk length; 0 disables chunking")
    parser.add_argument("--polish-model", default="nsfw-local:27b")
    parser.add_argument("--chunk-chars", type=int, default=3000)
    parser.add_argument("--chunk-segments", type=int, default=80)
    parser.add_argument("--llm-timeline", choices=["full", "compact"], default="compact")
    parser.add_argument("--skip-polish", action="store_true", help="Skip LLM; .zh.srt duplicates .asr.srt")
    parser.add_argument("--repolish-only", action="store_true", help="Re-run LLM from existing .asr.srt")
    parser.add_argument("--no-gpu-lock", action="store_true", help="Do not wait for data/.subtitle_gpu.lock")
    args = parser.parse_args()

    if args.extract_only and args.publish_only:
        raise SystemExit("--extract-only and --publish-only are mutually exclusive")

    if args.finished_root is not None:
        finished = args.finished_root.expanduser().resolve()
        if not finished.is_dir():
            raise SystemExit(f"finished root not found: {finished}")
    else:
        jav_root = resolve_jav_root(mount=args.mount)
        finished = finished_dir(jav_root=jav_root)
    if args.video:
        videos = [Path(v) for v in args.video]
    elif args.scan_finished:
        videos = iter_finished_mp4s(finished, vr_only=not args.all_mp4, name_filter=args.name_filter, sort_by="size")
    else:
        raise SystemExit("Provide --video or --scan-finished")
    if not videos:
        raise SystemExit("No videos to process")

    for video in videos:
        if not video.is_file():
            raise SystemExit(f"video not found: {video}")
        add_subtitle_for_video(
            video,
            finished_root=finished,
            wav_dir=args.wav_dir,
            srt_dir=args.srt_dir,
            skip_existing=args.skip_existing,
            force=args.force,
            extract_only=args.extract_only,
            subtitle_only=args.subtitle_only,
            publish_only=args.publish_only,
            start=args.start,
            duration=args.duration,
            language=args.language,
            profile=args.profile,
            asr_backend=args.asr_backend,
            asr_device=args.asr_device,
            asr_model=args.asr_model,
            asr_chunk_seconds=args.asr_chunk_seconds,
            polish_model=args.polish_model,
            chunk_chars=args.chunk_chars,
            chunk_segments_size=args.chunk_segments,
            llm_timeline=args.llm_timeline,
            skip_polish=args.skip_polish,
            dry_run=args.dry_run,
            use_gpu_lock=not args.no_gpu_lock,
            repolish_only=args.repolish_only,
        )


if __name__ == "__main__":
    sys.exit(main())
