# Digest — R12: H.264 entropy coding (CABAC vs CAVLC), the reverse trade (C14)

Second Tier-3 coupling run (RUN_QUEUE R12), overnight 2026-08-09.
**The reverse of R11 confirmed: paying ~11% more bits (CAVLC) buys a
46% software-decode power saving — and on hardware the entropy coder is
energy-invisible. One x264 flag prices the whole trade.**

## 1. Campaign metadata

- **Dates:** 2026-08-09 01:22–02:10 CEST.
- **Content:** Big Buck Bunny 4K60 master → 120 s 1080p60 ProRes HQ
  intermediate (t=120–240; encode source + scoring reference), raw
  store `/srv/data/owl/campaign_2026-08-09_r12/`.
- **Encoder:** x264 (ffmpeg-master N-124403), preset medium, high
  profile, GOP 120, yuv420p, 1080p60; ONLY `-coder` varies.
  - Matched-bitrate pair (the decode experiment): 2-pass ABR 8000k —
    achieved 8120 (CAVLC) vs 8114 kb/s (CABAC), byte-matched by design.
  - Matched-quality reading (from the CRF sweep): CABAC carries ~11–12%
    fewer bits at equal CRF with slightly higher VMAF-NEG at every rung
    (e.g. CRF 21: 3809 vs 4330 kb/s, 92.84 vs 92.41 NEG).
- **Capture:** encode = GoS1 parity-row mechanics (each measured encode
  = the full 2-pass pipeline, both passes inside the window; queue
  paused, lock held, focus mode). Decode = rig protocol v3 headless
  realtime, 105 s windows, HTTP delivery; Pi 5 (sw) + Google TV (hw),
  n=3 per cell, interleaved. Quality scores: VMAF-NEG
  (`model=version=vmaf_v0.6.1neg`), `sweep/scores.tsv`.

## 2. Scope statement

Single content family (BBB, animation — low-complexity end; a
high-SI/TI source would likely widen every delta), one software decoder
(ffmpeg/x264's decode path on BCM2712), one hardware box. Headless
realtime decode; no display/player stack. Delivery Wh/GB for the bit
delta not measured (origin counters available; open item with R11's).
Encode Wh borders #4941 — coordinate cite-vs-report before prose.

## 3. Findings

### F1 — At identical bitrate, CABAC costs +46% software decode power

- **Claim:** byte-matched 8 Mb/s files differing only in entropy coder,
  Pi 5 headless realtime: CABAC +1.394 ± 0.029 W vs CAVLC
  +0.953 ± 0.021 W — **+0.44 W, +46%, n=3 each, all 🟢**. On the GTV
  (fixed-function decode) the same pair reads +0.377 ± 0.034 vs
  +0.362 ± 0.007 W — **Δ within noise**.
- **Status:** 🟢 within this panel. The entropy-decode share of
  software H.264 decode is ~a third of the total at this rung — far
  larger than the "CABAC is a bit slower" folklore number.

### F2 — The trade CABAC buys with that power: ~11–12% bits at equal quality

- **Claim:** CRF sweep 18–27: CABAC −11–12% bitrate at every rung with
  slightly HIGHER NEG (+0.2–1.1); at matched bitrate CABAC is +0.43 NEG.
  Encode energy is a wash (2-pass pipeline: CAVLC 0.477 vs CABAC
  0.481 Wh/min, inside rep noise).
- **Status:** 🟢 for the sweep direction (single content); encode-wash
  🟢 n=3.

### F3 — The reverse-coupling ledger (pairs with R11's F4)

Per minute of content at ~8 Mb/s 1080p60:

| side | CABAC (default) | CAVLC | delta |
|---|---|---|---|
| encode (once/title) | 0.481 Wh | 0.477 Wh | ≈ 0 |
| delivery (per view) | baseline | +11–12% bits | CAVLC pays |
| decode, sw client (per view) | 1.394 W | 0.953 W | **CAVLC saves 0.44 W (−32%)** |
| decode, hw client (per view) | 0.377 W | 0.362 W | ≈ 0 |

R11 and R12 together give the framework's Tier-3 result as a pair of
mirror images: **an encode-side flag can move energy between the
datacentre, the network, and the viewer's device — and the viewer-side
term exists only where the function is not in silicon.** For a
software-decode audience (browsers without hw paths, SBCs, old
devices), a CAVLC rung is a defensible energy-accessibility variant;
for a hardware fleet it is pure bitrate waste.
- **Status:** 🟡 (ledger arithmetic; delivery Wh/GB term open, single
  content family).

## 4. Anomalies and open questions

- **Kranjska repeat RUN same night (04:10–04:30) — prediction
  falsified ⚙:** byte-matched 8 Mb/s pair on the hard family
  (1440×1080p30, SI 101), Pi 5 n=3: CABAC +0.894 ± 0.082 vs CAVLC
  +0.731 ± 0.018 W = **+0.16 W (+22%)** — direction holds, but the
  premium is SMALLER than BBB's +46%, not wider. The naive
  "more residual → bigger entropy share" model fails; plausible
  culprits: 30 vs 60 fps (half the per-second frame overhead) and x264
  spending Kranjska's bits differently (more transform coefficients per
  frame but fewer frames). Family comparison, not single-variable —
  cite the range **+22–46% by content/fps**, not one number. Raw:
  `/srv/data/owl/campaign_2026-08-09_r12k/`.
- The GTV CABAC r1 rep (+0.416) was the widest hw reading; still inside
  the noise band, n=3 mean settles at +0.377. No re-run needed.
- Delivery Wh/GB via CR-072 origin counters — shared open item with
  R11 F4; would complete both ledgers with one measurement session.

## 5. Figure manifest

- `figures/fig_coupling_ledgers.{svg,png}` — shared mirrored-ledger
  figure with C13. Command: `/srv/data/owl/figenv/bin/python figures/make_coupling_figures.py`.

## 6. Provenance

- Raw store: `/srv/data/owl/campaign_2026-08-09_r12/`
  (`sweep/scores.tsv`, `stage_b_results.jsonl`,
  `stage_c_results.jsonl` + job IDs, scripts, logs).
- Decode envelopes: `results/decode/{date}_{job_id}.json`.
- Analysis date: 2026-08-09 (on the bench).
