# Digest — C26: Bbox AV1 plays at 720p30 and costs +1.5 W; 1080p30 still fails (2026-09-27)

Handoff `runs/handoff-2026-09-27b-two-hours.md` item 2. C25 F2 showed
the Bbox cannot play 1080p60 AV1 (~5 fps). This asks whether any lower
rung plays, and at what cost.
- **720p30 AV1 plays at full rate (29.6–30.3 fps presented) and costs
  +1.508 W over the Bbox's idle (n=3, sd 0.018).** This is the first
  real software-AV1 viewing cost on an operator box.
- **1080p30 AV1 still fails** (9–24 fps against 30).
- **Hardware H.264 at the same rungs costs nothing measurable**
  (−0.08 / +0.02 W), so at 720p30 AV1 costs about +1.6 W more than
  H.264 on this box.

## 1. Campaign metadata

- **Date:** 2026-09-27, 20:00–20:44 CEST; batch `20260927c26b`, 12 rows.
- **Device:** Bbox 4K (Arcadyan HMB9213NW, Marvell Berlin, no AV1 block),
  Ethernet, C2 **HDMI_2**, screen mode.
  - Sink `panel:HDMI_2`, panel lit on every row.
  - Output: compositor vsync 20 ms = 50 Hz (UI plane; link not
    verified, CR-084).
  - Player: Just Player; AV1 through its in-app software renderer (no
    video decoder allocated); H.264 on `OMX.Berlin.video_decoder.avc`.
