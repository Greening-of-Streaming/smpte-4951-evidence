# Digest — R14: Preset ladder — system energy per encoder preset (C21)

Fourth Tier-3 run (RUN_QUEUE R14), overnight 2026-08-29→30. **Encoder
preset is an energy multiplier on BOTH sides of the wire on software
silicon: x264 ultrafast→veryslow is ~7.8× the encode energy AND +73%
the Pi 5 decode power; SVT-AV1 fastest→slowest is ~4.1× encode energy
and +30% Pi 5 decode power. On fixed-function hardware (GTV) decode
stays flat regardless of preset — the same coverage-gated-not-effort-
gated pattern R13/C15 already found for refs/bf generalises to preset.**

## 1. Campaign metadata

- **Dates:** 2026-08-30 01:27–03:31 CEST (encode+decode metering; prep
  01:27–01:38, one bug caught and fixed before any metered row — see
  §4).
- **Content:** `test_content/bbb_120s.mp4` (the canonical parity-
  harness BBB clip, 4K60 source, "high" spatial family), scaled to
  1080p at encode (`-vf scale=-2:1080`), full 120 s used throughout
  (no excerpting — the encode+decode+scoring artifact is the same
  file end to end, by design, after a scoring-alignment bug was found
  in an excerpt-based first draft).
- **Encoders/arms:** x264 (CRF 21, profile high, `-bf 2 -x264-params
  scenecut=0:open_gop=0`, GOP 120) at presets {ultrafast, medium,
  veryslow}; SVT-AV1 (profile main, `-svtav1-params scd=0`, GOP 120)
  at presets {12, 8, 4} — CRF 34, picked via a 2-trial calibration at
  preset 8 landing at VMAF 95.35 (see §4 scope note on why this isn't
  a full per-preset VMAF-92 search). Audio AAC 128k throughout,
  matching the live pipeline's own `build_cmd`.
- **Quality achieved (VMAF v0.6.1, measured post-hoc, not assumed):**
  h264 ultrafast 94.95 · medium 95.17 · veryslow 95.23 (kbps 13963 /
  5924 / 5497) — tight, 0.28-point spread. av1 p12 93.52 · p8 95.35 ·
  p4 95.71 (kbps 3238 / 3489 / 2841) — 2.2-point spread, p12
  noticeably softer than p8/p4 at the same CRF (faster AV1 presets are
  less RD-efficient, as expected).
- **Capture:** encode = GoS1 parity-row mechanics (n=3, queue paused,
  focus mode, MIN_TASK_S=120s repeat-to-window loop); decode = rig
  protocol v3 headless realtime — Pi 5 n=3 all six arms, GTV n=1
  scoping all six arms (hardware expected flat; confirmed).

## 2. Scope statement

One content family (BBB), one resolution rung (1080p), two codecs,
three preset points each (not the full 9-point x264/SVT-AV1 ladders —
see scope note below). Headless realtime decode; no display stack.
Same #4941 boundary note as C13–C17: encode-side Wh numbers sit on the
#4941 boundary, coordinate cite-vs-report with Tania before any number
enters prose.

**Scope decision, stated up front:** RUN_QUEUE's literal spec ("at
VMAF 92") implies a per-preset CRF/VMAF search — the bench note that
queued R14 estimated that alone at "~3h honest." This run instead
holds CRF fixed per codec (21 for x264 — the same value R13/C15
already validated near-VMAF-92 on this content family; one short
calibration for SVT-AV1) across a **reduced ladder** (3 of 9 named
x264 presets, 3 of 9 SVT-AV1 preset numbers, one content family) —
the same "fix one thing, verify the spread post-hoc" method R13/C15
already used successfully for refs/bf, applied here to preset. The
achieved VMAF is measured and reported per arm above, not assumed
constant — and it holds tightly enough (≤0.3 points for x264, the
av1 p12 softness noted) that the encode/decode findings below are not
meaningfully confounded by the quality gap.

## 3. Findings

### F1 — Encode energy scales hard with preset, on both codecs

- **Claim:** Wh per minute of content, n=3, CV <3% except ultrafast
  (see anomaly note): x264 ultrafast 0.180 · medium 0.399 · veryslow
  1.402 — **veryslow costs 7.8× ultrafast**. SVT-AV1 preset 12 0.242 ·
  preset 8 0.377 · preset 4 1.003 — **preset 4 costs 4.1× preset 12**.
  Both codecs show the same qualitative shape (a slow-preset "knee"
  well above the fast/medium points), x264's ladder is steeper.
- **Status:** 🟢 (n=3, CV <3% on 5 of 6 arms; see the ultrafast
  first-row caveat below — excluding that one row tightens x264
  ultrafast to ~0.192, not changing the finding's direction or size).

### F2 — On software silicon, preset ALSO costs at decode — extending
R13/C15's "effort leaks to the decoder" finding from refs/bf to preset

- **Claim:** Pi 5 decode ΔW, n=3: x264 ultrafast 0.813 · medium 1.310 ·
  veryslow 1.400 W (**+72% ultrafast→veryslow**). SVT-AV1 preset 12
  1.221 · preset 8 1.433 · preset 4 1.594 W (**+31% p12→p4**). Same
  direction as R13/C15's refs/bf finding (more encoder effort → more
  decode work), now shown on a different encoder knob entirely —
  strengthens the general claim that decoder-side complexity tracks
  encoder rate-distortion effort broadly, not just the refs/bf grid.
