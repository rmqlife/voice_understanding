"""NFS / fnOS mount VR video discovery under jav/#finished."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

DEFAULT_NFS_HOST = "192.168.1.188"
DEFAULT_NFS_SERVER_NAME = "atop-nuc-fnos.local"
DEFAULT_NFS_SHARE = "jav"
DEFAULT_MOUNT_ROOT = Path("/mnt/fnos/jav")
FINISHED_SUBDIR = "#finished"

LEGACY_PRESETS = {
    "kavr500_part2": (
        f"{DEFAULT_MOUNT_ROOT}/#finished/"
        "KAVR-5008K/489155.com@KAVR-500.PART2_8K.mp4"
    ),
    "kavr500_part3": (
        f"{DEFAULT_MOUNT_ROOT}/#finished/"
        "KAVR-5008K/489155.com@KAVR-500.PART3_8K.mp4"
    ),
}

NON_VR_MARKERS = ("Blacked.", "blacked.")
# Studio / filename must indicate VR (not flat JAV like MANX/NMSL/URE).
VR_STUDIO_MARKERS = (
    "SAVR",
    "KAVR",
    "DSVR",
    "MDVR",
    "VRKM",
    "PXVR",
    "AJVR",
    "SIVR",
    "HVR",
    "WAVR",
    "3DSVR",
    "BadoinkVR",
)
VR_TECH_MARKERS = ("180x180", "3dh")


def gvfs_jav_root(*, uid: int | None = None) -> Path:
    uid = uid if uid is not None else os.getuid()
    server = os.environ.get("VR_NFS_SERVER_NAME", DEFAULT_NFS_SERVER_NAME)
    share = os.environ.get("VR_NFS_SHARE", DEFAULT_NFS_SHARE)
    return Path(f"/run/user/{uid}/gvfs/smb-share:server={server},share={share}")


def mount_jav_share(*, host: str | None = None, share: str | None = None) -> None:
    """Mount SMB share via gio (no local mp4 copy)."""
    host = host or os.environ.get("VR_NFS_HOST", DEFAULT_NFS_HOST)
    share = share or os.environ.get("VR_NFS_SHARE", DEFAULT_NFS_SHARE)
    uri = f"smb://{host}/{share}"
    root = gvfs_jav_root()
    if root.is_dir():
        return
    proc = subprocess.run(["gio", "mount", uri], capture_output=True, text=True)
    if proc.returncode != 0 and not root.is_dir():
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"failed to mount {uri}: {detail}")


def resolve_jav_root(*, mount: bool = False) -> Path:
    """Return jav share root: VR_JAV_ROOT, /mnt/fnos/jav, or gvfs fallback."""
    if env := os.environ.get("VR_JAV_ROOT"):
        root = Path(env)
        if not root.is_dir():
            raise FileNotFoundError(f"VR_JAV_ROOT not found: {root}")
        return root
    if DEFAULT_MOUNT_ROOT.is_dir():
        return DEFAULT_MOUNT_ROOT
    if mount:
        mount_jav_share()
    root = gvfs_jav_root()
    if not root.is_dir():
        mount_jav_share()
        root = gvfs_jav_root()
    if not root.is_dir():
        raise FileNotFoundError(
            f"jav share not found at {DEFAULT_MOUNT_ROOT} or {root}; "
            f"set VR_JAV_ROOT or mount smb://{DEFAULT_NFS_HOST}/{DEFAULT_NFS_SHARE}"
        )
    return root


def resolve_finished_video(video: Path, *, finished_root: Path) -> Path:
    """Resolve mp4 on finished_root; remap legacy gvfs paths via #finished/ suffix."""
    if video.is_file():
        return video
    marker = f"/{FINISHED_SUBDIR}/"
    pos = video.as_posix().find(marker)
    if pos >= 0:
        candidate = finished_root / video.as_posix()[pos + len(marker) :]
        if candidate.is_file():
            return candidate
    return video


def video_from_local_stem(stem: str, finished_root: Path) -> Path | None:
    """Map local wav/srt stem back to mp4 under #finished."""
    candidate = finished_root / f"{stem.replace('__', '/')}.mp4"
    return candidate if candidate.is_file() else None


def finished_dir(*, jav_root: Path | None = None, mount: bool = False) -> Path:
    root = jav_root or resolve_jav_root(mount=mount)
    finished = root / FINISHED_SUBDIR
    if not finished.is_dir():
        raise FileNotFoundError(f"#finished not found: {finished}")
    return finished


def is_vr_mp4(path: Path) -> bool:
    if path.suffix.lower() != ".mp4":
        return False
    name = path.name
    if any(marker in name for marker in NON_VR_MARKERS):
        return False
    upper = name.upper()
    if any(marker in upper for marker in VR_STUDIO_MARKERS):
        return True
    if any(marker in name for marker in VR_TECH_MARKERS):
        return True
    # e.g. KAVR-500 PART 8K with 180 in filename
    if "8K" in upper and "180" in upper:
        return True
    return False


def sanitize_stem(text: str) -> str:
    text = text.replace("/", "__").replace("\\", "__")
    text = re.sub(r"\s+", "_", text.strip())
    return re.sub(r"[^\w.\-+#@\[\]()]+", "_", text)


def local_wav_path(
    video: Path,
    finished_root: Path,
    output_dir: Path,
) -> Path:
    rel = video.relative_to(finished_root)
    stem = sanitize_stem(str(rel.with_suffix("")))
    return output_dir / f"{stem}.wav"


def iter_finished_mp4s(
    finished_root: Path,
    *,
    vr_only: bool = True,
    name_filter: str | None = None,
    sort_by: str = "path",
) -> list[Path]:
    files = sorted(p for p in finished_root.rglob("*.mp4") if p.is_file())
    if vr_only:
        files = [p for p in files if is_vr_mp4(p)]
    if name_filter:
        needle = name_filter.lower()
        files = [p for p in files if needle in p.as_posix().lower()]
    files.sort(key=lambda path: path.as_posix().casefold() if sort_by == "path" else path.stat().st_size)
    return files
