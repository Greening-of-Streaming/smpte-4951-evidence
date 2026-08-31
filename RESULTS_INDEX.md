# Results Index

One entry per measurement campaign. This file is the evidentiary map of the
paper: Section 5's dual-track synthesis is assembled from these entries.

Status legend: 🟢 Repeatable · 🟡 Early Insight · 🔴 Need More Data

---

## C1 — November 2025 Cycle (Loop demonstration #1)

- **Track:** REM → OWL
- **Status:** 🟡 Early Insight (REM half: one testbed, one codec; every
  number reaches us only via reference [2] — the Nov-2025 raw data is not
  on GoS1 nor in the production REM DB. OWL half 🟢 within panel: S53
  encode-parity artifact, 138 rows all 🟢; #4941 boundary on the codec
  figures)
- **Headline:** REM found the variables — resolution ≈ 55 % of encoder
  power variance, bitrate a strong secondary (strongest at the packager),
  device-side bitrate/resolution effects 1–4 % and non-significant,
  luminance the strongest device-side correlate (r² ≈ 0.35–0.47). OWL
  priced them — NVENC 2.5–4.4× less Wh/min than CPU for the same codec,
  a gap as large as or larger than codec-vs-codec on one hardware path
  (cite [3] for the codec analysis). Nov-2025 capture: cloud path,
  10 s / 1 W, 150 samples per condition; server PDU at 4 s.
- **Digest:** `digests/2025-11-cycle.md` (2026-08-25)
- **Paper role:** First end-to-end demonstration of the measurement loop.

## C2 — July 2026 Cycle (Loop demonstration #2)

- **Track:** REM → OWL
- **Status:** umbrella — inherits C3/C4 (🟡/🟢 within dataset) and
  C5/C6/C11/C17/C18 (🟢 within panel)
- **Headline:** REM's null (codec/bitrate invisible at the socket,
  luminance dominant, with an 8K/HDR boundary case) explained and priced
  by OWL (≤ 0.08 W codec spread on fixed-function silicon; expensive
  exactly where silicon lacks the codec; connection method, not delivery
  pacing, is the device-side lever). Eight findings tabulated with
  found-by / explained-by. Capture facts: focus mode 10-s cloud tick
  (1 W) for every 2026 field session; LEM LAN path (10 s / **mW**, field
  API in REM v1.7.0, 2026-07-24) — the outline's "10 s / 1 W LAN" needs
  correcting. 8-minute / twenty-sub-sequence arithmetic: 24 s per
  sub-sequence = 2 samples at 10 s, 24 at 1 s — feasible only on the
  LAN path; no 8-min sequence file exists, fielded sequences were 6 min
  (Nov 2025) and 10 min (July 2026).
- **Digest:** `digests/2026-07-cycle.md` (2026-08-25)
- **Paper role:** Second demonstration; establishes the loop as repeatable
  method rather than one-off.

## C3 — World Cup TV Power Campaign (3 REM sessions, Jun–Jul 2026)

- **Track:** REM (field, cloud path 10 s / 1 W); Simon's ESP lux meter
  (final) is NOT in REM or on GoS1
- **Status:** 🟢 within this match for the ad-break finding on the
  logged (French) feed — F1 re-run 2026-08-25 against Ben's event log:
  W-per-step ×2.3 in the two in-play ad breaks, ×3.3 post-match, ×8.6 in
  the half-time ad block, mean −1.5 to −6 %; 🟡 across the UK/CA sets
  (half-time band only, feed lags unknown); 🔴 from GoS1's
  sources for the 99-s FR–UK latency and the 8K r ≈ 0.1 (need the lux
  trace + feed/household log — see digest §4); 🟡 for the 8K absolute
  step (+40 % vs SDR, no luminance tracking vs the co-located panel)
- **Headline:** In-play TV power is flat (block CV 1–2 %); half-time /
  pre-match raise variability ×3–5 (CV, W per step) while the mean moves
  < ±3 % with mixed sign. Cross-household traces align only after
  minute-scale lag searches; one 100 ± 10 s pair (r = 0.90) exists in the
  recorded-playback session, not on the final. 8K prototype: 423 W on
  the final vs 301 W SDR hackathon, r = 0.17 vs the co-located LG TV.
  Sessions: 06-26 live, 07-07 recorded playback, 07-19 final.
