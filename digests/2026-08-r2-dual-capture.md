# Digest — R2 / C8: LAN-versus-controlled dual capture (one playback, two readers per plug)

Run 2026-08-25 09:10–11:10 UTC on the GoS1 decode rig, per
`runs/handoff-2026-08-25-rem-digests-r2.md` Task 5. **Question:** what
does REM's field capture see of a playback that OWL's 1 s / mW bench
capture sees fully, and how are the two aligned? **Answer in one line:**
on the LAN path (LEM → REM field API) the field reader *is* the bench
reader — same plug, same instantaneous value, offset 0–1 s, energy within
1–3 % at 10 s and 0.2 % at 1 s — and what it loses is only what a 10-s
cadence cannot resolve; on the TP-Link **cloud** path the field reader is
a different instrument: integer watts that behave like a *floor*, a
2–5 s smear, +1–2 s offset, and an energy total 9–11 % low on a 4-W
device. The capture-alignment method (§3 F1) is written to be lifted
into Section 3.

## 1. Campaign metadata

- **Date:** 2026-08-25, 09:10–11:10 UTC. Batch `0825d0a1c0` (OWL
  `/decode/batch/0825d0a1c0`), 9 jobs run, 2 failed (§4).
- **Devices / arms:**
  - (a) **Google TV Streamer** (MediaTek, hardware H.264) on **Ethernet**,
    headless, plug **Lab-D** (P110 192.168.1.36). Decode-only signal
    (ΔW ≈ +0.3 W signature, +0.6 W BBB).
  - (a′) **Raspberry Pi 400**, software decode (ffmpeg over ssh, paced
    1×), headless, plug **Lab-B** (P110 .31). Added because Lab-B is the
    one rig plug the REM *cloud* collector polls (it is on the fleet
    TP-Link account since 2026-07-08 — see §4). ΔW ≈ +1.1–1.4 W.
  - (b) **LG OLED55C2** native playback (webOS browser, its own SoC
    decodes and displays), **panel metered** on plug **Lab-E** (P110 .71) —
    the REM field case; all-in figure, tens of watts of luminance signal.
