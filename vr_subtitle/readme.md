# VR Subtitle

Local VR subtitle app and CLI surface. It scans the NAS `jav/#finished` mount, extracts audio to `./data/vr`, writes SRT files to `./results/srt`, and copies `.zh.srt` back next to the source mp4.

ASR, audio extraction, LLM polish/translation, SRT writing, task TOML parsing, and NFS path helpers are reused from the main repo under `../python/sense_voice`.

Processing is cache-first by default:

- Existing `results/srt/<stem>.zh.srt` means the video is already translated and no work is done.
- Existing `results/srt/<stem>.asr.srt` means ASR/audio work is skipped and only translation is run.
- Existing `data/vr/<stem>.wav` means extraction is skipped.
- Pass `--force` to recompute instead of using cache.

## Commands

```bash
cd /home/rmqlife/work/voice_understanding/vr_subtitle

# Web app: enter a scan folder, unfinished videos are selected by default;
# one batch runs at a time
pixi run web

# Single video
pixi run add-subtitle -- \
  --video "/mnt/fnos/jav/#finished/SAVR-xxx/SAVR-xxx.mp4" \
  --language ja --profile vr

# Generate and run a batch task
pixi run gen-subtitle-task -- --folder "/mnt/fnos/jav/#finished" --name-filter vr -o tasks/vr_batch.toml
pixi run run-subtitle-task -- tasks/vr_batch.toml --continue-on-error

# Cron-friendly default batch for /mnt/fnos/jav/#finished
pixi run cron-subtitle-batch -- --continue-on-error

# Example crontab entry: every 6 hours
0 */6 * * * cd /home/rmqlife/work/voice_understanding/vr_subtitle && pixi run cron-subtitle-batch -- --continue-on-error >> results/cron-subtitle.log 2>&1

# No-GPU smoke check
pixi run test
```

Environment variables from the main repo still apply: `VR_JAV_ROOT`, `VR_NFS_HOST`, `VR_NFS_SERVER_NAME`, and `VR_NFS_SHARE`.

## Issue Notes

### Long subtitle durations after dropping filler

Symptom: some polished Chinese SRT entries lasted tens or hundreds of seconds after filler/nonsense lines were removed. One observed example was a short Chinese line inheriting a 181s source span.

Root cause:

- The SRT fragment merge step merged tiny tail fragments into the previous subtitle without checking the time gap.
- When a middle ASR/polish segment was cleaned to empty, the next tiny fragment could be merged across that missing interval.
- Polished subtitle display splitting had duration limits disabled, so a short surviving translation could keep a very long source segment time.

Fix:

- Added a temporal guard so fragment merges only happen for adjacent entries.
- Enabled an 8s max display duration for polished subtitles.
- Applied the duration cap after one-line entries, proportional splits, word-based splits, and final display-level merges.
- Added regression tests for dropped filler, short long-span lines, and long multi-chunk lines.

Follow-up performed:

- Rebuilt the generated task `.zh.srt` files with the fixed display post-processing.
- Published 23 corrected `.zh.srt` files back to `/mnt/fnos/jav/#finished`.
- Verified the task output had `0` entries over `8.01s`; max duration was `8.000s`.
- One task item was skipped because the source/local generated SRT was missing: `BadoinkVR_Suki_Sin_Slip_of_the_Tongue_8K_180_180x180_3dh`.

TODO list is in `./TODO.md`. Agent requirements are in `../.agent/`.
