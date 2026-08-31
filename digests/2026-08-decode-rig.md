# Digest — Decode Rig Campaign (five-device client bench, Jul 30–Aug 1 2026)

Campaign C11. Derived from the GoS1 living document
`/srv/data/owl/campaign_2026-07-31/DECODE_MEASUREMENTS.md` and three
findings docs in `~/wattlab/docs/findings/`. This digest restructures
those sources to DIGEST_SPEC and adds no numbers of its own; finding
numbers (F1–F11) follow the living document for traceability.
**Lab review completed 2026-08-09 (GoS1 bench session):** every cited
number re-verified against its stored envelope, the three findings docs
confirmed and de-DRAFTed, and F2's open ratio spread resolved by the R6
reconciliation run — statuses below are lab-confirmed, no longer
proposed. (F5 and F8 remain 🟡 by design.)

Relation to earlier digests: extends C5 (Pi decode bench) and C6 (STB
decode) with a rebuilt rig — protocol v3, stable-idle guard, five
concurrently metered devices, in-clip markers — and partially supersedes
them where re-measured (F2 hw-vs-sw re-read, F6 network share). C5's
open question Q1 (no baseline-floor guard) is resolved by protocol v3.

## 1. Campaign metadata

- **Dates:** 2026-07-29 to 2026-08-01. Rig build-out 07-30; 66-cell
  autonomous campaign 08-01 (12-cell duration study + 54-cell codec
  suite, 0 errors).
- **Devices (as of 08-01), five concurrently metered.** Silicon
  recorded verbatim from each box on 2026-08-26 (R3a: Android
  `getprop`; Pis `/proc/device-tree`) — note the panel spans **two
  vendors**, MediaTek (both streamers, same part) and Marvell (the
  operator box):
  - Raspberry Pi 5 Model B Rev 1.1 (Broadcom **BCM2712**, revision
    `e04171`, Bookworm, kernel 6.12.96-rpi-2712) — software decode (no
    usable H.264/AV1 hardware on stock Bookworm).
  - Fire TV Stick 4K 2nd-gen (AFTKRT "karat", Amazon; MediaTek
    **MT8696**: `ro.board.platform=mt8696`, `ro.hardware=mt8696`,
    `ro.vendor.mediatek.platform=mt8696`, `ro.soc.*` empty; Fire OS on
    Android 11 / SDK 30, build RS8180.3739N) — hardware H.264/HEVC/VP9/AV1.
    Added 07-31, replacing the Pi 400 on the bench.
  - Google TV Streamer ("kirkwood", Google; MediaTek **MT8696**:
    `ro.board.platform=mt8696`, `ro.hardware=mt8696`,
    `ro.soc.manufacturer=Mediatek`, `ro.soc.model=MT8696`; Android 14 /
    SDK 34, build UTTK.260317.003) — hardware H.264/HEVC/AV1. The same
    SoC as the Fire TV Stick: the two "MediaTek" streamers are one part
    on two OS stacks, not two chips.
  - Bbox Bouygtel4K (operator CPE; Arcadyan, brand BouyguesTelecom;
    **Marvell Berlin**: `ro.board.platform=marvellberlin`,
    `ro.hardware=marvellberlin`, `ro.product.board=HMB9213NW`,
    `ro.product.device=HMB9213NW`, `ro.soc.manufacturer` and
    `ro.soc.model` empty; Android 11 / SDK 30, build CALIFORNIE) —
    hardware H.264/HEVC, **no AV1 hardware**. First operator CPE
    measured on an OWL bench. **Not MediaTek** (corrected 2026-08-26;
    the digest previously recorded no SoC for it).
  - LG C2 55" OLED as a native decoder (α9 Gen5, built-in browser) —
    also the rig's display (webOS input/brightness control; replaced
    the ASUS PA329C LCD).
  - Raspberry Pi 400 Rev 1.0 (Broadcom **BCM2711**, revision `c03130`,
    Bookworm, kernel 6.12.20-rpi-v8) — early rows 07-30, then parked
    (config retained; back for R6 and CR-074).
