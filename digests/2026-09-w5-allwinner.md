# Digest — C27: TV Box W5 (Allwinner H618): hardware decode is not codec-flat, and AV1 fails in the flattering direction (2026-09-21→22)

Handoff `runs/handoff-2026-09-27b-two-hours.md` item 4 (digest only, no
new rows). Source lab doc: wattlab `docs/w5_onboarding_2026-09-21.md`
(S77). **Two findings:**
- On the Allwinner H618's own hardware decoders, H.264 costs about
  0.10 W more than HEVC and VP9, and the difference is resolved at n=3.
- The box cannot play AV1. It presents 1.7 fps, and the AV1 rows read as
  the cheapest codec while passing every harness gate.

The second is the second instance of the C25 F2 trap, on a second
vendor.

## 1. Campaign metadata

- **Dates:** 2026-09-21→22 (batch `3e54b322a9b4`, W5); same night,
  batch `4b94ea5075f3` (Google TV comparator).
- **Device:** no-brand "TV Box W5".
  - Its `ro.product.*` props are spoofed ("ADT-3", "Google blueline");
    identity comes from `ro.soc.*` = **Allwinner H618** (4× Cortex-A53,
    Mali-G31, 4 GB, 32-bit userland).
  - Android 12, legacy OMX IL decoders: hardware H.264, HEVC and VP9, no
    AV1 block.
  - Factory fresh (no account, no Play Services).
  - Ethernet; C2 **HDMI_1**, screen mode (panel lit, context ΔW +27 to
    +32 W on every row).
- **Output mode:** the HDMI link runs **4096×2160p60 (DCI 4K)**, and
  Android composes a **1280×720** framebuffer that the display engine
  upscales. So decode runs at 1080p but composition at 720p.
- **Content:** BBB iso-bitrate 1080p60 at ~8 Mb/s, marker-encoded
  (`loop_bbbiso_{h264,h265,vp9,av1}`), stereo audio.
- **Capture:** rig protocol v3, Tapo P110 (Lab-F3) at 1 s, 1095 s
  windows, n=3 per codec, 12 rows, none discarded.
- **Presented frame rate:** from SurfaceFlinger frame timestamps, **not
  sampled inside the campaign windows** (the harness did not then). It
  was measured on the same clips in the same session, before the
  campaign (90 s probe, all four codecs) and after it (AV1 and H.264
  marker clips).
- **Player:** Just Player 0.196; AV1 plays through its bundled in-app
  `Libgav1VideoRenderer` (software).
- **Comparator:** Google TV Streamer (MT8696), Wi-Fi, **dummy plug** sink,
  same template and protocol, 1080 s windows.

## 2. Scope statement

