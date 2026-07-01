#!/usr/bin/env python3
"""Small stdlib web app for selecting VR files and watching subtitle jobs."""

from __future__ import annotations

import html
import json
import os
import queue
import subprocess
import sys
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "python"))

from sense_voice.vr_sources import is_vr_mp4, local_wav_path  # noqa: E402

HOST = os.environ.get("VR_SUBTITLE_HOST", "127.0.0.1")
PORT = int(os.environ.get("VR_SUBTITLE_PORT", "8765"))
JOBS: dict[str, dict[str, object]] = {}
JOBS_LOCK = threading.Lock()
ACTIVE_JOB_ID: str | None = None


DEFAULT_SCAN_FOLDER = Path(os.environ.get("VR_SUBTITLE_SCAN_FOLDER", "/mnt/fnos/jav/#finished"))


def resolve_scan_folder(folder: str | None = None) -> Path:
    raw = (folder or "").strip()
    scan_folder = Path(raw).expanduser() if raw else DEFAULT_SCAN_FOLDER
    if not scan_folder.is_dir():
        raise FileNotFoundError(f"folder not found: {scan_folder}")
    return scan_folder.resolve()


def iter_web_mp4s(
    scan_folder: Path,
    *,
    vr_only: bool = True,
    name_filter: str | None = None,
) -> list[Path]:
    """Return only ./filename.mp4 and ./folder/filename.mp4 under scan_folder."""
    files = [p for p in scan_folder.glob("*.mp4") if p.is_file()]
    files.extend(p for p in scan_folder.glob("*/*.mp4") if p.is_file())
    if vr_only:
        files = [p for p in files if is_vr_mp4(p)]
    if name_filter:
        needle = name_filter.lower()
        files = [p for p in files if needle in p.as_posix().lower()]
    return sorted(files, key=lambda path: path.as_posix().casefold())


def scan_videos(
    name_filter: str | None = None,
    all_mp4: bool = False,
    folder: str | None = None,
) -> list[dict[str, object]]:
    finished = resolve_scan_folder(folder)
    videos = iter_web_mp4s(finished, vr_only=not all_mp4, name_filter=name_filter)
    items: list[dict[str, object]] = []
    for video in videos:
        rel = video.relative_to(finished).as_posix()
        stem = local_wav_path(video, finished, ROOT / "data" / "vr").stem
        items.append(
            {
                "path": str(video),
                "label": rel,
                "size_gb": round(video.stat().st_size / (1024**3), 2),
                "has_asr": (ROOT / "results" / "srt" / f"{stem}.asr.srt").is_file(),
                "has_zh": (ROOT / "results" / "srt" / f"{stem}.zh.srt").is_file(),
            }
        )
    return items


def start_job(
    videos: list[str],
    *,
    folder: str | None,
    skip_existing: bool,
    skip_polish: bool,
    dry_run: bool,
    force: bool,
) -> str:
    global ACTIVE_JOB_ID
    job_id = uuid.uuid4().hex[:10]
    cmd = [sys.executable, str(ROOT / "scripts" / "add_subtitle.py")]
    finished_root = resolve_scan_folder(folder)
    cmd.extend(["--finished-root", str(finished_root)])
    for video in videos:
        cmd.extend(["--video", video])
    if skip_existing:
        cmd.append("--skip-existing")
    if skip_polish:
        cmd.append("--skip-polish")
    if dry_run:
        cmd.append("--dry-run")
    if force:
        cmd.append("--force")
    log_q: queue.Queue[str] = queue.Queue()
    with JOBS_LOCK:
        if ACTIVE_JOB_ID is not None:
            active = JOBS.get(ACTIVE_JOB_ID)
            if active and active.get("status") == "running":
                raise RuntimeError(f"job {ACTIVE_JOB_ID} is already running")
        ACTIVE_JOB_ID = job_id
        JOBS[job_id] = {
            "id": job_id,
            "videos": videos,
            "folder": str(finished_root),
            "cmd": cmd,
            "status": "running",
            "started": time.time(),
            "returncode": None,
            "lines": [
                f"job {job_id} started",
                f"videos: {len(videos)}",
                "status: running",
            ],
        }

    def run() -> None:
        global ACTIVE_JOB_ID
        proc = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            log_q.put(line.rstrip())
        returncode = proc.wait()
        log_q.put(f"[exit {returncode}]")
        with JOBS_LOCK:
            job = JOBS[job_id]
            job["status"] = "done" if returncode == 0 else "failed"
            job["returncode"] = returncode
            if ACTIVE_JOB_ID == job_id:
                ACTIVE_JOB_ID = None

    def collect() -> None:
        while True:
            line = log_q.get()
            with JOBS_LOCK:
                lines = JOBS[job_id]["lines"]
                assert isinstance(lines, list)
                lines.append(line)
            if line.startswith("[exit "):
                return

    threading.Thread(target=run, daemon=True).start()
    threading.Thread(target=collect, daemon=True).start()
    return job_id


