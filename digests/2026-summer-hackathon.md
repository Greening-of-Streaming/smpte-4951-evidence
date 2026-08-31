# Digest — C4: Summer 2026 Hackathon REM dataset (codec at the TV wall socket)

Imported 2026-08-25 on GoS1 from the hackathon handoff Markdown
(`GoS_Summer26_Hackathon_REM_handoff.md`, prepared 2026-07-27 from the raw
CSV + the 102-min Fathom transcript) and the 27 July follow-up report
(`hackathon_summer26_followup.md`, which re-verified the handoff with
independent code). Reshaped to DIGEST_SPEC; **numbers are carried
unchanged** from those two documents, and every one below was re-run from
the raw CSV on 2026-08-25 (`verify_hackathon.py`). Where the two sources
differ (the correlation coefficient), both values are given and the
difference explained. **One capture, one content, five households: the
paper's REM-side evidence that codec and bitrate do not surface at the TV
wall socket.**

## 1. Campaign metadata

- **Date:** 2026-07-08, 14:10–15:32 UTC (REM experiment
  `suler-26-hackathon`, focus mode 14:11:57–15:31:57 UTC).
- **Participants / households (5):** Ben Schwarz (chair; France), Simon
  Jones (test design + stream hosting; UK), Tania Pouli (analysis
  methodology; France), Arian Koster (TNO, NL), Stan Moote (IABM). One
  further plug (`DR003-TV-65-LED-(Roku)`, Dom Robinson's group) was in
  the device group but read a constant 16 W.
- **Devices (10 plugs, REM group "Summer 26 Hackathon 080726"):**

  | Alias | Panel | Mean W (R2–R5) | White−black swing | Verdict |
  |---|---|---|---|---|
  | Tania LG OLED C5 | OLED | 48.2 | 81 W (3.3×) | valid |
  | Ben2-55-LG-OLED-C2 | OLED 55" (LG OLED55C2) | 44.8 | 62 W (2.7×) | valid |
  | STJ LG TV | LG TV (technology not logged) | 95.1 | 76 W (3.3×) | valid |
  | STJ Prototype 8K | 8K LCD prototype | 300.9 | 84 W (1.5×) | valid |
  | Stan-42" Plasma | plasma | 124.8 | 127 W (2.3×) | valid **R3–R5 only** |
  | Tania Philips LCD Ambilight | LCD, backlight pinned | 112.9 | 1 W | exclude (blind) |
  | Arian TV | — | 66.1 | 8 W | exclude (other content) |
  | Arian STB | set-top box | 2.0 | 0 W | exclude (below resolution) |
  | DR003-TV-65-LED (Roku) | LED | 16.0 | 0 W | exclude (dead channel) |
  | Lab-B | GoS1 rig plug, not a display | 9.6 | 0 W | not a display |

  Picture modes, HDR/SDR and firmware were not logged (handoff §9 #8 —
  freeze and record next time). Content was SDR 1080p.
- **Capture method:** TP-Link Tapo P110 per device, read by the REM
  collector through the **TP-Link cloud API** (not LAN), focus mode at a
  **10 s tick**; **integer-watt resolution** (all 4,811 samples are whole
  watts — verified). 481–482 samples per device; poll interval median
  10.0 s, p95 10.2 s, max 34.7 s (one gap). Devices poll independently:
  no shared sample index, per-device offsets within a 10-s slot up to ~2 s.
  Raw file: `power_readings.csv` (4,811 rows: timestamp UTC µs,
  device_alias, power_watts).
- **Content / codecs / bitrates:** one entertainment clip ("Entertainment"),
  ladder built by Simon with AVC as reference — AVC eq-MOS (reference),
  HEVC eq-MOS (VMAF ≈ 92), HEVC eq-bitrate-to-AVC, AV1 eq-MOS, AV1
  eq-bitrate. Delivered as HLS live loops (10-min cycle), local files as
  fallback. Bitrates were not recorded in the handoff. **AV1 never
  played** (HLS/DASH failed; local-file playback worked on a Samsung, not
  on LG); the R5 run is unlabelled and unusable.
- **Energy-signature sequence (the alignment reference):** each 10-min
  cycle, started on a 10-min wall-clock boundary:
  `black 30 s | white 30 s | black 30 s | content ~6.5 min | black 60 s`.
  The black/white/black head and the black tail are delimiters; analysis
  integrates the content window (390 s → 39 samples per device per run)
  to one energy figure per device per sequence. (This is the same
  structure OWL's `/prepare-rem` builds: timer + B/W/B markers + video +
  black tail ≈ 10 min.)
- **Run map** (transcript→UTC offset +13:45:10, calibrated on two black
  edges 10 min apart): R1 AVC eq-MOS 14:12:50–14:19:20 · R2 HEVC eq-MOS
  14:22:50–14:29:20 · R3 HEVC eq-bitrate 14:32:50–14:39:20 · R4 AVC
  eq-MOS repeat 14:42:50–14:49:20 · R5 unknown (AV1 attempt) — do not
  label. After 15:00:20: local-file playback, discard.
- **How samples were aligned across devices and runs:** the marker
  pattern is the only timing ground truth. For every cross-run
  comparison a lag search (±20 s, 10-s steps; the re-check used ±60 s)
  is run over the *widened* window that includes the markers, then the
  paired sample-wise delta is taken over the content window at the
  best-fit lag. Playback start drifted 10–50 s between runs (Ben's C2 R1
  +50 s; Tania C5 R2 +10 s; 8K R1/R3 −10…−20 s).

## 2. Scope statement

Whole-TV wall power (panel + decode + network + processing) of consumer
TVs in five homes, on one SDR entertainment clip, AVC vs HEVC at matched
quality and matched bitrate; a single 80-min capture. Not measured:
AV1 (failed), any STB decode delta (below the 1-W floor), HDR, 4K,
network or server side. Cloud-API capture at 10 s / 1 W: **the plugs
measure milliwatts at 1–2 s; the cloud path discards that** (the LEM LAN
path keeps it — see C8/R2). Precision of the run means is a property of
the protocol (39 samples of a fixed stimulus), not of the sensor.

## 3. Findings

### F1 — No measurable codec or bitrate effect at the TV wall socket

- **Claim:** paired sample-wise deltas over the content window, 95 % CI,
  after marker alignment — every interval spans zero on all four valid
  panels, and the codec delta is no larger than the AVC-vs-AVC replicate
  delta on the same hardware:

  | Device | HEVC − AVC (eq-MOS) | HEVC eq-MOS − eq-BR | AVC − AVC replicate |
  |---|---|---|---|
  | Ben2 OLED C2 | −0.03 W [−0.36, +0.31] | +0.21 W [−0.09, +0.50] | (R1 misaligned, see F3) |
  | Tania OLED C5 | +0.23 W [−1.40, +1.86] | +0.36 W [−1.27, +1.99] | +0.21 W [−1.44, +1.85] |
  | STJ LG TV | −0.77 W [−5.16, +3.62] | +0.10 W [−0.47, +0.67] | +1.36 W [−0.31, +3.02] |
  | STJ 8K | +1.33 W [−4.02, +6.68] | +6.10 W [−8.08, +20.28] | +0.10 W [−5.47, +5.67] |

  Independent re-check (2026-07-27 and again 2026-08-25): same
  conclusion, e.g. C2 HEVC−AVC −0.03 W [−0.34, +0.29]; all CIs span zero.
- **Status:** 🟢 Repeatable within this dataset — 4 panels of 3
  technologies, all CIs span zero, replicate ≥ codec delta, reproduced by
  two independent analyses. 🟡 beyond it: one clip, one capture, SDR
  1080p, bitrates unlogged.
- **Confounds:** picture settings changed mid-capture on one device
  (Philips 158→112 W at 14:13:50); plasma warm-up ramp in R2; 1-W
  quantisation means any sub-watt effect is invisible by construction
  (which is the point — see C6/C11 for the milliwatt answer).

### F2 — The wall-power trace is a luminance function; codec and bitrate leave it unchanged

- **Claim:** same content in different codecs/bitrates produces the same
  power curve on the same panel. Sample-aligned Pearson r between runs
  on the same device, ±20 s lag corrected, **markers included** (original
  analysis): Ben2 C2 **1.00** across R2/R3/R4/R5; Tania C5 0.99–1.00;
  STJ 8K 0.98–1.00; STJ LG TV 0.85–0.95. Independent re-check on the
  **content window only** (no marker edges to anchor the correlation):
  0.89–0.99 (0.99 on both OLEDs; 2026-08-25 run: C2 0.92, C5 0.89,
  8K 0.92–0.95, LG TV 0.99 for R2-vs-R3 but 0.22 for R2-vs-R4 — a
  single-run blip).
- **What "60–130 W" is:** the full-screen **white-minus-black marker
  swing** per valid panel (62 / 76 / 81 / 84 / 127 W; marker-window
  *means* +29 to +50 W). Under the entertainment content itself the
  within-run swing is far smaller: OLED C2 range 9–11 W (sd 2.3–2.6 W,
  CV 5–6 %), OLED C5 20–23 W (sd 4.5–4.8 W), STJ LG TV 31 W (R4),
  8K ~257 W (a mid-run dip to ~82 W — stream stall or panel blank, not
  content). So: *panel luminance moves a TV by tens of watts between
  black and white; content moves it by roughly 10–25 W on OLED; codec
  moves it by nothing measurable.*
- **Status:** 🟢 Repeatable within this dataset (4 panels; two analyses
  agree on the conclusion). The exact coefficient depends on whether
  marker edges are in the window — quote **r = 0.9–1.0**, or "r ≈ 1.00
  with markers included", not a bare "r ≈ 1.00".

### F3 — Misalignment manufactures phantom effects (methodology)

- **Claim:** uncorrected, Ben's C2 R1-vs-R4 (same codec) reads +6.46 W
  [+2.89, +10.03] — a 13 % "effect" from a 50-s playback offset alone
  (re-check: −6.15 W [−9.58, −2.72] with the opposite sign convention).
  Corrected, the pair collapses to the replicate delta. Tania C5's R2
  correlation rises 0.55 → 0.99 once a 10-s lag is applied.
- **Status:** 🟢 (reproduced twice; it is arithmetic on the same data).
  This is the reason the marker alignment is mandatory and is the
  method Section 3 should describe.

### F4 — Panel technology dominates absolute draw

- **Claim:** identical content: OLED 45–48 W, LG TV 95 W, plasma
  107–125 W, 8K LCD prototype 301 W.
- **Status:** 🟢 within this dataset (n=1 device per technology).

### F5 — STB decode delta is below the cloud path's floor (negative result that motivated OWL)

- **Claim:** the one STB (Arian's) read only the values 1, 2, 3 W
  (std 0.00 W in R2–R5); a "sub-1 W" HEVC-vs-AVC difference is
  consistent with the data but **not assertable** — 1 W is half the
  signal.
- **Status:** 🔴 Need More Data here → answered on the OWL bench (C6:
  ≤ 0.08 W; C11 F7; C17).

### F6 — Run-to-run repeatability of the protocol

- **Claim:** over R2–R5 (same content, different encodes) run means
  repeat to CV 0.25 % (C2), 0.46 % (LG TV), 0.92 % (C5), 1.03 % (8K),
  1.9 % (plasma R3–R5); minimum detectable two-run effect ≈ 0.7–5.5 %.
  Better than 1-W plugs suggest because 39 samples of a fixed stimulus
  average the quantisation out.
- **Status:** 🟢 within this dataset.

## 4. Anomalies and open questions

- **Prose check against Section 5.2 (as of 2026-08-25):** (a) "cross-codec
  Pearson r ≈ 1.00" — supported only with markers in the window; say
  r = 0.9–1.0 or qualify. (b) "panel luminance moved consumption by
  60–130 W **under normal content**" — not supported: 60–130 W is the
  black↔white marker swing; under content the swing is ~10–25 W on the
  OLEDs (F2). (c) "Early Insight overall … correlation a candidate for
  Repeatable" — the source rates F1/F2/F4 Repeatable *within the
  dataset*; Early Insight is right for generality (one clip, one
  capture). (d) "codec and bitrate invisible" — supported (F1).
- Blind-but-precise devices (Philips Ambilight CV 0.08 %, Roku constant
  16 W) — the white−black validity screen (< 5 % of mean → reject)
  should be an automatic REM pre-flight.
- R5's codec was never logged; AV1 has no field data. Log the stream URL
  per run; pre-verify AV1 per device.
- 10-s poll vs 30-s markers = 3 samples per marker edge; markers ≥ 6×
  the poll interval (60 s) or a faster path (LEM) next time.
- Plasma "draws less on dark content" (ads observation on the call) —
  🔴 contaminated by warm-up/desync.

## 5. Figure manifest

None in this repo. The follow-up's interactive charts live in
`hackathon_summer26_followup.html` (GoS1). A marker-alignment figure
(power trace of one panel across R2/R3/R4 with the B/W/B edges) would
serve Section 3; generate from `power_readings.csv` if wanted.

## 6. Provenance

- Raw: `/home/gos/wattlab/tmp/power_readings.csv` (4,811 rows) and the
  REM production DB (`gos_rem`, 2026-07-08 14:11–15:32 UTC, group
  "Summer 26 Hackathon 080726"); transcript
  `Summer_Hackathom_Transcript.rtf` (Fathom, 102 min; with Ben).
- Handoff: `/home/gos/wattlab/tmp/GoS_Summer26_Hackathon_REM_handoff.md`
  (2026-07-27); follow-up report + re-check code:
  `/srv/data/owl/hackathon-2026-summer/{hackathon_summer26_followup.md,
  verify_hackathon.py}`.
- Analysis dates: 2026-07-27 (handoff + re-check), 2026-08-25 (re-run of
  the re-check and the content-window swing numbers for this digest).