- **Digest:** `digests/2026-07-worldcup.md` (2026-08-25)
- **Paper role:** Field evidence for content-dependence of device power;
  the 8K case as the luminance rule's boundary (own finding, status
  honest). Section 5.2 wording changes listed in the digest §4.

## C4 — Summer Hackathon REM Dataset (2026-07-08)

- **Track:** REM (cloud path, 10-s focus tick, integer W; 10 plugs, 5
  households, 4 valid panels + plasma from R3)
- **Status:** 🟢 Repeatable within this dataset for the codec/bitrate null,
  the luminance-trace identity and panel-technology dominance (4 panels,
  all CIs span zero, replicate ≥ codec delta, two independent analyses);
  🟡 for generality (one clip, one capture, SDR 1080p, AV1 never played)
- **Headline:** Codec and bitrate invisible at the wall socket
  (HEVC−AVC −0.03 W [−0.36, +0.31] on the OLED C2; every CI spans zero).
  Same content across codecs gives the same power trace: r ≈ 1.00 with
  marker edges in the window, 0.89–0.99 on the content window alone —
  quote r = 0.9–1.0. Luminance swing black↔white 60–130 W per panel
  (marker-window means +29…+50 W); **under content** the swing is
  ~10–25 W on OLED — Section 5.2's "60–130 W under normal content" must
  change. Misalignment of 50 s fakes a +6 W (13 %) effect; STB decode
  below the 1-W floor (→ C6/C11).
- **Digest:** `digests/2026-summer-hackathon.md` (2026-08-25; imported
  from the 07-27 handoff + follow-up, numbers unchanged, re-run 08-25)
- **Paper role:** Core REM-side evidence that per-stream encode choices
  don't surface at CPE wall power; motivates OWL isolation work.

## C5 — Pi Decode Bench (July 2026)

- **Track:** OWL method applied to client devices (per-run idle
  baseline, ΔW, confidence model) at LEM plug resolution (1–2 s mW)
- **Status:** 🟡 Early Insight overall (per-run confidence 🟢 on all 21
  rows; Pi 5 realtime codec ordering 🟢 at n=2–3; most other cells n=1;
  lab review pending)
- **Headline:** A hardware decoder is worth 3.6× while playing, 4.1×
  saturated, on the same board and file. In software, HEVC is dearest
  at 1× on both boards (codec moves decode power up to ~60%).
  Measurement regime flips the codec ranking (saturated, AV1 cheapest).
  Stock-OS packaging strands usable hardware decode.
- **Digest:** `digests/2026-07-pi-decode.md`
- **Paper role:** Client-side "why" behind REM's wall-socket findings:
  decode cost is measurable at sub-watt resolution, and the framework's
  bench method transfers to consumer devices. Follow-up runs listed in
  the digest's §4 (repeats, player-with-display arm) are not yet in
  RUN_QUEUE.

## C6 — STB Decode Campaign (July 2026)

- **Track:** OWL-style instrumented playback on consumer STB
- **Status:** 🟡 Early Insight overall (all 24 runs 🟢 per-run;
  codec-flatness and delivery-mode findings proposed 🟢 within this
  panel — one box, one chipset; lab review pending)
- **Headline:** Decode nearly flat across codecs on fixed-function
  silicon (≤0.08 W, AV1 cheapest by a hair); bitrate barely registers;
  delivery mode outweighs codec by 5–14× (mean +0.42 W sustained vs
  burst), with network delivery alone +0.21 W.
- **Digest:** `digests/2026-07-stb-decode.md`
- **Paper role:** Bench-side quantification of C4's "codec and bitrate
  invisible at the wall socket". Encode:decode ratio context borders
  #4941 — confirm cite-vs-report before Section 5.
- **⚠ Reconciled 2026-08-24 (C18):** F3 "delivery mode outweighs codec
  5–14×" is RETIRED as stated (arms conflated Wi-Fi radio duty cycle
  with a since-fixed origin defect and an overlay); successor claim =
  connection method (Wi-Fi-active share) outweighs codec. F4's +0.21 W
  reproduced at n=3 but is a *Wi-Fi* share (Ethernet ≈ free). F1/F2/F5
  unaffected. See `digests/2026-08-netpath-c6-reconciliation.md`.

## C8 — R2 dual capture: LAN-versus-controlled (2026-08-25)

- **Track:** REM ↔ OWL method run — one playback, two readers per plug
  (bench 1 s/mW local; REM LAN path = LEM → field API at 10 s and 1 s;
  REM cloud path = TP-Link cloud under Strong focus, 10 s, integer W)