Device layer only: the W5's wall-plug draw above its own idle (~3.8 W),
panel excluded (metered as context), network excluded (Ethernet,
iso-bitrate). One content family, one bitrate, one box of this model.
The W5's composition runs at 720p and the other rig boxes compose at
1080p/4K, so its absolute ΔW is not drop-in comparable with them. The
**sink state** of every W5 cell is `panel:HDMI_1` (lit). The GTV
comparator cells are `dummy`. Encode side out of scope (#4941).

## 3. Findings

### F1 — On the Allwinner H618's hardware decoders, H.264 costs about 0.10 W more than HEVC and VP9

- **Claim (n=3 per codec, 1095 s windows):**

  | Codec | Decoder | Mean ΔW | Reps | sd | Presented fps |
  |---|---|---|---|---|---|
  | H.264 | `OMX.allwinner.video.decoder.avc` | **+1.073 W** | 1.051 / 1.083 / 1.086 | 0.019 | 60.0 |
  | HEVC | `…decoder.hevc` | **+0.966 W** | 0.931 / 0.975 / 0.993 | 0.032 | 60.0 |
  | VP9 | `…decoder.vp9` | **+0.971 W** | 0.923 / 0.987 / 1.002 | 0.042 | 60.0 |

  Welch comparisons:
  - H.264 − HEVC: +0.107 W (95 % CI +0.038…+0.176).
  - H.264 − VP9: +0.103 W (CI +0.018…+0.188).
  - HEVC − VP9: −0.004 W (tie).

  The rep ranges do not overlap. At iso-bitrate all three streams carry
  the same bit volume.
- **Traffic Light:** 🟢 Repeatable. n=3 per codec, all 9 rows 🟢, sd
  ≤0.042 W, the difference resolved by its CI. Rated for this box and
  this content only.
- **Confounds:**
  - One content family and one box.
  - Presented fps for these rows comes from the same-session probe, not
    in-window.
  - Row `64e14084` carries a disclosed 2 s adb excursion, biasing its ΔW
    by +0.0005 W (lab doc §7).
  - The older codec being the dearer one (H.264 > HEVC ≈ VP9) is the
    opposite of the software ordering. This is a property of this
    decoder, not a claim about codecs.
- **Relation to other campaigns:** C25 F1 has hardware decode on the
  MT8696 (GTV) within 0.08 W across H.264/HEVC/AV1, and on Marvell (Bbox)
  within 0.08 W across H.264/HEVC. The W5's 0.10 W spread is resolvable
  where those were not. The supported statement is narrower than
  "codec-flat": a fixed-function decoder makes codec choice cheap, and
  how cheap depends on the silicon.

### F2 — The W5 cannot play 1080p60 AV1, and its AV1 rows read as the cheapest codec while passing every gate

- **Claim:** AV1 has no decoder on this silicon; Just Player falls back
  to its in-app software renderer, which presents **1.7 fps** on the
  campaign's marker clip against a 1080p60 source. The H.264 marker clip
  presents 60.0 fps on the same box, same session, as the control. The
  90 s probe read 1.3 fps.

  The three AV1 rows read **+0.442 W** (0.422 / 0.451 / 0.452, sd
  0.017), 54 % below the cheapest codec the box can actually play. Every
  gate passed:
  - PLAYING from start to end;
  - flat trace;
  - correct, non-black mid-window screenshot;
  - 🟢 confidence.

  The only incidental tell: within-window sample sd was 0.126–0.139 W,
  against 0.063–0.079 W on every hardware row.
- **Traffic Light:** 🟢 Repeatable, for "these rows measure a failed
  playback and must not be quoted as AV1 decode energy". n=3 rows,
  consistent power, fps measured twice (1.3 and 1.7) against a 60.0 fps
  control.
- **Consequence:** this is the second box after the Bbox (C25 F2) where
  a software-fallback AV1 row is a failed playback. Here it errs low
  (the box does less work); on the Bbox it errs high (the box works
  flat out on software decode). **Neither sign can be trusted without a
  presented-fps check.**
- **Confounds:** fps was not sampled inside the campaign windows; the
  1.3–1.7 fps readings bracket it on the same clip, box, and session.

### F3 — Playing the same file, the W5 draws about 1.7× the Google TV's marginal power, but the comparison is below the n=3 bar

- **Claim:** same template, protocol and night.
  - W5 H.264: +1.073 W (n=3).
  - GTV H.264: **+0.619 W (n=2**: 0.595 / 0.643).
  - The third GTV row (`1e1a0c75`, −0.928 W) is discarded: its baseline
    read 2.757 W against 0.98–1.04 W on the other two, the box still
    coming down from boot.
  - Idle: W5 ~3.8 W, GTV ~1.0 W.
- **Traffic Light:** 🔴 Need More Data (the GTV cell is n=2).
- **Confounds, running in opposite directions:**
  - The GTV was on Wi-Fi (its Wi-Fi share is about +0.21 W, C18), which
    inflates the GTV and would widen the gap.
  - The GTV had a dummy sink against the W5's lit panel (sink term not
    quantified).
  - Factory-fresh W5 against an account-carrying GTV.
  - 720p against 1080p composition.
  - One codec, one content family.

## 4. Anomalies and open questions

- **The GTV comparator's discarded row is another negative that is not
  a playback failure** (PLAYING, decoder allocated). It was a
  boot-contaminated baseline, the same class as the F9 Fire TV rows in
  C25 §4. Add it to that ledger.
- **The lab doc's §6.3 labels the August `vp9_oneoff` §5.2 GTV rows
  "headless (no sink)".** The staleness handoff (item 4) says the rig
  wiring record has the GTV cabled to HDMI_2 from 2026-07-30 (input not
  selected). That correction to the owl doc is still pending (staleness
  item 4, not done in this session). This digest does not use those
  rows.
- **The idle spikes** (to 3.9–4.4 W on a 3.68 W floor, periodic) are
  handled with a 1.0 W idle-guard tolerance. The cause was not
  investigated.
- **The 720p composition** is a caveat on any cross-device W5 claim
  until resolved. No 4K claim from this box.
- **Resolving runs, if the draft needs them:**
  - GTV H.264 comparator to n=3, on the same sink as the W5.
  - An in-window fps sample on the W5 AV1 cell, which the C25/C26
    SurfaceFlinger method now gives.

## 5. Figure manifest

None. No figure was generated for this digest.

## 6. Provenance

- **Raw data (GoS1):** `/srv/data/owl/results/decode/2026-09-2*_{job}.json`
  for the jobs listed above (batches `3e54b322a9b4`, `4b94ea5075f3`);
  settle characterisation `/srv/data/owl/onboard_w5_2026-09-22.md`.
- **Lab doc:** wattlab `docs/w5_onboarding_2026-09-21.md` (commit
  `fac9405`, JOURNAL S77). Its Welch table and fps probes are the source
  for F1's CI and F2's fps. The per-row ΔW, baselines, flags, sinks and
  decoders were re-read from the stored envelopes on 2026-09-27 and
  match the lab doc.
- **Analysis date:** 2026-09-27.
