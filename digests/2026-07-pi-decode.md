# Digest — Pi Decode Bench (client decode energy, July 2026)

Campaign C5. Derived from the GoS1 draft report
`~/wattlab/docs/pi_decode_energy_2026-07.md` (analysis 2026-07-29, lab
review pending). This digest restructures that report to DIGEST_SPEC and
adds no numbers of its own. All statuses are proposed pending lab review.

## 1. Campaign metadata

- **Dates:** overnight bench run 2026-07-28/29. Google TV rows are
  context from the July STB round (see C6 digest).
- **Devices:**
  - Raspberry Pi 5 (16 GB, Raspberry Pi OS Bookworm), 4× Cortex-A76 @
    2.4 GHz. Software decode only: no H.264 or AV1 hardware; HEVC block
    present but unreachable from stock userspace (finding F4).
  - Raspberry Pi 400 (4 GB, Bookworm), 4× Cortex-A72 @ 1.8 GHz.
    Software decode plus hardware H.264 (`bcm2835-codec`, stateful
    v4l2m2m).
  - Google TV Streamer (MediaTek fixed-function decoders) — context
    rows only; full playback, not headless (see scope).
- **Capture:** Tapo P110 smart plugs, local mW API at 1–2 s cadence
  (LEM principle). Lab-A `.146` (Pi 5) and Lab-B `.31` (Pi 400), both
  fw 1.3.1; `.94` fw 1.4.6 (Google TV). Firmware cadence on the Lab
  plugs assumed, not probed (open question Q6).
- **Protocol per cell:** settle → per-run idle baseline → start → skip
  → sampled window → OWL `confidence.py`. Metric is marginal power ΔW
  over the per-run idle baseline.
- **Regimes:** realtime (`-re`, paced 1×, 150 s window — what a player
  pays while playing) and full-speed (`-stream_loop -1`, saturated,
  120 s — race-to-idle power).
- **Content:** Big Buck Bunny 1080p60 for all panels; Meridian and
  Kranjska MTB added on the Pi 5 full-speed panel only. Matched-VMAF
  (~92–93) 1080p NVENC encodes, one ladder rung, so bitrate co-varies
  with codec.
- **Codecs:** H.264, HEVC, AV1.
- **Idle baselines:** Pi 5 ~3.4 W, Pi 400 ~3.0 W, Google TV ~1.0 W.

## 2. Scope statement

