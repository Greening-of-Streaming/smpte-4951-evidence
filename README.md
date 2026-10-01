# SMPTE #4951 — Evidence Pack

The citable evidentiary record behind the SMPTE 2026 Media Technology
Summit paper "A Dual-Track Measurement Framework for Streaming Energy:
Real-World and Lab-Reproducible Approaches" (Greening of Streaming,
paper #4951).

The paper carries no working citations in its text. The table under
"From the paper to the evidence" below leads from each measured claim,
figure and table to the digest that supports it. The pack holds:

- `RESULTS_INDEX.md` — one entry per measurement campaign (C1–C28),
  with its status and headline.
- `digests/` — the campaign digests: findings with sample sizes,
  variance, confidence flags, scope statements, anomalies, and full
  provenance (job identifiers, raw-store paths on the instruments).
- `DIGEST_SPEC.md` — the contract every digest follows.
- `figures/` — the paper's figures with the scripts that generated
  them; each digest's figure manifest records the exact command.
- `analysis/` — the scripts behind the numbers in the C25, C26 and C28
  digests, in two groups:
  - **standalone, runnable from this pack:** `analysis/review_codec_diffs.py`,
    `analysis/review_lens_ratios.py` and `figures/make_c25_figures.py`
    (with `--runs`); see "Reproduce the paper's central numbers" below;
  - **host-dependent, shown for method only:** the C25 and C26 summaries,
    the C25 panel-state query, `device_idle_coeffs.py` and
    `c28_r8_calibration.py`. These read the raw per-second store on the
    measurement host, which is not published.

Findings carry a Traffic Light status: **Repeatable** (confirmed
across repetitions with stated confidence), **Early Insight** (single
panel or low n; direction trusted, magnitude provisional), or **Need
More Data**. Withdrawn or superseded findings are kept and marked, not
deleted; the corrections are part of the record.

Raw per-second polling data does not leave the measurement
instruments; the digests are the citable layer, and their provenance
sections say exactly where the raw stores live.

## From the paper to the evidence

Paper #4951 (V1.1, pre-submission, 30 September 2026) carries no working
citations in its text. This table is the route from each measured claim,
figure and table to the campaign digest that supports it. "C25 F1" means
campaign 25, finding 1; "R" items are the review checks in C28; an
"amendment" is a dated section at the end of that digest. Numbered
references in the paper ([1]–[12]) are published sources, not digests,
and are not listed here.

Built from the evidence notes kept beside each paragraph of the
manuscript source (`drafts/` in the working repository), 2026-10-01.

