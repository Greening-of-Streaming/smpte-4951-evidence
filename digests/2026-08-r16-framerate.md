# Digest — R16: Frame rate (30 vs 60 fps) at the decoder (C16)

Fourth Tier-3 run (RUN_QUEUE R16, trimmed to one family + two codecs ⚙),
overnight 2026-08-09. **Frame rate is the one knob tonight that moves
EVERY silicon class: halving fps saves ~26–29% software decode power —
and, unlike the codec/entropy/effort knobs, the effect is visible even
on fixed-function hardware.**

## 1. Campaign metadata

- **Dates:** 2026-08-09 03:07–03:55 CEST.
- **Content:** BBB 1080p60 ProRes intermediate (shared with C14/C15);
  30 fps arm = `fps=30` decimation of the same source. ⚙ Spec trimmed:
  one family (BBB), two codecs (H.264 x264 crf21 · AV1 SVT preset 6
  crf35), no HEVC, no second family — controlled same-content pair per
  codec was the point.
- **Bitrates (same CRF, quality ≈ matched by construction):** h264
  4051→3312 kb/s (−18% at half the frames) · av1 2669→1725 kb/s
  (−35%). Note halving fps does NOT halve bits.
- **Capture:** decode rig protocol v3 headless realtime; Pi 5 n=3,
  GTV n=1 scoping ⚙; 105 s windows; no metered encode arm (decode-side
  question only).

## 2. Scope statement

Single content family; one sw decoder, one hw box; 1080p rung;
headless (no display — a real display at 60 vs 30 Hz adds its own
term, deliberately excluded). Same-CRF arms mean bitrate co-varies
with fps (stated above) — fps and bits jointly drop, which is exactly
the deployment trade being priced.

## 3. Findings

### F1 — Software decode: 60→30 fps saves 26–29%

- **Claim:** Pi 5 headless realtime (n=3): H.264 1.159 ± 0.092 →
  0.851 ± 0.052 W (−27%); AV1 1.369 ± 0.061 → 0.974 ± 0.052 W (−29%).
  Sub-linear in frames (2× frames ≠ 2× power — per-stream overheads and
  the memory system don't scale down), but the largest single decode
  lever measured tonight after codec choice itself.
- **Status:** 🟢 within panel. All 12 Pi rows green.

### F2 — Unlike every other knob tonight, hardware pays too

- **Claim:** GTV (n=1 per cell, scoping): H.264 +0.355 → +0.152 W;
  AV1 +0.318 → +0.178 W. The fps effect (~+0.2 W at 60) is visible on
  fixed-function silicon where codec (C11 F7), entropy coder (C14) and
  encoder effort (C15) all vanished — a hardware pipeline still
  processes twice the frames.
- **Status (original, superseded):** 🟡 (n=1 per cell; the deltas sit
  at ~the ±0.2 W noise floor individually but the direction is
  consistent across both codecs). n=3 repeat is a 25-minute follow-up.

**Amendment (2026-08-24 gap-fill, batch `16b026082401`): n=3 achieved
and the HEVC arm added — 🟡 → 🟢 within panel.** Same clips (reps 2–3
re-use the 08-09 encodes), same upload/headless protocol on the GTV;
HEVC arm encoded to the same recipe (x265 medium CRF 23, fps=30
decimation of the same intermediate; 2399→2056 kb/s, VMAF-NEG 91.55 /
93.49 — commands and scores in
`/srv/data/owl/campaign_2026-08-24_r16b/` on GoS1). All 14 new rows 🟢.

- GTV ΔW, 60 → 30 fps, mean ± sd of n=3:
  - H.264: +0.348 ± 0.015 → +0.211 ± 0.052 W (−39 %)
  - AV1: +0.294 ± 0.038 → +0.206 ± 0.025 W (−30 %)
  - HEVC (new): +0.356 ± 0.046 → +0.186 ± 0.039 W (−48 %)
- The fps effect on fixed-function silicon is now replicated at n=3
  in the same direction on THREE codecs — ~+0.09–0.17 W per codec for
  doubling the frames, where codec choice itself moves ≤0.08 W. The
  coverage-gated vs workload-gated taxonomy's hardware leg no longer
  rests on n=1.
- **Status:** 🟢 within panel (one box, one content family — the
  taxonomy's generality beyond this panel stays 🟡).

### F3 — Placement in the coupling set

Frame rate breaks the silicon-coverage pattern: C13/C14/C15 all found
costs that exist ONLY where the function is in software; fps is a
workload-size knob, not a function-coverage knob, so it scales power on
every class. For the paper's Section 5 taxonomy: encode-side flags
split into **coverage-gated** (codec, FGS, entropy, effort — cost lands
on the software tail) and **workload-gated** (fps, and presumably
resolution — cost lands everywhere, incl. the display). 
- **Status:** 🟡 (taxonomy claim; resolution half is R15, unmeasured
  tonight).

## 4. Anomalies and open questions

- ~~GTV cells need n=3 to move F2 to 🟢 (~25 min).~~ ✅ Done
  2026-08-24 (see F2 amendment; HEVC arm added at the same time).
- Display term excluded by design: a 60 Hz panel refresh vs 30 fps
  content interacts with motion interpolation on TVs — a screen-mode
  arm on the C2 would price it (ties to C11 F8/Q5).
- Kranjska (native 30) vs BBB (native 60) cross-family check — the
  duration study already hints software decode tracks fps across
  families; a controlled same-family pair at 1440×1080 would close it.

## 5. Figure manifest

None yet; F1/F2 fold naturally into the coupling-summary figure
(coverage-gated vs workload-gated knobs) when Section 5 drafts.

## 6. Provenance

- Raw store: `/srv/data/owl/campaign_2026-08-09_r16/` (`scores.tsv`
  clip table, `stage_c_results.jsonl` + job IDs, `r16_prep.sh`,
  `r16_stage_c.sh`).
- Decode envelopes: `results/decode/{date}_{job_id}.json`.
- Analysis date: 2026-08-09 (on the bench).
