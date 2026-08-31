# Apple TV 4K (2017, A10X) — VLC-driven decode energy, four codecs (2026-08-26/27, +2026-08-29 addendum)

Apple TV 4K 1st gen (`AppleTV6,2`, A10X Fusion), player = **VLC for tvOS**.
Three sessions: a 2026-08-26 evening pilot (tvOS 18.0, n=2, one content), an
2026-08-26 evening→08-27 morning overnight campaign (tvOS 26.6, n=3, three
content families) that supersedes it for the codec claim, and a 2026-08-29
confirmation run (**F6**, below) that separates AV1 from VP9 for the first
time and corrects a public claim about them. The first Apple-silicon rows
on an OWL bench. Read §3 with the §4 caveats; **read F6 before quoting AV1
vs VP9 specifically, not just the AV1/VP9-vs-H.264/HEVC gap.**

## 1. Campaign metadata

- **Pilot:** 2026-08-26, 17:40–18:10 CEST — tvOS 18.0 build 22J357, n=2,
  BBB content only, park = tvOS Settings. Superseded for the codec table
  (§3 F3) by the overnight campaign below; its mechanism findings (F1, F2,
  F5) stand unchanged.
- **Overnight campaign:** 2026-08-26 23:00 → 2026-08-27 04:00 CEST
  (with a ~70-minute pause for a tvOS update mid-session — see §4). Owner
  granted the lab bench the rig until 10:00 to complete the data set and
  sanity-check the paper's existing device readings (wattlab CR-075/077).
- **Device:** `AppleTV6,2` = Apple TV 4K **1st generation (2017), A10X
  Fusion**, "TV Room", `192.168.1.152` (reserved). Updated mid-session to
  **tvOS 26.6 build 23L773** (was 18.0 22J357) — see §4 for the re-pairing
  and settle-time consequences. HDMI into the owner's desk monitor
  throughout (panel not on a lab meter; irrelevant to the box's own W).
- **Player (the important caveat, unchanged):** **VLC for tvOS**
  (`org.videolan.vlc-ios`), launched per row by pyatv Companion `launch_app`
  with VLC's x-callback stream scheme (AirPlay `play_url` is dead on tvOS —
  F1, reconfirmed on 26.6). VLC uses VideoToolbox for H.264/HEVC and
  software paths otherwise; its per-codec decoder choice is not observable
  from outside — the energy signature is the evidence. Every number below
  is "VLC on tvOS", not the native player.
- **Capture:** own Tapo P110 **Lab-F3** (`.1`, fw 1.3.1, local mW API, 1 s
  cadence). `decode_bench/bench.py`'s `AtvDevice` through the normal OWL
  `/decode` queue (`decode_bench/atv_night.py` sequencer), not the
  standalone pilot script. Protocol: park (VLC stopped, re-launched to its
  library screen — **not** tvOS Settings, which itself draws power on
  26.6, see §4) → settle → baseline → launch → window → stop → park.
  Per-device settle/baseline floor added mid-campaign (`rig.py`
  `min_settle_s: 25`, `min_baseline_samples: 40` for this device — see §4):
  the generic 5 s/20-sample protocol, tuned to the Android boxes' fast
  post-stop settle, was too short for this box. **120 s** sampling window,
  n=3 per cell. Liveness = pyatv playback state + `alive_at_window_end`.
  `confidence.py` on the raw samples.
- **Content:** iso-bitrate families (S65/C17 recipe), 3-min cuts of the
  20-min encodes: BBB, Kranjska, **Meridian** (new for the Apple TV — all
  three content families the rest of the panel already carries). 1080p60,
  matched-VMAF NVENC encodes, served by the Range-correct OWL origin.

## 2. Scope statement

Device layer only — the Apple TV's own socket. Display, network path,
origin excluded. Player = VLC for tvOS. The pilot's device-total **playing**
figures were citable, its baselines were not (screensaver ramp); the
overnight campaign's playing figures remain citable and its baselines are
mostly usable but carry a residual elevation caveat (§4) — device-total W
is the primary metric throughout this digest, matching how this paper
already treats the Bbox's own idle-drift caveat (C11 F5/F11).

## 3. Findings

