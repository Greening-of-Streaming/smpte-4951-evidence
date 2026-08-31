# Digest — VP9 iso-bitrate re-run: encode operating points + four-codec decode (C17)

Overnight campaign 2026-08-17→18 on GoS1 + the decode rig, run in response
to the VP9 LinkedIn discussion (Thierry Fautier's speed dial, Jan Ozer's
"software vs software" and everything-at-slow set, Tania's iso-bitrate ask).
Source report: wattlab `docs/vp9_oneoff_2026-08.md` §5 (+ analysis in
`docs/vp9_rerun_2026-08-17/`). This digest restructures that report to
DIGEST_SPEC and adds no numbers of its own.

## 1. Campaign metadata

- **Dates:** 2026-08-17 → 18 (overnight, two sequenced campaigns).
- **Encode bench:** GoS1 (AMD Ryzen 9 7900, 24 cores), parity harness,
  dual Tapo P110 (ci2 per-meter combine), focus mode, VMAF v1 (3d0h)
  scored post-hoc outside the energy window. 30 s 1080p trims of
  `bbb_120s` (high complexity) and `meridian_120s` (low), one-pass ABR
  at 2500/5000 kb/s, pinned GOP 120, AAC 128k, **n=3 per cell, reps not
  adjacent**. Software encoders only: libx264 (medium/slow), libx265
  (medium/slow), SVT-AV1 (preset 10 default / preset 3), libvpx-VP9
  (good, row-mt, 3 tile-cols, 16 threads; cpu-used 4/2/1).
- **Decode rig:** protocol v3 (stable-idle guard, 20-sample baseline,
  PLAYING gate, mid-window screenshot, trace-flat liveness), headless
  realtime playback, **1080 s windows**, five devices in parallel
  (parallel validated, C11 F10), n=2 (n=3 for H.264 and VP9).
  Devices: Google TV Streamer (MediaTek hw, Ethernet), Fire TV Stick 4K
  (MT8696 hw, Wi-Fi only), Bbox Bouygtel4K (operator CPE), Pi 400
  (BCM2711, all four codecs in software), LG C2 (webOS native, panel
  metered — context only).
- **Decode content — iso-bitrate loop family:** per content ONE bitrate
  for all four codecs (BBB 1080p60 @8 Mb/s, Kranjska 1440×1080p30
  @10 Mb/s, Meridian 1080p60 @4.5 Mb/s), software encoders at
  production points (x264 medium, x265 medium, SVT-AV1 preset 6,
  libvpx cpu-used 2), two-pass ABR, GOP 120, silent audio, 120 s cuts
  concatenated ×10 into 20-min loops. VP9 ships as WebM (MP4/vp09
  stalls the Google TV player). Clip VMAF v1 at these bitrates: BBB
  97.9/98.2/98.3/98.5 (H.264/HEVC/AV1/VP9), Kranjska
  90.5/87.0/87.0/89.2, Meridian 93.3/93.7/92.7/91.1 — broadly
  comparable quality, VP9 never the worst on the ProRes-sourced
  contents.

## 2. Scope statement

Device layer only, GoS1 server (encode) and the named client devices
(decode); network/CDN/datacentre/production boundaries excluded; no
amortised training cost. One server, five client devices, 1080p, one-pass
ABR on the encode side — **a first indication with repeats, not a
lab-reviewed finding**. Carried verbatim from the report (§5.3):

> Say: the software-encode cost of VP9 depends on the operating point more
> than on the codec — at defaults it is the dearest of the four on a
> 24-core server, at an everything-slow setting SVT-AV1 is; on hardware
> clients VP9 decode is energy-neutral vs H.264/HEVC/AV1 at matched bits;
> where decode falls back to software VP9 is the cheapest of the four and
> HEVC the dearest.
> Not say: any iso-bitrate *quality* ranking from the encode rows; any
> hardware-vs-software "×15" as a codec property; anything about
> distribution energy; anything from the C2 or the Bbox beyond "software
> AV1".

⚠ **#4941 boundary:** the encode-side Wh figures below sit on the
companion-paper boundary (codec energy analysis is Tania's paper).
Measured and reported freely here; any use in #4951 prose needs the
cite-vs-report check with Tania first (outline open item).

## 3. Findings

### F1 — The operating point decides which "new" codec is the expensive one (encode)

- **Claim:** at everyone's defaults (x264 medium · x265 medium · SVT-AV1
  p10 · VP9 cpu-used 4) VP9 is the outlier at ~4.6–4.9× x264 per minute
  of output (x265 ~2×, SVT-AV1 1.0–1.5×). At Jan Ozer's everything-slow
  set (x264 slow · x265 slow · SVT-AV1 p3 · VP9 cpu-used 2) VP9 is NOT
  the outlier: SVT-AV1 preset 3 costs 9.5–10.8× x264 (~2× VP9's
  4.6–5.0×), x265 slow 3.6–4.0×.
- **Status:** 🟢 Repeatable within this panel — n=3 per cell, sd ≤5 %,
  all rows green; two rows excluded for elevated baseline (documented,
  §4). 🟡 beyond it: one server, two 30 s trims, one-pass ABR at two
  bitrates.
- **Key stats:** Wh per minute of output (marginal; attributional ≈
  ×2.2, ratios unchanged): x264 medium 0.30–0.39 · x265 medium
  0.62–0.77 · SVT-AV1 p10 0.36–0.48 · VP9 cpu-used 4 1.37–1.96 · x265
  slow 1.33–2.10 · VP9 cpu-used 2 1.76–2.58 · SVT-AV1 p3 3.74–5.61.
  libvpx's dial is short: cpu-used 4→1 spans 1.7× energy for ~+0.5
  VMAF; its fastest useful multithreaded point already costs more than
  x265 slow. Direction agrees with Jan's i9-14900 ladder (x264 far
  cheapest, rest a large multiple); magnitudes differ (thread scaling,
  one-pass vs two-pass, fixed-bitrate vs per-title hull) — neither set
  is "the" ratio → that cross-comparison 🟡.
