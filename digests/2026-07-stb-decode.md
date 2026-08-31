# Digest — STB Decode Campaign (codec, content, delivery mode, July 2026)

Campaign C6. Derived from the GoS1 draft report
`~/wattlab/docs/stb_decode_energy_2026-07.md` (analysis 2026-07-27,
untracked on GoS1, lab review pending; interactive charts at
`/srv/data/owl/stb-decode-2026-07/results/stb_decode_report.html`).
This digest restructures that report to DIGEST_SPEC and adds no numbers
of its own. All statuses are proposed pending lab review.

## 1. Campaign metadata

- **Dates:** July 2026 (report dated 2026-07-27).
- **Device:** Google TV Streamer ("Office TV", 192.168.1.126),
  MediaTek fixed-function hardware decoders
  (`c2.mtk.avc/hevc/av1.decoder`), decoder use logcat-verified.
- **Capture:** dedicated Tapo P110, local mW API path, fw 1.4.6
  (1.5 s cadence). Device-total W during playback (see scope for why
  not ΔW).
- **Player:** Just Player (media3) driven via ADB — one pipeline for
  all codecs. Chosen because the Cast Default Media Receiver cannot
  decode AV1 on this box (audio-only fallback).
- **Content:** BBB (60 fps animation, 4–8 Mb/s), Meridian (60 fps
  film, 3–4.5 Mb/s), Kranjska MTB (30 fps sports, 11–13 Mb/s).
  1080p matched-VMAF (~92–93) NVENC encodes at the S53 parity
  operating points, served from GoS1 over LAN Wi-Fi.
- **Codecs:** H.264, HEVC, AV1.
- **Rounds:** 6-min files (burst-buffered playback, radio mostly idle)
  and 20-min files (sustained rolling-buffer streaming). 24 runs total.

## 2. Scope statement

Device layer only: the set-top box itself. The monitor is metered
separately and excluded; network and CDN energy excluded; datacentre
and production boundaries excluded. Ordered comparisons use
device-total W, not ΔW, because the box's home-screen baseline drifts
0.9–1.4 W between runs (ΔW per run is recorded for magnitude context
only). One box, three 1080p contents, one rung per codec — no claim
beyond this panel. No amortised training cost included. Encode-side
comparisons (F5) cite bench figures for ratio context only; codec
energy analysis belongs to #4941.

## 3. Findings

All 24 runs green on OWL's per-run confidence model. Significance:
Welch t on 30 s block means (autocorrelation-honest). Campaign-level
Traffic Light per finding below.

### F1 — Decode is nearly flat across codecs on fixed-function silicon

- **Claim:** largest within-content codec difference is 0.08 W (~4%).
  AV1 is consistently cheapest by a hair — bitrate-driven, not
  compute-driven. Content moves the needle more than codec (0.29 W
  spread across contents).
- **Status:** 🟢 Repeatable within this panel — ordering
  av1 ≤ h265 ≤ h264 replicated in both rounds for all three contents
  (24 runs); 20-min round significant for BBB pairs (h264 vs av1
  p≈7×10⁻⁶) and Meridian h264 vs both (p≈5×10⁻⁸, 4×10⁻¹⁰); Kranjska
  pairs ns. 🟡 Early Insight beyond it: one box, one chipset (RUN_QUEUE
  R3).
- **Confounds:** matched-VMAF rung means bitrate co-varies with codec;
  Meridian rows carry no audio-decode cost (see §4).

### F2 — Bitrate barely registers at the device

- **Claim:** Kranjska carries 2–3× Meridian's bits for ~0.1 W more.
- **Status:** 🟢 Repeatable within this panel (both rounds, all
  codecs); 🟡 beyond it (single box, 1080p only).
- **Confounds:** content differs in more than bitrate (frame rate,
  complexity); this is an across-content observation, not a controlled
  bitrate sweep.

### F3 — Delivery mode outweighs codec choice by 5–14×

- **Claim:** sustained rolling-buffer streaming (20-min files) sits
  +0.33–0.48 W (mean +0.42 W) above burst-buffered playback of the
  same content and codec (6-min files). Codec choice moves ≤0.08 W;
  delivery mode moves 5–14× that.