- **Status:** 🟢 within panel (3 plugs, 9 runs; GTV Ethernet decode arm
  n=3 + control + 1-s run; Pi 400 cloud arm n=3 + control; C2 panel arm
  n=2 + control — two C2 jobs lost to a harness mains-cycle that left the
  panel off the network); 🟡 that the cloud value is a *floor* (one plug)
- **Headline:** On the LAN path the field reader is the bench reader:
  offset 0–1 s, RMSE ≤ 0.03 W (GTV) / 0.2 W (C2 on 37–154 W), rows in REM
  identical to LEM's, energy within 0.4–2.7 % at 10 s and 0.2 % at 1 s;
  what 10 s loses is only sub-10-s structure (marker edges ±5 s, 3
  samples per 30-s segment). The cloud path is another instrument:
  integer watts that behave like a floor (−0.3…−0.4 W on a 4-W device,
  every segment, every run), a 2–5 s smear at +1–2 s, energy −9…−11 %;
  ~21 s cadence without focus. Capture-alignment method (time-to-time,
  trace-derived content clock, box/offset scan) written for Section 3.
  8-min/20-sub-sequence arithmetic: 2–3 samples per sub-sequence at
  10 s, 24 at 1 s — LAN-path-only design.
- **Digest:** `digests/2026-08-r2-dual-capture.md`; figure
  `figures/fig_c8_dual_capture.png`
- **Paper role:** Section 3's alignment method and the measured
  before/after of the polling constraint; grounds the C3/C4 field
  numbers' resolution caveat.

## C11 — Decode Rig Campaign (Jul 30–Aug 1 2026, five-device bench)

- **Track:** OWL client bench, protocol v3 (stable-idle guard, in-clip
  markers, five concurrently metered devices — parallel validated)
- **Status:** 🟢 lab-confirmed 2026-08-09 (66-cell campaign,
  run-ID-cited; findings docs de-DRAFTed); F5/F8 held at 🟡
- **Headline:** A streaming box plays 4–7× cheaper than a
  general-purpose board, display attached. Codec choice is nearly free
  where silicon covers it (fixed-function 4K ≈ 1080p; hw marginal below
  ±0.2 W noise at any run length) and expensive where it is not: HEVC
  ~1.9× H.264 in software (Pi 5), AV1 +1.4 W on an operator CPE with no
  AV1 block (Bbox Bouygtel4K — first operator CPE on an OWL bench).
  R6 reconciliation (2026-08-09): same-board hw-vs-sw H.264 =
  **3.7× realtime / 4.6× saturated** (n≥3 interleaved, protocol v3,
  all 🟢) — the earlier 3.6–7× spread was hw-arm run variability plus
  one baseline-suspect row, now a citable pair of numbers.
  Methodology: "can decode" ≠ "can play" (Pi 5 4K present-path break).
  **Silicon audited 2026-08-26 (R3a):** both streamers are one MediaTek
  part (MT8696) and the Bbox is **Marvell Berlin** (Arcadyan HMB9213NW)
  — the AV1-penalty half of the codec claim is Marvell, the flatness
  half remains MediaTek-only (Bbox H.264/HEVC inside its idle drift);
  cite the two halves separately (digest F11 silicon note, Q9).
  **F9 superseded 2026-08-24** (duration study re-run under keep_awake,
  n=2/duration + Pi 5 control): real signals green in seconds AND flat
  through 59 min — the ~1 h degradation leg and the "5–20 min window"
  guidance are retired (the old long-window STB rows were sleep-timer
  artefacts, job ids listed in the digest); a genuinely small margin
  flickers at every duration — repeats beat length. See the F9
  amendment in the digest.
- **Digest:** `digests/2026-08-decode-rig.md` (device list amended
  2026-08-26; Q9 — Bbox H.264/HEVC flatness — answered 2026-08-31:
  interleaved n=6 series confirms the "cannot be resolved on this box"
  outcome, both codecs near-zero with wide/inconsistent confidence,
  not a clean flat result but a legitimate one — see the digest's Q9
  entry)
- **Paper role:** Core evidence for the codec-assumption narrative
  (codec cost is a property of silicon coverage, not of the codec);
  extends C5/C6 and partially supersedes them where re-measured.