| Paper | What it says | Evidence | Digest |
|---|---|---|---|
| §2.1 | July 2026 field campaigns: 10 devices, 5 households, four countries | C3, C4 | `2026-07-worldcup.md`, `2026-summer-hackathon.md` |
| §2.1 | Focus mode; the vendor cloud's rate limit; LEM added July 2026 | C1, C2, C8 | `2025-11-cycle.md`, `2026-07-cycle.md`, `2026-08-r2-dual-capture.md` |
| §2.2 | ~14 s from launch to first frame; three polling intervals per state; the signature is a display instrument | C8 F1 | `2026-08-r2-dual-capture.md` |
| §2.2 | +6.46 W apparent difference from a 50 s start offset, gone after alignment | C4 F3 | `2026-summer-hackathon.md` |
| §2.3 | Cloud path under-reads a ~4 W device by 9–11% (n=4) | C8 F3 | `2026-08-r2-dual-capture.md` |
| §2.3, Figure 3 | LAN path: offset 0–1 s, r = 0.96–1.00, 0.4–2.7% at 10 s, 0.2% at 1 s (one run); cloud r = 0.48–0.81 | C8 F2, C28 R5e | `2026-08-r2-dual-capture.md`, `2026-09-review-checks.md` |
| §2.3 | What 10 s still loses; LAN path validated wired only | C8 | `2026-08-r2-dual-capture.md` |
| §3.1 | Idle guard: host does not cover a session's first run; rig gates every run | C15, C21, C28 R5c | `2026-08-r13-refs-bframes.md`, `2026-08-r14-preset-ladder.md`, `2026-09-review-checks.md` |
| §3.1 | Attributional lens: ratios shift ≤ 8% among CPU encoders, up to 24% CPU vs GPU | C28 R1 | `2026-09-review-checks.md` |
| §3.1 | Read-path agreement 0.2% is a consistency check, not a calibration; no reference meter | C8 F2, C28 R5e, R7 | `2026-08-r2-dual-capture.md`, `2026-09-review-checks.md` |
| §3.1, Table 1 | Rig devices, silicon, confirmed hardware decoders; Xiaomi Gen 2 and Gen 3; eleven on the rig, ten today | C11, C17, C19, C20, C24, C25, C27, C28 R9 | `2026-08-decode-rig.md`, `2026-08-vp9-isobitrate.md`, `2026-08-appletv-vlc.md`, `2026-08-roku-decode.md`, `2026-08-31-appletv-clean-dw.md`, `2026-09-c25-decode-rediag.md`, `2026-09-w5-allwinner.md`, `2026-09-review-checks.md` |
| §3.2 | Calibration 2.46% / 1.90% (20 pairs, 5 Sept); earlier 2.38% / 1.12% (7 July); SE floor ~1.5 W | C28 R8 | `2026-09-review-checks.md` |
| §3.2 | Client drift term 2–4× optimistic; no Section 4 flag changes | C28 R6 | `2026-09-review-checks.md` |
| §3.3 | Pacing can reorder software codecs (Pi 5); SVT-AV1 ~1× to ~10× x264 across presets | C5 F5, C17 F1 | `2026-07-pi-decode.md`, `2026-08-vp9-isobitrate.md` |
| §3.3, Figure 5 | A clear signal is confident within seconds; a ~0.1 W margin flickers at every length | C11 F9, C28 R8 | `2026-08-decode-rig.md`, `2026-09-review-checks.md` |
| §3.4 | Failed playback can read low (W5, 1.7 fps) or high (Bbox, ~5 fps) | C27 F2, C25 F2 | `2026-09-w5-allwinner.md`, `2026-09-c25-decode-rediag.md` |
| §3.4 | Hardware AV1 logged on MediaTek and Amlogic, measured in the case study on MediaTek alone | C25, C28 R9 | `2026-09-c25-decode-rediag.md`, `2026-09-review-checks.md` |
| §4.1 | November 2025 variable ranking (bitrate and resolution small at the device; luminance strongest) | C1 (and refs [2], [3]) | `2025-11-cycle.md` |
| §4.1 | Field null: HEVC − AVC spans zero on 4 of 4 displays; r = 0.9–1.0; 62–127 W white − black; 10–25 W within content | C4 | `2026-summer-hackathon.md` |
| §4.1 | Null Repeatable within the dataset, Early Insight beyond; set-top box read only 1, 2 and 3 W | C4, C4 F5 | `2026-summer-hackathon.md` |
| §4.2, Figure 7 | Hardware decode +0.43 to +0.51 W (Google TV), +0.25 to +0.33 W (Bbox); codec spread ≤ 0.08 W; Google TV streamed over Wi-Fi | C25 F1 and its delivery-path amendment | `2026-09-c25-decode-rediag.md` |
| §4.2 | Allwinner: H.264 +1.07 W vs HEVC/VP9 +0.97 W (95% CI +0.04 to +0.18 W) | C27 F1 | `2026-09-w5-allwinner.md` |
| §4.2 | Codec intervals are Welch on per-run means and reach ±0.27 W; 0.1 W is an observed range | C28 R2 | `2026-09-review-checks.md` |
| §4.2 | Pi 5 software: H.264 ~1.15 W, AV1 ~1.5 W, HEVC ~2.2 W; Apple TV AV1/VP9 +1.22/+1.11 W over H.264 | C11 F7, C24 amendment | `2026-08-decode-rig.md`, `2026-08-31-appletv-clean-dw.md` |
| §4.2 | Pi 400 hardware vs software, 3.7× (interleaved for the first three repeats) | C11 F2, C28 R5b | `2026-08-decode-rig.md`, `2026-09-review-checks.md` |
| §4.2, Figure 7 | Bbox AV1: ~5 of 59.94 fps at 1080p60; 14–17 of 30 at 1080p30; +1.51 W at 720p30 | C25 F2, C26 F1–F2, C28 R3 | `2026-09-c25-decode-rediag.md`, `2026-09-c26-bbox-av1-rungs.md`, `2026-09-review-checks.md` |
| §4.3 | OLED reads −0.66 W on a dark clip (display luminance dominates) | C4, C23 F2–F3 | `2026-summer-hackathon.md`, `2026-08-30-r7-c2-panel-differential.md` |
| §4.3 | Ethernet ≈ local file (Google TV, < 0.07 W); Wi-Fi ~0.2 W on both boxes; +0.98 W withdrawn | C18 F1–F2 and its 2026-09-30 amendment, C28 R5a | `2026-08-netpath-c6-reconciliation.md`, `2026-09-review-checks.md` |
| §4.4 | 1.6 W × 10⁶ devices ≈ 1.6 MW, illustrative; bitrate +0.17 W across 1.5–20 Mb/s | C18 F4, C4, C26 | `2026-08-netpath-c6-reconciliation.md`, `2026-summer-hackathon.md`, `2026-09-c26-bbox-av1-rungs.md` |
| Table 2, row 1 | 5–20 min window withdrawn | C11 F9 | `2026-08-decode-rig.md` |
| Table 2, row 2 | +0.42 W pacing premium withdrawn | C18 F3–F4 | `2026-08-netpath-c6-reconciliation.md` |
| Table 2, row 3 | VP9 cheaper than AV1 on Apple silicon withdrawn | C19 F6, C20 F2 | `2026-08-appletv-vlc.md`, `2026-08-roku-decode.md` |
| Table 2, row 4 | AV1 +1.2 to 1.4 W on the operator box withdrawn | C25 F2, C26 | `2026-09-c25-decode-rediag.md`, `2026-09-c26-bbox-av1-rungs.md` |
| Table 2, row 5 | Streaming box 4–7× cheaper withdrawn | C11 F1 amendment | `2026-08-decode-rig.md` |

