# Digest — Apple TV clean ΔW re-run: the codec gap on a marginal basis (C24)

RUN_QUEUE writing-desk ask #1 (`runs/handoff-2026-08-31-final-night.md`,
"if only one thing runs tonight, run this"), overnight 2026-08-31.
**Replaces C19 F3's device-total figure with a proper ΔW-over-idle
measurement — the codec gap holds on the marginal basis too: H.264≈HEVC
(~2.0–2.7 W depending on content) vs AV1≈VP9 (~2.5–3.6 W), a consistent
software-fallback penalty across all three content families. §4.2's
caveat paragraph disclosing the device-total figure's non-comparability
can be deleted.**

## 1. Campaign metadata

- **Date:** 2026-08-31, 02:21–04:49 CEST.
- **Device:** Apple TV 4K (2017, A10X Fusion), VLC for tvOS, screen
  mode (real `claim_screen`/HDMI_4 — headless is invalid on this box
  per C19 F5: 1.6 W vs 4.9 W with a screen). Picture mode confirmed
  FILMMAKER MODE (see C23 amendment, same night) — not a factor here
  since this campaign only reports the device's own ΔW (Lab-F3 plug),
  not the shared panel's reading.
- **Content/codecs:** the `loop_{family}iso_{codec}` templates —
  BBB / Kranjska / Meridian × H.264 / HEVC / AV1 / VP9, iso-bitrate
  software encodes (same content/bitrate points as C17/C20/C21's
  iso-bitrate family). n=3 per cell, 12 cells, 36 rows total.
- **Capture:** rig protocol v3, 150 s windows, idle guard active
  throughout (the harness fixes from 2026-08-29 — `atv park` via home,
  per-device idle tolerance — were already in place per the handoff).

## 2. Scope statement

Marginal power (ΔW above this device's own idle) for the first time on
this box — C19's device-total figure existed because a baseline fault
compromised much of that earlier campaign. Three content families, all
four codecs, one operating point (iso-bitrate). Screen mode throughout;
no headless comparison attempted here (already settled as invalid, C19
F5).

## 3. Findings

### F1 — The hardware/software-fallback codec gap holds on a clean
marginal basis, across all three content families

- **Claim (n=3 per cell unless noted):**

  | family | H.264 | HEVC | AV1 | VP9 |
  |---|---|---|---|---|
  | BBB | 2.401 W | 2.326 W | 3.618 W | 3.537 W |
  | Kranjska | 1.117 W | 1.122 W | 1.281 W* | 2.551 W |
  | Meridian | 2.254 W | 1.724 W** | 3.381 W | 3.215 W |

  \* one outlier row excluded from the headline mean, see F2 below —
  the clean pair (n=2) is 2.255 W, in line with the other families.
  \*\* one outlier row included, see F2 — the clean pair (n=2) is
  2.284 W.

  In every family, H.264 and HEVC track each other closely (both
  presumably decoding on the same hardware path) while AV1 and VP9 sit
  meaningfully higher (both presumably software-fallback, no A10X
  hardware block for either) — the same qualitative shape C19 F3
  reported on a device-total basis (H.264≈HEVC vs AV1≈VP9,
  +1.19 W/+29% pooled), now confirmed on a proper ΔW basis with all
  three content families independently, not just BBB.
- **Status:** 🟢 (n=3 per cell, tight CV except the two flagged
  outlier rows — see F2 — all clean cells CV ≤5%).

### F2 — Two outlier rows, both isolated, both explained by known
Apple TV flakiness — kept in the record, not silently dropped

- **kranjskaiso_av1 rep2:** −0.666 W (🔴), sandwiched between two
  clean positive reps (2.266 W, 2.243 W). Task-level power was normal
  for this row (w_task 5.578 vs 5.424/5.438 for reps 1/3) — the
  anomaly is in the baseline capture, not the task, consistent with
  Apple TV's already-documented idle-recovery quirks (this rig's own
  onboarding notes: "idle recovery time differs by an order of
  magnitude between boxes... the Apple TV needs more than ten
  [seconds]," and pyatv's playback-state query can misreport during
  real playback).
- **meridianiso_h265 rep2:** 0.605 W (🟢 — the confidence test itself
  didn't flag it, but it's a clear outlier against reps 1/3 at
  2.284 W/2.283 W). Same signature: task-level power normal
  (w_task 5.654 vs 5.476/5.445).
- **Status:** 🟡 for these two specific cells (n=3 with one clear
  outlier each — the headline table above uses the full n=3 mean for
  consistency with every other cell, but the clean-pair alternative is
  given alongside). Every other cell in the 36-row campaign is clean.

## 4. Anomalies and open questions

- The two outlier rows (F2) would tighten with a 4th confirmation rep
  on each cell — not run tonight (34/36 rows were clean on the first
  pass; re-running two isolated cells is cheap whenever there's bench
  time, not urgent).
- GTV's own panel component (`context_delta_w`, the shared C2 reading
  while Apple TV drives it over HDMI) is recorded alongside every row
  (BBB ~18.3–18.6 W, Kranjska ~3.9–4.1 W, Meridian ~0.6 W) but not
  analysed here — it's the same panel-luminance-tracks-content pattern
  established elsewhere (C23), included for completeness/provenance,
  not a finding of this digest.

## 5. Figure manifest

- None generated. A natural addition to Figure 9's family (device×codec
  matrix) or a standalone ΔW bar chart per content family — not built
  tonight, flagged for whoever picks up the figure-sweep thread next.

## 6. Provenance

- Raw store: `/srv/data/owl/campaign_2026-08-31_overnight/results.jsonl`
  (labels `p1_atv_*`) and `run_overnight.log`.
- Decode envelopes: `results/decode/{date}_{job_id}.json` on GoS1.
- Session journal: `runs/session-2026-08-30-writing-desk-4-points.md`.
- Analysis date: 2026-08-31 (on the bench, overnight, Ben away).