## C13 — R11: AV1 Film-Grain Synthesis coupling (2026-08-09)

- **Track:** OWL both sides of the wire — GoS1 encode energy (parity
  mechanics) + decode rig protocol v3 (Pi 5 sw / GTV hw), matched-NEG
  operating point (VMAF-NEG, method stated in digest).
- **Status:** 🟢 on the three measured panels (n=3, interleaved, all
  rows green); 🟡 on the combined ledger and the bitrate-saving
  generality (single content).
- **Headline:** The first confirmed encode↔decode coupling: FGS+denoise
  at matched quality saves 19% bits but costs 2.15× encode energy and
  +0.57 W (+26%) per software-decoding viewer — while hardware AV1
  synthesizes grain for free (Δ ≈ 0 on MediaTek). FGS is an energy win
  in proportion to fleet hardware-AV1 coverage. Bonus method finding:
  this SVT-AV1 build defaults film-grain-denoise to 0, where FGS makes
  files LARGER — the flag everyone quotes is half the mechanism.
- **Digest:** `digests/2026-08-r11-film-grain.md`
- **Paper role:** Section 5's Tier-3 exemplar — a datacentre choice that
  moves the fleet's per-viewer bill, sign depending on silicon coverage;
  the cleanest dual-track demonstration in hand.

## C14 — R12: CABAC vs CAVLC, the reverse trade (2026-08-09)

- **Track:** OWL both sides — GoS1 2-pass encode energy + decode rig
  protocol v3 (Pi 5 sw / GTV hw), byte-matched 8 Mb/s pair.
- **Status:** 🟢 on the measured panels (n=3, all rows green); 🟡 on
  the ledger (delivery term open; single content family, BBB = gentle).
