# Digest — R13: Reference frames / B-frames — encoder effort at the decoder (C15)

Third Tier-3 run (RUN_QUEUE R13, corner-trimmed ⚙), overnight
2026-08-09. **Encoder effort leaks to the software decoder: the
max-effort corner pays 2.3× the encode energy for −9% bits AND +18%
software decode power — the bit saving does not pay the decoder back.
The fast-decode corner is cheaper everywhere except +5% bits.**

## 1. Campaign metadata

- **Dates:** 2026-08-09 02:10–03:07 CEST.
- **Content/encoder:** BBB 1080p60 ProRes intermediate (shared with
  C14); x264 preset medium, high profile, CRF 21, GOP 120, yuv420p;
  arms differ ONLY in `-refs`/`-bf`:
  min = refs1/bf0 · def = refs4/bf3 (x264 default) · max = refs16/bf8.
  ⚙ Spec trimmed from the 3×3 grid to the three corners for bench time;
  the corners bound the grid.
- **Quality match:** fixed-CRF assumption verified by VMAF-NEG — spread
  0.32 across arms (92.51/92.84/92.83), inside the 0.5 tolerance set
  before the run. Bitrates: 3995 / 3808 / 3646 kb/s.
- **Capture:** encode = GoS1 parity-row mechanics (n=3, queue paused,
  focus mode); decode = rig protocol v3 headless realtime, Pi 5 n=3,
  GTV n=1 scoping ⚙ (hardware expected flat; confirmed), 105 s windows.

## 2. Scope statement

One content family (BBB — gentle, SI 33), one encoder (x264), one CRF
rung, corners only (interior of the refs×bf grid unmeasured). Headless
realtime decode; no display stack. Same #4941 boundary note as C13/C14.

## 3. Findings

### F1 — Encode energy ladder: effort is expensive, bits are cheap

- **Claim:** per content-minute (n=3, CV <1%): refs1/bf0 0.216 Wh ·
  refs4/bf3 0.292 Wh · refs16/bf8 0.498 Wh. Max effort costs **2.3×**
  the energy of min for **−9% bits** at equal quality; the default
  costs 1.35× min for −5% bits.
- **Status:** 🟢 within panel.

### F2 — The effort surfaces at the software decoder — with the sign
that hurts

- **Claim:** Pi 5 headless realtime (extended to n=6 on def/max ⚙):
  min +1.034 ± 0.039 (n=3) · def +1.155 ± 0.032 (n=6) · max
  +1.255 ± 0.061 W (n=6). Max decodes **+21% hotter than min despite
  carrying 9% fewer bits** — DPB/multi-ref motion-comp pressure
  outweighs the bit saving. GTV (n=1 per arm): 0.35/0.35/0.31 W —
  flat; fixed-function silicon absorbs even refs16/bf8.
- **Status:** 🟢 for min<def AND def<max (n=6 extension 04:00: the
  +0.10 W def→max step is significant, t≈3.5; max r1 +1.139 remains
  the low outlier of its six reps). All rows 🟢 per-run.

### F3 — The operator ledger for this knob

At equal quality on this rung: the **fast-decode corner (refs1/bf0) is
strictly cheaper at encode (−26% vs default) AND at software decode
(−11%) for +5% bits**; the max corner buys −4% bits vs default for
+70% encode energy and (indicatively) +6% sw decode. For any fleet
with a software-decode tail, "turn the encoder up to save bits" can be
energy-negative on BOTH sides of the wire — the opposite of the
intuition that effort is paid once at encode.
- **Status:** 🟡 (single family/rung; def↔max edge itself now 🟢 per
  F2's n=6 extension).

## 4. Anomalies and open questions

- max decode r1 (+1.139) sat low vs the other five reps (1.26–1.33);
  no baseline anomaly flagged; kept in the n=6 mean. The n=6 extension
  (same night) settled the def↔max edge — resolved.
- ~~Interior grid points (refs4/bf8, refs16/bf3 …) unmeasured~~ — done
  2026-08-30, see F4 below. Kranjska repeat also done, see F5.
- Same BBB-gentleness caveat as C14 — now partly addressed by the
  Kranjska repeat (F5).

## Amendment — 2026-08-30: interior grid points + Kranjska repeat (RUN_QUEUE R13 closed)

Two remaining RUN_QUEUE items closed in one overnight continuation
(2026-08-29→30, n=3 throughout, all rows 🟢): the interior grid points
(refs4/bf8, refs16/bf3 — a "cross" design swapping one knob at a time
between the def and max corners) and the Kranjska repeat (does the
finding generalise off BBB). Full data:
`/srv/data/owl/campaign_2026-08-29_tier3/r13cont/`.

### F4 — Encode energy is driven by B-frames, not reference frames

- **Claim:** n=3 per point: refs4/bf3 (def) 0.292 · refs4/bf8 0.298 ·
  refs16/bf3 0.482 · refs16/bf8 (max) 0.498 Wh/min. Holding `bf` fixed
  and varying `refs` (4→16) costs **+0.190–0.200 Wh/min (+65–67%)**;
  holding `refs` fixed and varying `bf` (3→8) costs only **+0.006–0.016
  (+2–3%, inside noise)**. So it is **refs**, not bf, that carries the
  encode-side cost on this grid — correcting the original F1 write-up's
  implicit framing (F1 never actually attributed the ladder to either
  knob individually; this closes that gap explicitly).
- **Status:** 🟢 (n=3, clean CV <2% on 3 of 4 new/repeated points; see
  the refs4bf8 outlier caveat below).
- **Caveat:** refs4bf8_r1 read dW=61.55 vs reps 2–3 at 72.81/73.42 (CV
  driven entirely by this one row) — this was the **first metered row
  of the entire night**, run immediately after r13cont's prep.sh NEG-
  scoring pass (heavy CPU). Baseline was likely still elevated from that
  prior load, which **undercounts** ΔW (hot baseline bias, not an
  inflation risk — see bench-preflight §3). The same pattern recurred
  on R14's very first row (h264_ultrafast_r1, 60.75 vs 73.96/74.21,
  again the first row after a compute-heavy prep phase). Recommend a
  standing fix: `power.cooldown_between_runs` (or an equivalent floor
  wait) before the *first* metered row of a session, not just between
  rows — currently the campaign's `focus_mode_enter()`/baseline fires
  immediately after prep with no settle. Both outliers are kept in the
  reported means (both rows still flagged 🟢 individually); excluding
  them would tighten refs4bf8 to ~0.314 Wh/min and h264_ultrafast to
  ~0.192, not changing either finding's direction.

