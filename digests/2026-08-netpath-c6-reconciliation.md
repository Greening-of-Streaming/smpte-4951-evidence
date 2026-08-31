# Digest — Network-path campaign + C6 delivery-mode reconciliation (C18)

Two things in one short digest: (a) the CR-074 connection-method campaign
(wattlab `docs/netpath_2026-08-18/`, 2026-08-18→19) as a paper-citable
campaign entry, and (b) the requested reconciliation of C6's headline
"delivery mode outweighs codec by 5–14×" against it (gap-fill handoff
2026-08-24, Task 2). **Desk-pass outcome: the discrepancy does not survive
— the two campaigns measured different arms and agree where they overlap.
No new bench cells were needed.** Which C6 numbers remain citable: §3 F4.

## 1. Campaign metadata (C18 half)

- **Dates:** 2026-08-18 → 19. Batch `20260818ae7ba7b0` (62 jobs:
  16 overnight + 14 Ethernet repeats + 32 daytime Wi-Fi arms).
- **Devices:** Google TV Streamer (hw decode; Ethernet AND Wi-Fi arms —
  cable pulled on-site 2026-08-19), Bbox Bouygtel4K (same two arms),
  Fire TV Stick 4K (Wi-Fi only), Pi 400 (software decode; Ethernet /
  Wi-Fi / local / radio-off by `nmcli` per run). C2 not switchable.
- **Capture:** decode rig protocol v3, 600 s windows, headless realtime,
  per-device Tapo P110 at 1 s, PLAYING gate + mid-window screenshot +
  trace-flat liveness; keep_awake pinned (post-`fec0065` era).
- **Content:** ONE clip family — BBB 1080p60 H.264 (hw-decoded on every
  STB, sw on the Pi) at 1.5 / 8 / 20 Mb/s.
- **Arms:** burst = plain HTTP from the CR-072 **Range-correct** origin
  (player buffers ahead as it likes); paced = origin caps delivery at
  1.25× clip rate (`?pace_kbps=`, live-edge approximation); local = file
  on device, no network.
- **n:** GTV/Bbox 3 per interface (one GTV Wi-Fi cell n=2, PAUSED start
  excluded); Fire TV 2; Pi 400 1 (local n=2).

## 2. Scope statement

Device layer only: client device wall power above idle. One content
family, one codec, one rig / one router / one room — a Wi-Fi premium is a
link property (distance, band, power-save), not a device constant.
Network infrastructure energy itself excluded. Bbox Ethernet rows sit
inside its idle drift (🔴/🟡 per row) — only the Ethernet↔Wi-Fi
*difference* is claimed there.

## 3. Findings

### F1 — Ethernet delivery costs nothing measurable on the client

- **Claim:** GTV local file +0.50 ± 0.02 W vs Ethernet HTTP +0.52 ± 0.02 W
  (8 Mb/s, n=3); Pi 400 Ethernet ≈ local across bitrates; Pi with Wi-Fi
  radio OFF ≈ radio on (1.39 vs 1.37 W) — an idle radio is also free.
- **Status:** 🟢 within panel (GTV n=3); Pi legs 🟡 (n=1).

### F2 — Wi-Fi costs every device more, by very different amounts

- **Claim:** while playing, Wi-Fi vs Ethernet: GTV +0.21 W average
  (+0.16 at 1.5 → +0.30 at 20 Mb/s, n=3); Bbox +0.98 W, ~flat across
  bitrate (largest single network effect on the rig); Pi 400 +0.32 W
  average, strongly bitrate-dependent; Fire TV (vs its local file)
  +0.1 → +0.35 W. Across the three dual-interface devices: Ethernet
  0.68 W → Wi-Fi 1.19 W average, **+0.50 W (+75 %)**.
- **Status:** 🟢 within panel for GTV/Bbox (n=3 both interfaces);
  🟡 Fire TV (n=2, local-file proxy for Ethernet) and Pi (n=1);
  🟡 as any device-level generalisation (one link, one room).
- **Confounds:** link-dependent by nature; Bbox premium unexplained
  (§4).

### F3 — Paced ("live-like") vs burst delivery: no consistent difference

- **Claim:** at n=3 on the STBs the origin-paced arm sits within noise
  of burst (GTV ±0.03 W, Bbox +0.0–0.07 W); on the Pi, pacing is weak
  by construction (`ffmpeg -re` already reads ~1×).
- **Status:** 🟢 within panel (GTV/Bbox n=3). Directly relevant to C6
  reconciliation below.

### F4 — C6 reconciliation: what "+0.42 W sustained vs burst, 5–14×" was, and what survives