- **F1 — AirPlay `play_url` is dead on tvOS (18 and 26), and it is the
  receiver, not our origin or URL.** 🟢, reconfirmed on 26.6. HAP
  pair-verify and the whole RTSP sequence succeed (`SETUP`, `RECORD`,
  `POST /play`, `POST /rate?value=1`, `setProperty` ×4 — every reply
  `errorCode 0`), then `GET /playback-info` answers **HTTP 500** and
  playback never starts; the origin logs **0 requests**. Same for HLS.
  Upstream pyatv #2403/#2512 (`/playback-info` is AirPlay-1 only, gone on
  tvOS 17+). **New on 26.6:** upstream **PR #2899** replaces `POST /play`
  with a play-queue call over `/command`, and under that patch the
  receiver *does* fetch the media (origin logged 25 Range requests) —
  playback still doesn't render because `atvremote` closes the session
  after queueing, not because the receiver refuses. A driver that holds
  the AirPlay session open for the row's window would give the **native
  tvOS player**, no VLC caveat — noted for CR-075, not built this session.
- **F2 — A working playback path: VLC via Companion.** 🟢, reproduced on
  both tvOS versions across the whole overnight campaign.
  `launch_app=vlc-x-callback://x-callback-url/stream?url=<origin URL>`
  over Companion. First launch per install raises a tvOS "Open VLC?"
  dialog needing one on-remote accept; every subsequent launch (including
  after the 26.6 update, which needed a fresh accept) goes straight to
  playback, fetching with Range. A launch that arrives mid-dialog fails
  `RPErrorDomain 58809 "Session not found"`.
- **F3 — On the A10X, H.264 and HEVC play at the same power; AV1 and VP9
  cost ~+1.19 W more (+29 %), confirmed across three content families.**
  🟢 **Repeatable** (upgraded from the pilot's 🟡): n=3 per cell, three
  content families, 36 rows total (one excluded — see §4), device-total W
  while playing, 120 s windows:

  | content | H.264 | HEVC | AV1 | VP9 |
  |---|---|---|---|---|
  | BBB | 4.487 (n=3) | 4.451 (n=3) | 5.740 (n=3) | 5.694 (n=3) |
  | Kranjska | 3.371 (n=3) | 3.352 (n=3) | 4.556 (n=2*) | 4.792 (n=3) |
  | Meridian | 4.438 (n=3) | 4.391 (n=3) | 5.465 (n=3) | 5.365 (n=3) |
  | **mean across contents** | **4.098** | **4.065** | **5.254** | **5.284** |

  \* one Kranjska-AV1 rep excluded, `alive_at_window_end=False` — an
  isolated VLC hiccup, not repeated on any other row that night (§4).

  **Hardware pair (H.264+HEVC) mean 4.082 W; software-fallback pair
  (AV1+VP9) mean 5.269 W — a gap of +1.187 W (+29.1 %).** This closely
  reproduces the pilot's single-evening estimate (+1.35 W/+27 %, n=2, one
  content) with 3× the reps and three content families instead of one.
  Within-content spread across reps: H.264/HEVC ≤0.12 W, AV1/VP9 ≤0.21 W
  (excl. the dropped row) — the codec gap (≈1.2 W) is 6–10× that spread.
  Reading, unchanged from the pilot: the hardware pair (VideoToolbox
  H.264/HEVC) is flat, exactly as on the MediaTek streamers; **AV1 falls
  back to software** on Apple silicon of this generation (no AV1 block
  before A17 Pro/M3) — the **third independent instance** of the paper's
  penalty claim after Marvell (Bbox, +1.2–1.4 W); **VP9 pays the same
  price**, i.e. no VP9 hardware path is reached by VLC on this box (native
  YouTube's VP9 path is a separate question this harness cannot ask).
  **Content moves the absolute level** (Kranjska ~1.1 W lower than
  BBB/Meridian across every codec, same direction/shape as C11 F5's
  luminance point on the MediaTek boxes) but the codec *gap* is stable
  across all three: BBB +1.25 W, Kranjska +1.31 W (using the corrected AV1
  mean), Meridian +1.01 W.
- **F4 — ΔW over baseline is directionally right but the magnitude is
  compromised for part of the overnight campaign (see §4's second
  incident) — device-total W (F3) is the citable metric.** Where the
  baseline genuinely reached its ~2.1–2.3 W floor (most pilot rows, some
  overnight rows), ΔW matches F3 exactly. Where it didn't (most of the
  overnight campaign, elevated to a stable ~3.2–3.5 W — see §4), ΔW is
  understated by roughly that offset for every codec equally, which is
  why the *codec-to-codec* comparison in F3 survives even though absolute
  ΔW does not: the offset is common-mode.
