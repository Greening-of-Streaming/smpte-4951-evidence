# SMPTE #4951 — Evidence Pack

The citable evidentiary record behind the SMPTE 2026 Media Technology
Summit paper "A Dual-Track Measurement Framework for Streaming Energy:
Real-World and Lab-Reproducible Approaches" (Greening of Streaming,
paper #4951).

Every bracketed working citation in the paper — `[C11 F7]` means
campaign 11, finding 7 — resolves here:

- `RESULTS_INDEX.md` — one entry per measurement campaign (C1–C28),
  with its status and headline.
- `digests/` — the campaign digests: findings with sample sizes,
  variance, confidence flags, scope statements, anomalies, and full
  provenance (job identifiers, raw-store paths on the instruments).
- `DIGEST_SPEC.md` — the contract every digest follows.
- `figures/` — the paper's figures with the scripts that generated
  them; each digest's figure manifest records the exact command.
- `analysis/` — the scripts that turn stored measurement rows into the
  numbers in the C25, C26 and C28 digests (exclusion rules, statistics,
  accounting formulas). They show the computation; they read the raw
  store on the measurement host, which is not published, so they cannot
  be run from this pack alone.

Findings carry a Traffic Light status: **Repeatable** (confirmed
across repetitions with stated confidence), **Early Insight** (single
panel or low n; direction trusted, magnitude provisional), or **Need
More Data**. Withdrawn or superseded findings are kept and marked, not
deleted; the corrections are part of the record.

Raw per-second polling data does not leave the measurement
instruments; the digests are the citable layer, and their provenance
sections say exactly where the raw stores live.

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

This pack is a snapshot exported from the manuscript's working
repository and is updated when the paper is. Questions and replication
attempts are welcome: greeningofstreaming.org.
