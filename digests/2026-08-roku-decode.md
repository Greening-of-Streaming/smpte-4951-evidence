# Roku Express 4K — decode energy, four codecs (2026-08-29)

First Roku rows on an OWL bench. New device, one campaign: a working
playback mechanism had to be found before any measurement was possible
(§1), then a four-codec headless sweep (§3 F2) — done the same day as,
and directly comparable with, the Apple TV AV1-vs-VP9 confirmation in
`digests/2026-08-appletv-vlc.md` F6. Read F3 before trusting any *other*
device's historical screen-mode HEVC/VP9 numbers — it explains a real
harness bug found and fixed here, and why it does not reach back to
retroactively contaminate anything already in this repo.

## 1. Campaign metadata

- **Device:** Roku Express 4K, on the C2's HDMI slot (rig `kind: "roku"`,
  reserved LAN IP). Control: Roku ECP (External Control Protocol,
  port 8060) — `/query/*` for state, `/keypress/*` for input,
  `/launch/{appId}` to start an app. No adb, no logcat equivalent:
  **this device has no decoder-provenance signal at all** (§4).
- **Playback path (the thing that had to be discovered before any
  measurement existed):** the box already carried a channel, id
  `775528`, "Greening of Streaming" — built by a GoS colleague (Dom) for
  a past hackathon, published to the Roku Channel Store, unmaintained
  for roughly a year. It is a simple `.m3u` playlist player. Its
  playlist URL pointed at a dead personal domain (`nas.levencode.com`,
  down ~a year) — every early attempt 404'd for that reason, not because
  the app or the ECP calls were wrong. **Fix:** repointed the app's
  playlist setting (one-time, on-device) at
  `http://192.168.1.62:8123/gos_local_test.m3u`; the harness now
  rewrites that file's single entry to the target clip before each
  launch, so the on-device setting never needs touching again.
- **Exact nav sequence** (ECP has no "play this URL" or "jump to track"
  primitive — all found live, each step confirmed necessary):
  `POST /launch/775528` → wait ~3 s (inputs sent earlier are silently
  dropped) → four `Down` keypresses (default focus sits 4 rows above the
  first playable item regardless of playlist length) → `Select` (enters
  track view) → a second `Select` (actually starts playback) → one more
  keypress to leave the windowed player and go full-screen (`Right` from
  this exact path; state-path-dependent — re-verify if the sequence
  above ever changes). Implemented in wattlab `decode_bench/bench.py`'s
  `RokuDevice`.