- **Content:** Meridian (120 s ProRes 1080p59.94 master), encoded for
  this campaign at two rungs, each 120 s concatenated ×3 to 6 min.
  Bitrates and VMAF against the identically scaled and rate-reduced
  master (VMAF caveat in §4):

  | Rung | AV1 (SVT-AV1 p6 CRF 25) | H.264 (x264 slow CRF 18) |
  |---|---|---|
  | 720p30 | 0.48 Mb/s, VMAF 89.7 | 1.36 Mb/s, VMAF 90.2 |
  | 1080p30 | 0.84 Mb/s, VMAF 87.8 | 3.39 Mb/s, VMAF 88.6 |

  The encodes are fixtures, not results (#4941 boundary). Only decode
  is reported.
- **Capture:**
  - Rig protocol v3, upload template (150 s windows), 1 s P110,
    20-sample baseline with idle guard (settled in 3.2–3.3 s on every
    row).
  - Player verified PLAYING; n=3 per cell, cell order rotated per
    repetition.
- **Presented frame rate:** sampled every 20 s inside every task window
  (7 samples per row) from the player's SurfaceView timestamps
  (`dumpsys SurfaceFlinger --latency`), as in C25.

## 2. Scope statement

Device layer only: the Bbox's wall-plug draw above its own idle
(~5.9–6.0 W), panel excluded (metered as context), network excluded
(Ethernet; AV1 and H.264 streams differ in bitrate by 2.8–4×, a
delivery difference that is negligible on Ethernet at these rates, C18).
One content family, one box, two rungs, 30 fps only. Every cell's sink
is `panel:HDMI_2` (lit); output 50 Hz. Encode side out of scope.

## 3. Findings

### F1 — At 720p30 the Bbox plays AV1 in real time, and it costs +1.5 W

- **Claim:** Meridian AV1 720p30 reads **+1.508 W** (1.495 / 1.528 /
  1.501, sd 0.018). Presented frame rate is 29.6–30.3 fps in all 21
  in-window samples. Absolute playback draw is 7.45 W against a 5.95 W
  idle. No hardware decoder is allocated (software AV1).
- **Traffic Light:** 🟢 Repeatable (n=3, sd 0.018 W, all rows 🟢, full
  frame rate verified on every row).
- **Comparison, same box, same rung:** H.264 720p30 on the hardware
  decoder reads −0.078 W (F3). **AV1 costs +1.59 W more than H.264 to
  watch the same content at 720p30 on this box.** That is about 25 % of
  the box's own idle draw, and roughly 2.5–6× the marginal cost of
  hardware decode on any box measured tonight or in C25 (+0.25 to
  +0.61 W).
- **Confounds:**
  - One content family; 30 fps only.
  - AV1 and H.264 were matched on VMAF (within 0.5 points), not on
    bitrate.
  - 720p is the rung that plays, not a rung a service would necessarily
    deliver to a 4K CPE.
  - The software decoder's headroom at 720p30 is unknown: a
    higher-motion or higher-bitrate 720p stream could fall short.

### F2 — At 1080p30 the Bbox still cannot play AV1 in real time

- **Claim:** Meridian AV1 1080p30 reads +2.029 W (2.024 / 2.049 / 2.013,
  sd 0.018) while presenting **9.3–24.0 fps** (row means 14–17 fps)
  against 30.
  - Along with C25 F2 (1080p60, ~5 fps), this places the software
    decoder's real-time limit between 720p30 and 1080p30 on this
    content.
  - The +2.03 W is the power of a decoder running flat out and falling
    about 50 % short. It is not a viewing cost.
- **Traffic Light:** 🟢 Repeatable, for "1080p30 AV1 fails on this box"
  (n=3, 21 fps samples, none within 20 % of 30 fps).
- **Consequence:** the Bbox's AV1 story is now complete at n=3:
  - 1080p60 fails (5 fps);
  - 1080p30 fails (14–17 fps);
  - 720p30 plays (+1.5 W).

  "AV1 is unplayable on this box" is too strong. "AV1 plays on this box
  only at 720p30 or below, at +1.5 W" is supported.

### F3 — Hardware H.264 at 30 fps and 1.4–3.4 Mb/s costs nothing measurable on the Bbox

- **Claim:** H.264 on `OMX.Berlin.video_decoder.avc`, presenting 30.0 fps
  on every sample:
  - 720p30: **−0.078 W** (−0.086 / −0.071 / −0.078, sd 0.008);
  - 1080p30: **+0.022 W** (+0.055 / −0.015 / +0.027, sd 0.035).

  Both are within ±0.1 W of the home-screen idle. The 720p30 cell sits
  consistently **below** idle, with baselines settled and stable
  (baseline sd 0.13–0.15 W).
- **Traffic Light:** 🟢 Repeatable, as a null: n=3 per cell, sd ≤0.035 W,
  playback verified. The per-row confidence flags are 🔴 because the
  flag tests for a positive ΔW, which is absent.
- **Consequence:** this is a candidate explanation for **C17's
  unexplained Bbox negatives** (−0.03 to −0.40 W, mostly Kranjska,
  C25 §4). On this box, hardware playback of light content can draw
  less than the animated home screen used as the idle reference. So a
  small negative ΔW can be real rather than a playback failure. Against
  C25 F1 (H.264 1080p60 Meridian at 4.5 Mb/s = +0.33 W), the Bbox's
  hardware-decode cost scales with frame rate and/or bitrate.
- **Confounds:**
  - The idle reference is the Bbox home screen, whose own draw is part
    of the comparison.
  - 30 fps against C25's 60 fps, and different bitrates, so the scaling
    cause is not separated.

## 4. Anomalies and open questions

- **VMAF ceiling.** Halving CRF (1.6–2.2× the bitrate) moved VMAF by
  only 0.6–1.4 points (87–90 in both passes). That points to a
  measurement ceiling, likely a one-frame alignment offset from the
  59.94 → 29.97 decimation (the null muxer reported a duplicate DTS),
  not a quality ceiling. The codecs are matched to each other at each
  rung (≤0.8 VMAF apart); absolute VMAF should not be quoted. The first
  pass (CRF 32/22, 0.30/0.67 and 0.50/1.54 Mb/s) is logged in
  `encode_summary_try1_crf32_22.txt`.
- **Output 50 Hz against 29.97 fps content:** presentation is
  rate-converted (judder), as in C25.
- **Not tested:** 720p60 and 1080p24/25 (the rungs between), other
  content, bitrate sensitivity at 720p30.
- **The 720p30 H.264 cell sits below idle** (F3) with tight reps. The
  C17 Kranjska rows may be the same effect. A Kranjska screen-mode run
  with fps would confirm it (C25 §4).

## 5. Figure manifest

None generated.

## 6. Provenance

- **Raw (GoS1):**
  - `/srv/data/owl/results/decode/2026-09-27_{job}.json` (12 jobs, ids
    in the CSV);
  - `/srv/data/owl/campaign_2026-09-27_c26/{jobs,fps}.jsonl`, encode
    logs, `vmaf_*.json`, `encode_summary*.txt`.
- **Commands (this repo, on GoS1):**
  - encodes: `bash analysis/c26_encode_bbox_rungs.sh 25 18` (the first
    pass used the defaults 32 22);
  - rows: `python3 analysis/c26_bbox_rungs_feeder.py`;
  - summary: `python3 analysis/c26_summary.py --csv digests/2026-09-c26-bbox-av1-rungs.csv`.
- **Code:** wattlab `d242579` (harness protocol v3).
- **CSV:** `digests/2026-09-c26-bbox-av1-rungs.csv` (arm = rung).
- **Analysis date:** 2026-09-27.
