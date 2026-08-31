# Digest — R11: AV1 Film-Grain Synthesis, encode↔decode coupling (C13)

First Tier-3 coupling hunt (RUN_QUEUE R11), executed overnight
2026-08-08→09 on GoS1 + the decode rig. **The textbook coupling
confirmed and priced: FGS saves bits and encode-side quality-matching
holds, but costs 2.15× the encode energy and +26% software decode power
per viewer — while fixed-function silicon synthesizes grain for free.**

## 1. Campaign metadata

- **Dates:** 2026-08-09 00:11–01:20 CEST, one session.
- **Content:** Netflix Open Content *Nocturne* film-grain variant (the
  grain-plate master Netflix built "for film grain encoding tests";
  CC BY 4.0). 120 s excerpt (t=240–360) of
  `nocturne_60fps_uhd_filmgrain_sdr.mov` (ProRes 422 10-bit UHD60),
  range-fetched without re-encode; lanczos-downscaled to a 1080p60
  ProRes HQ intermediate = encode source AND scoring reference. Grain
  verified visible at 1080p (1:1 crop). Provenance + commands:
  `/srv/data/owl/test_content/grain/PROVENANCE.md`.
- **Encoder:** SVT-AV1 via ffmpeg-master N-124403, preset 6, GOP 120,
  yuv420p, 1080p60. Arms: `film-grain=0` vs
  `film-grain=8:film-grain-denoise=1` (see §4 for why denoise must be
  explicit). Operating point CRF 25 (matched-NEG, below).
- **Encode-energy capture:** GoS1 wall power (dual Tapo P110, parity-row
  mechanics: per-row baseline → poll during repeat-to-min-120 s encode
  loop → ΔW, Wh normalised per content-minute, `confidence.py` with raw
  samples; queue paused, measure lock held, focus mode on).
- **Decode capture:** decode rig protocol v3 (idle guard, 1 s mW
  cadence), headless realtime (`ffmpeg -re … -f null`), HTTP delivery
  from the CR-072 origin, 105 s windows. Devices: Raspberry Pi 5
  (BCM2712, dav1d software decode — synthesis on CPU) and Google TV
  Streamer (MediaTek, hardware AV1 — synthesis in silicon). n=3 per
  cell, arms interleaved.
- **Quality matching:** VMAF-NEG (`model=version=vmaf_v0.6.1neg`,
  scoring binary `ffmpeg-score-20260717`), scored on decoded output
  WITH grain synthesis applied (dav1d default), against the ProRes
  intermediate. NEG chosen because plain VMAF mis-scores grain; the
  no-enhancement model is the defensible comparator. All sweep scores:
  `/srv/data/owl/campaign_2026-08-08_r11/sweep/scores.tsv`.

## 2. Scope statement

Single content title (one 120 s grain-heavy excerpt), single encoder
implementation (SVT-AV1) at one preset, one software decoder (dav1d via
ffmpeg) and one hardware implementation (MediaTek/GTV). Client decode is
headless realtime — no display/player stack. Encode energy is GoS1
(Ryzen 9 7900 24-thread CPU encode) — absolute Wh/min is
hardware-specific; the between-arm ratio is the finding. Delivery
energy (Wh/GB for the 19% bitrate saving) NOT measured tonight — noted
open. Encode-side Wh numbers border #4941: coordinate cite-vs-report
with Tania before any encode number enters prose; the coupling claim
itself is #4951's.

## 3. Findings

### F1 — FGS's bitrate saving exists only where grain still costs bits

- **Claim:** at CRF 25, FGS+denoise gives an *identical* VMAF-NEG
  (89.05 vs 89.05) for **19% fewer bits** (8.12 → 6.59 Mb/s); at CRF 20
  it saves 26% (20.3 → 15.0 Mb/s) at −0.25 NEG. At CRF ≥ 35 the saving
  vanishes (±few %) — the quantizer is already crushing the grain, so
  denoise+resynthesis has nothing to sell.
- **Status:** 🟡 Early Insight (single content, single sweep pass per
  point; the ≥35 null is consistent across 3 CRFs × 2 sub-arms).
- **Confound:** 4K→1080p downscale attenuates grain; a native-4K arm
  would likely show larger savings (Netflix reports ~30% on 4K).

### F2 — FGS costs 2.15× the encode energy per content-minute

