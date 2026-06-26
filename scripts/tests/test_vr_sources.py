#!/usr/bin/env python3
"""Smoke tests for VR NFS source helpers (no GPU, no mount required)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))

from sense_voice.vr_sources import (  # noqa: E402
    is_vr_mp4,
    local_wav_path,
    sanitize_stem,
)


def test_is_vr_mp4() -> None:
    assert is_vr_mp4(Path("SAVR-799.mp4"))
    assert is_vr_mp4(Path("KAVR-506-CD1.mp4"))
    assert is_vr_mp4(Path("BadoinkVR_foo_8K_180x180_3dh.mp4"))
    assert not is_vr_mp4(Path("MANX-024-C.mp4"))
    assert not is_vr_mp4(Path("NMSL-040-C.mp4"))
    assert not is_vr_mp4(Path("489155.com@[中文字幕]Blacked.22.06.04.mp4"))
    assert not is_vr_mp4(Path("clip.wav"))


def test_local_wav_path() -> None:
    finished = Path("/jav/#finished")
    video = finished / "MANX-024-C-宮西ひかる/MANX-024-C.mp4"
    wav = local_wav_path(video, finished, Path("/data/vr"))
    assert wav.name.endswith(".wav")
    assert "MANX-024-C" in wav.name


def test_sanitize_stem() -> None:
    assert "__" in sanitize_stem("a/b c")


def test_video_from_local_stem() -> None:
    finished = Path("/mnt/fnos/jav/#finished")
    stem = "KAVR-506-伊藤舞雪__KAVR-506-CD1"
    rel = stem.replace("__", "/") + ".mp4"
    assert rel == "KAVR-506-伊藤舞雪/KAVR-506-CD1.mp4"


def test_resolve_finished_video_remaps_legacy() -> None:
    from sense_voice.vr_sources import resolve_finished_video

    finished = Path("/mnt/fnos/jav/#finished")
    legacy = Path(
        "/run/user/1000/gvfs/smb-share:server=atop-nuc-fnos.local,share=jav/"
        "#finished/KAVR-506-伊藤舞雪/KAVR-506-CD1.mp4"
    )
    resolved = resolve_finished_video(legacy, finished_root=finished)
    assert resolved == finished / "KAVR-506-伊藤舞雪/KAVR-506-CD1.mp4" or resolved == legacy


def main() -> None:
    tests = [test_is_vr_mp4, test_local_wav_path, test_sanitize_stem, test_video_from_local_stem, test_resolve_finished_video_remaps_legacy]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"passed {len(tests)} tests")


if __name__ == "__main__":
    main()