- **Capture:** Tapo P110 (device's own meter on the rig), 1 s cadence.
  Two device states available: headless (`calibrate=false`, no display
  needed, faster/cheaper — used for §3 F2) and screen mode
  (marker-calibrated black/white/black head, for visual sanity-checking
  and cross-checking against a display — used during the fixes in §4,
  not in the F2 table).
- **Content:** the existing iso-bitrate **bbbiso** clip family (same BBB
  1080p60 @8 Mb/s encodes used in C17, `digests/2026-08-vp9-isobitrate.md`
  — x264 medium / x265 medium / SVT-AV1 preset 6 / libvpx-VP9 cpu-used 2,
  two-pass ABR), looped to 20-minute files; VP9 in WebM (its own
  established convention — MP4/vp09 has stalled other players in this
  project before). No new encodes for this campaign.
- **Protocol:** headless realtime 1×, 150 s window, n=3 per codec, four
  codecs (H.264/HEVC/AV1/VP9), OWL confidence per row. Batch
  `c876cc890df2` (shared with the Apple TV F6 addendum — both ran the
  same session).

## 2. Scope statement

Device layer only (the Roku box itself, via its own meter). Network,
CDN, and production/storage excluded. Energy (W / Wh), not CO₂e.
Realtime playback regime only — not a saturated-transcode reading.

## 3. Findings

- **F1 — A working, reproducible playback path exists and is now
  automated.** 🟢 for the mechanism. Confirmed end-to-end via a real
  `/decode` job in screen mode: correct full-screen playback, position
  advancing, `alive_at_window_end: true`. This device is now a normal
  citizen of the OWL decode rig, not a one-off probe.
- **F2 — AV1 and VP9 cost the same to decode; H.264/HEVC are ~0.1 W
  cheaper.** 🟢, n=3 per codec, ΔW above device idle, bbbiso content,
  150 s headless windows, all rows green:

  | codec | ΔW (mean, n=3) | range |
  |---|---|---|
  | H.264 | **0.381** | 0.369–0.397 |
  | HEVC | **0.470** | 0.456–0.483 |
  | AV1 | **0.476** | 0.469–0.483 |
  | VP9 | **0.481** | 0.465–0.492 |

  AV1/VP9 gap: +0.005 W (~1 %) — inside both codecs' own run-to-run
  range, i.e. a tie, not a ranking. H.264/HEVC sit ~0.09–0.10 W below
  the AV1/VP9 pair. Decoder path is **unconfirmed** (§4) — this is a
  device-total energy reading, not attributable to a specific decode
  block. **This independently reproduces the same-day Apple TV finding**
  (`digests/2026-08-appletv-vlc.md` F6: AV1 3.435 W vs VP9 3.495 W, also
  a tie) on a second device — see that digest for the public-claim
  correction this pair of results together supports.
- **F3 — Two marker-encoder harness bugs found and fixed on this device;
  neither reaches back to contaminate other devices' existing data.**
  Screen-mode playback on this device requires a synthetic black/white/
  black marker head spliced onto the front of each clip (used for visual
  sanity-checks and edge-detection, not for F2's headless numbers). Two
  distinct bugs surfaced while building that path for HEVC and VP9,
  both with the identical symptom (screen frozen on the marker's last
  frame, flat ~37 W trace, decoder never reaching content):
  1. **HEVC:** the marker segments were encoded with `hevc_nvenc`, which
     pads its coded height to the next 64-multiple (1080→1088); this
     project's HEVC source content is a clean, unpadded 1080. Splicing
     the two together (stream-copy concat) put a real coded-buffer-size
     discontinuity in the file. Roku's hardware HEVC decoder froze on
     it; VLC on the Apple TV (software decode) played the identical file
     fine — a hardware-vs-software decoder robustness gap, not a
     Roku-specific defect. **Fix:** HEVC marker segments now use
     `libx265` (clean, unpadded 1080) instead of `hevc_nvenc`.
  2. **VP9:** a *different* root cause producing the same symptom, found
     immediately after ruling out the HEVC-style explanation (profile/
     pix_fmt/color all matched exactly). The marker-segment container
     was hardcoded to `.mp4` for every codec; VP9's own source content is
     `.webm` (this project's convention, since VP9-in-MP4 has stalled
     other players before — see C17). Concatenating a VP9-in-MP4 marker
     onto VP9-in-WebM content produced the same stuck-decoder failure via
     a container/muxing-level mechanism, unrelated to codec parameters.
     **Fix:** marker-segment container now matches the source clip's own
     extension instead of a hardcoded `.mp4`.
  **Why neither bug reaches back into this repo's existing data:** VP9
  had no marker encoder at all before this session (nothing to
  retroactively affect). HEVC marker segments *did* exist before today
  and *did* use `hevc_nvenc` — but the only two devices ever measured in
  screen mode with a marker head are this Roku (new) and the Apple TV
  (VLC, software decode, confirmed tolerant of the exact same file, see
  above). Every other device on the bench (Google TV, Fire TV, Bbox, the
  Pis) uses headless + adb/logcat liveness, not screen-mode markers, so
  never exercised this code path. Both fixes verified live, twice each,
  before this campaign's numbers were trusted.

## 4. Anomalies and open questions

- **Q1 — Decoder path unconfirmed, and likely to stay that way.** Roku
  exposes no logcat equivalent, no dev-tools decoder query reachable
  from this harness. F2's numbers are honest device-total ΔW, not
  attributed to a specific decode block (hardware or software). Not
  currently resolvable without a different introspection method (rooted/
  homebrew channel, USB debug bridge if Roku ever exposes one — no known
  path today). Feeds RUN_QUEUE.md as an open item, not urgent: F2's
  cross-device tie with the Apple TV doesn't depend on knowing which
  block did the work.
- **Q2 — One content family only (bbbiso/BBB).** Reusing C17's clips
  buys direct comparability but means F2 hasn't been checked against
  Kranjska or Meridian on this device yet — would strengthen F2 from
  🟢-within-panel to something closer to C19's three-content
  confirmation, if a future run has spare rig time.
  **Answered 2026-08-31 (writing-desk ask #3,
  `runs/handoff-2026-08-31-final-night.md`) — Kranjska added, all four
  codecs, n=3 screen mode:** H.264 0.265 W · HEVC 0.307 W · AV1 0.343 W
  · VP9 0.363 W (all 🟢, CV ≤9%). Same qualitative shape as BBB's
  headless numbers (§3 F2) — codecs sit close together, no large
  coverage-gap penalty visible — but at roughly half BBB's absolute
  level (BBB ΔW range was ~0.9–1.0 W across codecs per the original
  headless sweep; Kranjska here is ~0.26–0.36 W), consistent with
  Kranjska being genuinely lower-complexity/darker content on this
  device too, matching the pattern seen elsewhere on this bench
  (C23). F2 is now checked against a second content family and holds.
- **Also answered 2026-08-31 — the F2/F5 headless-vs-screen question,
  outstanding since 2026-08-29.** ("C20 F2 is a headless reading; C19
  F5 showed headless is not a measurement on the Apple TV — was the
  Roku's headless level checked against its screen-mode level?") Same
  content/codec (bbbiso/H.264), n=3 each, back-to-back: **headless
  0.384 W (CV 5%) vs screen 0.403 W (CV 2%) — statistically
  indistinguishable.** Unlike the Apple TV (headless 1.6 W vs
  screen-mode 4.9 W, a 3× difference that invalidated every headless
  Apple TV row), **headless is a valid measurement on the Roku** — F2's
  original headless numbers mean what they appear to mean, no
  retroactive caveat needed. Raw store:
  `/srv/data/owl/campaign_2026-08-31_overnight/results.jsonl` (labels
  `p3_roku_headless`/`p3_roku_screen`/`p3_roku_krj_*`); journal
  `runs/session-2026-08-30-writing-desk-4-points.md`.
- **Q3 — Full-screen requires a state-path-dependent keypress (§1).**
  The `Right`-vs-`Left` expand behaviour observed during discovery
  suggests the windowed→full-screen transition is not a fixed toggle;
  re-verify the nav sequence if this ever silently regresses (a wrong
  keypress would leave playback windowed, which would read as a lower
  wrong-in-a-non-obvious-way device-total number rather than an obvious
  failure).

## 5. Figure manifest

None (the table in F2 is the deliverable; summary CSV alongside this
file).

## 6. Provenance

- OWL `/decode` batch **`c876cc890df2`** (shared with the Apple TV F6
  addendum). Roku rows, per-row JSON on GoS1:
  `results/decode/2026-08-29_{0ec0f05a,305561b2,97c47248}.json` (H.264),
  `{6ce7dc03,704959dc,e2a6de84}.json` (HEVC),
  `{9114fb90,d6a6242e,b5f5bbb2}.json` (AV1),
  `{38b13c96,41c25f50,5fe6c26d}.json` (VP9).
- Harness: wattlab `decode_bench/bench.py` (`RokuDevice`, new this
  session), `decode_run.py` (`_ensure_marked_clips_sync`, F3's two
  fixes), `rig.py` (device entry, HDMI assignment). Wattlab commits
  2026-08-29 (same session as the Apple TV F6 addendum).
- Summary CSV: `digests/2026-08-roku-decode.csv`.
- Analysis date 2026-08-29.
