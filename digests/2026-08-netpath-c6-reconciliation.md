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

## Amendment 2026-09-30 — Bbox Wi-Fi premium re-measured: +0.98 W was a baseline-state artefact

Desk check of stored runs; no rig time. Ben remembered a later Bbox
re-measurement near +0.5 W. It exists: a Bbox-only follow-up to CR-074 on
**2026-09-14/15** (`/srv/data/owl/campaign_2026-09-14_bbox_wifi/`,
`OVERNIGHT_REPORT.md`, `README.md`). It was never digested until now.

**What the records show:**

| Run | Dates | Design | n | Wi-Fi − Ethernet, W while playing |
|---|---|---|---|---|
| C18 (this digest) | 2026-08-18/19 | BBB 1.5/8/20 Mb/s × burst/paced, 600 s; Ethernet day vs Wi-Fi day | 18 / 18 rows | **+0.48 W absolute** (6.517 ± 0.171 vs 6.037 ± 0.161 W); **+0.98 W on ΔW** |
| A-B-A, same evening | 2026-09-14 21:46–22:50 | BBB 8 Mb/s, 300 s, cable pulled and re-plugged | 3 / 3 | **+0.18 W** |
| Ladder, night Wi-Fi vs day Ethernet | batches `20260914bb0c` (Wi-Fi) and `20260915bb0e` (Ethernet), same clips, same sink (panel HDMI_2) | BBB, Meridian, football × H.264/HEVC × 3 rungs, 150 s | 2–3 per cell, 6 cells per rung | **+0.16 ± 0.02** (1080p 10 Mb/s), **+0.21 ± 0.02** (2160p 20), **+0.25 ± 0.03** (2160p 35) |

- **Local-file controls** (the same clip from the box's storage, no
  traffic) put Wi-Fi-associated and Ethernet-only **equal**: 6.58 vs
  6.69, 7.94 vs 7.93, 8.03 vs 8.05 W.
- **Idle** (menu, no player): the two interfaces are equal within
  0.03 W.

**Why +0.98 W differs (🟢 for the arithmetic, 🟡 for the screen-state
attribution):**
- C18's +0.98 W compares **ΔW over idle**. The two interfaces' idle
  baselines differed by 0.50 W: **5.36 W on Wi-Fi vs 5.86 W on
  Ethernet** (n=18 each).
- In absolute watts while playing, the gap was **+0.48 W**, and
  0.48 + 0.50 = 0.98.
- The September runs show why the baselines differed. The same box
  idles at ~5.4 W on the Settings menu and ~5.8–6.0 W on the live home
  screen, whose preview decodes video behind the overlay (+0.4–0.6 W on
  either interface).
  - August's Wi-Fi baselines match the menu level; its Ethernet
    baselines match the live home screen.
  - The August Wi-Fi rows therefore started from a cheaper screen,
    inflating their ΔW. The connection itself costs nothing at idle.
- **What remains is a real receive-path term.** It appears only when
  streaming over Wi-Fi: +0.16–0.25 W at 10–35 Mb/s, a large fixed part
  with a mild bitrate slope.
- August's absolute +0.48 W (different day, different state history)
  is the upper data point.
- The records do not separate "a dearer Wi-Fi receive path" from "a
  box that powers its radio down more fully when Wi-Fi is off" (report
  §6).
- Link: Wi-Fi 6 at 5.5–5.6 GHz, RSSI −55 to −59 dBm, PHY 680–1134 Mb/s.
  The Google Cast receiver holds a high-performance Wi-Fi lock, but
  the framework reports it unused (`high_perf_active_time_ms: 0`), so
  it is not the mechanism.

**Status:**
- **+0.98 W is superseded (withdrawn as a playback cost).** 🟢
- **Replacement: the Bbox's Wi-Fi term while playing is +0.16 to
  +0.25 W** at 10–35 Mb/s. 🟢 within this box: two independent designs
  agree (A-B-A +0.18 W, n=3/3; ladder, 18 cells within ±0.03 W per
  rung).
- **August's absolute +0.48 W is the upper bound of the range on
  record.** 🟡 (different day and state history).
- Quote **"about 0.2 to 0.5 W"**.
- **Knock-ons:**
  - F2's cross-device "+0.50 W (+75 %)" average includes the Bbox
    artefact, so **do not quote it**.
  - The "connection method 2.5–12× the codec spread" upper end (12×)
    rested on +0.98 W. With the Bbox at 0.2–0.5 W, the ratio against
    the ≤0.08 W spread is roughly **2–6×**.
  - The Google TV's +0.21 W (n=3) is unaffected: its two interfaces
    shared a baseline state.

**§4.3 sentence the data supports:** "Wi-Fi added about 0.2 W while
playing on both the Google TV (+0.21 W) and the operator box (+0.16 to
+0.25 W at 10–35 Mb/s, same-sink re-measurement), and nothing at idle
or with the file on the box; an earlier +0.98 W for the operator box
compared baselines taken on different screens."

**Commands:**
- August absolute watts by interface (the Bbox's eth0 and wlan0 addresses, per `decode_bench/README.md`):

      python3 -c "import json,glob,statistics as st,collections;c=collections.defaultdict(list)
      [c[d['devices']['bbox']['rows'][0]['device']['serial']].append((r['w_base'],r['w_task'])) for f in glob.glob('/srv/data/owl/results/decode/2026-08-*.json') for d in [json.load(open(f))] if d['template'].startswith('net_') for r in d['runs'] if r['device']=='bbox']
      [print(k,len(v),st.mean(x[0] for x in v),st.mean(x[1] for x in v)) for k,v in c.items()]"

- September tables: `/srv/data/owl/campaign_2026-09-14_bbox_wifi/eth_vs_wifi_tables.md`
  and `night_tables.md`, produced by `eth_vs_wifi.py` and
  `night_report.py` in that folder.
- Timeline and A-B-A rows: that folder's `README.md`. Its
  `note_for_oualid_*` drafts carry a device serial and are not for
  publication.