- **Headline:** At identical bitrate, CABAC costs +22–46% software
  decode power by content/fps (+0.44 W on BBB 1080p60, +0.16 W on
  Kranjska 1080p30 — same-night hard-family check; the "widens on hard
  content" prediction was falsified) and ~0 on hardware; what it buys
  is ~11–12% bits at equal quality, with encode energy a wash. Mirror
  image of R11: a CAVLC rung is an energy-accessibility variant for
  software-decode audiences, pure bitrate waste for hardware fleets.
- **Digest:** `digests/2026-08-r12-cabac-cavlc.md`
- **Paper role:** Second Tier-3 exemplar; with C13 it makes the
  "encode flags move energy between boundaries, gated by silicon
  coverage" argument as a matched pair.

## C15 — R13: refs/B-frames corners (2026-08-09, amended 2026-08-30)

- **Track:** OWL both sides — GoS1 encode ladder + decode rig v3
  (Pi 5 n=3 / GTV scoping), x264 fixed-CRF corners (NEG-verified).
  2026-08-30: interior grid points + a bitrate-matched Kranjska repeat
  added (same n=3 rig protocol) — RUN_QUEUE R13 now fully closed.
- **Status:** 🟢 encode ladder + min<def decode edge + Kranjska
  direction; 🟡 def<max decode edge magnitude, interior-grid decode
  decomposition (F5), and Kranjska magnitude vs BBB (F6, bitrate- not
  CRF-matched).
- **Headline:** Encoder effort leaks to the software decoder with the
  wrong sign: refs16/bf8 costs 2.3× encode energy for −9% bits AND
  +18% Pi 5 decode power vs refs1/bf0; hardware is flat. The
  fast-decode corner is cheaper on both sides of the wire for +5% bits.
  **Amendment:** on the encode side it's `refs`, not `bf`, that drives
  the cost (F4); on the decode side, only the corner where BOTH knobs
  are maxed together costs more — the interior points sit statistically
  with `def`, not on a smooth ramp (F5); the same min<def<max ordering
  holds on Kranjska (harder/sport content), generalising the finding
  off BBB (F6).
- **Digest:** `digests/2026-08-r13-refs-bframes.md`
- **Paper role:** Third Tier-3 exemplar — completes the set with C13
  (pay encode+decode, save bits), C14 (pay bits, save decode): effort
  knobs, entropy knobs, and synthesis knobs all obey the
  silicon-coverage law. Now generalised off a single content family.

## C16 — R16: Frame rate at the decoder (2026-08-09)

- **Track:** OWL decode rig v3 (Pi 5 n=3 / GTV n=1 scoping), same-content
  30 vs 60 fps pairs, H.264 + AV1.
- **Status:** 🟢 software panel; 🟢 hardware panel within its panel
  since 2026-08-24 (GTV n=3 across H.264/AV1/HEVC, all rows green);
  taxonomy generality beyond the panel stays 🟡.
- **Headline:** 60→30 fps saves 26–29% software decode power — and,
  uniquely among tonight's knobs, the effect shows on fixed-function
  hardware too: GTV −30…−48 % (H.264 +0.348→+0.211, AV1 +0.294→+0.206,
  HEVC +0.356→+0.186 W; n=3, 2026-08-24 gap-fill incl. the new HEVC
  arm). Splits encode-side levers into
  coverage-gated (codec/FGS/entropy/effort → software tail only) and
  workload-gated (fps → every silicon class).
- **Digest:** `digests/2026-08-r16-framerate.md`
- **Paper role:** Completes the Tier-3 set; gives Section 5 its
  two-way lever taxonomy.

## C17 — VP9 iso-bitrate re-run: encode operating points + four-codec decode (2026-08-17→18)

- **Track:** OWL both sides — GoS1 software-encode panel (parity
  harness, dual P110, n=3, reps not adjacent) + decode rig protocol v3
  (five devices parallel, 1080 s windows, n=2–3).
- **Status:** 🟢 within panels (encode 36 cells n=3 sd ≤5 %; decode
  valid rows all green); 🟡 on cross-campaign/cross-ladder comparisons
  and device generality. First indication with repeats, not
  lab-reviewed.
- **Headline:** The operating point decides which "new" codec is the
  expensive one: at defaults VP9 is ~4.6–4.9× x264 per minute of
  output; at the everything-slow set SVT-AV1 p3 is (9.5–10.8× x264,
  ~2× VP9). On hardware clients VP9 decode is energy-neutral vs
  H.264/HEVC/AV1 at matched bits (±0.1 W); in software VP9 is the
  cheapest of the four and HEVC the dearest (2–3× VP9, Pi 400).
  Content moves the hw decode number ~2×. Saturated-CPU method point:
  time is energy (ΔW 65–71 W on every row → timing ladders proxy
  marginal encode energy).
- **Digest:** `digests/2026-08-vp9-isobitrate.md`
- **Paper role:** Sibling of C5's regime-flips-the-ranking for the
  encode side — operating point, like silicon coverage, is a scoping
  axis a codec energy claim cannot omit. ⚠ Encode Wh figures sit on
  the #4941 boundary — cite-vs-report check before prose use.

## C18 — Network-path campaign + C6 delivery-mode reconciliation (2026-08-18→19, desk pass 08-24)

- **Track:** OWL decode rig protocol v3 (Ethernet vs Wi-Fi vs local ×
  1.5/8/20 Mb/s × burst/paced, one content family) + desk audit of C6.
- **Status:** 🟢 within panel (GTV/Bbox n=3 per interface); 🟡 Fire TV
  (n=2) / Pi (n=1) and any device-level generalisation (one link, one
  room).
- **Headline:** Ethernet delivery ≈ local file (network free at the
  client); Wi-Fi costs every device more, by very different amounts
  (GTV +0.21 W avg, Bbox +0.98 W, Pi +0.32, Fire TV +0.1–0.35; overall
  +0.50 W = +75 % while playing); paced vs burst is a null at n=3.
  Reconciliation: C6 F3's "delivery mode outweighs codec 5–14×"
  RETIRED (conflated radio duty cycle with a since-fixed origin defect);
  successor claim = connection method outweighs codec (Wi-Fi share
  2.5–12× the ≤0.08 W codec spread); C6 F4's +0.21 W reproduced at
  n=3 as the GTV *Wi-Fi-active* share.
- **Digest:** `digests/2026-08-netpath-c6-reconciliation.md`
- **Paper role:** Unfreezes Section 5's delivery-mode sentence in
  corrected form; adds the connection-method lever to the
  device-side story with the codec-flatness contrast.

---

## C19 — Apple TV 4K (2017, A10X), VLC-driven, four codecs (2026-08-26/27, +2026-08-29)

- **Track:** OWL client bench (wattlab CR-075) — first Apple-silicon rows
  on an OWL bench
- **Status:** 🟢 **Repeatable** (upgraded 2026-08-27: overnight campaign,
  n=3 per codec, **three content families** — BBB/Kranjska/Meridian,
  player = VLC for tvOS, 36 rows/1 excluded; supersedes the 2026-08-26
  pilot's 🟡 n=2/one-content estimate, which it closely reproduces). 🟢 for
  the mechanism findings throughout (AirPlay `play_url` dead on tvOS 18
  **and** 26; VLC via Companion works; headless is not a measurement).
- **Headline:** On the 2017 A10X, **H.264 and HEVC play at the same power
  (device-total mean 4.08 W, VideoToolbox) across all three content
  families, while AV1 and VP9 both cost +1.19 W more (+29 %)** — the third
  independent instance of "the codec the silicon lacks is paid for in
  software" (after Marvell/Bbox AV1, against MediaTek where AV1 is free),
  now confirmed rather than estimated: the codec gap is stable across
  content (+1.01 to +1.31 W) and 6–10× the between-rep spread. Answers the
  VP9 question: no hardware VP9 path is reached by VLC on this box.
  Corrects CR-075's device description (`AppleTV6,2`, not A15).
  **Headless is not a measurement on this box** (F5): VLC reports
  `Playing` at 1.6–1.8 W with no display — below the paused-with-display
  draw and a third of full-screen playback — and a display hot-plug in
  either direction pauses VLC; playback state alone is not liveness here.
  **Resolved caveat (2026-08-27):** the overnight campaign's elevated
  baseline plateau (~3.2–3.5 W vs the ~2.1–2.3 W floor) was NOT a higher
  resting idle under tvOS 26.6 — a rested, cold-booted re-check with a
  full 4-min settle read 2.57 W mean (n=290, 90% under 3.0 W),
  statistically the same as tvOS 18. The plateau was recurring post-boot
  housekeeping re-triggering on the campaign's ~4-min park/relaunch
  cycle, not a permanent property of the OS (digest §4 Q3). Device-total
  W (the headline metric) was never at risk either way.
  **2026-08-29 addendum (F6) — corrects a public claim:** re-reading F3's
  own table by codec (not by pair) already shows AV1 5.254 W ≈ VP9
  5.284 W (0.6 % apart); a dedicated independent re-check the same day
  (ΔW protocol, n=3 each, batch `c876cc890df2`) confirms it — **AV1
  3.435 W vs VP9 3.495 W, a 1.7 % gap smaller than either set's own
  run-to-run spread.** This corrects a claim made in the public LinkedIn
  thread on the VP9 report that VP9 would be *cheaper* than other
  codecs in software decode on this device — the data says AV1 and VP9
  tie, on two independent readings. Same-day tie on a second device
  (C20, Roku) reproduces it.
- **Digest:** `digests/2026-08-appletv-vlc.md` (+ 2 `.csv`)
- **Paper role:** Section 5.3 silicon-coverage argument now spans three
  vendors (MediaTek / Marvell / Apple) for the penalty half; cite as
  Early Insight with the VLC and n=2 caveats stated. F6 is citable
  directly against the LinkedIn thread if the paper or a follow-up post
  references that discussion.

## C20 — Roku Express 4K, four codecs (2026-08-29)

- **Track:** OWL client bench (wattlab, new device this session) —
  first Roku rows on an OWL bench.
- **Status:** 🟢 within panel (n=3 per codec, one content family — BBB
  iso-bitrate, reused from C17). ~~First indication for this device;
  not yet checked against a second content family (digest §4 Q2).~~
  **2026-08-31: both open questions answered.** Headless vs screen
  mode: statistically indistinguishable (0.384 W vs 0.403 W, n=3
  each) — unlike the Apple TV, headless is a valid measurement on
  this device, F2's original numbers stand as-is. Second content
  family (Kranjska, all four codecs, n=3): 0.265–0.363 W, same
  qualitative shape as BBB at roughly half the absolute level — F2
  holds on a second content family.
- **Headline:** **AV1 and VP9 tie (0.476 W vs 0.481 W ΔW, +1 %,
  inside both codecs' own run-to-run range); H.264/HEVC sit ~0.09–0.10 W
  lower** (0.381 / 0.470 W). Reproduces the same-day Apple TV tie (C19
  F6) on a second, unrelated device — two independent devices now agree
  AV1 ≈ VP9 in software/unconfirmed decode, contradicting the "VP9 is
  cheaper" claim from the LinkedIn thread on both. Decoder path on this
  device is unconfirmed (no logcat equivalent, digest §4 Q1) — this is a
  device-total reading either way. Getting this device onto the bench at
  all required finding a working playback path first: the box carried a
  dormant GoS colleague's hackathon channel (`.m3u` playlist player)
  whose playlist URL had gone dead about a year earlier — fixed and
  automated (digest §1). Along the way, found and fixed two distinct
  harness bugs (marker-segment coded-height padding on HEVC; a marker-
  segment container mismatch on VP9) that were stalling screen-mode
  playback — confirmed neither reaches back to contaminate any other
  device's existing data in this repo (digest §3 F3 explains why).
- **Digest:** `digests/2026-08-roku-decode.md` (+ `.csv`)
- **Paper role:** A second software/unconfirmed-decode device for the
  AV1-vs-VP9 tie in C19 F6 — turns a single-device observation into a
  two-device pattern. Adds a fifth client vendor to the bench.

## C21 — R14: Preset ladder — system energy per encoder preset (2026-08-30)

- **Track:** OWL both sides — GoS1 encode (x264 3 presets + SVT-AV1 3
  presets, fixed CRF per codec) + decode rig v3 (Pi 5 n=3 / GTV n=1
  scoping), one content family (BBB).
- **Status:** 🟢 encode ladder (F1) + x264 decode edge (F2); 🟡 SVT-AV1
  decode edge, hardware-flatness (n=1 scoping), and the cross-device
  synthesis (F4) — all directionally clean, none yet at C15/C17's n or
  device count.
- **Headline:** Preset is an energy multiplier on both sides of the
  wire on software silicon — x264 ultrafast→veryslow costs 7.8× the
  encode energy AND +72% the Pi 5 decode power; SVT-AV1 fastest→slowest
  costs 4.1× encode energy and +31% Pi 5 decode power. GTV (hardware)
  stays flat regardless of preset (14% x264 spread, 3.5% AV1 spread,
  vs Pi 5's 72%/31%) — the same coverage-gated-not-effort-gated pattern
  C11/C15 already found, now shown on a third distinct encoder knob.
- **Digest:** `digests/2026-08-r14-preset-ladder.md`
- **Paper role:** A concrete instance of the OWL(encode)+decode-rig
  complementarity the paper's spine already argues structurally (C8/R2)
  — the SAME preset choice is a double win on software-decode fleets
  and close to a decode-side free lunch on fixed-function fleets;
  neither an encode-only nor a decode-only measurement shows that by
  itself (F4). Caught and fixed a scoring-alignment bug in its own prep
  stage before any metered row landed (digest §4, full incident in
  `runs/session-2026-08-29-r13-r14-r15.md`).

## C22 — R15 Leg A: device-side upscale is not free (2026-08-30)

- **Track:** OWL decode rig, new `output_scale` template capability
  (`decode_run.py`, commit `ab44d58`) — Pi 5 headless decode-only, n=3
  new + 2×n=3 historical comparators.
- **Status:** 🟡 F1 (real spread on the new leg, comparators are
  historical not same-session); 🟢 F2 (a second, previously-unstated
  number surfaced from existing historical rows).
- **Headline:** Upscaling 1080p to 4K on-device costs the Pi 5 +150.7%
  over native-1080p decode (2.14 W) — a real tax, not free — though
  it's still 21.6% cheaper than decoding an actual native-4K bitstream.
  Ordering: native 1080p (1.42 W) < upscaled (3.56 W) < native 4K
  (4.55 W), all three clearly separated. Also surfaced that native-4K
  decode itself costs +219.9% over 1080p on this board — a number C11
  F3/F4 never actually stated (F3 measured throughput, not power).
- **Digest:** `digests/2026-08-r15-upscale-leg-a.md`
- **Paper role:** Unlike R13/R14 (moved to the sibling article), R15
  is squarely in scope — it directly extends §4.1's REM resolution-
  variance finding and §4.3's "fixed-function decode shrugs off 4K"
  claim (C11 F3/F4) to the device-side-upscale case, which neither of
  those covered. First OWL result this session that lands directly in
  the paper rather than the article.

## C23 — R7: C2 native decode vs GTV-on-HDMI, panel-cancelled differential (2026-08-30)

- **Track:** OWL decode rig — C2 native (webOS, own α9 Gen5 SoC) vs
  GTV-on-HDMI, same content, screen mode (real `claim_screen`), n=3
  per arm (n=6 on C2-native Kranjska).
- **Status:** 🟢 F2, F3 (Kranjska sign-flip finding + its GTV
  comparator — reproduced, cross-validated); 🟡 F1 (BBB codec panel —
  both halves individually clean, but the panel-cancelled subtraction
  itself doesn't resolve, a real ~10 W discrepancy reported honestly
  rather than forced).
- **Headline:** Confirms R7's own premise more sharply than expected —
  a single-content C2-native reading isn't just imprecise, it can have
  the **wrong sign**. Kranjska (genuinely dark content — GTV's own
  panel-only reading is only 4.8–4.9 W for it vs BBB's ~26 W) read as
  **negative** power on C2-native six times running (mean −0.655 W,
  n=6, reproduced under a confirmed-settled idle guard), because it's
  darker than whatever bright idle/home-screen state preceded each
  row — the small positive decode signal gets swamped and inverted
  entirely. GTV-on-HDMI on the identical file: clean, small, positive
  (0.217 W, n=3). Separately, GTV-on-HDMI's panel-only component for
  BBB (25.9–26.0 W) came in ~10 W above C2-native's *entire* combined
  reading (16.0–16.3 W) — not explained by decode cost (wrong
  direction/magnitude), most likely a picture-mode/processing
  difference between native and HDMI-fed playback; flagged as open,
  not resolved into a clean "decode differential" number.
  **2026-08-31 amendment: the picture-mode hypothesis was tested live
  with Ben at the TV and refuted, not confirmed.** Both contexts
  standardised to FILMMAKER MODE (was Auto Power Save on C2-native,
  Cinema on GTV-on-HDMI — first confirmation that picture mode is
  stored per-HDMI-input on this TV, not globally). The BBB gap did
  NOT close — it widened to ~13 W, and C2-native's reading moved
  further *below* GTV's panel-only reading, which no additive
  decode-overhead model can produce. The Kranjska sign-flip got
  *more* negative (−2.52 W mean, n=3, vs the original −0.66 W) under
  the same standardisation — ruling out Auto Power Save's adaptive
  behaviour as the mechanism and strengthening rather than resolving
  F2. Both findings now point at an idle-reference-state question
  (not picture mode) as the likely remaining explanation — not
  investigated further this session.
- **Digest:** `digests/2026-08-30-r7-c2-panel-differential.md`
- **Paper role:** Directly strengthens §4.3's device-class/panel
  narrative — the Kranjska sign-flip is a citable, vivid illustration
  of why single-content OLED-panel decode readings aren't trustworthy
  without a cancellation method, which is exactly the argument R7 was
  queued to make. The unresolved F1 discrepancy is a caveat to state
  plainly, not a blocker to citing F2/F3.

## C24 — Apple TV clean ΔW re-run: the codec gap on a marginal basis (2026-08-31)

- **Track:** OWL decode rig, Apple TV 4K (A10X), screen mode, n=3 ×
  4 codecs × 3 content families (36 rows) — the writing desk's top
  priority for the final overnight window before the draft
  circulates ("if only one thing runs, run this").
- **Status:** 🟢 (34/36 rows clean, CV ≤5%; 2 isolated outlier rows
  kept in the record and reported alongside their clean-pair
  alternative, not silently dropped).
- **Headline:** **Replaces C19 F3's device-total figure with a proper
  ΔW-over-idle measurement — the codec gap holds on the marginal basis
  too, across all three content families:** H.264≈HEVC (2.0–2.7 W)
  vs AV1≈VP9 (2.5–3.6 W), the same qualitative shape C19 F3 reported
  pooled and device-total, now confirmed per-family on a clean marginal
  basis. §4.2's caveat paragraph disclosing the device-total figure's
  non-comparability with the rest of the paper's ΔW numbers can be
  deleted.
- **Digest:** `digests/2026-08-31-appletv-clean-dw.md`
- **Paper role:** Directly strengthens §4.2 — removes a stated
  limitation rather than adding a new finding. Also the fourth
  independent device (after MediaTek ×2, Marvell) confirming the
  hardware/software-fallback codec-gap shape on a clean ΔW basis.

## Candidate campaigns (pending RUN_QUEUE execution)

- **C7 — CBR fix re-run** (Tier 1, R1)
- **C8 — LAN-vs-cloud dual-capture formalisation** (Tier 1, R2)
- **C9 — Second STB chipset** (Tier 2, R3)
- **C10 — Live-edge pacing arm** (Tier 2, R4)