- **Confounds:** one-pass ABR missed targets by −32 % to +46 %
  (achieved bitrates recorded per row) — energy ratios stand, but **no
  iso-bitrate quality claim** from the encode rows.

### F2 — On a saturated CPU, time is energy (method)

- **Claim:** ΔW was 65–71 W on every software encode row regardless of
  encoder, so energy-per-minute ratios equal wall-clock ratios; a
  timing ladder is a fair proxy for marginal encode energy on a
  dedicated box. The attributional lens multiplies every row ~2.2× and
  leaves ratios unchanged.
- **Status:** 🟢 within this panel (36 cells, n=3). Method point for
  the paper's marginal-vs-attributional discussion.

### F3 — With a hardware decoder, VP9 costs what the other three cost

- **Claim:** GTV (`c2.mtk.vp9.decoder` allocated on every VP9 row) and
  Fire TV Stick: VP9 inside the ±0.1 W four-codec spread on all three
  contents at iso-bitrate; per-run 95 % CIs (±0.05–0.20 W) overlap.
  GTV means, BBB/Kranjska/Meridian: VP9 +0.58/+0.30/+0.57 W vs H.264
  +0.59/+0.29/+0.53 W.
- **Status:** 🟢 within this panel (n=2–3 per cell, all valid rows
  green); 🟡 beyond it (two MediaTek-family boxes; Fire TV emits no
  decoder provenance — its VP9 level is *consistent with* hardware
  decode, not logcat-proven).
- **Confounds:** Fire TV is Wi-Fi-only — its device-total W carries a
  radio share the Ethernet boxes don't (state next to cross-device
  comparisons; cf. C18 netpath campaign).

### F4 — Where decode falls back to software, VP9 is the cheapest of the four

- **Claim:** Pi 400, all four codecs in software, ΔW above idle: VP9
  +1.13/+1.15/+1.19 W across the three contents, tied with or below
  H.264 (+1.08–1.42), AV1 +1.45–1.82, HEVC +2.41–3.25 W (HEVC 2–3×
  VP9). Replicates the 08-09 BBB-only ordering at iso-bitrate.
- **Status:** 🟢 within this panel (n=2–3); 🟡 generality (one software
  board, one player pipeline).

### F5 — Content moves the hardware-decode number ~2× (method)

- **Claim:** GTV: BBB ~+0.58 W vs Kranjska ~+0.30 W at iso-bitrate —
  any per-hour client decode figure that ignores content is quoting one
  clip. Sibling of C5 F5's regime point: content and regime must be
  stated for a decode-energy claim to be interpretable.
- **Status:** 🟢 within this panel (consistent across all four codecs
  and both hw boxes).

### F6 — Operator box corroboration (context)

- **Claim:** Bbox 4K: AV1 +1.2 W on every content (software AV1, no hw
  path listed); H.264/HEVC/VP9 inside its idle drift (🔴/🟡) — no
  ranking claimable. Corroborates C11 F11's "codec-not-in-silicon =
  expensive" with a fourth codec panel.
- **Status:** 🟡 (AV1 leg consistent but the flat legs are below the
  box's idle drift by construction).

## 4. Anomalies and open questions

- **Fire TV `alive_at_window_end` false negative:** the end-of-window
  liveness probe returned False on rows whose power trace is flat to
  the last second — instrumented (`playback_state_at_end` recorded per
  row), root cause open in wattlab. Three rows where the trace really
  dropped or the player was PAUSED are excluded and documented.
- **Encode target misses** (one-pass ABR, 30 s trims): −32 % (SVT-AV1
  Meridian) to +46 % (libvpx BBB). Resolving run: CRF/two-pass sweep if
  an iso-bitrate quality ranking is ever needed (not queued — out of
  paper scope).
- **Two encode rows excluded** for elevated baseline (w_base > median
  +10 W): meridian VP9 cpu-used 2 2500k rep 2; meridian x264 slow 2500k
  rep 3. Hot baselines under-count ΔW.
- **C2 rows are panel-dominated** (BBB +16 W, Kranjska/Meridian ≈0 or
  negative — OLED draws by picture, not codec) — context only, not a
  decode measurement (C11 F8 unchanged).

## 5. Figure manifest

None generated for this digest. The report's tables are the citable
artefact; if Section 5 needs a figure, the encode-ratio bars
(defaults vs everything-slow) can be generated on GoS1 from
`encode_parity_nvenc_24c_2026-08-17.json` — request via RUN_QUEUE.

## 6. Provenance

- Raw encode rows: GoS1
  `results/diagnostics/encode_parity_nvenc_24c_2026-08-17.json`
  (108 rows, raw samples included).
- Decode envelopes: GoS1 `results/decode/2026-08-1[78]_*.json`, batch
  `20260817b9c0de` (campaign page `/decode/batch/20260817b9c0de`).
- Analysis scripts + clip manifest:
  `/srv/data/owl/campaign_2026-08-17_vp9b/` and wattlab
  `docs/vp9_rerun_2026-08-17/` (analysis 2026-08-18).
- Narrative source: wattlab `docs/vp9_oneoff_2026-08.md` §5
  (report status: stays a report until the LinkedIn discussion
  settles; Tania checked, Ben posting).
- Digest produced 2026-08-24 on GoS1.