- **Readers on each plug, simultaneously:**
  - *Bench:* decode-bench protocol v3, Tapo local (KLAP) at **1 s,
    milliwatt** (`raw_task_t/w` per run), per-run 20-sample idle
    baseline, stable-idle guard, keep_awake pinned (GTV
    `secure.sleep_timeout=-1`, `screen_off_timeout=2147460000`; the C2 via
    the harness claim) — disclosed: a bench configuration, not living-room
    behaviour.
  - *REM LAN path:* **LEM** (LAN-reader, `~/dev/LAN-reader` on GoS1,
    f69903f 2026-07-29) reading Lab-D and Lab-E over the LAN at **10 s**,
    milliwatt (3-decimal W), streaming into the production REM
    (`rem.greeningofstreaming.org`) experiment `r2-dual-capture-2026-08-25`
    through the field API (`POST /api/field/batch`, join code issued by
    the admin API). **The production ingestion path was used**; the rows
    were then read back from `gos_rem` for the comparison. One extra run
    with LEM at **1 s** (LEM `--interval 1`; REM's experiment cadence
    hint bottoms out at 5 s, but LEM's local interval and the field API
    both accept 1-s rows).
  - *REM cloud path:* the production collector polling Lab-B through the
    TP-Link cloud under **Strong focus** (system `focus_level=2`,
    experiment cadence 10 s — the configuration every 2026 field session
    used; annotation "Focus Mode started — polling 3 device(s) at 10s
    tick" 09:14:33 UTC). Before focus the same plug arrived every ~21 s
    (fleet round time). **Integer watts.**
- **Content:** the fielded July-2026 REM energy-signature file
  (`/prepare-rem` output `rem_0bf36c5d_h264_1080p.mp4`, Meridian source,
  H.264 1080p60 2.33 Mb/s, 600 s): **timer/black 0–90 s · white 90–120 ·
  black 120–151 · Meridian 151–540 · black tail 540–599** (luma-probed
  per second, `sig_yavg_0bf36c5d.txt`). Window 585 s from +8 s after
  launch (+5 s on the C2). Control: BBB H.264 iso-bitrate 20-min file
  (`bbbiso_h264_20min.mp4`, C17 family), 1080-s window. n=3 signature
  per arm (C2: n=2, §4), n=1 control per arm, n=1 GTV signature with LEM
  at 1 s.
- **Signature (per the handoff's "real 8-minute sequence"):** no
  8-minute / twenty-sub-sequence file exists on GoS1 (C2 digest §4); the
  10-min July sequence with its three 30-s marker segments is what was
  fielded, so it is what was run.

## 2. Scope statement

One rig, one plug model (Tapo P110, fw as installed), one LAN. The LAN
path is LEM on GoS1 (a server, wired), not a volunteer's laptop on
Wi-Fi — upload reliability under field conditions is not tested here.
The cloud path is measured on one plug during Strong focus (3 devices);
fleet-scale behaviour (34 devices, back-off) is REM's own
`POLLING_FINAL_RESULTS.md`. Panel arm is all-in (panel + decode); the
GTV arm is decode-only (headless). Two local KLAP readers shared each
plug (bench 1 s + LEM 10 s / 1 s) without a single dropped sample
(586/586 and 1080/1080 on every row) — one plug *can* serve two readers.

## 3. Findings

### F1 — Capture-alignment method (for Section 3)

- **Clock.** Every reader stamps its own wall-clock time (bench: epoch
  per sample; LEM: UTC ISO-8601 per tick, identical timestamp for all
  plugs in a tick; REM cloud: server receipt time). Alignment is
  therefore *time-to-time*, not sample-index-to-sample-index — REM's
  July analyses had to align by content markers because the cloud path
  gave no usable timing; with LEM the timestamp is the alignment.
- **Reader offset.** For each REM-path sample at time *t*, compare with
  the bench's 1-s trace averaged over a trailing box of width *b* ending
  at *t + δ*; scan *b* ∈ {1, 2, 5, 10} s and δ ∈ [−15, +15] s; take the
  (b, δ) minimising RMSE. Result — **LAN path: b = 1–2 s, δ = 0 to +1 s,
  RMSE 0.00–0.03 W (GTV) / 0.21–0.23 W (C2, on a 37–154 W trace),
  r = 0.96–1.000** on every run: the P110 reports an instantaneous value
  and LEM stamps it within a second of the bench. **Cloud path: b = 2–5 s,
  δ = +1 to +2 s, RMSE 0.37–0.52 W, r = 0.48–0.81**: the cloud value is a
  short-window figure a second or two old, then truncated (F3).
- **Content clock.** Playback start is *not* the launch command: the
  bench's 1-s trace locates the signature's edges itself — Pi 400
  content-start step at 151–156 s (clip 151 s), C2 white edges at 91 and
  121 s (clip 90/120), GTV first visible step at 164–172 s, i.e. the app
  needs ~14 s to start playing. Rule: derive clip time from the trace's
  own edges (or from the marker pattern on the 10-s path), never from
  the command timestamp.
- **Transition identifiability at 10 s.** A step between two 10-s
  samples is located to ±5 s (the mid-point); a 30-s marker segment
  yields 3 samples (observed: white 3, black 3–4) — enough to *detect*
  the edge on the panel arm (white 153.5 W vs black 36.9 W, sd within
  the segment 2.8 W at 10 s vs 29 W at 1 s because the 1-s bins straddle
  the edge), not enough to time it better than ±5 s. On the decode-only
  arm the markers are **not** identifiable at either cadence: the GTV's
  decode power does not respond to luminance (segment means
  1.66–1.75 W, differences < 0.1 W, inside run-to-run noise); the only
  usable edge is content start (a complexity step, ~+0.5 W on the Pi,
  < 0.1 W on the GTV).
- **Status:** 🟢 (method; reproduced on 9 runs across three plugs).

### F2 — LAN path (LEM → REM) is lossless to the bench within cadence

- **Claim:** the rows REM ingested via the field API are identical to
  LEM's local CSV (every fit identical), and to the bench's 1-s reading
  at the same instant (F1). Energy over the window, LEM/REM vs bench:
  GTV signature −0.4 / −0.8 / −1.6 %, GTV BBB −1.1 %, C2 signature
  −0.6 / −0.8 %, C2 BBB −2.7 %; **at 1 s: −0.2 %** (GTV, 0.2755 vs
  0.2760 Wh). The 10-s deficit is the sampling of an instantaneous value
  on content whose power moves within 10 s (largest on bright dynamic
  BBB on the panel); it is a cadence effect, not a resolution effect.
- **What survives at 10 s / mW:** on the panel arm, everything the 1-s
  trace shows above ~10-s timescale — the marker steps, the content
  segment's mean and its slow structure (content 48.5 vs 48.6 W; sd 4.03
  vs 4.13 W); on the decode arm the run mean and the idle-to-play step
  (1.7 vs 1.35 W) but not sub-10-s events (the GTV's 2.0-W spike at
  ~430 s is one sample or none).
- **What survives at 1 s / mW via LEM:** everything (r = 0.94 with the
  bench's own 1-s trace on a 0.02-W-RMSE signal; the residual is the two
  readers' 1-s phase).
- **Status:** 🟢 within panel (3 plugs, 9 runs, two devices classes).

### F3 — Cloud path: integer watts that floor, a 2–5 s smear, and −9…−11 % energy

- **Claim (Pi 400, Lab-B, n=4 runs incl. control):** the cloud value
  reads **below** the bench in every segment of every run — content
  segment 3.95–3.97 W vs 4.27–4.37 W (−0.30 to −0.40 W); black/timer
  3.33 vs 3.78; tail 3.60 vs 3.89 — the pattern of a truncation (floor)
  of a value whose fractional part was mostly > 0.5, not of rounding.
  The figure shows it directly: bench at 4.2–4.5 W → cloud "4"; bench at
  3.6–3.9 W → cloud "3". Energy over the window: **−11.4, −11.4, −11.1 %
  (signature) and −9.1 % (BBB 20-min)** — 0.592/0.604/0.600 vs
  0.668/0.682/0.675 Wh; 1.188 vs 1.306 Wh.
- **Cadence:** 10.0–10.1 s under Strong focus (46–58 samples per
  585-s window — the first run started before focus was on and got 46);
  ~21 s without focus (fleet round time, 34 devices / 8 workers).
- **Implication for the July field numbers (C3, C4):** every 2026 field
  session ran on this path. Means over hundreds of samples are fine
  (C4's 0.25 % run-to-run CV), but *absolute* cloud-path watts on a
  device carry a systematic ≈ −0.5 W (mean floor bias) and per-device
  energy totals are low by that amount × time; on a 2–4 W STB that is
  10–25 %, on a 150-W TV 0.3 %. The C4 handoff's STB reading
  "1–3 W" is consistent with a 1.5–3.9 W device.
- **Status:** 🟢 within panel for the direction and size on this plug
  (4 runs, same sign every segment); 🟡 that the mechanism is a floor in
  the TP-Link cloud value (inferred from the bias pattern; the plug's
  own local value is not floored — F2). Confirm on a second plug/firmware
  before calling it a property of the path rather than of this plug.

### F4 — Sample-count arithmetic per segment (ties to the 8-minute design)

- Observed, 10-s LAN/cloud paths: 30-s marker → **3** samples (white:
  3, 3, 3; black: 3–4); 389-s content → 38–39; 585-s window → 59 (LAN)
  / 46–58 (cloud, focus). At 1 s: 30 and 387–389.
- For the abstract's 8-minute / 20-sub-sequence design (24 s per
  sub-sequence): **2–3 samples at 10 s, 24 at 1 s, ~1 at the 21-s
  unfocused fleet cadence** — the design is only countable on the LAN
  path at ≤ 5 s (LEM), consistent with C2 digest §4. On the cloud path
  the same 8 minutes supports ~8 sub-sequences of 60 s (6 samples each,
  edge ±5 s).
- **Status:** 🟢 (arithmetic on observed counts).

### F5 — Same energy from both readers (agreement statement)

| Arm | Run | Bench 1 s (Wh) | LAN 10 s (Wh) | Cloud 10 s (Wh) | LAN − bench | Cloud − bench |
|---|---|---|---|---|---|---|
| GTV sig rep 1–3 | 99fc/7d82/2462 | 0.278 / 0.273 / 0.274 | 0.277 / 0.271 / 0.270 | — | −0.4 / −0.8 / −1.6 % | — |
| GTV BBB 20 min | cca6 | 0.579 | 0.573 | — | −1.1 % | — |
| GTV sig, LEM 1 s | a327 | 0.276 | 0.2755 (1 s) | — | −0.2 % | — |
| Pi 400 sig rep 1–3 | 99fc/7d82/2462 | 0.668 / 0.682 / 0.675 | — | 0.592 / 0.604 / 0.600 | — | −11.4 / −11.4 / −11.1 % |
| Pi 400 BBB 20 min | cca6 | 1.306 | — | 1.188 | — | −9.1 % |
| C2 sig rep 1–2 | 75d7/6107 | 8.273 / 7.742 | 8.226 / 7.682 | — | −0.6 / −0.8 % | — |
| C2 BBB 20 min | f6f9 | 22.48 | 21.88 | — | −2.7 % | — |

- **Status:** 🟢 within panel.

### F6 — Bench ΔW for the record (decode signal sizes)

GTV signature +0.32 / +0.27 / +0.30 W (rep 1 baseline hot at 1.92 W
post-boot → −0.22 W, excluded from ΔW, trace used), GTV BBB +0.60 W;
Pi 400 sw +1.28 / +1.14 / +1.29 W, BBB +1.43 W; C2 all-in 50.8 / 47.3 W
mean on the signature vs 65.1 / 57.8 W home-screen baseline (negative
ΔW = the known panel-arm artefact, C11 F8), BBB 74.9 W (+19 W). All
rows 586/586 or 1080/1080 samples, liveness gate passed.
🟢 per run; not the point of this digest.

## 4. Anomalies and open questions

- **C2 arm at n=2 and no 1-s C2 run.** Two of four C2 jobs failed with
  "panel did not return after cycle": the harness mains-cycles the
  panel (Lab-E) before a C2 job and the C2 came back with the screen on
  (44 W) but **off the network** (no ping, SSAP ports closed) — still so
  at close-out 11:20 UTC. Needs on-site attention (network reconnect /
  remote). Harness item: don't mains-cycle the C2 between consecutive
  C2 jobs; wake over SSAP instead.
- **Pi 400 decoded in software** (the upload template has no decoder
  knob); the spec's hardware-decode arm is the GTV. The cloud-path
  finding does not depend on which decoder ran.
- **Lab-B is on the fleet TP-Link account** (cloud rows since
  2026-07-08, registry `source: api`). If unintended, unshare it; it
  was the only way to put the cloud path on the rig without an on-site
  change. Lab-D / Lab-E reach REM only through LEM.
- **REM experiment cadence floor is 5 s** (`target_cadence_s` 5–300);
  LEM's `--interval` overrides locally and the field API accepts 1-s
  rows, so 1-s field capture works today but the experiment cannot
  *ask* for it. Small REM change if 1 s is to be a first-class field
  cadence.
- **Strong focus is fleet-wide:** while on, the other ~30 fleet devices
  were not polled (09:14–11:20 UTC). Turned off at close-out.
- Floor vs round on the cloud path (F3) — confirm on a second plug and
  firmware; the REM audit's "1 W class resolution" understates it if
  it is a floor.
- The 10-s LAN energy deficit grows with content dynamics (−0.4 % dark
  signature → −2.7 % bright BBB on the panel): quote LAN-path energy
  at 10 s as "within ~3 %", or run 1–2 s where energy totals matter.

## 5. Figure manifest

- `figures/fig_c8_dual_capture.png` — the signature seen by the bench
  (1 s) and by REM's path on the same plug, three arms (GTV/LAN,
  Pi 400/cloud, C2/LAN), with the 1-W floor of the LAN trace overlaid on
  the GTV and C2 panels. Command (GoS1):
  `/srv/data/owl/figures-venv/bin/python figures/make_c8_dual_capture_figure.py 75d7e183`
  (script in `figures/`; reads the raw store below).

## 6. Provenance

- Raw (GoS1): bench per-run JSONs
  `/srv/data/owl/decode-bench/results/ui-{upload,loop_bbbiso_h264}-{99fcb000,7d82cb7d,24622933,cca63c8b,75d7e183,61079862,f6f99174,a32764ff}-{gtv,pi400,c2}.json`
  (raw_task_t/w at 1 s); OWL envelopes `results/decode/2026-08-25_<job>.json`,
  batch `0825d0a1c0`; LEM CSVs
  `/srv/data/owl/r2-dual-capture/lem/r2_2026-08-25_*.csv` (10 s) and
  `r2_1s_2026-08-25_*.csv` (1 s); REM rows exported from `gos_rem`
  (`rem_rows.csv`, Lab-B/D/E, 09:00→11:15 UTC); REM admin state
  (experiment `r2-dual-capture-2026-08-25`, group `R2-cloud-LabB`, focus
  annotations).
- Analysis: `/srv/data/owl/r2-dual-capture/r2_analysis.py` → 
  `r2_analysis_output.txt`, `r2_summary.csv`; signature luma probe
  `sig_yavg_0bf36c5d.txt`. Failed jobs: `ba159d99`, `6d51920f`.
- Analysis date: 2026-08-25.