- **Claim:** film-grain=8 + denoise at preset 6: 1.361 Wh/min vs
  0.632 Wh/min without (n=3 each, interleaved, CV <1%, all 🟢). Wall
  draw is nearly identical (+74.6 vs +72.6 W) — the cost is throughput:
  grain analysis + denoise roughly halves encode speed.
- **Status:** 🟢 within this panel (one preset, one box). SVT itself
  warns FGS is a significant compute add above preset 6.

### F3 — Software decode pays +26% for grain synthesis; hardware pays ~0

- **Claim:** same matched-NEG pair, headless realtime: Pi 5 (dav1d)
  +2.762 ± 0.024 W with FGS vs +2.189 ± 0.042 W without = **+0.57 W
  (+26%) per stream** — despite the FGS file carrying 19% fewer bits.
  GTV (MediaTek hw AV1): +0.374 ± 0.018 vs +0.388 ± 0.025 W =
  **Δ −0.014 W, zero within the noise floor**. All 12 rows 🟢.
- **Status:** 🟢 within this panel (one sw decoder, one hw box, one
  content). Run IDs in `stage_c_results.jsonl` (envelopes
  `results/decode/`, template `upload`).
- **Reading:** the same silicon-coverage law as the codec finding —
  the cost lands wherever the function is NOT in fixed function. For
  the Pi 5 the synthesis premium (+0.57 W) is bigger than the whole
  h264→av1 codec gap measured in C11 (~0.35 W).

### F4 — The coupled ledger (the paper's dual-track demonstration)

Per minute of content, at the matched-quality operating point:

| side | paid by | film-grain off | FGS+denoise | delta |
|---|---|---|---|---|
| encode (once/title) | datacentre | 0.632 Wh | 1.361 Wh | **+0.73 Wh** |
| delivery (per view) | network | 8.12 Mb/s | 6.59 Mb/s | **−19% bits** |
| decode, sw client (per view) | viewer | 2.19 W | 2.76 W | **+0.0095 Wh/min** |
| decode, hw client (per view) | viewer | 0.39 W | 0.37 W | **≈ 0** |

Break-even against the encode premium alone: after ~77 software-decode
viewer-minutes per content-minute, FGS is net energy-negative on the
device layer; on an all-hardware fleet it is net positive (encode
premium amortises, bits saved, decode free). **The operator-actionable
sentence: FGS is an energy win exactly in proportion to the fleet's
hardware-AV1 coverage** — the same deployment question as AV1 itself
(C11 F11's Bbox).
- **Status:** 🟡 (arithmetic over 🟢 panels; delivery Wh/GB not yet in
  the ledger — origin byte counters make it measurable, queued as an
  open item).

## 4. Anomalies and open questions

- **This SVT-AV1 build defaults `film-grain-denoise` to 0** — FGS
  without explicit denoise made files LARGER (grain params as pure
  overhead over a still-noisy source; observed +~50 kbps at every CRF).
  Any FGS energy/bitrate claim must state the denoise setting; worth a
  methods sentence in the paper.
- First scoring pass was invalidated by a double-trim (input `-ss` +
  filter trim) and redone — scores.tsv is the corrected pass. ⚙
- Delivery Wh/GB for the −19% bits: measurable via CR-072 origin
  counters; not run tonight (bench time went to R12). Would complete
  F4's ledger.
- Native-4K FGS arm (grain undamaged by downscale) — expected larger
  bitrate saving, same decode asymmetry; one evening.
- Does the GTV's *player* path (ExoPlayer/Just Player) ever fall back
  to software AV1 where FGS would then cost? Not probed.

## 5. Figure manifest

- `figures/fig_coupling_ledgers.{svg,png}` — R11+R12 mirrored ledgers
  (shared with C14): per-boundary % change per flag. Command: `/srv/data/owl/figenv/bin/python figures/make_coupling_figures.py`
  (numbers = the digest means; script header lists raw stores).

## 6. Provenance

- Raw store: GoS1 `/srv/data/owl/campaign_2026-08-08_r11/`
  (`sweep/scores.tsv`, `stage_b_results.jsonl` encode rows,
  `stage_c_results.jsonl` decode rows + job IDs, stage logs, all
  scripts `r11_stage_{a,a2,a3,b,c}.{sh,py}`, `r11_rescore.sh`).
- Decode envelopes: `results/decode/{date}_{job_id}.json` per row.
- Grain source provenance:
  `/srv/data/owl/test_content/grain/PROVENANCE.md`.
- Analysis date: 2026-08-09 (this digest, written on the bench).
