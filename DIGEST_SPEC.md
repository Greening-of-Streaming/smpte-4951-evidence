# Digest Specification

The contract for what the lab bench (Claude Code on GoS1) produces per
campaign. A digest must let a writing session make defensible claims without
access to raw data. Target size: < 50 KB per digest so several fit in one
session's context.

## File naming

`digests/YYYY-MM-<slug>.md` plus optional `digests/YYYY-MM-<slug>.csv`
(summary statistics only — never raw 10-second samples).

## Required sections (Markdown)

### 1. Campaign metadata
Date range, devices (with panel type, mode, HDR/SDR — device fact sheets
resolve anomalies), firmware where known, capture method (REM plug model,
polling interval, resolution / OWL configuration), content, codecs, bitrates.

### 2. Scope statement
What was and was not measured. Boundary assumptions (CPE scope, network
exclusions). One paragraph, explicit.

### 3. Findings
Each finding gets:
- One-sentence claim, bounded to what was actually measured
- Traffic Light status with justification (n, variance, repetitions)
- Key statistics (means, CV, correlation coefficients, effect sizes with CIs
  where computable)
- Known confounds

### 4. Anomalies and open questions
Anything unexplained, plus what run would resolve it (feeds RUN_QUEUE.md).

### 5. Figure manifest
List of figures generated to `figures/`, each with a one-line caption and
the exact script/command that produced it (reproducibility).

### 6. Provenance
Where the raw data lives on GoS1 (path), analysis scripts used (path or
wattlab repo commit hash), date of analysis.

## Summary CSV (optional but preferred)

One row per experimental condition; columns for condition variables and
summary statistics. Column names lowercase_snake_case, units in the header
(e.g. `mean_power_w`, `cv_pct`).
