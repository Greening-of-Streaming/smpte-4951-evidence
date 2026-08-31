# Digest — R15 Leg A: device-side upscale is not free on software silicon (C22)

RUN_QUEUE R15, Leg A only (Pi 5 software upscale), same night as the
R13/R14 write-up, 2026-08-30. **Upscaling 1080p to 4K on-device costs
the Pi 5 roughly 2.5× its native-1080p decode power — a real,
measurable tax, not the free lunch the "ship 1080p, let the device
upscale" assumption implies. It is cheaper than shipping true native
4K (−22%), but it is not free.**

## 1. Campaign metadata

- **Date:** 2026-08-30, ~04:15–04:30 CEST (three ~2.5 min decode jobs).
- **Content:** BBB, same source family as C11/C15/C21 — 1080p60 H.264
  (`bbb_h264_6min.mp4`, the existing 1080p decode-bench reference) vs
  the existing separately-encoded native-4K file
  (`bbb_h264_4k_2min.mp4`, 3840×2160@60, NVENC ~20 Mbps — the same file
  C11 F3/F4 already measured).
- **New capability:** `output_scale` template field, added to
  `wattlab_service/decode_run.py` this session (commit `ab44d58`) —
  threads an ffmpeg `-vf scale=W:H` filter onto the existing headless
  decode-only path (`_row_for`'s ssh/non-screen branch), mirroring the
  existing `decoder`/`decoder_by_device` precedent. New template
  `bbb_h264_1080_upscale4k` (Pi 5 only — no HDMI attached, headless by
  design, matching how C11's own native-4K row was scoped).
- **Capture:** rig protocol v3, headless decode-only (ffmpeg to null),
  Pi 5, n=3, 90 s window (matching `bbb_h264_4k`'s bench settings
  exactly for a clean three-way comparison). Native-1080p and
  native-4K comparators are historical rows (same template family,
  same protocol, `results/decode/2026-07-29…2026-07-31`), not re-run
  tonight — pulled directly from stored result JSON, not re-typed from
  memory.

## 2. Scope statement

One device (Pi 5, software decode only — no fixed-function silicon
tested this leg, that's Leg B, not attempted), one content family
(BBB), one codec (H.264), headless decode-only (no present/display
stage — matches C11 F3's own scoping, which found the *present* path
breaks at native 4K on this board regardless of decode). This is a
decode-energy comparison, not a decode-capability or visual-quality
one; no VMAF is computed on the upscaled output.

## 3. Findings

### F1 — Device-side upscale has a real, non-trivial energy cost

- **Claim:** Pi 5 headless decode-only ΔW, n=3 each: native 1080p
  1.421 W (CV 4.4%, historical) · **1080p decoded + upscaled to 4K
  3.563 W (CV 14.3%, tonight)** · native 4K 4.546 W (CV 7.5%,
  historical). Upscaling costs **+150.7% (+2.14 W) over native 1080p**
  — more than double. It is **21.6% cheaper (−0.98 W) than decoding an
  actual native-4K bitstream**, so the ordering is 1080p < upscaled <
  native-4K, all three legs clearly separated.
- **Status:** 🟡 — n=3 with a real spread on the new leg (see anomaly
  note below); the two comparators are historical single-campaign
  rows, not run alongside tonight's in the same session, though same
  protocol/template/content. Direction (upscale costs meaningfully
  more than native-1080p, meaningfully less than native-4K) is clean;
  the exact +150.7%/−21.6% magnitudes would tighten with a same-night
  re-run of all three legs together.

### F2 — A second, unplanned finding: native-4K decode itself is far
from free on this board

- **Claim:** the historical comparator rows themselves show native 4K
  costs **+219.9% (+3.13 W) over native 1080p** on Pi 5 decode-only —
  a number C11 F3/F4 never actually stated (F3 reported *throughput*
  — 75 fps, 1.25× realtime — not power; F4's "shrugs off 4K" result is
  about the GTV, not the Pi 5). Pulling the raw stored rows for this
  digest is the first time this specific Pi-5-decode-only 4K energy
  delta has been written down as an energy number.
- **Status:** 🟢 (n=3, CV 7.5%, clean historical rows) for the
  existence and rough size of the effect; the number was not
  previously reported anywhere, so treat it as newly surfaced rather
  than independently re-confirmed tonight.

## 4. Anomalies and open questions

- **Rep 1 of the new leg (2.975 W) sits noticeably below reps 2–3
  (3.887, 3.826 W)** — the CV-14.3% spread is driven almost entirely by
  this one row; reps 2–3 agree to within 0.06 W. This is the same
  first-row-of-a-fresh-session shape flagged twice already tonight in
  the R13/R14 write-up (a baseline measured before the system fully
  settled from the preceding restart/idle transition undercounts ΔW)
  — rep 1 here followed a service restart + lab-session-on, the same
  kind of transition. Kept in the reported mean; excluding it would
  raise the upscale mean to ~3.86 W, which would *widen* the gap to
  native-1080p and *narrow* the gap to native-4K, not change the
  finding's direction.
- **Leg B (GTV hardware scaler) not attempted** — separate task, gated
  on an on-device probe of whether `adb shell wm size` (or another
  command) actually engages hardware scaling; see RUN_QUEUE R15.
- **The two comparator legs are historical, not same-session** — a
  same-night three-row-per-leg re-run (9 rows total, ~30 min) would
  remove the only real methodological gap in F1 and is cheap to do
  whenever this needs to move from 🟡 to 🟢.
- **Present-path cost is still unmeasured for the upscale leg** — this
  digest is decode-only, matching C11 F3's own scoping; if the paper
  wants a *playback* number (not just decode), that's a further leg,
  not covered here, and Pi 5 has no HDMI attached to measure it with
  regardless (would need re-cabling).

## 5. Figure manifest

- None generated. A natural addition to a resolution-cost figure: a
  simple three-bar chart (native 1080p / upscaled / native 4K) would
  make F1 legible at a glance; not built tonight.

## 6. Provenance

- New-leg raw results: `results/decode/{date}_{job_id}.json` on GoS1,
  job ids `9fd8841f`, `4369c829`, `226e574d` (template
  `bbb_h264_1080_upscale4k`, device `pi5`).
- Historical comparator rows: native 1080p —
  `results/decode/2026-07-31_8f045d5a.json`,
  `2026-07-31_5efee987.json`, `2026-07-29_94c0db74.json` (templates
  `bbb_h264_rt`/`bbb_h264_smoke`); native 4K —
  `results/decode/2026-07-31_de498468.json`,
  `2026-07-30_c7c18e8b.json`, `2026-07-31_4a57deb7.json` (template
  `bbb_h264_4k`). All pulled directly from stored JSON, not retyped.
- Code change: `wattlab_service/decode_run.py` commit `ab44d58` (not
  yet pushed to wattlab's remote — local commit only, per house
  practice of not pushing wattlab_service changes without being asked).
- Analysis date: 2026-08-30 (on the bench).
