# Digest — R7: C2 native decode vs GTV-on-HDMI, panel-cancelled differential (C23)

RUN_QUEUE R7, overnight 2026-08-30. **Confirms the spec's own premise
more sharply than expected: a single-content C2-native reading is not
just imprecise but can have the WRONG SIGN — content darker than the
panel's idle/home-screen reference reads as negative power. The
"panel-cancelled" framing is not a nicety here, it's load-bearing.**
Separately, GTV-on-HDMI's own panel-only component (captured
automatically via the harness's dual-meter design) turned up a real,
unexplained ~10W discrepancy against C2-native's combined reading that
this digest reports honestly rather than forces into a clean number.

## 1. Campaign metadata

- **Dates:** 2026-08-30 17:06–18:35 CEST.
- **Devices:** C2 (LG OLED55C2, native decode — its own α9 Gen5 SoC
  decodes+displays in the built-in webOS browser; metered on its own
  plug, Lab-E, since it IS the shared panel) vs GTV (Google TV
  Streamer, MediaTek MT8696, HDMI-fed — metered on its own plug, Lab-D,
  **plus** the panel's plug as a "context" meter, captured
  automatically by the harness's dual-meter design — see
  `decode_bench/bench.py`'s `Meters` class, "Primary (device) +
  optional context (monitor) P110").
- **Content:** BBB (`bbb_h264_rt`/`bbb_codecs_rt` templates — H.264,
  HEVC, AV1, 150 s each) and Kranjska (`krj_def_full.mp4`, the same
  bitrate-matched file from tonight's R13 continuation, 105 s window).
- **Capture:** rig protocol v3, screen mode (real `claim_screen`/
  `recycle_c2_panel` — not headless; see tonight's separate finding
  that headless GTV rows never claim the screen at all). n=3 per
  arm except C2-native Kranjska (n=6, see §3 F2).

## 2. Scope statement

Two devices, one content family plus one repeat family, H.264/HEVC/AV1
on BBB only (Kranjska is H.264 only). This measures device-total power
on each device's own plug — it is not a decode-only isolation the way
the Pi 5's headless path is; the panel is inseparable from C2's own
reading by construction, which is exactly the confound R7 exists to
characterise.

## 3. Findings

### F1 — C2-native BBB readings are dominated by panel luminance, as
predicted, but the panel-cancelled subtraction doesn't resolve cleanly

- **Claim:** C2-native device-total ΔW, n=3 each: H.264 16.31 W ·
  HEVC 16.30 W · AV1 16.05 W (tight, CV ≤2.5%, codec-flat — same
  pattern as every other device on this bench). GTV-on-HDMI's **panel-
  only** component for the same content (`context_delta_w`, the C2's
  own plug while GTV drives it over HDMI): H.264 25.98 W · HEVC 25.97 W
  · AV1 25.91 W — also tight, also codec-flat, but **~10 W higher**
  than C2-native's entire combined (decode + panel) reading.
- **What this means:** naively subtracting would give a **negative**
  "C2 decode overhead" of roughly −9.7 W, which is not physically
  sensible as a decode-cost number — decode work does not un-draw
  power. The likely explanation is a **picture-processing/mode
  difference between C2's native browser player and its HDMI-input
  path** (different default picture preset, tone-mapping, or local-
  dimming behaviour applied per-source), not decode overhead at all.
  This digest reports both raw numbers and does **not** publish a
  subtracted "decode differential" figure — the two readings are not
  yet established to be measuring comparable panel states.
- **Status:** 🟡 — both halves individually 🟢 (tight, n=3, clean), but
  the differential itself is Need More Data. Resolving it needs a
  visual/settings-level check (confirm C2's active picture preset is
  identical whether the source is its own browser or an HDMI input) —
  the same class of live verification that resolved tonight's GTV
  resolution question, not something more automated data alone fixes.

### F2 — Kranjska on C2-native: a real negative reading, not a bug —
the panel-cancellation premise demonstrated directly

- **Claim:** six C2-native Kranjska attempts across the session, every
  one negative: −0.806, −0.747, −0.882 (idle_guard unsettled, first
  batch) · −0.785 (**idle_guard confirmed settled** — waited its full
  30 s budget, converged, and the reading held) · −0.35, −0.358 (a
  second batch, unsettled). Mean −0.655 W, consistently negative
  regardless of settle status. **This is genuine, reproducible signal,
  not a settle-time artefact** — the settled retry landing in the same
  range as the unsettled ones rules out "hot baseline" as the
  explanation. Cross-validated independently: GTV-on-HDMI's own panel-
  only component for the identical file is only **4.82–4.91 W**
  (n=2, `context_delta_w`) against BBB's ~26 W — Kranjska is
  genuinely, substantially darker content. C2-native's pre-row
  reference state (whatever the idle/home-screen shows) is bright
  enough that dropping to Kranjska's low average picture level reads
  as a power *decrease* large enough to swamp and invert the small
  positive decode signal entirely.
- **Why this is the finding, not a failure:** RUN_QUEUE's own R7 spec
  says single-content C2-native numbers are "uncitable" because panel
  luminance swamps the decode delta. A same-sign result would have
  merely been consistent with that; a **sign flip** is a sharper,
  more direct demonstration — panel luminance doesn't just add noise
  on top of the decode signal, it can dominate the sign outright.
- **Status:** 🟢 (n=6, reproduced under a confirmed-settled condition,
  cross-validated against an independent meter on a different device).

### F3 — GTV-on-HDMI Kranjska: clean, small, positive, as expected

- **Claim:** n=3: 0.220, 0.202, 0.229 W (mean 0.217 W, CV 6.4%) — a
  small, clean, positive decode signal on GTV's own plug, in sharp
  contrast to C2-native's negative reading on the byte-identical file.
  This is the STB-side number tonight's R13 continuation and R15
  screen-mode work would predict; nothing new here beyond confirming
  it holds in screen mode too.
- **Status:** 🟢.

## Amendment — 2026-08-31: the picture-mode hypothesis was tested live and refuted

Ben checked in person (writing-desk ask #4, `runs/handoff-2026-08-31-
final-night.md`): C2-native was on **"Auto Power Save"**, GTV-on-HDMI
was on **"Cinema"** — confirming for the first time that this TV
stores picture mode **per HDMI input, not globally** ("I was certain
settings were global across the TV, but clearly not"). Both were
standardised to **FILMMAKER MODE** (a UHD-Alliance-defined reference
mode, chosen over Cinema specifically for citability) with advanced
processing disabled (Noise Reduction/MPEG NR foremost — it reacts to
compression artifacts, a direct per-codec confound — plus Dynamic
Contrast, Dynamic Color, Super Resolution, Edge Enhancer, Smooth
Gradation, TruMotion; Black Level and Color Gamut pinned rather than
left on Auto) across all five contexts (native + all four HDMI
inputs).

**The BBB gap did not close — it persisted at essentially the same
size, and moved in the direction a "decode overhead" story cannot
explain.** Re-run overnight, screen mode, n=3 per codec both sides:

| | H.264 | HEVC | AV1 |
|---|---|---|---|
| C2-native (combined, was ~16.3 W under Auto Power Save) | 15.36 W* | 13.38 W | 13.28 W |
| GTV-on-HDMI panel-only `context_delta_w` (was ~26 W under Cinema) | 26.45 W | 26.28 W | 26.60 W |

\* first rep read 18.6 W (a likely hot-baseline artefact, same class
already documented for other campaigns this week); the clean pair is
13.7–13.8 W, in line with HEVC/AV1.

C2-native's own reading **dropped** under FILMMAKER MODE (from ~16.3
to ~13.5 W) while GTV's panel-only component stayed statistically
unchanged (~26 → ~26.4 W) — the gap is now **~13 W, wider than the
original ~10 W**, and C2-native's *combined* (decode+panel) reading
sits *below* GTV's *panel-alone* reading, which a simple additive
"C2 = panel + decode overhead" model cannot produce regardless of sign.
**The picture-mode-difference hypothesis is refuted, not confirmed —
this was a real, informative negative result, not a resolution.**
The likely remaining explanation is that the two measurements' *idle
reference states* are not equivalent (C2's own idle Home/browser
screen vs. how the shared panel behaves on an inactive-but-connected
HDMI input before playback starts) — a different, deeper question than
picture mode, not investigated further tonight.

**Kranjska moved the same direction, more sharply.** C2-native Kranjska
under FILMMAKER MODE: **−2.523 W mean (n=3, CV 5%, all three rows
individually 🔴)** — more negative than the original six Auto-Power-
Save attempts (−0.35 to −0.88 W, mean −0.655 W). GTV-on-HDMI Kranjska:
unchanged, clean, positive (0.217 W → 0.217 W, n=3 both times). **The
sign-flip finding (original F2) is not only reproduced but
strengthened** — it is not a property of Auto Power Save specifically;
it persists, and grows, under a non-adaptive reference picture mode
too. This rules out "the TV's own power-saving algorithm was
compensating" as the mechanism and leaves the idle-reference-state
question above as the more likely explanation for both the BBB gap and
the Kranjska sign flip.

**Bottom line for citation:** F2 (the sign-flip finding) is now
*stronger*, not resolved — cite it as-is, it does not need the picture-
mode caveat removed, it needs it added (the effect survives a picture-
mode standardisation that was expected to reduce it). F1 (the BBB
discrepancy) stays exactly where it was: report the two raw numbers,
not a subtraction, and note that a same-content-family idle-reference
investigation — not a picture-mode one — is what would resolve it.

## 4. Anomalies and open questions

- **F1's ~13 W discrepancy is still the main open item, sharper than
  before.** Picture mode is ruled out (see amendment above). The next
  candidate is the idle-reference-state question, not yet investigated.
  Until resolved, cite F1's two raw numbers separately, not a
  subtraction.
- **The C2-native idle_guard settled inconsistently** across the
  Kranjska retries (settled once, unsettled twice more) despite the
  panel having had real time to cool between attempts — worth checking
  whether `min_idle_tolerance_w`/`min_idle_max_wait_s` for the "c2"
  device are well-calibrated, or whether the panel's own post-content
  decay is just slow/variable. Did not block this digest (F2 held
  under both conditions) but could bias other C2-native campaigns
  that don't cross-check against a settled retry the way this one did.
- **BBB vs Kranjska average-picture-level difference is asserted from
  the context-meter evidence, not independently confirmed by eye** —
  plausible (BBB is bright 3D animation, Kranjska is outdoor sport
  footage) but not visually verified the way the resolution question
  was tonight.

## 5. Figure manifest

- None generated. A natural figure: C2-native vs GTV-context ΔW side
  by side per content family, showing the sign flip on Kranjska —
  would make F2 legible at a glance.

## 6. Provenance

- Raw store: `results/decode/{date}_{job_id}.json` on GoS1. Job ids —
  C2-native BBB H264/codecs: dispatched via
  `/srv/data/owl/campaign_2026-08-30_r7/run_r7.sh`
  (`campaign_2026-08-30_r7/run_r7.log`, `results.jsonl`). C2-native
  Kranjska: `d0805da5` (unsettled ×3 via the script), `eb31a6c3`
  (settled retry), two more unsettled retries (see journal). GTV-on-
  HDMI BBB: `4ef960f8` (codecs), `20b30233`/`57f377e6`/`079196a6`
  (h264_rt, from tonight's R15 screen-mode validation). GTV-on-HDMI
  Kranjska: original scoping row from the integrity check + `b916afe4`,
  `eec460f6`.
- Session journal: `runs/session-2026-08-29-r13-r14-r15.md`.
- **2026-08-31 amendment raw store:**
  `/srv/data/owl/campaign_2026-08-31_overnight/results.jsonl` (labels
  `p0_c2_krj`, `p0_gtv_krj`, `p0_c2_bbbcodecs`, `p0_gtv_bbbcodecs`) and
  `run_overnight.log`. Session journal:
  `runs/session-2026-08-30-writing-desk-4-points.md`.
- Analysis date: 2026-08-30 (original), 2026-08-31 (amendment).