- **F5 — Headless is not a measurement on this box, and a display hot-plug
  pauses VLC.** 🟢 for the mechanism (unchanged from the pilot night — one
  59-min row, owner at the screen for every transition, 1-s trace
  segmented by wall-clock; job `fe9d69b0`). Device-total W: **headless
  "Playing" 1.62 W** vs **quarter-screen (unscaled) 4.42 W** vs
  **full-screen 4.87 W**; a display hot-plug in either direction pauses
  VLC (frozen frame). Whatever runs headless is not the decode-and-render
  path measured on screen — **headless Apple TV rows must never be quoted
  as decode energy.** Every row in F3 was taken with the display attached
  and stable throughout.
- **F6 — 2026-08-29 addendum: AV1 and VP9 do NOT differ from each other on
  this box; corrects a public claim that VP9 would be cheaper.** In a
  LinkedIn thread on the VP9 one-off report (see wattlab
  `docs/vp9_oneoff_2026-08.md` §4.4/§6), the owner told a commenter
  (Murat Pisat) that if Apple TV decode falls back to software, VP9 would
  *at least be cheaper to decode than the other codecs there*. Two
  independent readings on this box say otherwise:
  1. **Re-reading F3's own table by codec, not by pair:** AV1 5.254 W
     mean vs VP9 5.284 W mean across the three content families — a
     0.030 W (0.6 %) gap. F3's "(AV1+VP9) mean 5.269 W" framing was
     correct for the H.264/HEVC-vs-AV1/VP9 comparison it was making, but
     never separately asserted AV1 ≈ VP9 — this addendum makes that
     explicit.
  2. **A fresh, independent n=3 confirmation run** (same rig, same bbbiso
     content, ΔW-above-idle protocol rather than device-total, batch
     `c876cc890df2`, after two harness bugs were fixed the same day —
     see `digests/2026-08-roku-decode.md` §4 for what they were and why
     they don't affect this box's numbers): **AV1 3.435 W (n=3,
     3.387–3.486), VP9 3.495 W (n=3, 3.473–3.536)**. The 0.060 W (1.7 %)
     gap is smaller than the run-to-run spread inside either 3-run set,
     and points the wrong way for the claim (VP9 trends fractionally
     *higher*, not lower).
  Both readings — one from the original overnight campaign, one from a
  dedicated re-check — agree: **AV1 and VP9 cost the same to decode in
  software on this device.** The same-day Roku sweep (four codecs, n=3
  each, `digests/2026-08-roku-decode.md`) reproduces the tie
  independently on a second device. Not contradicted by C17's Pi 400
  result (VP9 *was* the cheapest of four there, ARM CPU) — read as
  architecture-dependent, not a universal codec property; open question,
  not resolved either way.

## 4. Anomalies and open questions

- **Q1 — RESOLVED: screensaver ramp.** The pilot's Q1 (tvOS Settings park
  ramping 2.6→6.6 W via the Aerial screensaver) is gone in the overnight
  campaign — the owner disabled the screensaver, and the park state moved
  from "sit in Settings" to "VLC stopped, relaunched to its library
  screen" (Settings itself turned out to draw power on 26.6, see Q2).
- **Q2 — NEW: tvOS 26.6's Settings app is not a safe park state either.**
  Discovered live: launching `com.apple.TVSettings` for a park briefly
  spikes the box from ~2.2 W to ~5.7 W for tens of seconds on 26.6 (it
  goes and checks something). Fixed by parking on VLC's own library
  screen instead (`decode_bench/bench.py` `AtvDevice.park()`), which
  needed no app switch and stayed flat.
