# SMPTE #4951 — Evidence Pack

The citable evidentiary record behind the SMPTE 2026 Media Technology
Summit paper "A Dual-Track Measurement Framework for Streaming Energy:
Real-World and Lab-Reproducible Approaches" (Greening of Streaming,
paper #4951).

Every bracketed working citation in the paper — `[C11 F7]` means
campaign 11, finding 7 — resolves here:

- `RESULTS_INDEX.md` — one entry per measurement campaign (C1–C24),
  with its status and headline.
- `digests/` — the campaign digests: findings with sample sizes,
  variance, confidence flags, scope statements, anomalies, and full
  provenance (job identifiers, raw-store paths on the instruments).
- `DIGEST_SPEC.md` — the contract every digest follows.
- `figures/` — the paper's figures with the scripts that generated
  them; each digest's figure manifest records the exact command.

Findings carry a Traffic Light status: **Repeatable** (confirmed
across repetitions with stated confidence), **Early Insight** (single
panel or low n; direction trusted, magnitude provisional), or **Need
More Data**. Withdrawn or superseded findings are kept and marked, not
deleted; the corrections are part of the record.

Raw per-second polling data does not leave the measurement
instruments; the digests are the citable layer, and their provenance
sections say exactly where the raw stores live.

## The platforms

- OWL (Online Watt Lab): github.com/Greening-of-Streaming/wattlab
- REM (Remote Energy Measurement): github.com/Greening-of-Streaming/rem
- LEM (Local Energy Measurement): github.com/Greening-of-Streaming/LEM

This pack is a snapshot exported from the manuscript's working
repository and is updated when the paper is. Questions and replication
attempts are welcome: greeningofstreaming.org.