Device layer only: marginal decode power on the named boards, measured
headless as pure decode (`ffmpeg … -an -f null -`) — video only, no
audio, no display path, clips staged in `/dev/shm` so no network or
storage I/O inside the measurement window. Both Pi desktops held at
1920×1080@60 scanout throughout. One resolution rung (1080p); no 4K, no
HDR. Google TV rows are full playback (display output plus audio) from
a separate round and are indicative context, not like-for-like against
the headless Pi rows. Network, CDN, datacentre and production
boundaries excluded. No amortised training cost included; encode-side
energy is not measured here (see C6 and the #4941 boundary).

## 3. Findings

Per-run confidence: all 21 rows green on OWL's confidence model; key
Pi 5 realtime cells n=2–3, all other cells n=1. Campaign-level Traffic
Light per finding below.

### F1 — A hardware decoder is worth 3.6× while playing, 4.1× saturated

- **Claim:** on the Pi 400, same board and same file, hardware H.264
  decode costs +0.35 W realtime vs +1.25 W software (3.6×); +0.64 W vs
  +2.62 W full-speed (4.1×). Direct single-variable measurement of what
  dedicated silicon buys.
- **Status:** 🟡 Early Insight — large effect and single-variable
  design, but n=1 per Pi 400 cell; per-run confidence green.
- **Key stats:** ΔW as above; BBB 1080p60 only.
- **Confounds:** single chipset, single content, one rung. Repeats
  queued (open question Q4).

### F2 — The Pi 5 pays for its dropped H.264 block

- **Claim:** the Pi 5 software-decodes H.264 at +1.57 W where the
  Pi 400's hardware does the same job for +0.35 W — newer device, older
  codec, ~4.5× the energy.
- **Status:** 🟡 Early Insight — cross-board comparison; boards differ
  in DRAM, clocks and process, and the Pi 400 cell is n=1.
- **Key stats:** Pi 5 realtime H.264 +1.57/+1.60 W (n=2, task power
  agreeing across a third anomalous-baseline run, see §4); Pi 400 hw
  +0.35 W (n=1).
- **Confounds:** board-generation differences; client-side mirror of
  OWL's `input-master-sensitivity` finding, cited as interpretation.

### F3 — In software, HEVC is the dearest codec at 1× on both boards

- **Claim:** realtime software decode orders h264 < av1 < hevc on both
  boards (Pi 5: +1.57/+1.81/+2.56 W; Pi 400: +1.25/+1.75/+2.54 W). On
  software-decoding clients codec choice moves decode power by up to
  ~60%, where fixed-function boxes show ≤0.08 W (C6).
- **Status:** 🟢 Repeatable for the Pi 5 realtime ordering (HEVC n=3 at
  +2.56/+2.57/+2.63 W; H.264 n=2 at +1.57/+1.60 W; AV1 n=2 at
  +1.81/+1.85 W; spreads ≤0.07 W). 🟡 Early Insight for the two-board
  generalisation (Pi 400 cells n=1).
- **Confounds:** matched-VMAF rung means bitrate co-varies with codec;
  BBB only in realtime panels.

### F4 — Usable hardware decode is stranded by packaging on stock OS

- **Claim:** both Pis' HEVC hardware exists but is unreachable from
  stock Bookworm userspace (stateless V4L2 blocks; ffmpeg 5.1/mpv have
  no V4L2-request path; VLC 3.0.23 built `--disable-mmal
  --disable-libva`; GStreamer 1.22 lacks `v4l2slh265dec`, which lands
  in 1.24). The Pi 5 has no AV1 or H.264 hardware at all; the Pi 400's
  usable hardware is H.264 only. Stock-OS users software-decode
  everything, at the energy prices measured above.
- **Status:** 🟢 Repeatable — capability audit, not a power
  measurement; each blocked path was attempted directly and the failure
  documented.
- **Confounds:** distribution-specific (Bookworm stock packages);
  GStreamer 1.24 expected to change this (open question Q5).

### F5 — Measurement regime changes the codec ranking

- **Claim:** saturated, AV1 draws the least power of the three on the
  Pi 5 (+4.15 W vs H.264 +5.13 W) despite using the most CPU time;
  paced at 1×, H.264 is cheapest. A codec energy claim without its
  regime (and buffering model) stated is not interpretable.
- **Status:** 🟡 Early Insight — full-speed cells n=1; the rank
  inversion is large but unreplicated. The methodological implication
  stands on the measured inversion itself.
- **Key stats:** race-to-idle vs sustained energy per video-minute,
  Pi 5 H.264 0.022 Wh/video-min vs AV1 0.041 (regime-dependent).
- **Confounds:** no real player's buffering characterised yet (Q2).

### F6 — Content moves software decode cost far less than codec does

- **Claim:** on the Pi 5 full-speed panel across three contents (BBB,
  Meridian, Kranjska), content choice moves each codec ≤0.11 W; the
  decoder, not the content, drives cost.
- **Status:** 🟡 Early Insight — one board, one regime, n=1 per cell.

## 4. Anomalies and open questions

- **Q1 — Hot-baseline undercount.** A third Pi 5 realtime H.264 run
  measured ΔW +0.97 W with task power identical to its siblings (5.09
  vs 4.94/4.96 W) against an elevated idle baseline (4.12 vs ~3.4 W).
  Same failure mode OWL closed on the server bench with CR-070's
  pre-job idle guard; `bench.py` has no baseline-floor guard yet.
  Until it does, cross-check `w_task` when a ΔW looks anomalous.
  Resolving run: add baseline-floor guard to `bench.py`, re-run cell.
- **Q2 — Which regime real players occupy.** Race-to-idle favours
  H.264; sustained favours AV1. Needs the player-with-display arm
  (mpv/KMS) on both Pis before any "codec X is cheapest for playback"
  claim on these boards.
- **Q3 — Why AV1 draws less than its CPU share suggests.**
  Instruction-mix / power-density hypothesis (NEON-dense H.264 kernels
  vs dav1d's mix). Interpretation, not a result; needs perf/PMU
  counters or per-rail measurement.
- **Q4 — Pi 400 software decode measured cheaper than Pi 5's** (+1.25
  vs +1.57 W realtime H.264), n=1 per board. Do not read as "older is
  more efficient" without repeats and a clocks-matched control.
- **Q5 — GStreamer 1.24 expected to unstrand the HEVC blocks.**
  Untested. F1's hw-vs-sw gap predicts roughly a 2 W saving per stream
  on these boards if it works.
- **Q6 — Plug firmware hygiene.** Lab-A/B plugs assumed ≥1 Hz-class
  cadence from fw 1.3.1 (S47); `bin/probe-p110-fw` has not been run on
  them. Ten-minute item that would firm every row's effective sample
  count.

## 5. Figure manifest

No figures exported to `figures/` with this digest. Raw per-row JSON
(1.5 s samples) permits regeneration of any panel; candidate figures
(ΔW bar chart per cell; regime-inversion plot for F5) should be
produced on GoS1 with commands recorded here when Section 5 drafting
needs them.

## 6. Provenance

- Raw data: GoS1 `/srv/data/owl/decode-bench/results/` (per-row JSON
  with 1.5 s samples; harness `bench.py` alongside).
- Source report: GoS1 `~/wattlab/docs/pi_decode_energy_2026-07.md`,
  draft of 2026-07-29, lab review pending.
- Analysis date: 2026-07-28/29. Digest prepared 2026-08-08 on the
  writing desk from the report text only (no raw-data access).
- Data discipline: two early rows discarded as contaminated (a
  concurrent full-speed job overlapped the first realtime H.264/HEVC
  windows); discarded values retained in the raw logs, marked, and
  excluded here. The stray-process risk is closed with codec-targeted
  stop commands. The Range-request defect in the ad-hoc `:8123` file
  server (200/full-body to ranged GETs) breaks ffmpeg-over-HTTP and is
  the prime suspect for July's media3 2.1× over-fetch (C6, Q1 there);
  clips were therefore staged locally for every Pi row.
