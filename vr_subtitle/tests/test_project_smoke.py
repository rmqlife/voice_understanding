#!/usr/bin/env python3
"""No-GPU smoke checks for the vr_subtitle subproject."""

from __future__ import annotations

import py_compile
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_ROOT = ROOT.parent
sys.path.insert(0, str(MAIN_ROOT / "python"))

from sense_voice.subtitle_task import SubtitleDefaults  # noqa: E402
from sense_voice.subtitle import build_zh_srt_entries_from_texts  # noqa: E402
from sense_voice.vr_sources import is_vr_mp4, local_wav_path  # noqa: E402


def test_compile_entrypoints() -> None:
    for path in [
        ROOT / "app.py",
        ROOT / "scripts" / "add_subtitle.py",
        ROOT / "scripts" / "gen_subtitle_task.py",
        ROOT / "scripts" / "run_subtitle_task.py",
        ROOT / "scripts" / "cron_subtitle_batch.py",
        ROOT / "scripts" / "publish_vr_srt.py",
        ROOT / "scripts" / "sync_vr_audio.py",
    ]:
        py_compile.compile(str(path), doraise=True)


def test_main_library_imports() -> None:
    assert is_vr_mp4(Path("SAVR-799.mp4"))
    assert is_vr_mp4(Path("ATVR-068-CD1.mp4"))
    assert is_vr_mp4(Path("FAVR-004-CD1.mp4"))
    assert is_vr_mp4(Path("BIBIVR-129-CD1.mp4"))
    assert not is_vr_mp4(Path("MANX-024-C.mp4"))
    defaults = SubtitleDefaults()
    assert defaults.wav_dir == "data/vr"
    assert defaults.finished_root == ""
    assert defaults.asr_chunk_seconds == 0


def test_local_output_stem() -> None:
    finished = Path("/mnt/fnos/jav/#finished")
    video = finished / "SAVR-799/SAVR-799.mp4"
    wav = local_wav_path(video, finished, ROOT / "data" / "vr")
    assert wav == ROOT / "data" / "vr" / "SAVR-799__SAVR-799.wav"


def test_dropped_filler_does_not_create_long_fragment_merge() -> None:
    segments = [
        {"start": 0.0, "end": 1.0, "text": "ちゃんと"},
        {"start": 1.0, "end": 30.0, "text": "あああ"},
        {"start": 30.0, "end": 31.0, "text": "続き"},
    ]
    entries = build_zh_srt_entries_from_texts(
        ["继续", "啊", "地方"],
        segments,
        words=[],
    )
    assert entries == [(0.0, 1.0, "继续"), (30.0, 31.0, "地方")]


def test_short_polished_line_is_duration_capped() -> None:
    entries = build_zh_srt_entries_from_texts(
        ["可以请您开始吗？"],
        [{"start": 1268.74, "end": 1450.57, "text": "お願いします"}],
        words=[],
    )
    assert entries == [(1268.74, 1276.74, "可以请您开始吗？")]


def test_long_polished_line_chunks_are_duration_capped() -> None:
    entries = build_zh_srt_entries_from_texts(
        ["不过看着那个挺起的阴茎，感觉很不错。"],
        [{"start": 669.27, "end": 728.37, "text": "長い原文"}],
        words=[],
    )
    assert entries
    assert max(end - start for start, end, _text in entries) <= 8.01


def test_cache_stage_decision() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    from add_subtitle import add_subtitle_for_video  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        finished = base / "#finished"
        video_dir = finished / "SAVR-799"
        video_dir.mkdir(parents=True)
        video = video_dir / "SAVR-799.mp4"
        video.write_bytes(b"not real media")
        wav_dir = base / "data" / "vr"
        srt_dir = base / "results" / "srt"
        srt_dir.mkdir(parents=True)
        (srt_dir / "SAVR-799__SAVR-799.asr.srt").write_text("asr\n", encoding="utf-8")
        (srt_dir / "SAVR-799__SAVR-799.zh.srt").write_text("done\n", encoding="utf-8")

        result = add_subtitle_for_video(
            video,
            finished_root=finished,
            wav_dir=wav_dir,
            srt_dir=srt_dir,
            skip_existing=False,
            force=False,
            extract_only=False,
            subtitle_only=False,
            publish_only=False,
            start=None,
            duration=None,
            language="ja",
            profile="vr",
            asr_backend="official",
            asr_device=None,
            asr_model=None,
            asr_chunk_seconds=0,
            polish_model="dummy",
            chunk_chars=3000,
            chunk_segments_size=80,
            llm_timeline="compact",
            skip_polish=False,
            use_gpu_lock=False,
            dry_run=False,
        )
        assert result["cache"] == "translated"
        assert (video_dir / "SAVR-799.zh.srt").is_file()
        assert not (video_dir / "SAVR-799.asr.srt").is_file()