- **Q3 — RESOLVED (2026-08-27, ~9 hours later): tvOS 26.6 does NOT have a
  higher resting idle floor — the overnight elevation was recurring
  post-transition housekeeping, not a new baseline.** During the
  overnight campaign, the box's baseline sat at an elevated, stable
  plateau (~3.2–3.5 W, easing toward ~3.1–3.3 W) for two hours after a
  ~35-minute post-update instability episode, never fully returning to
  the pre-update ~2.1–2.3 W floor. Re-checked clean, many hours later
  (box fully rested — off since the rig's idle auto-off, cold-booted
  fresh, HDMI/display attached throughout, parked in tvOS Settings this
  time rather than VLC's library): the first ~3 minutes after boot showed
  the same bursty 5.7–8.0 W pattern in ~20–40 s cycles (some background
  check/sync routine), but it **fully stopped** after that — a clean 5
  minute / 1 s window (n=290) starting 4 minutes post-boot read **mean
  2.567 W, median 2.462 W, sd 0.238 W, min 2.339 W, max 3.391 W, 90% of
  samples under 3.0 W** — statistically indistinguishable from the tvOS
  18 floor (2.5–2.7 W). Reading: the overnight campaign's "new plateau"
  was this same post-transition burst re-triggering on every ~4-minute
  park/relaunch cycle, not a permanent property of tvOS 26.6 — a
  genuinely rested, fully-settled measurement shows no elevation at all.
  Device-total **playing** W (F3) was never at risk either way — it
  matched the pilot's pre-update numbers throughout.
- **Q4 — RESOLVED (with the caveat above): settle-time mismatch.** The
  rig's generic protocol (5 s settle / 20-sample baseline, tuned to the
  Android boxes) produced base sd up to 2 W and several false 🔴 rows
  early in the overnight campaign; task-level numbers were unaffected
  throughout (e.g. AV1 5.69–5.71 W across reps even on contaminated
  rows). Fixed with a per-device floor (`min_settle_s: 25`,
  `min_baseline_samples: 40`) — a `max()` over the protocol default, never
  lowering another device's numbers. Generalized into wattlab **CR-077**
  (device-onboarding idle-settle characterization tool), which found and
  fixed a second bug in itself (a fresh-boot warm-up gap) when validated
  live against two other rig devices.
- **Q5 — One dropped row.** Kranjska-AV1 rep 1 (`alive_at_window_end`
  False, task 3.35 W vs an expected ~4.1–4.6 W) — an isolated VLC hiccup;
  the very next row (Kranjska-VP9) came back clean without intervention,
  and no other row that night showed the pattern. Not used in F3's mean
  (n=2 for that one cell).
- **Q6 — What runs headless?** (unchanged from the pilot) Unresolvable
  from the socket; doesn't matter for the paper — the number is not
  decode energy either way.
- **Q7 — Not measured:** 4K, HDR, the native tvOS player (PR #2899 makes
  it reachable — see F1 — but needs a driver that holds the session
  open), a `rig.py` power/boot entry using pyatv `turn_on`/`turn_off`
  (currently manual). The box is not yet integrated into automated
  campaigns beyond this one-off sequencer (`atv_night.py`).
- Tooling: pyatv now runs from git master at `/srv/data/owl/pyatv-venv`
  (0.18.0 release predates the tvOS-26 fixes); `/tmp/pyatv-venv` is a
  dead 0.18.0 leftover.

## 5. Figure manifest

None (the tables are the deliverable; summary CSVs are next to this file).

## 6. Provenance

- Pilot raw rows: `/srv/data/owl/atv/probe_2026-08-26.jsonl` (8 rows).
  Summary CSV: `digests/2026-08-appletv-vlc.csv`.
- Overnight campaign: OWL `/decode` batch **`9d39def85f1b`** (36 rows, one
  excluded), per-row JSON at `results/decode/*-atv.json` on GoS1;
  sequencer log `/srv/data/owl/atv/night_9d39def85f1b_clean.log`. Summary
  CSV: `digests/2026-08-appletv-vlc-clean.csv` (`decode_bench/batch_cells.py
  9d39def85f1b`). An earlier same-night batch (`bb65c5494a6b`, 2 rows) was
  captured mid-instability (Q3) and is **not cited**.
- Harness: wattlab `decode_bench/bench.py` (`AtvDevice`), `atv_night.py`
  (sequencer), `atv_probe.py`/`atv_summary.py` (pilot), `onboard_device.py`
  (CR-077, used to validate the settle-time fix against two other
  devices), `rig.py` (device entry + settle/baseline floor), commits of
  2026-08-26/27 (S69). pyatv git master; Tapo P110 fw 1.3.1.
- **F6 addendum (2026-08-29):** OWL `/decode` batch **`c876cc890df2`**,
  screen mode (`ui_screen`), 165 s windows, per-row JSON
  `results/decode/2026-08-29_{1f2c4f9e,c7479e15,b1d642f8}.json` (AV1) and
  `{4728f8b8,f10c86a0,f5ecaf0a}.json` (VP9) on GoS1. Same-day harness
  fixes: `AtvDevice.park()` moved from `atv("stop")` (confirmed live,
  twice, not to reliably halt VLC) to `atv("home")`; `rig.py` idle_guard
  given a per-device `min_idle_tolerance_w: 1.0` (the noisy floor is
  permanent, not a one-time contamination — see this digest's own Q2–Q4
  for the same class of issue). Wattlab commits same day; see
  `docs/vp9_oneoff_2026-08.md` §6 for the full write-up this addendum
  summarises.
- Analysis dates 2026-08-26, 2026-08-27, and 2026-08-29.
