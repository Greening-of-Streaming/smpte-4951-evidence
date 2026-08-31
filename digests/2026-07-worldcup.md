# Digest — C3: World Cup 2026 TV power campaign (REM field, three sessions)

Produced 2026-08-25 on GoS1 from the REM production database (experiment
`world-cup-recordings`, "Three selected matches from the WC", device
group `WC2026`). **The bench had no analysis notes, no ad-break log and
no lux-meter trace for this campaign** — everything below is re-derived
from the REM power samples alone, and the three Section 5.2 claims are
tested against that. What the data supports: **in-play TV power is
remarkably flat and the breaks show up as variability, not as a mean
shift.** What it does not support from GoS1's sources: the 99-s
France–UK figure and the 8K power-vs-luminance r ≈ 0.1 (both need
material that lives with Simon/Ben — see §4).

## 1. Campaign metadata

- **Sessions (REM focus-mode windows, all 10-s tick, cloud path, 1 W):**

  | # | Window (UTC) | Devices polled | Live/recorded | Active TVs in the data |
  |---|---|---|---|---|
  | S1 | 2026-06-26 17:56–21:07 (191 min) | 9 | group-stage evening (identity not logged) | Roku-TV (Dom), STJ LG TV, Stan plasma, TP Sammy; Arian TV 0 W |
  | S2 | 2026-07-07 15:31–18:10 (160 min) | 9 | weekday afternoon — no live match; "recordings" | Ben old Samsung, TP Sammy, STJ LG TV, STJ 8K, Stan plasma, Tania C5, Arian TV (flat 75 W), Roku (flat 87 W) |
  | S3 | 2026-07-19 18:46–22:11 (205 min) | 10 | **the final** (kick-off ~19:00 UTC) | Ben Samsung 55" 4K (FR), STJ Prototype 8K (UK), Stan plasma, TP Sammy; BHL TCL 45 flat 47 W, Roku flat 87 W; STJ LG TV / Tania C5 / Arian TV 0 W |