def current_status() -> dict[str, object]:
    with JOBS_LOCK:
        active = dict(JOBS[ACTIVE_JOB_ID]) if ACTIVE_JOB_ID and ACTIVE_JOB_ID in JOBS else None
        latest = None
        if JOBS:
            latest_key = max(JOBS, key=lambda item: float(JOBS[item].get("started", 0)))
            latest = dict(JOBS[latest_key])
        return {
            "active_job_id": ACTIVE_JOB_ID,
            "active": active,
            "latest": latest,
            "busy": bool(active and active.get("status") == "running"),
        }


INDEX = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VR Subtitle</title>
<style>
:root { color-scheme: light dark; --line: #8a8a8a55; --accent: #0f766e; }
body { margin: 0; font: 14px/1.45 system-ui, -apple-system, Segoe UI, sans-serif; background: Canvas; color: CanvasText; }
header { display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid var(--line); }
main { display: grid; grid-template-columns: minmax(340px, 42%) 1fr; min-height: calc(100vh - 58px); }
section { padding: 14px; min-width: 0; }
.left { border-right: 1px solid var(--line); }
.bar { display: flex; gap: 8px; align-items: center; margin-bottom: 10px; flex-wrap: wrap; }
input[type="search"] { flex: 1; min-width: 160px; padding: 8px 10px; border: 1px solid var(--line); border-radius: 6px; background: Canvas; color: CanvasText; }
input[type="text"] { flex: 1 1 300px; min-width: 220px; padding: 8px 10px; border: 1px solid var(--line); border-radius: 6px; background: Canvas; color: CanvasText; }
button { padding: 8px 10px; border: 1px solid var(--line); border-radius: 6px; background: ButtonFace; color: ButtonText; cursor: pointer; }
button:disabled { cursor: not-allowed; opacity: .55; }
button.primary { background: var(--accent); color: white; border-color: var(--accent); }
label { display: inline-flex; gap: 6px; align-items: center; }
.list { display: grid; gap: 6px; max-height: calc(100vh - 166px); overflow: auto; }
.item { display: grid; grid-template-columns: 22px 1fr; gap: 8px; align-items: start; border: 1px solid var(--line); border-radius: 8px; padding: 9px; background: Canvas; }
.item.done { opacity: .62; }
.name { font-weight: 650; overflow-wrap: anywhere; }
.meta { opacity: .72; font-size: 12px; margin-top: 4px; }
pre { margin: 0; padding: 12px; min-height: 56vh; max-height: calc(100vh - 190px); overflow: auto; border: 1px solid var(--line); border-radius: 8px; white-space: pre-wrap; background: #111; color: #eee; }
.jobs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.job { border: 1px solid var(--line); border-radius: 999px; padding: 5px 9px; }
@media (max-width: 780px) { main { grid-template-columns: 1fr; } .left { border-right: 0; border-bottom: 1px solid var(--line); } }
</style>
</head>
<body>
<header><strong>VR Subtitle</strong><span id="status">idle</span></header>
<main>
<section class="left">
  <div class="bar">
    <input id="folder" type="text" value="__DEFAULT_SCAN_FOLDER__" aria-label="folder path">
  </div>
  <div class="bar">
    <input id="filter" type="search" placeholder="name filter">
    <button id="scan">Scan</button>
  </div>
  <div class="bar">
    <button id="selectTodo">Select Todo</button>
    <button id="selectAll">Select All</button>
    <button id="selectNone">Select None</button>
    <span id="selectedCount">0 selected</span>
  </div>
  <div class="bar">
    <label><input id="skipExisting" type="checkbox" checked> cache first</label>
    <label><input id="skipPolish" type="checkbox"> skip polish</label>
    <label><input id="dryRun" type="checkbox"> dry run</label>
    <label><input id="force" type="checkbox"> force</label>
    <button id="run" class="primary">Run Selected</button>
  </div>
  <div id="videos" class="list"></div>
</section>
<section>
  <div id="jobs" class="jobs"></div>
  <pre id="log">Untranslated videos are selected automatically after scan.</pre>
</section>
</main>
<script>
let activeJob = null, poll = null;
const $ = (id) => document.getElementById(id);
function selectedVideos() {
  return Array.from(document.querySelectorAll('.video-check:checked')).map(x => x.value);
}
function updateSelectedCount() {
  const count = selectedVideos().length;
  $('selectedCount').textContent = `${count} selected`;
  $('run').textContent = `Run Selected (${count})`;
  $('run').disabled = count === 0;
}
async function scan() {
  $('status').textContent = 'scanning';
  const qs = new URLSearchParams({folder: $('folder').value, name_filter: $('filter').value});
  const res = await fetch('/api/videos?' + qs);
  const items = await res.json();
  if (!res.ok) {
    $('status').textContent = items.error || 'scan failed';
    $('log').textContent = items.error || 'scan failed';
    return;
  }
  $('videos').innerHTML = '';
  for (const item of items) {
    const row = document.createElement('label');
    row.className = item.has_zh ? 'item done' : 'item';
    const checked = item.has_zh ? '' : 'checked';
    row.innerHTML = `<input class="video-check" type="checkbox" value="${escapeAttr(item.path)}" data-done="${item.has_zh ? '1' : '0'}" ${checked}><div><div class="name">${escapeHtml(item.label)}</div><div class="meta">${item.size_gb} GB · ASR ${item.has_asr ? 'yes' : 'no'} · ZH ${item.has_zh ? 'yes' : 'no'}</div></div>`;
    row.querySelector('input').onchange = updateSelectedCount;
    $('videos').appendChild(row);
  }
  updateSelectedCount();
  $('status').textContent = `${items.length} video(s), ${selectedVideos().length} selected`;
}
async function run() {
  const videos = selectedVideos();
  if (!videos.length) return;
  const res = await fetch('/api/jobs', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({
    videos: videos, folder: $('folder').value, skip_existing: $('skipExisting').checked, skip_polish: $('skipPolish').checked, dry_run: $('dryRun').checked, force: $('force').checked
  })});
  const data = await res.json();
  if (!res.ok) {
    $('status').textContent = data.error || 'job rejected';
    $('log').textContent = data.error || 'job rejected';
    refreshStatus();
    return;
  }
  activeJob = data.id;
  watch();
}
async function watch() {
  if (!activeJob) return;
  clearTimeout(poll);
  const res = await fetch('/api/jobs/' + activeJob);
  const job = await res.json();
  $('status').textContent = job.status;
  const header = [`job: ${job.id}`, `status: ${job.status}`, `videos: ${(job.videos || []).length}`, `return: ${job.returncode ?? ''}`, ''].join('\\n');
  $('log').textContent = header + job.lines.join('\\n');
  $('log').scrollTop = $('log').scrollHeight;
  $('jobs').innerHTML = `<span class="job">${job.id} · ${job.status}</span>`;
  const running = job.status === 'running';
  $('run').disabled = running || selectedVideos().length === 0;
  if (running) poll = setTimeout(watch, 1200);
}
async function refreshStatus() {
  const res = await fetch('/api/status');
  const data = await res.json();
  const job = data.active || data.latest;
  $('run').disabled = data.busy || selectedVideos().length === 0;
  if (job) {
    activeJob = job.id;
    $('status').textContent = data.busy ? `running ${job.id}` : `${job.status} ${job.id}`;
    $('jobs').innerHTML = `<span class="job">${job.id} · ${job.status}</span>`;
    const header = [`job: ${job.id}`, `status: ${job.status}`, `videos: ${(job.videos || []).length}`, `return: ${job.returncode ?? ''}`, ''].join('\\n');
    $('log').textContent = header + (job.lines || []).join('\\n');
    if (data.busy) {
      clearTimeout(poll);
      poll = setTimeout(watch, 1200);
    }
  }
}
function escapeHtml(s) { return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c])); }
function escapeAttr(s) { return escapeHtml(s).replace(/`/g, '&#096;'); }
function setChecks(mode) {
  document.querySelectorAll('.video-check').forEach(check => {
    check.checked = mode === 'all' || (mode === 'todo' && check.dataset.done !== '1');
  });
  updateSelectedCount();
}
$('scan').onclick = scan;
$('run').onclick = run;
$('selectTodo').onclick = () => setChecks('todo');
$('selectAll').onclick = () => setChecks('all');
$('selectNone').onclick = () => setChecks('none');
scan().catch(err => $('status').textContent = err);
refreshStatus().catch(() => {});
</script>
</body>
</html>
"""


def index_html() -> str:
    return INDEX.replace("__DEFAULT_SCAN_FOLDER__", html.escape(str(DEFAULT_SCAN_FOLDER), quote=True))


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_text(index_html(), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/videos":
            params = parse_qs(parsed.query)
            folder = (params.get("folder") or [""])[0].strip() or None
            name_filter = (params.get("name_filter") or [""])[0].strip() or None
            try:
                self.send_json(scan_videos(name_filter=name_filter, folder=folder))
            except Exception as exc:
                self.send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        if parsed.path == "/api/status":
            self.send_json(current_status())
            return
        if parsed.path.startswith("/api/jobs/"):
            job_id = parsed.path.rsplit("/", 1)[-1]
            with JOBS_LOCK:
                job = JOBS.get(job_id)
                data = dict(job) if job else None
            if data is None:
                self.send_json({"error": "job not found"}, HTTPStatus.NOT_FOUND)
            else:
                self.send_json(data)
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/api/jobs":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        length = int(self.headers.get("content-length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        raw_videos = payload.get("videos")
        if isinstance(raw_videos, list):
            videos = [html.unescape(str(item).strip()) for item in raw_videos if str(item).strip()]
        else:
            video = str(payload.get("video") or "").strip()
            videos = [html.unescape(video)] if video else []
        if not videos:
            self.send_json({"error": "at least one video is required"}, HTTPStatus.BAD_REQUEST)
            return
        try:
            job_id = start_job(
                videos,
                folder=str(payload.get("folder") or "").strip() or None,
                skip_existing=bool(payload.get("skip_existing", True)),
                skip_polish=bool(payload.get("skip_polish", False)),
                dry_run=bool(payload.get("dry_run", False)),
                force=bool(payload.get("force", False)),
            )
        except RuntimeError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.CONFLICT)
            return
        self.send_json({"id": job_id})

    def send_json(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_text(self, text: str, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"VR subtitle web app: http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