def test_web_job_lock() -> None:
    sys.path.insert(0, str(ROOT))
    import app  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        cmd = Path(tmp) / "slow.py"
        cmd.write_text("import time\nprint('start', flush=True)\ntime.sleep(0.4)\nprint('done', flush=True)\n", encoding="utf-8")
        original_root = app.ROOT
        original_jobs = app.JOBS
        original_active = app.ACTIVE_JOB_ID
        try:
            app.ROOT = Path(tmp)
            app.JOBS = {}
            app.ACTIVE_JOB_ID = None
            scripts = Path(tmp) / "scripts"
            scripts.mkdir()
            shutil.copyfile(cmd, scripts / "add_subtitle.py")
            job_id = app.start_job(
                ["/tmp/a.mp4"],
                folder=tmp,
                skip_existing=True,
                skip_polish=False,
                dry_run=True,
                force=False,
            )
            try:
                app.start_job(
                    ["/tmp/b.mp4"],
                    folder=tmp,
                    skip_existing=True,
                    skip_polish=False,
                    dry_run=True,
                    force=False,
                )
                raise AssertionError("expected running job conflict")
            except RuntimeError:
                pass
            assert app.current_status()["busy"] is True
            deadline = time.time() + 3
            while time.time() < deadline and app.current_status()["busy"]:
                time.sleep(0.05)
            status = app.current_status()
            assert status["busy"] is False
            assert status["latest"]["id"] == job_id
            assert status["latest"]["status"] == "done"
        finally:
            app.ROOT = original_root
            app.JOBS = original_jobs
            app.ACTIVE_JOB_ID = original_active


def test_web_scan_max_depth() -> None:
    sys.path.insert(0, str(ROOT))
    import app  # noqa: E402

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        root_video = base / "SAVR-001.mp4"
        one_level = base / "SAVR-002" / "SAVR-002.mp4"
        too_deep = base / "#S" / "SAVR-003" / "SAVR-003.mp4"
        for video in [root_video, one_level, too_deep]:
            video.parent.mkdir(parents=True, exist_ok=True)
            video.write_bytes(b"not real media")

        items = app.scan_videos(folder=tmp)
        paths = {Path(item["path"]) for item in items}
        assert root_video in paths
        assert one_level in paths
        assert too_deep not in paths


def test_folder_task_and_cron_dry_run() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        finished = base / "#finished"
        video_dir = finished / "SAVR-001"
        video_dir.mkdir(parents=True)
        video = video_dir / "SAVR-001.mp4"
        video.write_bytes(b"not real media")
        task = base / "tasks" / "batch.toml"

        gen = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "gen_subtitle_task.py"),
                "--folder",
                str(finished),
                "-o",
                str(task),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert gen.returncode == 0, gen.stderr + gen.stdout
        text = task.read_text(encoding="utf-8")
        assert f'finished_root = "{finished}"' in text
        assert str(video) in text

        run = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_subtitle_task.py"), str(task), "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert run.returncode == 0, run.stderr + run.stdout
        assert "finished 1 video(s)" in run.stdout

        cron_task = base / "tasks" / "cron.toml"
        cron = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "cron_subtitle_batch.py"),
                "--folder",
                str(finished),
                "--task",
                str(cron_task),
                "--lock-file",
                str(base / "cron.lock"),
                "--dry-run",
                "--continue-on-error",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        assert cron.returncode == 0, cron.stderr + cron.stdout
        assert cron_task.is_file()


def main() -> None:
    tests = [
        test_compile_entrypoints,
        test_main_library_imports,
        test_local_output_stem,
        test_dropped_filler_does_not_create_long_fragment_merge,
        test_short_polished_line_is_duration_capped,
        test_long_polished_line_chunks_are_duration_capped,
        test_cache_stage_decision,
        test_web_job_lock,
        test_web_scan_max_depth,
        test_folder_task_and_cron_dry_run,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"passed {len(tests)} tests")


if __name__ == "__main__":
    main()
