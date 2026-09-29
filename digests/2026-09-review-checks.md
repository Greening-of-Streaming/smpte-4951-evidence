# Digest — Review checks on the shortened draft: accounting lenses, codec intervals, Figure 7 frame rates, figure provenance, fact checks (2026-09-30)

Two external reviews of the shortened draft (Tania's revision of V1.0)
raised technical points that need numbers from the raw store. This
digest answers them. Most items recompute stored samples; no new rig
time was used (item 7 had no reference meter to use).

Items 1 and 2 decide wording in the abstract and Section 3:
- **Item 1, accounting lenses.** "Leaves every ratio between encoders
  unchanged" (`drafts/03-owl.md`) is **false as written**.
  - Attribution multiplies each row by 1 + W_base/ΔW, so ratios move
    wherever ΔW differs.
  - On this host, ratios among CPU encoders move by at most 8 % and no
    CPU ranking changes.
  - Ratios between CPU and NVENC move by up to 24 %. CPU stays the
    dearer path at every matched codec and bitrate.
- **Item 2, codec intervals.** "About 0.1 W or less" (abstract) holds as
  the **observed range** of point estimates under hardware decode: the
  largest is 0.107 W, on the W5. It does **not** hold as an upper bound.
  - At n=2–3 per cell the 95 % Welch intervals reach 0.27 W (GTV, n=3)
    and 0.56 W (Fire TV, n=2).
  - Only 13 of 37 hardware pairs have their whole interval inside
    ±0.1 W.

## 1. Campaign metadata

- **Date of analysis:** 2026-09-30 on GoS1.
  - smpte-4951 at `daa1eed` before this digest.
  - wattlab at `d242579`.
- **Type:** desk recomputation over stored results. There was no new
  measurement. The only live action was one read-only
  `get_device_info()` per P110 (item 5d). It ran after confirming no
  measurement lock, an empty queue and no campaign process.
- **Encode rows (item 1):** GoS1 host, Ryzen 9 7900 + RTX 5080, dual
  P110 at 1 s.
  - **S53 + VP9 parity set:**
    - `results/calibration/encode_parity_nvenc_24c_2026-06-20_plus_ext.json`:
      240 rows, n=1 per cell. It holds the 207 S53 rows from 2026-06-20
      and 33 extension rows from 2026-08-28.
    - `results/diagnostics/encode_parity_nvenc_24c_2026-08-09.json`:
      4 VP9 rows, n=1.
    - Codecs: x264, x265 and SVT-AV1 on the CPU. NVENC H.264, HEVC
      and AV1 in `gpu_baseline` and `gpu_tuned` (p7 / hq / 2-pass).
    - Clips: Meridian, BBB and Kranjska, 30 s trims.
    - Rungs: the 1080p bitrate sweep and a 4-rung ladder.
  - **C17 preset sweep:** `results/diagnostics/encode_parity_nvenc_24c_2026-08-17.json`.
    - 108 rows = 9 codec×preset arms × 2 clips × 2 bitrates, n=3.
    - CPU only: x264, x265, SVT-AV1 and libvpx-vp9 at default, slow
      and slower.
  - **R14 preset ladder (C21):** `/srv/data/owl/campaign_2026-08-29_tier3/r14/stage_b_results.jsonl`.
    - 18 rows = 6 arms × n=3.
    - x264 ultrafast / medium / veryslow and SVT-AV1 p12 / p8 / p4,
      all on BBB at a fixed CRF per codec.
  - None of the C17 or R14 rows is NVENC. The only NVENC rows in these
    sets are S53's.
- **Decode rows (item 2):** OWL client rig, protocol v3, P110 at 1 s mW.
  One row is one run; ΔW is taken over that run's own 20 s idle
  baseline.

  | Set | Batch | Devices × codecs | Content | Rows |
  |---|---|---|---|---|
  | C25 F1 (screen arm) | `20260927d1a6` | GTV H.264/HEVC/AV1; Bbox H.264/HEVC | Meridian 1080p59.94 | n=3 per cell |
  | C27 F1 | `3e54b322a9b4` | W5 H.264/HEVC/VP9 | BBB iso 1080p60 8 Mb/s | n=3 |
  | C17 F3 | `20260817b9c0de` | GTV, Fire TV × H.264/HEVC/AV1/VP9 | BBB, Kranjska, Meridian, iso-bitrate | n=1–3 |
  | C11 F7 (contrast) | 2026-07-31 + 2026-08-01 `loop_*` rows | Pi 5 software, H.264/HEVC/AV1 | three families | n=2–7 |
  | C24 amendment (contrast) | `20260927e7e5` | Apple TV (A10X) H.264/AV1/VP9 | BBB iso, **absolute task W** as in the digest | n=3 |
  | C26 (contrast) | `20260927c26b` | Bbox AV1 vs H.264 at 720p30 / 1080p30 | Meridian | n=3 |

  The C17 validity rule is the campaign's own
  (`campaign_2026-08-17_vp9b/analyze_night.py`): mid-window PLAYING,
  and a flat trace rescues the Fire TV's false `alive=False` flag. It
  excludes 3 Fire TV rows (jobs `0649ef79`, `4da1e7d8`, `b4d1476c`).

## 2. Scope statement

Device layer only.
- Item 1 covers the GoS1 encode host's wall power.
- Item 2 covers the decode client's wall power, which includes the box
  and excludes the display, except where a row's sink is noted.

Network, CDN, CPE upstream of the client, datacentre and production are
excluded. The encode-side numbers in item 1 sit on the #4941 boundary.
This digest reports the lens arithmetic, not the encode findings, so
the cite-vs-report rule for encode figures still applies.

The attributional lens charges the whole wall draw while a job
occupies the box. It is an accounting choice, not a measurement: it
uses the same samples as the marginal figure.

The meters' absolute accuracy is untested (item 7). Every figure here
depends on P110 agreement, not on a reference instrument.

## 3. Findings

### R1 — Attribution does not leave encoder ratios unchanged; a narrower statement holds

- **Claim.** Under the attributional lens every row is multiplied by
  m = (W_base + ΔW)/ΔW. A ratio between two rows therefore shifts by
  m_a/m_b and is unchanged only when the two rows draw the same ΔW.
  - Clean-baseline CPU rows are near-saturated (ΔW 62–75 W), so m is
    nearly constant: ×2.08–2.28. Ratios among CPU encoders move by at
    most 8 %, and no ranking with a marginal gap above 5 % changes.
  - NVENC rows draw 44–80 W (`gpu_tuned` 44–55 W), so m = ×1.99–2.79.
    CPU/NVENC ratios move by −24 % to +10 %.
- **Numbers.** "Clean" means a row baseline below 84 W, i.e. less than
  5 W above the 79 W floor. Five cells are hot; see Confounds.

  | Set | Cells (clean) | n per cell | Multiplier m | Max shift of any within-set ratio |
  |---|---|---|---|---|
  | S53+VP9, CPU | 94 | 1 | 2.10–2.28 | 8.4 % |
  | S53, NVENC `gpu_baseline` | 92 | 1 | 1.99–2.74 | — |
  | S53, NVENC `gpu_tuned` | 56 | 1 | 2.43–2.79 | — |
  | S53+VP9, all encoders | 242 | 1 | 1.99–2.79 | 40 % (bound) |
  | C17, CPU | 34 | 3 | 2.10–2.24 | 6.8 % |
  | R14, CPU | 5 | 3 | 2.08–2.12 | 2.1 % |

  - **Same-codec, same-bitrate CPU vs NVENC pairs** (the S53 F4
    comparison):
    - CPU/`gpu_baseline`: 1.16–11.07× marginal → 1.23–11.18×
      attributional, shift −19 % … +10 % (90 pairs).
    - CPU/`gpu_tuned`: 1.30–4.87× → 1.12–3.94×, shift −24 % … −10 %
      (54 pairs).
    - Order flips: **0**. CPU is dearer at every matched codec and
      bitrate under both lenses.
  - **Rank changes:**
    - Among CPU encoders: none with a marginal gap above 5 %, in any
      set. There is one C17 flip at a 1 % near-tie: Meridian 2.5 Mb/s,
      x265 slow vs VP9 default, 1.011× → 0.994×.
    - Across codec and bitrate, NVENC rows (mostly `gpu_tuned`) swap
      order with CPU rows whose marginal cost differs by up to about
      30 %. Example:
      Meridian H.264 CPU at 8 Mb/s costs 0.466 Wh/min marginal, NVENC
      HEVC tuned at 8.5 Mb/s costs 0.374. Attributional: 0.995 vs
      1.003.
    - There are 37 (BBB), 30 (Kranjska) and 19 (Meridian) such flips
      with a marginal gap above 5 %, per the script. All involve an
      NVENC row: 84 are CPU vs NVENC and 2 are NVENC vs NVENC.
  - **Row-baseline vs nominal 79 W:** on the rows that store W_base,
    the maximum shift is C17 14.0 % → 9.8 % and R14 6.5 % → 3.8 %. The
    extra comes from the hot rows.
- **Sentence the data supports:** "The attributional view roughly
  doubles every encode figure on this host (×2.1–2.3 on CPU rows,
  ×2.0–2.8 on NVENC rows). Ratios among CPU encoders move by at most
  8 % and no CPU ranking changes; ratios between CPU and NVENC
  encoders move by up to a quarter, though CPU stays the dearer path
  at every matched codec and bitrate."
  - Shorter form for §3: "which on this host roughly doubles encode
    figures, moves ratios among CPU encoders by under 10 % and those
    between CPU and NVENC by up to 25 %."
- **Traffic Light:**
  - 🟢 Repeatable for the mechanism and the CPU bound. It is
    arithmetic on stored rows, and C17 and R14 give n=3 per cell with
    all rows 🟢 per run.
  - 🟡 Early Insight for the S53 magnitudes: n=1 per cell, and most
    S53 rows use the nominal 79 W, not a measured W_base.
- **Confounds:**
  - **Hot baselines.** Five cells have W_base ≥ 84 W: S53 Meridian
    HEVC-CPU 8.5 Mb/s (86.4); S53 Kranjska AV1-CPU 13 Mb/s (103.6,
    m = 3.71); C17 Meridian 2.5 Mb/s x264 slow (85.4) and VP9 slow
    (86.3); R14 x264 ultrafast (84.3, rep 1).
    - A hot baseline under-counts the **marginal** figure.
    - The attributional sum W_base + ΔW is the measured task draw and
      does not depend on the baseline.
    - So the largest raw shifts are a marginal-side bias, not a lens
      effect. This is why the table reports clean cells.
  - **Nominal W_base.** The 79 W on pre-2026-08-15 rows is the
    display-blanked floor. On an active display (about 101 W) m rises
    for every row, and the ratio shifts grow roughly in proportion.
  - **Design differences.** S53 uses codec-specific bitrate grids, so
    same-bitrate codec pairs are few. The set-wide bound max(m)/min(m)
    covers every pair regardless.
  - **OWL_OVERVIEW.md is mislabelled.** Its "×2.1–2.7 on CPU rows"
    pairs the CPU lower bound with the NVENC-tuned upper bound. The
    wattlab commit `79045ab` message ("ratios stay ~12–17×") also
    shows the ratio moving.

### R2 — Codec-to-codec decode differences: "about 0.1 W or less" is an observed range, not a bound

- **Claim.** Under hardware decode (C25 F1, C27 F1, C17 F3; 37 codec
  pairs across 5 boxes and 3 content families):
  - The largest point estimate is **+0.107 W**: W5 H.264 − HEVC,
    95 % CI [+0.042, +0.172], Welch df 3.3.
  - The largest 95 % upper bound is **0.27 W at n=3**: C25 GTV AV1 −
    H.264, −0.041 W [−0.273, +0.192], df 2.6.
  - At n=2 the bound reaches **0.56 W**: C17 Fire TV Meridian AV1 −
    HEVC, −0.068 [−0.561, +0.425], df 1.4.
  - Only 13 of 37 pairs have the whole interval inside ±0.1 W. Three
    exclude zero:
    - W5 H.264 − HEVC +0.107;
    - W5 H.264 − VP9 +0.103 [+0.015, +0.191];
    - Fire TV Kranjska AV1 − H.264 −0.082 [−0.160, −0.004].
  - In software the same comparison runs from 0.19 W to 2.0 W.
- **Numbers.** Hardware-covered set, all n=3 per cell (full table,
  including C17, in the CSV):

  | Device / content | Pair | Diff (W) | 95 % CI | df |
  |---|---|---|---|---|
  | GTV / Meridian (C25) | AV1 − H.264 | −0.041 | [−0.273, +0.192] | 2.6 |
  | GTV / Meridian (C25) | AV1 − HEVC | −0.079 | [−0.170, +0.013] | 4.0 |
  | GTV / Meridian (C25) | H.264 − HEVC | −0.038 | [−0.272, +0.196] | 2.5 |
  | Bbox / Meridian (C25) | H.264 − HEVC | +0.082 | [−0.006, +0.169] | 3.2 |
  | W5 / BBB (C27) | H.264 − HEVC | +0.107 | [+0.042, +0.172] | 3.3 |
  | W5 / BBB (C27) | H.264 − VP9 | +0.103 | [+0.015, +0.191] | 2.8 |
  | W5 / BBB (C27) | HEVC − VP9 | −0.004 | [−0.091, +0.083] | 3.7 |

  - **C17 F3** (GTV and Fire TV, 30 pairs with intervals):
    - |point| ≤ 0.090 W; |CI| ≤ 0.237 W on the GTV and ≤ 0.561 W on
      the Fire TV.
    - 12 of 30 intervals lie inside ±0.1 W.
    - Six more Fire TV pairs have n=1 on one side and no CI.
  - **Software contrast:**

    | Device | Pair(s) | Diff (W) | 95 % CI | n | df |
    |---|---|---|---|---|---|
    | Pi 5 (C11 F7) | HEVC − H.264 | +1.04 … +1.10 | e.g. BBB [+0.93, +1.22] | 2–7 per cell | — |
    | Pi 5 (C11 F7) | AV1 − H.264 | +0.19 … +0.57 | Meridian [−0.64, +1.02] | 2 vs 6 | 1.2 |
    | Apple TV (C24 amendment, absolute W) | AV1 − H.264 | +1.221 | [+0.984, +1.458] | 3 | — |
    | Apple TV (C24 amendment, absolute W) | VP9 − H.264 | +1.110 | [+0.901, +1.319] | 3 | — |
    | Apple TV (C24 amendment, absolute W) | AV1 − VP9 | +0.111 | [−0.127, +0.350] | 3 | — |
    | Bbox 720p30 (C26) | AV1 − H.264 | +1.586 | [+1.549, +1.624] | 3 | 2.7 |
    | Bbox 1080p30 (C26) | AV1 − H.264 | +2.006 | [+1.934, +2.079] | 3 | — |

    - The Pi 5 Meridian AV1 − H.264 interval spans zero.
    - At 1080p30 the Bbox AV1 plays at 14–17 of 30 frames per second,
      a failed playback. It is shown for scale only.
- **n needed to bound the difference below 0.1 W at 95 %.** Take equal
  n per cell and the observed pooled sd, and require
  |d̂| + t·s_p·√(2/n) < 0.1 W.
  - If the true difference were zero, most C17 and W5 pairs (s_p
    0.02–0.04 W) would already need only **n = 2–3**. The C25 GTV
    pairs (s_p 0.081 W, driven by one H.264 rep at 0.344 against
    0.53) need **n = 7**.
  - At the **observed** differences, n rises to 15–30 for the C25
    pairs: GTV 15–29, Bbox 30.
  - For W5 H.264 vs HEVC/VP9 the difference **cannot be bounded below
    0.1 W at any n**, because the point estimate is already ≥ 0.1 W.
  - Rule of thumb: n ≈ 2·(t·s/(0.1 − |d|))² per cell. With
    s ≈ 0.04 W and |d| ≈ 0.05 W, that is about 6–8 per cell.
- **Sentence the data supports:** "Where a hardware block covers the
  codec, the codec-to-codec differences we measured were at most about
  0.1 W (largest 0.11 W, W5; n = 3 per cell). At that n the 95 %
  intervals reach ±0.27 W, so this is the observed range, not a bound.
  In software, the codec moves decode power by 0.2 to 1.6 W, or the
  stream fails to play in real time."
  - The per-run Traffic Light flag tests only "above idle" and is not
    a codec-difference test. §3/§4 should not imply that the green
    flags bound the codec spread.
- **Traffic Light:**
  - 🟢 Repeatable for the observed range: point estimates ≤ 0.11 W,
    n=3 per cell in C25/C27 and n=2–3 in C17, 5 boxes, all valid rows
    🟢 per run except one 🟡 (C25 Bbox HEVC).
  - 🔴 Need More Data for "≤ 0.1 W" read as an upper bound.
  - 🟢 for the W5's resolvable spread (C27 F1 unchanged).
- **Confounds:**
  - **Content.** C25 is Meridian, C27 is BBB, C17 has three families.
    Content moves the hardware level about 2× (C17 F5), so compare
    codec differences within a device and content, never across.
  - **Fire TV.** It is Wi-Fi only, so its rows carry a radio share,
    and its decoder is not logcat-proven (C17 F3).
  - **Pi 5 cells** mix 2026-07-31 and 2026-08-01 rows, headless
    software decode. The Meridian AV1/HEVC cells are n=2.
  - **Apple TV** figures are absolute task W, as in its digest,
    because the tvOS idle swing makes ΔW unusable. Two of its nine
    rows carry a 🟡 or a swung baseline.
  - **Per-run SE is optimistic by about √2** on the boxes: about half
    of the 1 s samples are repeats (R6). This does not affect the
    Welch intervals, which use between-run spread.

### R3 — Figure 7 and the fps wording: the counter counts frames presented, capped by a 50 Hz output

- **Claim.** The Bbox composes at **50 Hz** (compositor vsync period
  20.0 ms). The presented-fps counter counts **distinct frames that
  reached the screen per second** on the player's surface: the
  non-zero actual-present timestamps of the last ~127 latched buffers,
  as (n−1)/span. It is therefore capped at the refresh rate. It is not
  the output rate (repeats are not recounted) and not decoded source
  frames (dropped frames never appear).
  - Healthy 59.94 fps rows read **50.0**.
  - Healthy 30 fps rows read **30.0**.
  - AV1 on Meridian 1080p59.94 reads **~5**.
- **Numbers** (Bbox, Meridian; 24–25 SurfaceFlinger samples per row):

  | Cell | Rows | Row means (fps) | Sample range |
  |---|---|---|---|
  | C25 H.264 1080p59.94 | 3 | 49.9 / 50.0 / 50.0 | 49.2–50.0 |
  | C25 HEVC 1080p59.94 | 3 | 50.0 ×3 | 50.0–50.0 |
  | C25 AV1 1080p59.94, screen | 3 | 4.99 / 5.04 / 4.97 | 4.6–5.2 |
  | C25 AV1 1080p59.94, headless | 3 | 4.89 / 5.00 / 4.89 | 4.3–5.3 |
  | C26 H.264 720p30 | 3 | 29.95 / 29.98 / 29.96 | 29.9–30.1 |
  | C26 AV1 720p30 | 3 | 29.86 / 29.97 / 29.92 | 29.4–30.3 |
  | C26 H.264 1080p30 | 3 | 29.98 / 29.98 / 30.01 | 29.9–30.1 |
  | C26 AV1 1080p30 (in window) | 3 | **16.6 / 14.4 / 14.7** | 9.3–24.0 |

  - An independent probe corroborates the 50 Hz ceiling. The
    2026-09-27 e2e pilot's SurfaceFlinger `--timestats` put every Bbox
    60 fps arm at averageFPS 50.3–51.5 (about 20 rows), against 62.5 on
    the GTV, Fire TV and Xiaomi Gen 3 (60 Hz), and every 30 fps arm at
    30.1–30.2.
  - "14–17" is the **in-window** row-mean range. Including the lead-in
    and tail it is 13.2–15.2.
- **Wording:**
  - **Figure 7 annotation** (`figures/make_c25_figures.py:109`,
    currently "plays at ~5 fps (output 50 fps)"): "software decode —
    presents ~5 of 59.94 frames/s". Optionally add "(hardware codecs
    present 50/s, the ceiling of the box's 50 Hz output)".
  - **Caption:** "presenting about 5 of the content's 59.94 frames per
    second, where hardware decode presents 50 (the box's 50 Hz
    output)".
    - The revision's "5 frames/s from 60 fps content" is correct.
    - V1.0's "about 5 frames per second against 50" is correct only if
      "50" is read as what hardware decode achieves on this output.
      Neither caption should imply 50 fps content.
  - **30 fps:** "14 to 17 of 30 frames per second in the measurement
    window". The healthy 30 fps controls present 30.0, so 30 is the
    right denominator.
- **Traffic Light:**
  - 🟢 Repeatable for the counter's meaning and the values (n=3 rows
    per cell, 24 samples per row, two independent probe methods).
  - 🔴 for the HDMI link mode itself. It is inferred from the
    compositor and the presentation ceiling, never read from the link
    or the TV (CR-084 caveat).
- **Confounds:** a 60 Hz sink was not tried on the Bbox. Whether the
  box would output 60 Hz with frame-rate matching enabled is unknown.

### R4 — Figure provenance (paper figures 1–7)

Paper figure numbers follow `drafts/` at `daa1eed`, after `d1cd517`
renumbered them. "PNG commit" is the last commit that touched the PNG.

| Fig | File | Kind | What produces the committed PNG | PNG commit | Reproducible from repo? |
|---|---|---|---|---|---|
| 1 | `fig_measurement.png` | **Hand-authored SVG**, no data | `soffice --headless --convert-to pdf fig_measurement.svg && pdftoppm -r 600 -png -singlefile fig_measurement.pdf fig_measurement` (MacBook) | `d1f5442` | Render yes; content is hand-drawn |
| 2 | `fig_sequence.png` | **Hand-composed** from Simon Jones's slides 2–3 (`sources/2026-03_simon-jones_rem-tv-settings-v1.pptx`) | `sips` crops of Ben's slide exports → SVG with data-URI panels → `qlmanage -t -s 3000` → `sips -c 2535 3000` (MacBook; figures/README.md) | `ba97a67` | **No.** The slide exports are not in the repo; re-export from the .pptx |
| 3 | `fig_c8_dual_capture.png` | Data figure | GoS1: `/srv/data/owl/figures-venv/bin/python figures/make_c8_dual_capture_figure.py 75d7e183` | `e5ed641` | **Yes.** 1760×1520 at 160 dpi, the script's output |
| 4 | `fig_owl_architecture.png` | **Hand-authored SVG**, no data | Same soffice → pdftoppm -r 600 recipe (MacBook) | `c129ac7` | Render yes; content is hand-drawn |
| 5 | `fig_c11_f9_duration_v2.png` | Data figure, but the committed PNG is a render of a **hand-edited SVG** | `soffice … fig_c11_f9_duration_v2.svg && pdftoppm -r 300 …` (MacBook, 2026-09-28, text edits from Dom's review). Data generator: GoS1 `/srv/data/owl/figures-venv/bin/python figures/make_f9_rerun_figure.py` | `e8093e2` | **Not byte-for-byte.** The script writes 180 dpi (1368×738); the committed PNG is 300 dpi (2280×1230). Same data and wording per README |
| 6 | `fig_loop.png` | **Hand-authored SVG**; its evidence numbers are typed in | Same soffice → pdftoppm recipe (MacBook) | `c129ac7` | Render yes; its numbers must be checked by hand against the digests |
| 7 | `fig_c25_codec_matrix.png` | Data figure | MacBook: `python3 figures/make_c25_figures.py --csv digests/2026-09-c25-decode-rediag.csv`. GoS1 raw-store equivalent: `/srv/data/owl/figenv/bin/python figures/make_c25_figures.py` | `22c04e1` | **Yes.** The annotation text needs R3's fix |

- **No generating command from data:** Figures 1, 2, 4 and 6.
- **Status:** 🟢. Every mapping was checked against the drafts' image
  links and `git log`.

### R5 — Fact checks (one line each)

- **a. C18 F1, "Ethernet = local file": one box at n=3.** On the GTV,
  local +0.501 W vs Ethernet +0.520 W: +0.019 W, 95 % CI
  [−0.034, +0.073], df 3.96, n=3 each.
  - The Pi 400 has n=1 per cell, scattering ±0.1–0.2 W.
  - The Bbox has no local arm, and the Fire TV is Wi-Fi only.
  - 🟢 for the GTV; 🔴 as a multi-device statement.
- **b. C11 F2, Pi 400 arms: interleaved for reps 1–3,** in the order
  hw realtime → sw realtime → hw saturated → sw saturated (2026-08-08,
  23:11–23:55).
  - Hw realtime reps 4–6 were appended as a block (23:55–00:06).
  - The blocked reps (0.35–0.48 W) fall inside the interleaved range
    (0.33–0.51 W).
- **c. Idle guard: still skips a session's first run on the host; not
  fixed.**
  - `wattlab_service/queue_control.py::_pre_job_idle_guard` has no
    reference (`power.LAST_W_BASE` is `None`) for the first job after
    a service start. It was last changed in `e17db39` (2026-07-29).
  - Campaign scripts use a fixed 120 s settle before row 1
    (`campaign_2026-08-29_tier3/common.py`), which is a timed wait, not
    a floor check.
  - **The decode rig is covered on every run, including the first:**
    since wattlab `26158d1` it gates on each device's known idle
    floor.
  - The Xiaomi Gen 3 and Roku floors in `rig.py` are marked
    "UNMEASURED guess", and the C2-native entry has none, so it falls
    back to waiting for self-stability.
- **d. Plug firmware today (read live 2026-09-30): not all 1.3.1.**
  - Host inner meter: 1.3.1 Build 240621.
  - **Host outer meter: 1.4.0 Build 251020.**
  - All 11 rig plugs: 1.3.1 Build 240621.
  - The decode envelopes' `meter.fw: "1.3.1"` is a hard-coded literal
    (`wattlab_service/decode_run.py:1263`), not a reading from the
    plug.
- **e. C8 F2, "0.2 % at 1 s": exactly one run.** Job `a32764ff`: GTV
  on Lab-D, 587 s, LEM 1 s vs bench, 0.2755 vs 0.2760 Wh (−0.18 %),
  RMSE 0.023 W, offset +1 s.
  - Both readers poll the same P110, so this is agreement between read
    paths, not accuracy.
  - The simultaneous 1 s LEM capture on Lab-E was never paired or
    analysed.
  - The multi-run evidence is at 10 s: 7 LAN runs, −0.4 … −2.7 %.
  - 🟡 for the 1 s figure (n=1); 🟢 for the 10 s range.
- **f. Scaled host coefficients vs each device's own idle variance:**
  see R6.

### R6 — Client devices' own idle coefficients vs the scaled host coefficients (item 5f)

- **Claim.** This had never been checked. CONFIDENCE_MODEL.md: "a
  client device's noise shape has never been calibrated".
  - The rig (`decode_bench/bench.py:828`) applies the host's c_idle and
    c_drift as percentages of each device's W_base:
    - 2.38 % / 1.12 % for rows from 2026-07-07 to 09-04;
    - 2.46 % / 1.90 % from 09-05 onward.
    - Recomputing all 2,367 stored decode rows with these reproduces
      every stored flag.
  - Computed from each device's stored pre-run baselines, with the
    host calibration's own estimators:
    - **c_idle:** the scaled value is conservative where it binds
      (Bbox, C2, Roku). The per-run term already covers noisier
      devices.
    - **c_drift:** the additive term that nothing per-run covers. It
      is **2–4× optimistic** on the GTV, Fire TV, Pi 400 and C2, and
      **14–24×** on the Apple TV.
  - Re-flagging with device-own coefficients changes 127 of 2,367 rows
    (5.4 %): 118 down, 9 up. 91 rows lose 🟢, 49 of them Apple TV.
    **None of the 51 C25/C26/C27 rows changes flag.**
- **Numbers** (baselines are 20 × 1 s windows; c_drift is the median
  over batches with at least 4 baselines):

  | Device | Baselines | Median W_base | c_idle own | c_drift own |
  |---|---|---|---|---|
  | Bbox | 458 | 6.24 W | 1.79 % | 1.72 % |
  | Google TV | 429 | 1.33 W | 8.64 % | 4.20 % |
  | Fire TV | 294 | 1.45 W | 22.4 % | 4.10 % |
  | Apple TV | 248 | 3.22 W | 12.1 % | 26.6 % |
  | Pi 5 | 215 | 3.17 W | 4.19 % | 1.84 % |
  | Pi 400 | 168 | 3.25 W | 6.58 % | 2.78 % |
  | Xiaomi Gen 3 | 168 | 1.93 W | 5.46 % | 1.83 % |
  | Xiaomi Gen 2 | 125 | 2.04 W | 8.06 % | 2.23 % |
  | LG C2 (native) | 144 | 49.9 W | 1.46 % | 3.40 % |
  | Roku | 103 | 1.82 W | 1.99 % | 0.98 % |
  | W5 | 15 (1 batch) | 3.82 W | 3.09 % | 0.97 % |

  - In watts the drift floor is small. GTV: 4.2 % × 1.33 W = 0.056 W,
    against 0.015 W (07) or 0.025 W (09-05) scaled.
  - It matters only for margins of about 0.1 W.
- **Sentence the data supports:** "The client bench applies the host's
  calibrated coefficients, scaled to each device's baseline. Checked
  against 2,367 stored device baselines, the scaling is conservative
  for within-window noise, which the per-run term covers anyway. The
  between-window drift term is 2–4× optimistic on most boxes.
  Re-flagging with each device's own coefficients changes 5 % of
  per-run flags, mostly on the Apple TV, and none of the rows behind
  Section 4's decode figures (C25–C27)."
- **Traffic Light:** 🟡 Early Insight. n is large (≥ 100 baselines per
  device except the W5), but the windows are pre-run baselines, not a
  dedicated idle session, and they mix sinks, panel states and
  sessions.
- **Confounds:**
  - **Repeated samples.** 47–57 % of consecutive 1 s baseline samples
    on the boxes repeat exactly (C2 about 1 %); the plug refreshes
    about every 2 s at these loads.
    - The per-run SE uses the raw n, so it is **understated by about
      √2** on every box. That is a second optimistic bias, separate
      from the coefficients.
    - De-duplicating barely moves the CVs: GTV 8.6 → 9.2 %.
  - Baselines follow the previous run, so any residual tail inflates
    the device-own values.
  - Apple TV per-run 🟢 flags in C19/C24 do not survive device-own
    drift and should not be cited as per-run evidence. The C24
    amendment's absolute-watts gap, which uses between-rep sd, is
    unaffected.

### R7 — Reference meter (item 7): none available; not run

- There is no reference instrument (bench power analyser, Yokogawa,
  Fluke or similar) on GoS1 or the rig.
- The only other meter is the Shelly Plug PM Gen3 upstream of eight
  rig P110s. It is another consumer metering IC, reads the sum of
  eight plugs plus their self-consumption (4.9 W with every device
  off), and cannot isolate one 2–5 W load.
- Nothing was run. The 0.2 % (R5e) is therefore agreement between read
  paths only; absolute accuracy at 2–5 W is untested (§4).

### R8 — 2026-09-30 amendment: calibration provenance (host c_idle / c_drift)

Asked by the writing desk after R6. §3.2 says "thirty paired encode runs
on 17 July 2026 gave c_idle = 2.38% and c_drift = 1.12%" and that the
drift term "sets a floor of roughly 0.9 W on SE". Both are out of date.
Desk check on stored data; no rig time.

**R8a — Provenance of 2.46 % / 1.90 %: a routine calibration, same
protocol as July's.** 🟢 Repeatable (read from the records).
- Both values come from **step 0 of the in-app overnight benchmark**.
  The benchmark runs `video.run_variance_calibration`, which writes its
  result into `settings.json` and appends a line to
  `results/variance/history.jsonl`.
  - **July:** benchmark `e121c415`. Calibration 02:01–05:14 on
    **2026-07-07**, **30 pairs**, idle mean 75.59 W.
  - **September:** benchmark `591d63c9`. Calibration 01:54–04:03 on
    **2026-09-05**, **20 pairs**, idle mean 78.36 W.
  - Both nights used the same benchmark configuration (10 reps ×
    Meridian/BBB, then LLM, RAG and image compares) and the same
    kernel (6.17.0-35).
  - wattlab code: `owl_version` 8087d23 (09-05) against e70f808 (07-07),
    both dirty.
- **One calibration pair** = 5 × 1 s idle baseline, H.264 CPU encode of
  Meridian 4K, 50 s cooldown, 5 × 1 s baseline, HEVC NVENC encode.
  - **c_idle** is the mean within-window CV.
  - **c_drift** is the CV of the window means: 40 windows at 20 pairs,
    60 at 30. Only the summary survives; per-window samples are not
    persisted.
- **"17 July" is the git date, not the calibration date.** The 30-pair
  run is dated **7 July** in `history.jsonl` and in the benchmark
  record. wattlab `5027e76` (2026-07-17, "settings catch-up: 2026-07
  recalibration (n=30, cooldown 50s)") committed the values it had
  written.
- **The September values were never committed.** `settings.json` is
  live state; `git diff settings.json` shows 2.38 → 2.46,
  1.12 → 1.90 and `variance_runs` 30 → 20.
  - wattlab JOURNAL (Session 76, item 7) records it: "an automatic calibration
    ran 2026-09-05 04:03 … wrote itself in … left live per Tania".
  - The last commit touching the tracked values is still `5027e76`.
- **What triggered it:** the benchmark launched at 01:54 with the
  variance step enabled. Its pair count was 20 because `variance_runs`
  had been set to 20 through the /settings slider.
  - The records don't say who set it or when.
  - Nothing marks the run as a deliberate recalibration, a warm-room
    run or a manual edit.
- **Conditions:**
  - **GPU:** RTX 5080 on both nights.
  - **Display:** blanked on both nights. The idle means of 75.6 and
    78.4 W match the display-blanked ~79 W floor, not the ~101 W
    active-display level.
  - **Location:** GoS1 has been in the basement since 06-19.
  - **Ambient:** not logged (see R8e).

**R8b — What is live, and which coefficients made each stored flag.**
🟢 for the decode rows (recomputed); 🟡 for the encode rows (assigned
by date).
- **One object.** The host encode paths (`video.py:612`,
  `parity.py:376`) and the rig (`decode_bench/bench.py:828`) all call
  `confidence()` without settings. It then does `cfg.load()`, reading
  the live `settings.json` **at the time of each run**.
  - Today every path uses **2.46 % / 1.90 %**.
  - A stored flag carries whatever was live when its row ran. Nothing
    re-flags old rows after a recalibration.
- Coefficients behind each cited campaign:

  | Rows | Run dates | Coefficients (c_idle / c_drift) | How established |
  |---|---|---|---|
  | S53 artifact (06-20 rows) | 2026-06-20 | 2.44 / 1.35 (calibration 06-20 05:07) | by date; parity rows keep no raw samples |
  | S53 extension rows | 2026-08-28 | 2.38 / 1.12 | by date |
  | VP9 parity rows | 2026-08-09 | 2.38 / 1.12 | by date |
  | C17 encode + decode | 2026-08-17/18 | 2.38 / 1.12 | decode: recompute reproduces every stored flag |
  | R14 (C21) | 2026-08-29/30 | 2.38 / 1.12 | by date |
  | C11 F9 re-run (Figure 5) | 2026-08-24 | 2.38 / 1.12 | recompute reproduces every stored flag |
  | C27 (W5 + GTV comparator) | 2026-09-21/22 | **2.46 / 1.90** | recompute reproduces every stored flag |
  | C25, C26 | 2026-09-27 | **2.46 / 1.90** | recompute reproduces every stored flag |

  - The decode check is C28 R6's recompute of all 2,367 stored rows;
    it also holds for the subsets here.
  - The S53 06-18 artifact (not cited) would carry 2.18 / 1.25.

**R8c — The numbers §3.2 needs (current calibration).**
🟢 arithmetic; 🟡 for the value of c_drift itself (one calibration; see
R8e for how much it varies).
- **Current calibration:**
  - c_idle **2.46 %**, c_drift **1.90 %**;
  - 20 pairs (40 idle windows of 5 × 1 s);
  - 2026-09-05;
  - calibration idle mean **78.4 W, display blanked**.
- **The host idle level to quote** is the display-blanked one: "about
  79 W" or "78 W". That is the state of the calibration runs and of
  every overnight campaign. 101 W applies only with an active desktop
  display, which no cited measurement used.
- **SE floor and threshold.** The floor is c_drift × W_base / 100. The
  ΔW needed for p⁺ ≥ 0.95 at any duration is 1.645 × the floor.

  | Calibration | W_base | SE_drift floor | ΔW for p⁺ ≥ 0.95 at any duration |
  |---|---|---|---|
  | September (current) | 78.4 W | **1.49 W** | **2.45 W** |
  | September (current) | 79 W | 1.50 W | 2.47 W |
  | July (in the paper) | 75.6 W | 0.85 W | 1.39 W |
  | July (in the paper) | 79 W | 0.88 W | 1.46 W |
  | Either, active display | 101 W | 1.13 / 1.92 W | 1.86 / 3.16 W |

  - This is a floor. p⁺ ≥ 0.95 also needs SE_cal or SE_run on top, so
    the real threshold is somewhat higher.
  - Every stored encode row clears it by a wide margin (R8d).

**R8d — Does any claim move? No; two Figure 5 markers would change.**
🟢 Repeatable (the rows were recomputed with wattlab's own
`confidence()`).
- **C11 F9 re-run (Figure 5)**, 20 plotted rows re-flagged under the
  September coefficients:
  - 18 unchanged.
  - **Two Fire TV rows go 🟢 → 🟡:**
    - 20 min, ΔW +0.124 W, p⁺ 0.957 → 0.937 (job `7f195277`);
    - 59 min, ΔW +0.144 W, p⁺ 0.953 → 0.936 (job `a7dff199`).
  - Every Pi 5 and GTV marker is unchanged.
  - **The figure's statement holds and is, if anything, sharper.**
    "A clear signal is confident within seconds" rests on the Pi 5 and
    GTV rows. "A margin near 0.1 W flickers at every length" is exactly
    what the two Fire TV markers do, and under September's values they
    flicker amber at 20 and 59 min.
  - The committed figure plots the stored (July-era) flags. If it is
    redrawn under current coefficients, those two filled markers become
    open.
- **C25–C27:** these rows were **flagged with the current
  coefficients** in the first place.
  - Recomputing reproduces every stored flag, so **no flag changes
    under the host's current values**. C28 R6 found none under
    device-own values either.
  - Under the older July values one row would be 🟢 rather than 🟡:
    C25 Bbox HEVC, +0.200 W, job `42ab84d2`, p⁺ 0.979 vs 0.916.
- **C17 decode (145 rows):** 5 flags would drop under September's
  values.
  - Three Bbox 🟡 → 🔴 (+0.095 to +0.113 W).
  - One Bbox 🟢 → 🟡 (+0.215 W).
  - One C2 🟢 → 🟡 (+1.427 W on a ~50 W panel).
  - None is in C17 F3's GTV/Fire TV hardware set, so R2 is unaffected.
- **Encode rows** (S53, VP9, C17 parity, R14; 370 rows): the September
  drift term, added in full to each stored SE, leaves the lowest p⁺ at
  **0.996** (the hot-baseline S53 Kranjska AV1-CPU row, ΔW 38.3 W). No
  encode flag can change.

**R8e — Ambient: 1.90 % is not a warm-room figure on any available
evidence; it is calibration-to-calibration spread.** 🟡 Early Insight
(no ambient sensor; proxies only).
- **No room temperature is logged.** Two proxies from the same nights,
  taken from the 20 video jobs each benchmark ran right after its
  calibration:
  - **Idle temperatures match:** CPU Tctl median 66.0 °C (July) vs
    65.8 °C (September), GPU 51 vs 50 °C.
  - **An independent estimate reverses the order.** Clean baselines
    only (under floor + 4 W; 96 and 92 windows) give:

    | Night | c_idle | c_drift |
    |---|---|---|
    | July | 2.90 % | 1.75 % |
    | September | 2.49 % | 1.36 % |

    The September night was no noisier than July's on this measure; if
    anything it was quieter.
- **The spread across calibrations.** Six calibrations on the current
  host (RTX 5080, from 2026-05-30):

  | Date | c_drift | Pairs |
  |---|---|---|
  | 2026-05-30 | 1.01 % | 12 |
  | 2026-06-10 | 1.03 % | 20 |
  | 2026-06-11 | 1.25 % | 20 |
  | 2026-06-20 | 1.35 % | 20 |
  | 2026-07-07 | 1.12 % | 30 |
  | 2026-09-05 | 1.90 % | 20 |

  - c_idle runs 1.84–2.46 % over the same six.
  - A CV estimated from 40 autocorrelated window means is a noisy
    statistic. 1.90 % is the top of that range, not an outlier from
    another regime.
- **The warm-room example needs correcting.**
  - "3.92 % against 1.10 % clean" is the 2026-05-29 03:28 calibration.
    It was taken on the **AMD RX 7800 XT host** (idle mean 59 W), the
    night after the heat-wave run that carries the record's only
    explicit ambient note (2026-05-28: 4.40 %, "Paris heat wave;
    server room ~+10 % warmer").
  - wattlab JOURNAL also calls the 05-29 run "the warm-ambient 3.07 %
    recalibration" (3.07 % is its `variance_pct`).
  - **No calibration reads 1.10 %.** The nearest are 1.01 % (05-30,
    RTX era) and 1.12 % (07-07).
  - The pair therefore spans a GPU swap as well as a room-temperature
    change. It illustrates ambient sensitivity, but not like-for-like.
  - Like-for-like would be "4.40 % in a May 2026 heat wave against
    1.0–1.4 % under normal ambient". The hardware differs, and it
    should be labelled.
- **Which value the paper should quote as the calibration:** the
  **current** one, **2.46 % / 1.90 % (20 pairs, 5 September 2026)**.
  - It is live, and it produced the flags on C25–C27, the rows the
    paper's central claims rest on.
  - Nothing marks it as ambient-inflated.
  - The July value remains true of the rows flagged before 09-05 (C11
    F9, C17, R14), so it belongs in the text as the earlier
    calibration, not as the current one.
- **Sentence the data supports (replaces both quoted §3.2 sentences):**
  "The host is calibrated by paired encode runs during an overnight
  benchmark; the current calibration (20 pairs, 5 September 2026,
  idle about 78 W with the display blanked) gives c_idle = 2.46% and
  c_drift = 1.90%. The earlier one (30 pairs, 7 July) gave 2.38% and
  1.12%, and flagged the rows measured before September; across six
  calibrations since June, c_drift has ranged from 1.0% to 1.9%. The
  drift term does not shrink with longer runs: on the host it sets a
  floor of about 1.5 W on SE, so a run must draw about 2.5 W above idle
  before it can be confident at any duration."
  - If §3.2 must stay short, the minimum fix is: "c_idle = 2.46% and
    c_drift = 1.90% (20 paired encode runs, 5 September 2026) … sets a
    floor of roughly 1.5 W on SE".
- **Side note for wattlab (not the paper):** the comment in
  `video.py` (`run_variance_calibration`) still calls
  `variance_idle_drift_pct` "diagnostic, not consumed by the confidence
  flag". It has been consumed since CR-028 phase 2 (`confidence.py`
  line 118). The comment is stale; the code is right.

## 4. Anomalies and open questions

**What the draft should change (the data does not support the current
wording):**

1. **`drafts/03-owl.md` §"Two accounting lenses"**: "leaves every ratio
   between encoders unchanged" is false. Use R1's sentence. Also,
   "roughly doubles CPU encode figures" is correct (×2.1–2.3), but
   NVENC rows are multiplied by 2.0–2.8 too, so "roughly doubles
   encode figures" is the accurate form.
2. **`OWL_OVERVIEW.md` lines 85–88**: "attribution ×2.1–2.7 on CPU
   rows … ratios between encoders are unchanged under either lens" is
   wrong on both counts. The CPU range is ×2.1–2.3; 2.7 belongs to
   NVENC `gpu_tuned`. The platform-facts file feeds the writing desk,
   so it should be corrected there.
3. **Abstract, "codec choice moves decode power by about 0.1 W or
   less"**: supported as an observed range only (R2). If the sentence
   stays, it needs "measured" and the n. It must not read as a bound;
   the 95 % intervals reach ±0.27 W at n=3.
4. **Figure 7 annotation** (`make_c25_figures.py:109`) and both
   captions: use R3's wording. "(output 50 fps)" invites a reader to
   take the content as 50 fps. The 14–17 figure needs "in the
   measurement window".
5. **"0.2 % at 1 s"** in the abstract, §4 (about line 34) and the
   conclusion ("one instrument scale within 0.2 %"):
   - It is n=1 (one run, one plug, one GTV).
   - It is read-path agreement, not accuracy (R5e, R7).
   - 02-rem.md already says "(one run)"; the other three places do
     not.
6. **`drafts/03-owl.md` line ~36**: "the chain is pinned to plug
   firmware 1.3.1, since later firmware removes that protocol". Today
   the host's **outer** meter runs **1.4.0 Build 251020** and
   answered a local `get_device_info()` read this morning. As
   observed, local access survives 1.4.0 on this unit; what 1.4.0
   changes is the refresh (about 1.5 s, so about a third of 1 s polls
   are repeats; CR-065 records). The same "locks out local polling"
   claim is in OWL_OVERVIEW.md line 63. Unresolved: whether a later
   build than 251020 removes local access. A precise sentence would
   be: "one of the two host meters is on 1.4.0, which refreshes about
   every 1.5 s; the 1-s samples it returns are about one-third
   repeats."
7. **`drafts/03-owl.md` idle-guard sentence** ("it does not yet cover a
   session's first run [C15, C21]") is true for the **host**. Scope it
   to the host/encode path. The decode rig gates every run on a
   per-device floor (R5c).
8. **C18 "Ethernet ≈ local file"**: one box (GTV) at n=3. "On the same
   box" (singular) is right; do not widen it. "Nothing measurable"
   means < 0.07 W at 95 %.
9. **Apple TV per-run flags**: per-run 🟢s in C19/C24 are not citable
   as per-run evidence under device-own drift (R6). The absolute-watts
   gap stands.

**Open questions and what would resolve them:**

10. **Codec bound below 0.1 W.** Rerun the C25 GTV/Bbox cells at n=7–8
    per codec, interleaved (see R2's n table). This would turn the
    observed range into a bound on the MT8696 and Marvell. It is not
    queued; it needs about 2 h of rig time.
11. **Absolute accuracy.** It needs a reference meter (a bench power
    analyser) in series with one P110 at 2–5 W during playback. The
    lab owns none. Until then the paper can claim read-path agreement
    and consistency, not accuracy.
12. **Bbox HDMI link rate.** It is inferred at 50 Hz, never read.
    Read it from the C2's input info panel (Ben at the TV, about one
    minute), and try frame-rate matching once to see whether 1080p60
    AV1 presents more than 5 fps at 60 Hz.
13. **Duplicate 1 s samples (R6).** The per-run SE on boxes is
    understated by about √2. A wattlab-side fix would de-duplicate or
    use n_eff in `confidence.py`. It does not move the digests'
    finding-level statuses, which rest on between-run spread; it
    matters for per-run flags near threshold.
14. **Device calibration.** A dedicated idle session per box (20 idle
    windows, one sitting), as the host has, would replace R6's
    opportunistic estimate. Only the Apple TV, Fire TV and GTV
    materially need it.
15. **Host first-run guard.** Persisting `LAST_W_BASE` across service
    restarts, or waiting for a stored floor, would close R5c for the
    host. This is a wattlab-side code change, noted here rather than
    queued.
16. **Figure 5 reproducibility.** The committed PNG is a 300 dpi
    render of a hand-edited SVG. Either the script should emit the
    same text at 300 dpi, or figures/README should state the SVG as
    the source. figures/README's 09-28 heading still calls it
    "Figure 6".
17. **Evidence repo sync (item 6): pushed 2026-09-30 after Ben's
    confirmation** (public `66c82f8`); the R8 amendment, its script and
    the re-rendered Figure 7 followed in public `9528da8`. As first
    prepared:
    - Scratch clone commit on top of public `2067f82`; 25 files,
      +2164/−31. It carries C25–C27, the C24 and C11 F1 amendments,
      RESULTS_INDEX, figures/README, all seven paper figures, and this
      digest plus its index entry once they are final.
    - Scrub: no IPs, MACs, emails, serials, SSIDs, credentials or
      /home paths.
      - Raw-store `/srv/data/owl/...` paths and the first names Ben,
        Dom and Simon are kept, per the pack's precedent.
      - The new CSVs are summary rows only.
    - Decisions for Ben: keep or drop the retired figures in the pack,
      and whether to ship the `analysis/` scripts, which the pack has
      never carried.

## 5. Figure manifest

No new figures. R4 records the provenance of the paper's seven
figures. The Figure 7 annotation fix is text only
(`figures/make_c25_figures.py:109`). It is for the writing desk to
apply and re-render, not done here.

## 6. Provenance

- **Scripts (smpte-4951 `analysis/`, added with this digest):**
  - `review_lens_ratios.py`: R1.
    `python3 analysis/review_lens_ratios.py --csv digests/2026-09-review-checks-lens.csv`
  - `review_codec_diffs.py`: R2 (needs scipy; system python3 on GoS1).
    `python3 analysis/review_codec_diffs.py --csv digests/2026-09-review-checks.csv`
  - `device_idle_coeffs.py`: R6. It imports
    `wattlab_service/confidence.py` at wattlab `d242579`.
    `python3 analysis/device_idle_coeffs.py --json /tmp/device_idle_coeffs.json`
- **R3 fps:**
  - `python3 analysis/c25_rediag_summary.py`
  - `python3 analysis/c26_summary.py` (in-window row means)
  - Raw samples in `/srv/data/owl/campaign_2026-09-27_{rediag,c26}/fps.jsonl`
  - Independent probe: `grep bbox /srv/data/owl/campaign_2026-09-27_e2e_pilot/fps_probes.log`
  - Counter implementation: `bbox_fps()` in
    `analysis/c25_rediag_feeder.py` / `c26_bbox_rungs_feeder.py`
- **R5a:** `/srv/data/owl/campaign_2026-08-18_netpath/netpath_cells.json`
  (keys `…|local|…`, `…|eth…`).
- **R5b:** `grep -E "submitting|START" /srv/data/owl/campaign_2026-08-08_r6/campaign.log`;
  per-row values are in `/srv/data/owl/campaign_2026-08-08_r6/results.jsonl`.
- **R5c:**
  - wattlab `queue_control.py` (`1bf87d6` CR-070, `e17db39`);
    `git log --since=2026-08-09 -- wattlab_service/{queue_control,power,idle_wait}.py`
    is empty.
  - Rig: `26158d1`, `decode_run.py:643–644`, `decode_bench/bench.py:725–744`.
- **R5d:** one read-only tapo `ApiClient(...).p110(ip).get_device_info().fw_ver`
  per plug, 2026-09-30, queue idle. The hard-coded field is at
  `wattlab_service/decode_run.py:1263`.
- **R5e:** `grep -n -A11 a32764ff /srv/data/owl/r2-dual-capture/r2_analysis_output.txt`
  (from `/srv/data/owl/r2-dual-capture/r2_analysis.py`).
- **Raw stores:**
  - Decode envelopes: `/srv/data/owl/results/decode/{date}_{job}.json`.
  - Encode artifacts: wattlab `results/{calibration,diagnostics}/` (GoS1).
  - R14: `/srv/data/owl/campaign_2026-08-29_tier3/r14/`.
  - Host coefficient history: `results/variance/history.jsonl`.
- **Summary CSVs:**
  - `digests/2026-09-review-checks.csv`: R2, one row per codec pair,
    with n, diff, CI, df, pooled sd and n needed.
  - `digests/2026-09-review-checks-lens.csv`: R1, one row per encoder
    cell, with n, W_base source, ΔW, marginal, attributional and the
    multiplier.
- **R8 (amendment):** `python3 analysis/c28_r8_calibration.py`. It prints
  the calibration history, the two nights re-estimated from their
  benchmark video jobs, the decode re-flags (July vs September), the
  encode-row bound and the §3.2 numbers.
  - Records: `results/variance/history.jsonl`;
    `results/benchmark/2026-07-07_e121c415.json`, `…/2026-09-05_591d63c9.json`;
    `git -C ~/wattlab diff settings.json`; `git -C ~/wattlab show 5027e76 --stat`.
  - Code: `wattlab_service/video.py` `run_variance_calibration`,
    `wattlab_service/confidence.py` (`cfg.load()` when no settings are
    passed).
- **Analysis date:** 2026-09-30 (R8 the same day, after `c994579`).