- **Devices (group WC2026, Tapo P110 each):** Arian TV (NL) · BHL USA
  TCL 45 · Ben-old-Samsung-TV (FR) · BenSamsung55" 4K2015 (FR, 2015
  Samsung 4K LCD) · DR003-TV-65-LED-(Roku) (UK) · STJ LG TV (UK) ·
  **STJ Prototype 8K** (UK, 8K LCD prototype — make/mode/HDR not logged
  in REM; hackathon mean 301 W in SDR) · Stan-42" Plasma · TP Sammy
  (Samsung; household not logged) · Tania LG OLED C5 (FR). Lux
  instrumentation (Simon's ESP lux meter, final only) is **not** in REM.
- **Capture:** TP-Link cloud API via the REM collector; per-device
  cadence median 10.0 s, p95 10.2–11.3 s; integer watts; 938–1,216
  samples per device per session. No annotations (ad breaks, kick-off,
  half-time) were recorded in the experiment.
- **Content:** live broadcast (S1, S3) / recorded match playback (S2);
  broadcasters, feeds (DTT/IPTV/OTT) and HDR/SDR per household not
  logged.

## 2. Scope statement

Whole-TV wall power in volunteers' homes during football broadcasts,
one plug per TV, 10 s / 1 W cloud capture; between four and eight TVs
active per session, in up to four countries. No luminance reference in
the data; no ground truth for ad-break timing; no per-household feed
metadata. Statements about "ad breaks" below rest on the half-time band
located from the power data itself (§3 F1 method), which cannot separate
advertising from studio content.

## 3. Findings

### F1 — Breaks raise short-term variability 3–5×; the mean barely moves

- **Method:** 5-min block statistics on the final (S3). In-play blocks
  = +20…+65 min and +100…+145 min after window start (19:07–19:52 and
  20:27–21:12 UTC); the half-time band = the contiguous run of
  high-variance blocks +70…+95 min (19:57–20:22 UTC), consistent with a
  ~19:10 kick-off after the ceremony; pre-match = first 15 min. Block
  CV and mean |ΔW| per 10-s step are the variability measures.
- **Result (S3, final):**

  | TV | In-play mean W / block CV / W per step | Half-time band | Ratio CV / step | Mean shift |
  |---|---|---|---|---|
  | Ben Samsung 55" 4K (FR) | 156.1 / 1.2 % / 1.4 | 151.9 / 6.4 % / 5.8 | ×5.2 / ×4.1 | −4.2 W |
  | STJ Prototype 8K (UK) | 425.7 / 2.0 % / 6.6 | 413.2 / 6.6 % / 15.1 | ×3.2 / ×2.3 | −12.5 W |
  | TP Sammy | 99.5 / 1.6 % / 1.3 | 102.5 / 5.0 % / 3.0 | ×3.1 / ×2.3 | +3.0 W |
  | Stan plasma | 169.1 / 9.6 % / 12.9 | 177.8 / 17.9 % / 16.7 | ×1.9 / ×1.3 | +8.8 W |

  The mean shifts are within ±3 % and of mixed sign; the variability
  ratios are ×3–5 on the three LCD/LED sets and ×2 on the plasma (which
  is noisy in play already). S2 shows the same structure on the STJ
  pair and the C5 (block CV 0.5–1 % in the flat stretches vs 12–20 %
  in the busy ones). During play a football pitch is a near-constant
  luminance field — hence the flat trace; breaks cut between bright
  studio, graphics and adverts.
- **Status:** 🟡 Early Insight — one live match with four active TVs,
  break timing inferred from the data (no logged ad-break times), ratio
  depends on block length. Direction is robust across the four sets;
  "roughly triples" is a fair summary of ×2–5. Section 5.2's wording
  ("mean does not reliably shift; CV / W-per-step roughly triple") is
  supported in this form, with "half-time and pre-match breaks" as the
  honest label rather than "ad breaks".

**Amendment (2026-08-25, re-run against Ben's logged events —
`runs/worldcup-final-2026-07-19/events.csv`, second-precision, French
feed; kick-off 19:08:20 UTC, final whistle 22:02:29 after extra time).**
Same 10-s grid, same statistics, intervals now from the log: in play
(six intervals, 800 samples on the Samsung; the 31-s unplug at 20:26:50
excluded), the two **ad breaks inside play** (19:31:45–19:32:45 and
20:45:20–20:46:49, 6 + 9 samples — the ad-break test proper), the
half-time block split into ads→show→ads (19:55:30–20:14:30, inner
boundaries unlogged) and ads-only (20:14:30–20:19:20), post-match ads
(after full time 21:16:25–21:17:45; after the final whistle
22:05:35–22:08:58), and studio/stadium segments. Ben's Samsung is the
only set on the logged feed; the UK/CA sets carry unknown feed lags and
their own ad schedules, so for them only the half-time block (common
to every feed) is interpretable.

| Ben Samsung 55" 4K (FR) | n | mean W | within-interval CV | W per 10-s step |
|---|---|---|---|---|
| in play (regulation halves) | 569 | 156.2 | 0.8–1.7 % | 1.05–1.53 |
| in play (extra time) | 231 | 153.1 | 3.0–3.3 % | 2.9–4.0 |
| in play (all) | 800 | 155.3 | 1.9 % | 1.96 |
| **ad breaks inside play** (2) | 15 | 153.0 (−1.5 %) | 2.5 % | 4.46 (**×2.3** vs all play, ×3.5 vs regulation) |
| half-time ads → show → ads | 114 | 151.7 (−2.3 %) | 6.7 % | 4.81 (×2.5) |
| half-time ads only | 29 | 146.5 (−5.7 %) | 14.5 % | 16.8 (**×8.6**) |
| post-match ads (2) | 28 | 151.9 (−2.2 %) | 4.0 % | 6.38 (×3.3) |
| studio / stadium (6) | 90 | 154.6 | 0.3–1.3 % (post-final 16.7 %) | 0.4–1.7 (post-final 13.6) |

- **Mean:** never moves more than 6 % and only downward (ads are darker
  than a floodlit pitch on this LCD); in the short in-play ad breaks
  −1.5 %. Confirmed.
- **Variability:** W-per-step ×2.3 in the two in-play ad breaks, ×3.3
  in post-match ads, ×8.6 in the half-time ad block; CV ×1.3 / ×2 / ×7.6.
  "Roughly triples" is right for W-per-step in short breaks and
  post-match ads; the half-time ad block is far busier, and the CV
  increase in a 1-min break is smaller (×1.3) because 6 samples at 10 s
  barely resolve it. Extra-time play is itself 2× busier than
  regulation play (the figure's "play itself busier").
- **Other sets, half-time ads-only band vs play:** STJ 8K step 48 vs
  7 W (×7), CV 17 vs 2.6 %; TP Sammy 7.6 vs 1.3 W (×5.8), CV 10.5 vs
  1.6 %; plasma 24 vs 14 W (×1.7), CV 16 vs 10 % (noisy in play). The
  French in-play ad-break windows show nothing on the UK sets (8K CV
  1.2 %, TP Sammy 0.9 %) — different feed, different schedule, as
  expected; they are not a null.
- **Status after the re-run:** 🟡 → **🟢 within this match for the
  Samsung on the logged feed** (every logged break, every direction
  agrees; n = 15 samples in the clean in-play breaks is the limit);
  🟡 across sets (half-time band only, lags unknown). Section 5.2 may now
  say "ad breaks" with the log as the basis; the number to quote is
  W-per-step ×2–3 in ad breaks (×8 across the half-time ad block),
  mean within −2 to −6 %. Numbers: `c3_f1_logged.csv` (GoS1).

### F2 — Cross-household alignment and the broadcast-latency figure

- **What the data gives:** best-fit lag between TV traces (10-s grid,
  ±600 s search). Final (S3): Ben Samsung (FR) vs STJ 8K (UK) r = 0.20
  at −360 s; vs TP Sammy r = 0.47 at +230 s; vs Stan plasma r = 0.09.
  Session S2: Ben old Samsung vs TP Sammy **r = 0.90 at −100 s**
  (r = 0.88 at ±10 s either side — the estimate is 100 ± 10 s), the only
  strong cross-device alignment in the campaign; STJ LG TV vs STJ 8K
  (same household) r = 0.17 at lag 0, 0.40 at +30 s.
- **On the "99-second France–UK latency gap":** not derivable from REM
  at 10-s cadence with the households as logged — the FR-vs-UK pairs on
  the final correlate weakly (r ≤ 0.2) and give lags of −360 s, not
  ~100 s; the one 100-s alignment (S2) is between two Samsungs whose
  countries and feeds are not recorded, during a recorded-playback
  session. The 99-s figure was presumably established another way
  (event timestamps, or Simon's 1-s lux trace against a French feed).
- **Status:** 🔴 Need More Data from GoS1's sources for the 99-s claim
  (cite it only if Ben/Simon can name the pair, the method and the
  sources of the two feeds); 🟡 for "power traces of the same live event
  align across households only after a lag search of minutes" (they do,
  weakly).

### F3 — The 8K prototype in UHD HDR: the luminance rule stops here (own finding)

- **What REM shows:** the 8K set drew **423 W mean on the final** (in-play
  block CV 1–2 %, min 112 W at a stall) against **301 W** on the July
  hackathon (SDR 1080p entertainment) and 330 W in S2 — a +40 %
  absolute step consistent with an HDR/UHD picture mode, though the
  mode is not logged. Within a session its trace correlates with the
  co-located LG TV at only r = 0.17 (S2, lag 0), where in the hackathon
  the same panel correlated r = 0.92–1.00 with its own runs on SDR
  content — i.e. on SDR entertainment the 8K tracked luminance like
  every other panel; on the football sessions it does not track the
  other panels.
- **On "power and luminance essentially uncorrelated (r ≈ 0.1)":** that
  coefficient needs the lux trace (Simon's ESP lux meter at the final)
  against the 8K power trace; the lux data is not in REM or on GoS1.
  The bench cannot confirm or refute it; the co-located-panel proxy
  (r = 0.17) is consistent with it but is not the same measurement.
- **Why it matters (unchanged):** an LCD panel with a full-array
  backlight held at HDR peak spends its power in the backlight
  regardless of scene luminance — the luminance-dominance finding of C4
  is a property of panels that dim with content (OLED, local-dimming
  LCD), not a law. The 8K case is the boundary of the rule, found by the
  same instrument.
- **Status:** 🟡 Early Insight for "absolute draw +40 % in the football
  sessions vs SDR, and no visible luminance tracking on that panel"
  (n = 1 device, mode unlogged); 🔴 for the numeric r ≈ 0.1 until the
  lux trace is on file and the correlation re-run. Panel facts needed
  for the paper: make/model, picture mode, HDR format, whether the
  broadcast was UHD HDR at the set.
- **Panel facts, supplied 2026-08-27 by S. T. Jones (owner of the set)
  as review comments on the cf7e8cd review copy:** the set is a Samsung
  Q800 8K 65" QLED (his suggestion: name the model rather than call it
  a prototype), and it viewed the final on BBC iPlayer with the UHD HDR
  stream selected. Picture mode and HDR format at the set remain
  unlogged. Recorded here 2026-08-29 (MacBook, from the review round,
  not a measurement).

### F4 — Fixed-draw sets and dead channels (validity screen)

- BHL TCL 45 (47 W ± 0.3), Roku 65" (87 W ± 0.5), Arian TV in S2
  (75 W ± 3) are flat throughout — standby/menu or a pinned backlight,
  not football; three group TVs were off (0 W) on the final. The same
  blind-device screen as C4 applies; only 4 of 10 group TVs carry
  content-driven data on the final.
- **Status:** 🟢 (it is the data).

## 4. Anomalies and open questions

- ~~Ad-break log exists — on the desk, not on GoS1~~ ✅ recovered to
  `runs/worldcup-final-2026-07-19/events.csv` and F1 re-run 2026-08-25
  (amendment above). Original note kept:
- **Ad-break log (as first noted):**
  a precise ad log for the final was supplied to the desk session that
  did the original analysis. F1's break band here is a data-driven
  stand-in; the desk should re-run F1 against that log (in-play vs
  ad-break blocks, same CV / W-per-step statistics, same grid CSV) and
  the "×3" then becomes a logged-ad-break number rather than a half-time
  number. The bench could not access the log.
- **Missing from GoS1 (needed to close F2/F3):** Simon's lux-meter trace
  (final), the match/broadcaster/feed per household per session, the 8K
  panel's make/mode/HDR state, and whoever computed 99 s and r ≈ 0.1 —
  their method. These are desk/owner items, not bench runs.
- No experiment annotations were made (REM supports them): future field
  campaigns should stamp kick-off, half-time and ad breaks live.
- "Three selected matches": the experiment description says matches;
  the DB shows three sessions, one of which (S2, weekday 15:31 UTC) is
  recorded playback with no cross-household alignment except one pair.
  Section 5.2's "during three World Cup broadcasts" should read "three
  REM sessions (two live broadcasts, one recorded playback)".
- ~~TP Sammy's country~~ ✅ resolved by the desk 2026-08-25: TP Sammy
  is a UK set, the plasma is in Canada (six recording devices, four
  markets: FR Samsung, UK 8K + TP Sammy + Roku, CA plasma, US TCL).
- A bench follow-up that would make F3 a measurement rather than an
  observation is already queued: R9 (OLED brightness sweep) plus an
  HDR-mode arm on the C2 with the panel metered.

## 5. Figure manifest

- `figures/fig_c3_final_bands.png` — the final's four content-reactive
  traces (10 s / 1 W) with the logged advertising / studio bands (French
  feed) shaded; kick-off and final whistle marked. Command (GoS1, repo
  root): `/srv/data/owl/figures-venv/bin/python figures/make_c3_final_figure.py`
  (reads `grid_2026-07-19.csv` on GoS1 + `runs/worldcup-final-2026-07-19/events.csv`).

## 6. Provenance

- Raw (exported 2026-08-25 from the REM production DB on Linode,
  `gos_rem`): `/srv/data/owl/worldcup-2026-07/power_{2026-06-26,
  2026-07-07,2026-07-19}_all.csv` (all aliases, session ± margin) and
  the 10-s grids `grid_<date>.csv`; REM admin state
  (`experiments.json`, `annotations.json`, `device_groups.json`,
  `device_registry.json`) read from the `stats-admin` container.
- Analysis scripts (alongside the raw): `wc_analysis.py`,
  `wc_timeline.py`, `c3c4_numbers.py`, `c3_f1_logged.py` (+ `c3_f1_logged.csv`)
  (`/srv/data/owl/worldcup-2026-07/`).
- Analysis date: 2026-08-25.