- **Status:** 🟢 Repeatable within this panel — nine content×codec
  pairs, all in the same direction; mechanism verified (server TCP
  counters show continuous ~stream-rate delivery in the sustained
  case). 🟡 beyond it: single box and player; part of the premium is
  not yet attributed (F4, §4).
- **Confounds:** window length and a first-run tooltip overlay differ
  between rounds (see §4); both are candidates for the non-network
  share of the premium.

### F4 — Sustained-premium decomposition: network alone is +0.21 W

- **Claim:** back-to-back on the same clip (bbb_h264 20-min): local
  file 2.029 W / 1.4 MB Wi-Fi RX vs sustained HTTP 2.237 W / 2,545 MB
  RX. Network delivery alone accounts for +0.21 W (~10%); the HTTP arm
  reproduces the earlier round value (2.235 W) almost exactly. The
  remaining ~0.14 W of the 20-vs-6-min premium is not network.
- **Status:** 🟡 Early Insight — n=1 per arm; the cross-check against
  the earlier round supports it but the residual is unattributed.
- **Confounds:** candidates for the residual are window length and the
  first-run overlay (§4).

### F5 — Encode:decode ratio (context for the per-viewer argument)

- **Claim:** for the same 2 min of video, bench GPU encode costs
  1.9–4.0× one device decode; CPU encode 6.2–22.7×. Encoding is
  amortised across the audience; decode is paid per viewer-hour.
- **Status:** 🟡 Early Insight — heterogeneous comparison (bench
  encode vs one device's decode); ratio ranges depend on encoder
  implementation and operating point.
- **Note:** encode-side numbers are #4941 territory; confirm cite-vs-
  report with Tania before this appears in Section 5 (outline open
  item).

## 4. Anomalies and open questions

- **Q1 — media3 fetched ~2.1× the file size** in the sustained-HTTP
  arm (2,545 MB for a 1,221 MB file). Possible double-fetch or
  buffer-discard behaviour; the `:8123` Range-request defect
  (200/full-body to ranged GETs, demonstrated to break
  ffmpeg-over-HTTP) is the prime suspect. Needs its own experiment
  before claiming; would be a player-efficiency finding, not a codec
  one.
- **Q2 — Non-network share of the sustained premium (~0.14 W)**
  unattributed. Candidates: window length, first-run overlay.
  Resolving run: repeat with overlay suppressed (force-stop + grants,
  no `pm clear`) and matched windows.
- **Q3 — First-run tooltip overlay** re-triggered by the 20-min
  protocol's per-run app reset in all nine runs (screenshot-verified,
  identical composition — codec comparisons unaffected). Protocol fix
  as Q2.
- **Q4 — Kranjska 20-min logcat ring wrapped:** h264/av1 decoder
  provenance captured mid-run (screenshots and excerpts in results
  dir); h265 inferred, not verified.
- **Q5 — Meridian's 5.1-AAC re-encode is silent on this box** (PCE
  quirk) — its rows carry no audio-decode cost. Affects cross-content
  comparisons that include audio.
- **Q6 — Second chipset needed** before any generalisation beyond this
  box (RUN_QUEUE R3). A 2-min cast round exists but is context-only
  (window-truncation bug).
- One discarded 20-min attempt (permission stall after app reset left
  a UI screen, not decode); excluded and documented.

## 5. Figure manifest

No figures exported to `figures/` yet. Interactive charts exist in
`stb_decode_report.html` on GoS1 (path in provenance); export candidates
for Section 5 (device-total W by codec/content/round; sustained-vs-burst
premium chart) should be regenerated on GoS1 with commands recorded here.

## 6. Provenance

- Raw data: GoS1 `/srv/data/owl/stb-decode-2026-07/` — `streams/` (all
  encodes), `results/` (per-round JSON with raw 1.5 s samples,
  `analysis_summary.json`, harness scripts, provenance screenshots,
  source report).
- Source report: `stb_decode_energy_2026-07.md` (2026-07-27, untracked
  on GoS1, lab review pending).
- Digest prepared 2026-08-08 on the writing desk from the report text
  only (no raw-data access).