- **Status:** 🟢 x264 (clean monotonic, CV 5–13%); 🟡 SVT-AV1 (also
  monotonic and clean, CV 2–7%, but n=3/one content family, same
  caveat class as R13's F2 before its n=6 extension).

### F3 — Fixed-function hardware absorbs preset effort almost entirely

- **Claim:** GTV decode (n=1 scoping, hardware expected flat): x264
  0.57 / 0.65 / 0.61 W (ultrafast/medium/veryslow — 14% spread, no
  clear monotonic order) — av1 0.675 / 0.69 / 0.666 W (p12/p8/p4 — 3.5%
  spread, essentially flat). Contrast with Pi 5's 72% (x264) and 31%
  (av1) spreads on the identical files. **Same coverage-gated-not-
  effort-gated pattern the codec-flatness findings (C11 F4, R13/C15
  F2's GTV rows) already established for refs/bf and for codec choice
  generally — preset joins that list.**
- **Status:** 🟡 (n=1 scoping only, matching R13/C15's own convention
  for GTV rows on this grid — hardware flatness has now been observed
  across three different encoder knobs on this same silicon, which is
  suggestive but each individual observation is still n=1).

### F4 — The encode/decode coupling has a device-class-dependent sign,
not a universal one — the OWL+REM/LEM "1+1=3" case

- **Claim:** for a fleet that plays back on software-decode clients
  (Pi-class, or STBs without hardware coverage for the chosen codec —
  see C11/R3's silicon-coverage findings), choosing a faster encode
  preset is a **double win**: cheaper to encode AND cheaper to decode
  per view. For a fleet that plays back on fixed-function hardware
  (GTV-class), the SAME preset choice is close to a **decode-side
  free lunch** — the encode-side cost still applies, but the decode
  side barely moves, so the "spend more encode effort for a smaller
  file" tradeoff is decided almost entirely by delivery cost and
  encode amortisation (how many times the asset is viewed), not by
  decode energy. **Neither OWL's encode-only view nor a decode-only
  measurement tells this story alone** — it only shows up by holding
  the same preset choice against both device classes' decode cost at
  once, which is exactly the encode-(OWL)/decode-(REM-LEM-shaped rig
  data) complementarity the paper's spine already argues for structurally
  (C8/R2). This run is a concrete instance of it on a new knob.
- **Status:** 🟡 — directionally clean and consistent with three prior
  device-class-flatness findings (C11, C15, F3 above), but this run
  alone is one content family, three preset points, and n=1 on the
  hardware side; framed here as an interpretive synthesis of F1–F3,
  not a new independent measurement.

## 4. Anomalies and open questions

- **A scoring-alignment bug was caught and fixed before any metered
  row.** The first draft of `r14/prep.py` scored a 30–90s encode
  excerpt directly against the untrimmed 120s reference from frame 0
  — total misalignment (VMAF≈3.6, nonsense). It surfaced through the
  AV1 CRF auto-calibration: a real quality signal would move sharply
  between CRF 30 and CRF 1; this one barely moved (3.61→3.68), which
  is what caught it. Fixed by scoring every arm's actual full-length
  upload artifact directly against the untrimmed source (zero-offset
  by construction) rather than a separate excerpt. No metered rows
  were affected — full incident in `runs/session-2026-08-29-r13-r14-r15.md`.
- **First-row-of-session hot-baseline pattern**, same as R13/C15's
  amendment tonight: `h264_ultrafast_r1` read dW=60.75 vs reps 2–3 at
  73.96/74.21 — the first metered row of R14, immediately after
  `prep.py`'s CPU-heavy encode+score work. Consistent with a baseline
  measured before the system fully settled from prior load (hot
  baseline undercounts ΔW — bench-preflight §3), not a real effect.
  Kept in the reported mean (flagged 🟢 individually); recommend the
  standing fix noted in the R13 amendment (a settle wait before the
  *first* metered row of a session, not just between rows).
- **Reduced ladder, not the full 9-point spec** — see the scope note
  in §2. If the paper wants the full ladder, the six arms here
  (endpoints + one interior point per codec) already bound it; interior
  refinement would be incremental, not a redesign.
- **No system-total (encode+decode summed) number is reported** —
  encode is Wh/min (paid once per asset) and decode is ΔW (paid per
  view); combining them requires a view-count assumption that belongs
  to Section 3/5 modelling, not this digest. F4 states the qualitative
  shape instead.

## 5. Figure manifest

- None generated yet. A natural pairing with R13/C15's
  `fig_effort_ladder` figure: encode Wh/min vs Pi 5 decode ΔW per
  preset point, one line per codec, would let both figures share a
  script (`figures/make_coupling_figures.py` already does this shape
  for the refs/bf grid).

## 6. Provenance

- Raw store: `/srv/data/owl/campaign_2026-08-29_tier3/r14/`
  (`scores.tsv`, `av1_crf.txt`, `stage_b_results.jsonl`,
  `stage_c_results.jsonl` + job IDs, `prep.py`/`driver.py`; shared
  `common.py` in the parent `campaign_2026-08-29_tier3/`).
- Session journal (full incident log incl. the scoring-bug catch/fix
  and every stage's raw summary as it landed):
  `runs/session-2026-08-29-r13-r14-r15.md`.
- Decode envelopes: `results/decode/{date}_{job_id}.json`.
- Analysis date: 2026-08-30 (on the bench).