Figures 1, 2, 4 and 6 are diagrams with no measured data of their own;
the numbers printed on Figure 6 repeat §2.3, §4.1 and §4.2 above. Each
figure's generating command or source is in `figures/README.md` and in
C28 R4.

## Reproduce the paper's central numbers

Everything below runs from this pack alone, with no access to the
measurement host. Requirements: Python 3.10+, `scipy` and `matplotlib`
(`pip install scipy matplotlib`). Run from the repository root.

**§4.2 codec-to-codec differences with Welch 95 % intervals (C28 R2).**
The input is one row per metered decode run (C25, C26, C27, and the C17,
C11 F7 and C24 comparison sets), 143 rows, including the failed-playback
AV1 rows that are kept out of the comparison:

    python3 analysis/review_codec_diffs.py --runs digests/2026-09-review-checks-runs.csv --csv /tmp/pairs.csv
    cmp /tmp/pairs.csv digests/2026-09-review-checks.csv    # identical

**Accounting-lens ratios, marginal vs attributional (C28 R1).** The input
is one row per encode run (S53, VP9, C17 and R14 parity rows), 370 rows:

    python3 analysis/review_lens_ratios.py --rows digests/2026-09-review-checks-lens-runs.csv --csv /tmp/lens.csv
    cmp /tmp/lens.csv digests/2026-09-review-checks-lens.csv    # identical

**Figure 7 (marginal decode power by codec, GTV and Bbox, C25).** It is
drawn from the same per-run table:

    python3 figures/make_c25_figures.py --runs digests/2026-09-review-checks-runs.csv --out /tmp

The other scripts in `analysis/` (the C25 and C26 summaries, the C25
panel-state query, `device_idle_coeffs.py` and `c28_r8_calibration.py`)
read the raw per-second store on the measurement host, which is not
published. They show exactly how those digests' numbers were computed.

## The platforms

- OWL (Online Watt Lab): github.com/Greening-of-Streaming/wattlab
- REM (Remote Energy Measurement): github.com/Greening-of-Streaming/rem
- LEM (Local Energy Measurement): github.com/Greening-of-Streaming/LEM

OWL runs on the public internet at https://wattlab.greeningofstreaming.org.
Without an account, a visitor can:
- read the methodology and the catalogued findings;
- watch the host's live power and job queue;
- take the guided tour;
- launch curated runs (a preset video encode, fixed LLM, image and RAG
  tasks), measured live on the host.

Settings and the client decode rig are lab-only. Reviewers who would like
full access can write to info@greeningofstreaming.org; temporary access
can be granted.

This pack is a snapshot exported from the manuscript's working
repository and is updated when the paper is. Release `v1.1-submission`
is the snapshot cited at pre-submission. `main` carries later amendments,
each marked in `RESULTS_INDEX.md`: the C18 Bbox Wi-Fi re-measurement,
the C25 delivery path, the C28 R9 Xiaomi status, and Figures 3 and 5 at
600 dpi.

Questions and replication attempts are welcome: greeningofstreaming.org.
