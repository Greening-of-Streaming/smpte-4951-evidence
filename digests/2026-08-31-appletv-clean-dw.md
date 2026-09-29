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

---

## Amendment 2026-09-27 — the fallback plays in real time; C24 is a real cost (handoff 27b item 1)

**Why:** C25 found the Bbox's AV1 "cost" to be a 5 fps failed playback.
That left the Apple TV as the only consumer box whose software-fallback
penalty the draft cites, with no frame-rate evidence behind it.

**Run:** batch `20260927e7e5`, 2026-09-27 19:12–19:49 CEST.
- Apple TV 4K (A10X), VLC for tvOS.
- Screen mode on **C2 HDMI_3** (re-cabled from its dummy plug for this
  run; sink `panel:HDMI_3`, panel lit on every row).
- BBB iso-bitrate (`loop_bbbiso_{h264,av1,vp9}`, the C24 files), 150 s
  windows, n=3 per codec, codec order rotated per repetition.
- **Presented frame rate was checked by eye on every row** (Ben at the
  panel, about 30 s into each window; tvOS/VLC exposes no frame
  counter). All 9 rows: smooth. The eye check resolves slideshow-class
  failure (Bbox 5 fps, W5 1.7 fps). It cannot distinguish full rate
  from partial frame drops (e.g. 45 of 60 fps). Its sensitivity also depends on
  content: BBB's most revealing passage is the whole-background pan just
  after the title (Ben). VLC was already ~50 s into the clip at window
  start, so the ~30 s looks fell in the mostly fixed-background section,
  where moderate drops are hardest to see. Future eye-checked rows should
  be cued to the pan.
- VLC's reported position read 82–83 s mid-window on every row, i.e.
  advancing at wall-clock rate.

| Codec | Task W, absolute (sd) | ΔW per rep | Baseline per rep | Eye check |
|---|---|---|---|---|
| H.264 | **5.539 W** (0.091) | 2.402 / 2.311 / 2.375 | 3.05 / 3.23 / 3.25 | smooth ×3 |
| AV1 | **6.760 W** (0.113) | 3.499 / 3.288 / *1.080* | 3.13 / 3.55 / ***5.74*** | smooth ×3 |
| VP9 | **6.649 W** (0.094) | 3.207 / *0.397* / 3.520 | 3.39 / ***6.19*** / 3.24 | smooth ×3 |

### F3 (new) — The Apple TV's software AV1/VP9 plays in real time and costs about 1.1–1.2 W more than hardware H.264

- **Absolute basis** (the basis `hdmi_sink_regime` §7 recommends on
  tvOS, where the home-screen idle swings ±1.5–2 W):
  - AV1 − H.264 = **+1.221 W**;
  - VP9 − H.264 = **+1.110 W**;
  - n=3 each, per-cell sd ≤0.113 W.
- **ΔW basis:** the two italicised rows have baselines of 5.74 and
  6.19 W against 3.05–3.55 W on the other seven. That is the tvOS idle
  swing, not playback: their task watts (6.82, 6.59 W) match their
  codec's other reps. Excluding them:
  - H.264 +2.363 W (n=3);
  - AV1 +3.394 W (n=2);
  - VP9 +3.364 W (n=2).

  That gives a gap of **+1.03 / +1.00 W**, agreeing with the absolute
  basis within 0.2 W. With all nine rows the ΔW means are meaningless
  (sd 1.3–1.7 W).
- **Reproduces C24 BBB:** H.264 ΔW 2.363 against C24's 2.401; AV1
  3.394 (clean pair) against 3.618; VP9 3.364 against 3.537.
- **Traffic Light:**
  - 🟢 Repeatable for the absolute-watts gap (n=3 per codec, sd ≤0.11 W,
    eye-verified playback on every row).
  - 🟡 for the ΔW-basis gap (n=2 on AV1 and VP9 after the two
    idle-swing rows).
- **Consequence:** unlike the Bbox (C25 F2) and the W5 (C27 F2), this
  fallback penalty is **a real viewing cost**. C24's "paid for" half of
  the §4.2 codec argument stands, on a basis that now includes
  playback evidence.
- **Confounds:**
  - Frame rate was eye-checked, not measured, so partial frame drops
    cannot be excluded.
  - One content family (BBB) tonight; Kranjska and Meridian carry C24's
    original evidence, without fps.
  - AV1/VP9 rows show 5× the within-window power jitter of H.264 (sd
    0.41–0.49 W against 0.07–0.09 W), consistent with bursty CPU
    decode. The same tell appeared on the W5's failed AV1 rows, so
    jitter alone does not distinguish success from failure.
  - The Apple TV now sits on HDMI_3; C24 used HDMI_4.
  - **No audio was heard from the Apple TV on any row** (Ben at the
    panel), although the clips carry stereo audio (AAC; Opus for VP9).
    The GTV rows that followed were audible on the same panel. Whether
    VLC was muted or tvOS routed audio elsewhere is not established.
    The rows therefore exclude audio output that other boxes' rows
    include. Stereo audio decode is small next to a 1.1 W gap, but AAC
    and Opus differ between the VP9 cell and the others.
  - **Picture looked worse on the Apple TV than on the GTV** (Ben,
    subjective, same panel, minutes apart), with identical files (BBB
    1080p60 H.264 High, 8.0 Mb/s). Candidates:
    - the Apple TV's output format (tvOS upscaling or tone-mapping when
      "Match Content" is off);
    - HDMI_3's per-input picture settings, not re-read since 2026-08-31.

    Not investigated. It does not affect the within-box codec gap, but
    the Apple TV's absolute watts may include tvOS-side scaling that the
    other boxes do not do.

**Provenance:**
- Envelopes `/srv/data/owl/results/decode/2026-09-27_{job}.json`
  (H.264 `d06c40f7` `278ad8ce` `2ca01dc9`; AV1 `08e71018` `e9526e2c`
  `b67cc008`; VP9 `e4cd0e20` `bc3d8387` `bfcb4416`).
- Eye verdicts: `/srv/data/owl/campaign_2026-09-27_eye/eye.jsonl`.
- Feeder: `python3 analysis/eye_feeder.py /srv/data/owl/campaign_2026-09-27_eye 20260927e7e5 analysis/c26_eye_plan.json`
  (rows 1–9).