- **Capture:** per-device Tapo P110 (fw 1.3.1, local mW API, 1 s
  cadence); shared display metered separately. Protocol v3: fixed
  settle → stable-idle guard (reference floor, shared code with the
  server bench's CR-070 guard) → fixed-length baseline → sampled window
  → `confidence.py` → per-row checkpoint. In-clip 5 s black·white·black
  marker head, auto-segmented, verifies real content on screen.
- **Content:** BBB / Meridian / Kranjska families, 1080p matched-VMAF
  (~92–93) NVENC encodes (bitrate co-varies with codec: BBB
  8.0/6.6/4.0 Mb/s for h264/hevc/av1); 4K60 H.264 arm (BBB upscaled to
  3840×2160, resolution-isolated); 60-min concat clips for long-window
  runs.
- **Codecs:** H.264, HEVC, AV1. Windows 30 s–59 min (duration study);
  150 s cells (codec suite). Delivery: HTTP from a Range-correct
  OWL-owned origin (CR-072) or local staging, per arm.

## 2. Scope statement

Client device layer only. The device under test and the shared display
are metered on independent plugs; display energy is excluded from
device figures. Network/CDN energy is excluded except in F6, where
network delivery is the isolated variable (origin byte counters make
Wh/GB computable per run). One device per silicon class in most cells;
one resolution rung (1080p) except the explicit 4K arms; no HDR arm.
Matched-VMAF encodes mean bitrate co-varies with codec (iso-quality
framing, not equal-bitrate). Datacentre and production boundaries
excluded; no amortised training cost included; encode-side codec energy
analysis belongs to #4941.

## 3. Findings

Statuses are the lab's own per the living document, proposed pending
lab review.

### F1 — A streaming box plays 4–7× cheaper than a general-purpose board

- **Claim:** same BBB 1080p60 H.264 clip, local delivery, display
  attached, marker-verified: Google TV +0.30 W · Pi 400 hw +1.32 W
  (4.4×) · Pi 400 sw +1.96 W (6.5×) · Pi 5 sw +2.03 W (6.8×). The gap
  survives even against the board's own hardware decoder.
- **Status:** 🟢 (all four rows green; runs `357b087d`, `606d5ad3`,
  `d99775a0`, `ea55f33b`).
- **Confounds:** single content, single rung, one device per class.
  GTV row is full Android playback (compositor inherent — the frame is
  each device's real product stack, but the ratios are not pure
  decoder-silicon ratios). Pi 400 hw path uses `v4l2m2m-copy` (copy
  adds CPU; +1.32 W is an upper bound for that board's hw playback).

### F2 — Hardware vs software decode, same board (RECONCILED 2026-08-09, R6)

- **Claim:** Pi 400, same 1080p60 H.264 BBB file, headless, protocol v3,
  arms interleaved: hw +0.411 ± 0.073 W (n=6) vs sw +1.503 ± 0.034 W
  (n=3) at 1× — **3.7× realtime**; hw +0.594 ± 0.049 vs sw
  +2.723 ± 0.073 W saturated (n=3 each) — **4.6× saturated**. All 18
  rows 🟢. The Pi 5, which shipped without the block, pays +1.57 W (C5).
- **Status:** 🟢 — now n≥3 per cell under one protocol. July v2's
  3.6×/4.1× replicate within noise; the 07-30 "~7×" rested on a single
  hw row (+0.221 W) below tonight's n=6 range (0.33–0.51 W) — same
  session as the post-boot-plateau incident (run 57e8ba84), consistent
  with a residually-elevated baseline under-counting the small hw ΔW.
  **Cite 3.7× realtime / 4.6× saturated**; the hw arm's own rep spread
  (CV ~18% on a ~0.4 W signal) is why single-pair ratios ranged 3.6–7×.
- **Run IDs:** hw_rt c22219b7 b7dca03d aef16058 2d247351 b82a150e
  4241d0e4 · sw_rt f01b24c3 81225ea1 37374ca2 · hw_sat 09d012c8
  38f41876 bffab9f5 · sw_sat bbdad90a 0dd11e8f 596c3ee6
  (raw store `/srv/data/owl/campaign_2026-08-08_r6/`).
- **Confounds:** hw-vs-sw measurable for H.264 only (HEVC blocks
  stranded, C5 F4); single content family (BBB); cross-board Pi 5
  comparison still n=2 July rows.

### F3 — "Can decode" ≠ "can play": 4K breaks at the present path

- **Claim:** Pi 5, 4K60 H.264: decode-only sustains 75 fps (1.25×
  realtime), but full playback (mpv fullscreen) pegs all four cores and
  visibly stutters — the bottleneck is the display/render/present
  pipeline, not the decoder.
- **Status:** 🟢. Methodology finding: wall power plus achieved-fps
  disambiguates what a naive "can't do 4K" reading gets wrong; a
  playback-capability claim must state which stage it measured.

### F4 — Fixed-function silicon shrugs off 4K

- **Claim:** Google TV plays the same 4K60 H.264 clip smoothly at
  ~1.49 W device-total (range 1.34–1.93), essentially unchanged from
  its 1080p draw (~1.9 W total). Paired with F3: going 1080p→4K costs a
  purpose-built streamer roughly nothing while breaking a
  general-purpose board's playback, and the break is not at the decoder.
- **Status:** 🟢 within this panel (one box, one clip).

### F5 — Operator CPE absolute draw (held back)

- **Claim:** Bbox Bouygtel4K draws ~6.4 W decoding 1080p BBB via its
  default player, vs Google TV ~1.9 W for the same job (>3×).
- **Status:** 🟡 Early Insight — single reading, default-player
  pipeline, ad-laden launcher inflates awake-idle. Not for the paper in
  this form; the controlled-pipeline result is F11.

### F6 — Network delivery share isolated (~+0.3 W), confirming C6

- **Claim:** GTV local-file +0.30 W vs HTTP +0.62 W (07-30): ~0.3 W is
  network delivery, consistent with July's decomposed +0.21 W (C6 F4).
  Origin byte counters now make Wh/GB computable per run.
- **Status (original):** 🟢 within this panel. July's larger finding
  stands: delivery mode outweighs codec 5–14×.
- **Supersede note (2026-08-25):** the "5–14×" sentence is RETIRED —
  see C18 F4 (`digests/2026-08-netpath-c6-reconciliation.md`): C6 F3's
  arms conflated Wi-Fi radio duty cycle with an origin over-fetch and an
  overlay; the successor claim is *connection method outweighs codec*.
  The +0.30 W local-vs-HTTP share above (07-30) was measured on the
  **pre-CR-072 origin** (Range requests ignored → media3 fetched ~2× the
  file bytes, C6 Q1) over the GTV's Wi-Fi interface, so it **does carry
  the over-fetch** as well as the radio share and is not a clean network
  number. C18 F4's Wi-Fi-active share, +0.21 W at n=3 on the fixed
  origin, supersedes it. Prose should cite C18 F1–F4, not this finding.

### F7 — Codec vs silicon, quantified at scale (08-01 suite)

- **Claim:** software decode (Pi 5, ΔW over idle, three content
  families): H.264 ~1.15 W (1.0–1.3) · AV1 ~1.5 W (1.1–1.7) · HEVC
  ~2.2 W (2.1–2.4) — HEVC ~1.9× H.264; ordering h264 < av1 < hevc holds
  across all families and both run modes. Fixed-function boxes
  (Firestick, GTV): H.264 marginal ≈ free (below the ±0.2 W noise
  floor); HEVC and AV1 add a real ~+0.3–0.5 W even in hardware. So
  "codec barely matters on fixed-function silicon" is true to first
  order only, and codec choice dominates in software.
- **Status:** 🟢 (54-cell suite, parallel and sequential agreeing —
  F10). Regime caveat from July stands: saturated, AV1 drew least on
  the Pi 5; paced at 1×, H.264 is cheapest — a codec-energy claim
  without its regime and buffering model stated is not interpretable.
- **Confounds:** matched-VMAF rung (bitrate co-varies with codec);
  headless HTTP-delivery cells; one board per silicon class.

### F8 — Display panel gates the luminance signal (partly uncitable)

- **Claim:** LCD (PA329C) white−black swing only ~5 W (backlight
  dominates); OLED (C2) content-responsive into tens of W (~67 W lit).
  As a native decoder the C2 is content-signed: +16 W on BBB, −3 W on
  Meridian (dark content draws less than the idle-home baseline), so
  its ~1.4 W decode delta is buried under panel luminance. On a big
  OLED the panel is the story and decode-path choice is marginal — the
  inverse of a stick.
- **Status:** 🟡 Early Insight. Single-run C2 numbers are explicitly
  not citable; only the screen-mode differential will be (see §4).
  Connects to the Nov-2025 REM luminance finding (r²≈0.47) and the C3
  8K counter-case.

### F9 — Confidence vs run length is non-monotonic (methodology)

**⚠ SUPERSEDED 2026-08-24 (gap-fill re-run) — original text kept below;
see the amendment for what stands.** The original long-window STB legs
were invalidated by wattlab JOURNAL S62: pre-`fec0065` rows could die
mid-window (Fire TV screensaver at 5 min, GTV inattentive-sleep at
20 min, GTV CEC standby, ADB launches coming up PAUSED) and read as
negative ΔW.

- **Original claim (superseded):** duration study, 30 s / 5 m / 20 m /
  59 m windows. A real
  signal is confident almost immediately and stays so (Pi 5 sw 🟢 at
  30 s, stable within ±0.15 W to 59 m). A genuinely-zero margin cannot
  be rescued by length (GTV/Bbox hw decode 🔴 at every duration). Small
  signals degrade over long runs (Firestick +0.6 🟢 at 5 m → −0.3 🔴 at
  59 m: baseline captured once up front, thermal/baseline drift swamps
  a ~0.5 W margin over an hour). Practical window ~5–20 min for
  small-margin devices; >1 h counter-productive without re-anchoring
  the baseline.

**Amendment (re-run 2026-08-24, protocol v3 WITH keep_awake pinned,
batch `f9d026082401`: GTV + Fire TV × 30 s/5 m/20 m/59 m, n=2 per
duration, PLAYING gate + foreground log + flat-trace; Pi 5 control
pair 5 m + 59 m, n=2):**

- **Stands (re-derived from valid rows):**
  - *Real signals are green in seconds and stay green.* GTV
    (+0.44…+0.68 W): 🟢 at every duration, n=2 each, task level flat
    at ~2.0 W through 59 min. Pi 5 control (+1.17…+1.41 W): 🟢 at 5 m
    and 59 m, task pinned at 4.53–4.55 W — the control legs stand.
  - *Length cannot rescue a small margin.* Fire TV's genuinely small
    signal in this regime (~+0.1 W) flickered 🔴/🟡/🟢 across ALL
    durations (30 s: +0.25 🟢 / +0.13 🟡 · 5 m: +0.08 🔴 / +0.15 🟡 ·
    20 m: +0.12 🟢 / +0.02 🔴 · 59 m: +0.14 🟢 / +0.13 🟡), playback
    foreground-verified on every row.
- **Retired:**
  - *The ~1 h degradation leg.* With keep_awake pinned there is NO
    degradation: both STBs are alive and flat to the end of 59-min
    windows (Fire TV 59 m: +0.14 🟢 / +0.13 🟡 vs the old −0.3 🔴).
    The old Firestick degradation rows match the S62 dead-playback
    signature exactly (green at short windows → negative at 3540 s on
    all three families). Invalidated original rows by job id:
    Fire TV 3540 s `83ae9b02` `e519c729` `2011f22f`; Fire TV kranjska
    redo (dead/paused session at every duration) `fcb3a313` `3178fa71`
    `2e367611`; GTV long/negative rows `ff57230b` `4ffea805`
    `d9b74975` (1200 s) + `83ae9b02` `e519c729` `2011f22f` (3540 s)
    and kranjska 30 s PAUSED-launch rows `a909f057` `a051f8a4`; Bbox
    negative rows from 300 s up (same signature) `8ff253a9` `b5ac7b15`
    `e45ef136` `79aca4f5` `4ffea805` `485c2c99` `d9b74975` `e519c729`
    `2011f22f`. Pi 5 rows in those jobs remain valid (its legs were
    never affected).
  - *The "practical window ~5–20 min" guidance.* In the re-run, longer
    windows bought nothing for the small-margin device — 5 m, 20 m and
    59 m flags are no more stable than 30 s. What decides the flag on
    such a device is baseline validity, not window length: the box's
    idle screen churns (autoplay carousel; three re-run rows were
    discarded for exactly that — see §4 Q7). Replacement guidance:
    for small margins, repeats (n) beat length; re-anchor or re-take a
    suspect baseline rather than lengthening the window.
- **Disclosures:** keep_awake pins sleep/screensaver/CEC timers OFF —
  a bench configuration, not living-room behaviour (a default GTV
  sleeps at 20 min). Re-run ran with the shared panel dark: the Fire
  TV plays at a lower absolute level in this state (task ~1.26 W vs
  2.02 W in the 08-16 anchor `2c793c73`; display ON at 4K60, video on
  a hardware overlay, foreground-verified — see §4 Q8). Pi 5 control
  ran headless (no HDMI attached) on its new plug and now also runs a
  Pi-hole DNS service — a small, steady background load included in
  its baseline.
- **Status:** 🟢 for the two surviving legs (n=2 per duration per
  device, every valid row liveness-gated); the degradation leg and the
  window guidance are withdrawn, not restated.

### F10 — Five-device parallel measurement validated (methodology)

- **Claim:** every codec cell run both all-5-parallel and
  one-at-a-time; Pi 5 matches within ~0.05 W across all nine
  family×codec cells (e.g. BBB H.264 +1.33 ∥ vs +1.34 seq); the
  fixed-function boxes match within noise. Only the C2 diverges
  (unstable panel baseline, not parallel contamination). Parallel runs
  give 5× throughput with no accuracy penalty for the decode devices.
- **Status:** 🟢.

### F10b — Seven-device parallel measurement (2026-08-27 addendum, exploratory)

- **Claim:** F10 validated five devices metered in parallel; the same
  dispatch (one bench.py subprocess per device, independent settle →
  baseline → window on its own meter, no shared lock) run with **all
  seven** rig devices (Pi 5, Pi 400, Fire TV, GTV, Bbox, Apple TV, C2)
  against the same clip on three content families (BBB/Kranjska/Meridian
  iso-bitrate H.264, one rep each, `bin` batch `1cbf04e86b15`) reproduces
  each device's own known device-total W within **≤0.06 W for Pi 400/GTV/
  Fire TV** (task-level; two Fire TV/Bbox baseline readings were transiently
  elevated — same class as the Bbox network-transition note above, not a
  parallel-dispatch fault) and **within Bbox's own documented idle-drift
  band**. Two real misses at 7-way concurrency: the **Apple TV's Meridian
  baseline** spiked (task itself matched its own solo numbers to within
  0.02 W — only the baseline was hit) and **C2's Kranjska/Meridian
  magnitude drifted ~1-2 W low** while the *direction* (Meridian < BBB,
  the known luminance effect) was preserved. Plausible cause for both:
  origin/network/CPU contention from six simultaneous other devices
  landing exactly in the pre-row settle window — not tested further
  tonight (n=1/cell, exploratory).
- **Status:** 🟡 Early Insight, n=1/cell — encouraging (19/21 cells clean),
  not citable as a campaign. **Kept as a separate dataset per the owner's
  instruction** (batch `1cbf04e86b15`); candidate for a proper n≥3
  seven-device campaign if this holds up, at which point it would extend
  F10's claim from five to seven devices.
- **Confound:** exercises the same origin/LAN path C18 studies for
  connection method — a seven-way concurrent fetch is a different network
  regime from the one-or-two-device case every other finding in this
  digest was measured under.

### F11 — Operator CPE pays for the codec its silicon lacks

- **Claim:** Bbox (controlled Just-Player pipeline, 08-01 suite):
  H.264 and HEVC at essentially zero marginal, like the streamers, but
  AV1 at ~+1.4 W across all three content families (BBB +1.4, Meridian
  +1.4, Kranjska +1.2 W) — the signature of software AV1 decode on a
  box with no AV1 block. Concrete "codec-not-in-silicon = expensive"
  data point for the CPE segment; cautionary for AV1 rollout on
  installed operator hardware.
- **Status:** 🟢 within this panel (one operator box).
- **Silicon note (2026-08-26, R3a):** the Bbox is **Marvell Berlin**
  (Arcadyan HMB9213NW), not MediaTek. So the two halves of the
  codec-vs-silicon claim now rest on different vendors and must be
  cited separately: the *penalty* half (AV1 falls back to software
  where the block is missing: +1.2…+1.4 W) is **Marvell**, and with the
  MediaTek streamers' free AV1 the *coverage* argument spans two
  vendors; the *flatness* half (H.264 ≈ HEVC ≈ AV1 within ±0.2 W where
  the silicon covers them) remains **MediaTek-only** — the Bbox's
  H.264/HEVC rows sit inside its own idle drift (idle 6.3–6.8 W, ΔW
  ≈ 0 ± noise), which is consistent with flatness but cannot
  demonstrate it. Section 5.3 is written to say exactly that.

## 4. Anomalies and open questions

- **Q1 — RESOLVED 2026-08-09 (R6):** the 3.6× vs ~7× spread was the hw
  arm's run-to-run variability plus one baseline-suspect row, not a
  protocol effect. n≥3 interleaved under v3: **3.7× realtime / 4.6×
  saturated** (see F2 for the full numbers and run IDs).
- **Q2 — C2 panel-cancelled decode differential** (screen-mode C2 vs
  GTV-on-HDMI, same clip) still to publish; single-run C2 numbers are
  not citable (F8).
- **Q3 — Headless clean 4K decode energy on the Pi 5** — isolate
  decode cost from the present-path cost identified in F3.
- **Q4 — GStreamer 1.24 hw-HEVC on the Pis** — predicted ~2 W/stream
  saving (C5 F1 gap), untested.
- **Q5 — OLED brightness sweep** as an energy axis (webOS `backlight`;
  luminance-vs-power curve on emissive silicon). Feeds the REM
  luminance narrative.
- **Q6 — One stray ERR cell** in the 08-01 suite (bbox×kranjska 20 m,
  single near-zero cell, not re-run).
- **Q7 (added 2026-08-24; numbered Q3 until 2026-08-25) — media-session PLAYING ≠ foreground.** In
  the F9 re-run, Fire OS post-boot churn backgrounded the player while
  its media session still reported PLAYING: the liveness gate passed
  on rows whose mid-window screenshot shows the Amazon home screen.
  Three Fire rows (and one operator-interference job) were discarded
  and are documented in the campaign notes
  (`campaign_2026-08-24_r16b/NOTES.txt` on GoS1). Harness fix wanted:
  add a foreground-activity check to the gate; also let Fire OS settle
  ≥10 min after a cold mains start before the first row.
- **Q8 (added 2026-08-24; numbered Q4 until 2026-08-25) — Fire TV absolute level depends on panel
  state.** With the shared panel dark, the stick plays the same clip at
  task ~1.26 W vs ~2.02 W in the 08-16 anchor (display ON 4K60, video
  on a hardware overlay — screencap shows black by construction on
  this box, so screenshots cannot verify content there). Candidate
  mechanism: HDMI link into a sleeping vs active sink. Cross-era
  Fire TV comparisons must state the panel state; within-night
  comparisons unaffected.
- **Resolved from C5:** the hot-baseline failure mode (C5 §4 Q1) is
  closed by protocol v3's stable-idle guard, which caught a
  stable-but-not-idle post-boot plateau in testing.

- **Q9 (added 2026-08-26) — Bbox flatness is untested, not confirmed.**
  Its H.264/HEVC marginal is inside its idle drift; a flatness claim on
  Marvell would need the Bbox's idle pinned (its live-TV UI runs in the
  background) or a longer paired H.264↔HEVC series. Note also that the
  Bbox has been on **Wi-Fi** (`.173`) since the CR-074 cable pull on
  2026-08-19 — the 08-01 rows here are Ethernet; any new Bbox row until
  the cable goes back carries the +0.98 W radio share (C18).
  **Q9 answered, 2026-08-31 (writing-desk ask #2,
  `runs/handoff-2026-08-31-final-night.md`) — the cable was already
  back in (Ethernet, confirmed via `/decode/status.json` before this
  session, no radio-share confound), so this ran the harder, more
  rigorous version of the test: an INTERLEAVED H.264↔HEVC series
  (alternating arms rep-by-rep, not blocked by codec — cancels slow
  idle-drift trends rather than letting them land on one arm), n=6
  each, screen mode, one content family (BBB iso-bitrate). Result:
  **H.264 mean 0.151 W (n=6, CV 36%, flags 🟢🟢🟡🟡🟡🟡 — sliding from
  clean to marginal across reps) · HEVC mean 0.075 W (n=6, CV 121%,
  flags 🟡🔴🔴🟡🔴🟡 — mostly red).** Both codecs sit very close to
  zero with wide, inconsistent confidence even at n=6 with proper
  interleaving. **This is the "cannot be resolved on this box" outcome
  the handoff named as one of two legitimate answers — not a failure
  of the test, a real result.** The flatness claim on Marvell remains
  genuinely unresolvable at this measurement resolution: both codecs
  read small enough to be consistent with true near-zero cost, but the
  confidence intervals are too wide to distinguish that from a small
  nonzero one. (One data-quality note: rep 5 of the HEVC arm recorded
  `context_delta_w = -19.874`, sign-flipped against every other row's
  ~+18–21 W — a computation quirk in that row's panel-context field
  only; the device's own `delta_w` reading for that row, 0.086 W, is
  unaffected and was used normally. Excluding that one row, the mean
  panel context is 19.878 W, consistent with the rest.) Raw store:
  `/srv/data/owl/campaign_2026-08-31_overnight/results.jsonl` (labels
  `p2_bbox_h264`/`p2_bbox_h265`); journal
  `runs/session-2026-08-30-writing-desk-4-points.md`.

## 5. Figure manifest

Exported 2026-08-08 on GoS1. All three produced by ONE script —
`figures/make_c11_figures.py` — reading the raw campaign store
(`/srv/data/owl/campaign_2026-07-31/results.jsonl` and the four F1 run
envelopes under `/srv/data/owl/results/decode/`); reproduce with:

    /srv/data/owl/figenv/bin/python figures/make_c11_figures.py

(`figenv` = matplotlib 3.11.1 venv on GoS1; SVG + 300-dpi PNG pairs.)

- `fig_c11_f1_ladder.{svg,png}` — F1 cross-silicon playback ladder:
  ΔW for the same BBB 1080p60 H.264 clip on GTV / Pi 400 hw / Pi 400 sw
  / Pi 5 sw, display attached, 95% CI whiskers, ratios vs the GTV row.
  **2026-08-30 figure-sweep check (writing-desk handoff):** all four
  run ids (`357b087d`, `606d5ad3`, `d99775a0`, `ea55f33b`) verified
  directly from their result envelopes — window_s=165 (well under the
  5-min Fire TV screensaver / 20-min GTV sleep thresholds that
  invalidated F9's long-window legs), `alive_at_window_end: true`,
  confidence Repeatable, all four. Not in the invalidated set. Figure
  stands as-is, no regeneration needed.
- `fig_c11_f7_f11_codec_matrix.{svg,png}` — F7/F11 codec×silicon
  matrix: grouped bars (family-mean ΔW, dots = per-family means over
  parallel+sequential runs) for Pi 5 / Firestick / GTV / Bbox with the
  ±0.2 W noise band; the Bbox AV1 bar is F11's software-fallback
  **2026-08-30 figure-sweep check (writing-desk handoff, Ben's stated
  concern):** every Firestick/GTV row feeding this figure (all 36
  `B_all_*`/`B_seq_*` cells across bbb/meridian/kranjska ×
  h264/h265/av1) checked directly against `campaign_2026-07-31/
  results.jsonl` — every one is `window_s=150`, safely under both
  invalidation thresholds (Fire TV 5 min, GTV 20 min); none carry the
  short-vs-long dead-playback signature (that contrast doesn't exist
  in this dataset — every cell is uniformly 150 s). The consistent
  near-zero/negative H.264 values and GTV's consistently-negative AV1
  reading (−0.39 to −0.41 W, same sign/magnitude across all three
  content families — a real reproducible pattern, not noise) are
  physically plausible given the flat-hardware-decode finding this
  figure exists to demonstrate, not evidence of a dead row. **Figure
  stands as-is, no regeneration needed.** Completeness question
  (VP9/Pi 400/Apple TV/Roku, different operating points) is separate
  from validity — see the writing-desk handoff's option (a)/(b) ask,
  addressed in RUN_QUEUE/RESULTS_INDEX, not here.
  signature. C2 excluded (F8: panel-signed, uncitable).
- ~~`fig_c11_f9_duration.{svg,png}`~~ — **SUPERSEDED 2026-08-24, do
  not use in prose**: drawn from the invalidated pre-`fec0065` rows and
  titled with the retired degradation claim. Kept for provenance only.
- `fig_c11_f9_duration_v2.{svg,png}` — F9 re-run (keep_awake pinned,
  batch `f9d026082401`): ΔW at 30 s/5 m/20 m/59 m, valid rows only,
  per-rep markers (filled=green, open=yellow, X=red), BBB H.264, GTV +
  Fire TV (panel-dark regime) + Pi 5 control (headless).
  Command: `/srv/data/owl/figures-venv/bin/python
  figures/make_f9_rerun_figure.py` on GoS1.

## 6. Provenance

- Raw data: GoS1 `/srv/data/owl/campaign_2026-07-31/` (`results.jsonl`,
  `campaign.log`); per-run JSON at `results/decode/<id>.json` (run IDs
  cited per finding above); rig `/decode` in the wattlab service,
  orchestrator `decode_bench/campaign.py` (resumable, fault-tolerant).
- Source documents: `DECODE_MEASUREMENTS.md` (living doc, campaign
  source of record) and findings drafts
  `streaming-box-plays-4-7x-cheaper-than-general-purpose.md`,
  `hw-decoder-cuts-client-energy-4x.md`,
  `codec-decode-energy-depends-on-silicon-and-regime.md` — all DRAFT
  pending lab review.
- Analysis dates: 2026-07-29 to 2026-08-01. Digest prepared 2026-08-08
  on the writing desk from the lab documents only (no raw-data
  recomputation).
- Device-list amendment 2026-08-26 (GoS1): `adb shell getprop` on the
  three Android boxes via the rig (`/srv/data/owl/decode-bench/tools/
  platform-tools/adb` r37.0.0), `/proc/device-tree/model|compatible`
  and `/proc/cpuinfo` over ssh on the Pis; wattlab commit of the same
  day (rig.py `silicon` strings + MAC follower).