- **Desk-pass finding (arm audit, no new measurement):** C6's July arms
  and C18's arms are not the same experiment.
  - C6 "burst" = a **6-min file** over **Wi-Fi** from the pre-CR-072
    origin, which ignored Range requests and pushed the full body — the
    player buffered the whole file early and the radio idled for most
    of the window. C6 "sustained" = a **20-min file**, rolling buffer,
    radio active all window — *plus* media3 fetching ~2.1× the file
    bytes (C6 Q1, the Range defect since fixed by CR-072), *plus* the
    first-run tooltip overlay on all nine sustained rows (C6 Q3), and
    a window-length difference between rounds. So C6 F3 compared
    radio-active vs radio-idle **plus an artefact stack**, on Wi-Fi.
  - C18 burst-vs-paced compares two radio-active deliveries of the
    same 20-min file on a Range-correct origin — pacing, not duty
    cycle. Its null (F3 above) does not contradict C6; it removes
    "pacing" as the explanation of C6's premium.
  - **Where the campaigns overlap they agree,** three ways to ~+0.2 W
    on the GTV: C6 F4 local-vs-HTTP over Wi-Fi = +0.21 W; C18 Wi-Fi
    average premium = +0.21 W; C18 Wi-Fi burst 8 Mb/s (+0.70) vs local
    (+0.50) = +0.20 W.
- **Verdict — what remains citable from C6:**
  - **F1 codec flatness (≤0.08 W)** — citable, unaffected;
    corroborated since by C11 F7 and C17 F3.
  - **F2 bitrate** — citable in its cross-content form; C18's
    controlled sweep refines it (GTV +0.41→+0.58 W from 1.5→20 Mb/s —
    bitrate does move an STB measurably, demux/decode work, even on
    Ethernet).
  - **F3 "delivery mode outweighs codec by 5–14×" — RETIRED as
    stated.** The premium conflated Wi-Fi radio duty cycle with an
    origin-defect over-fetch and an overlay; its arms cannot be
    reconstructed on the fixed origin, and the pacing half of "delivery
    mode" is a measured null (C18 F3). The defensible successor claim:
    **connection method outweighs codec choice** — the Wi-Fi-active
    share (GTV +0.21 W avg; Bbox +0.98 W; Pi +0.32; Fire TV +0.1–0.35)
    is 2.5–12× the ≤0.08 W codec spread, while Ethernet delivery is
    free. Section 5's frozen sentence should be redrafted in this form.
  - **F4 network share +0.21 W** — citable and upgraded: reproduced at
    n=3 (C18), but relabel it **Wi-Fi-active share**, not "network
    delivery" generically (Ethernet ≈ 0).
  - **F5 encode:decode ratio** — untouched by this reconciliation
    (still 🟡, still on the #4941 boundary).
- **Status:** 🟢 for the reconciliation logic (arm audit + three-way
  numeric agreement); the successor claim inherits C18 F2's statuses.

## 4. Anomalies and open questions

- **Bbox ~1 W Wi-Fi premium** unexplained (radio power-save? band? the
  box's network stack) — resolve before quoting as an operator-CPE
  property. Candidate run: same arms after `iw`-level diagnostics.
- Single content family (BBB); a second content (Meridian/Kranjska iso
  clips exist) and a wired-adapter Fire TV arm would lift the device
  claims from 🟡. Not queued (backlog discipline).
- One GTV Wi-Fi row excluded (player came up PAUSED — caught by the
  PLAYING gate, listed in the batch page).

## 5. Figure manifest

- `netpath_summary.png`, `netpath_detail.png` — in wattlab
  `docs/netpath_2026-08-18/` (produced by `make_charts.py` there; exact
  command in that folder's README).
  **2026-08-30 (writing-desk figure-sweep, Figure 10):**
  `netpath_summary.png` re-exported as-is to
  `figures/fig_c18_netpath_summary.png` (`cp` from wattlab
  `docs/netpath_2026-08-18/`, command recorded here). Note: PNG only,
  dpi=160 — `make_charts.py` (line 74) has no SVG output and this repo
  prefers SVG at 300 dpi (see `figures/README.md`); regenerating in
  house style would need a small addition to that script, not done
  tonight since it's wattlab-side code, not this repo's. `netpath_detail.png`
  not re-exported — not requested by the handoff.

## 6. Provenance

- Raw rows: GoS1 `results/decode/2026-08-1[89]_*.json`, batch
  `20260818ae7ba7b0` (`/decode/batch/20260818ae7ba7b0`).
- Scripts + cell table: wattlab `docs/netpath_2026-08-18/`
  (`net_feeder.py`, `net_feeder_pass2.py`, `wifi_day.py`,
  `make_charts.py`, `netpath_cells.json`).
- C6 side of the audit: `digests/2026-07-stb-decode.md` §3–4 and GoS1
  `~/wattlab/docs/stb_decode_energy_2026-07.md`.
- Desk pass + digest: 2026-08-24 on GoS1 (no new measurement).