### F5 — Interior decode points don't cleanly separate refs from bf —
only the extreme corner costs more

- **Claim:** Pi 5 decode ΔW, n=3 each: refs4/bf3 (def) 1.155 W (n=6,
  original) · refs4/bf8 1.129 W · refs16/bf3 1.159 W · refs16/bf8 (max)
  1.255 W (n=6, original). The two interior points and def are
  statistically indistinguishable from each other (spread 0.03 W
  against per-arm stdev 0.05–0.09 W) — **decode cost is not a smooth
  function of either knob alone; only the corner where BOTH refs and
  bf are maxed together costs more.** This is a genuine (if modest)
  correction to F2/F3's implicit framing that "more effort always
  costs more at decode" — on this grid, effort has to be maxed on
  *both* axes simultaneously before the Pi 5 pays for it.
- **Status:** 🟡 — n=3 on the new points (vs n=6 on the original
  corners), single content family, and the null result (interior ≈
  def) is inherently harder to certify than a clear direction; worth a
  larger n if this decomposition matters to the paper's argument.

### F6 — Kranjska repeat: the corner ordering generalises off BBB

- **Claim:** bitrate-matched (10504 kbps, the VMAF-92 iso point for
  kranjska_120s/h264 from `docs/smpte_2026/iso_vmaf_table.csv` — CRF
  does not transfer across content, see methodology note below) 2-pass-
  free single-pass ABR, n=3: encode min 0.165 · def 0.252 · max 0.474
  Wh/min; decode min 0.912 · def 0.946 · max 1.121 W. **Same min<def<max
  ordering on BOTH encode and decode as BBB**, on a harder/sport-motion
  content family and a bitrate-matched (not CRF-matched) methodology —
  the F1–F3 story is not a BBB-specific artefact.
- **Status:** 🟢 direction (ordering holds cleanly, n=3, low CV); 🟡
  magnitude (bitrate-matched methodology means the quality achieved
  isn't held constant across corners the way BBB's CRF21 was — NEG-
  scored post-hoc: min 93.35 / def 91.65 / max 91.29, a real ~2.1-point
  spread, not assumed away. So part of Kranjska's larger encode-side
  gap (min→max +187% vs BBB's +71%) may be partly a quality-vs-bitrate
  tradeoff rather than a pure effort-cost, since higher-refs/bf arms
  are producing SLIGHTLY lower measured quality at the same bitrate —
  the opposite of what CRF-matching would show. Treat the Kranjska
  *decode* ordering as the more load-bearing generalisation claim;
  the encode-side magnitude comparison to BBB needs a CRF-matched
  Kranjska run to fully trust.
- **Methodology note:** no NEG-verified CRF existed for Kranjska before
  this session (sport content needs materially more bitrate than BBB
  for equal quality, per `parity.py`'s own note); rather than run a
  fresh CRF search, this reused the already-measured VMAF-92 bitrate
  point and scored quality post-hoc rather than assuming it constant.
  This is a deliberate, documented deviation from both R13's original
  CRF-matched BBB method and from R12k's own Kranjska check (which used
  2-pass ABR; this run used single-pass, matching `parity.py`'s own
  `build_cmd` convention and tonight's R14 run for internal
  consistency). A CRF-matched Kranjska re-run would settle F6's 🟡.

**RUN_QUEUE R13 status: fully closed** (original corners n=3 + n=6
def/max extension + tonight's interior grid + Kranjska repeat, all in
one continuation).

## 5. Figure manifest

- `figures/fig_effort_ladder.{svg,png}` — encode Wh/min vs Pi 5
  decode ΔW per corner (up-and-right = worse both sides). Command:
  `/srv/data/owl/figenv/bin/python figures/make_coupling_figures.py`.
- Interior-grid and Kranjska figures not yet generated — raw data is in
  the JSONL files below, figure script not yet extended to plot the
  4-point grid or the two-family comparison.

## 6. Provenance

- Original raw store: `/srv/data/owl/campaign_2026-08-09_r13/` (`sweep/`,
  `stage_b_results.jsonl`, `stage_c_results.jsonl` + job IDs, scripts).
- 2026-08-30 amendment raw store:
  `/srv/data/owl/campaign_2026-08-29_tier3/r13cont/` (`sweep/`,
  `stage_b_interior_results.jsonl`, `stage_b_krj_results.jsonl`,
  `stage_c_results.jsonl` + job IDs; `common.py`/`driver.py`/`prep.sh`
  in the parent `campaign_2026-08-29_tier3/`); session journal at
  `runs/session-2026-08-29-r13-r14-r15.md` (full incident log incl. a
  scoring bug caught and fixed in the sibling R14 run before any
  metered rows were taken).
- Decode envelopes: `results/decode/{date}_{job_id}.json`.
- Analysis date: 2026-08-09 (original), 2026-08-30 (amendment).
