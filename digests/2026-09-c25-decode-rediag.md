# Digest — C25: Figure 8 re-diagnosis — the July negatives were playback that was not happening (2026-09-27)

Handoff `runs/handoff-2026-09-27-staleness.md` item 1 (Figure 8), worked
live with Ben at the rig. **Figure 8's anomalies are not a panel-standby
effect. They are rows in which the box was not decoding.** Every July
H.264 row on the Fire TV and the GTV, and the GTV's sequential AV1 rows,
were a media player sitting PAUSED. The GTV's parallel AV1 rows were a
box that fell asleep about 9 s into playback. The PAUSED mechanism was
reproduced on both boxes today. Re-measured with playback verified and
the panel lit, both boxes' hardware decode costs **+0.25 to +0.51 W**
for every covered codec. No cell is negative, and none sits inside the
caption's ±0.2 W band. **The Bbox's "AV1 costs +1.4 W" is a software
decoder presenting ~5 fps against a 50 fps output: it is not the cost
of watching AV1.**

## 1. Campaign metadata

- **Date:** 2026-09-27, 14:10–16:10 CEST. Query of existing data (1a)
  plus 21 metered rows (batch `20260927d1a6`) plus reproduction tests.
- **Devices:**
  - **Google TV Streamer**: MediaTek MT8696, Google TV (Android 14),
    Wi-Fi. **Re-cabled for this campaign from its dummy plug to C2
    HDMI_1** (the W5 moved to a dummy), so the GTV had a real panel sink.
  - **Bbox 4K**: Arcadyan HMB9213NW operator CPE, Marvell Berlin,
    Ethernet, C2 HDMI_2.
  - **Fire TV Stick 4K**: MT8696, Wi-Fi, C2 HDMI_4. Reproduction test
    only, not metered as a campaign row.
  - Firmware for all three is not recorded beyond the OS version.
- **Panel:** LG C2 (Lab-E), lit and awake on every metered row
  (`panel_awake=True`; Lab-E context 45–72 W). Picture mode is FILMMAKER
  MODE per input, as set on 2026-08-31. It was not re-read today and
  does not enter this digest's numbers, which are box-plug ΔW only.
- **Output mode:** read from the box's compositor vsync period, which
  describes the UI plane, not the HDMI link (the CR-084 caveat).
  - Bbox: 20.0 ms = 50 Hz.
  - GTV: 16.67 ms = 60 Hz.
  - Link resolution was not verified on either box.
- **Content:** Meridian 1080p59.94, the C11 loop files:
  - H.264 High, 4.49 Mb/s, 60-minute file;
  - HEVC Main, 3.50 Mb/s, 20-minute file;
  - AV1 Main, 2.81 Mb/s, 20-minute file.
- **Capture:**
  - Rig protocol v3, screen mode (the panel is claimed and switched to
    the box's input), 150 s windows, 1 s P110 polling (fw 1.3.1).
  - 20 baseline samples with the idle guard; player verified PLAYING
    before the baseline.
  - Keep-awake pins applied (sleep timer and screensaver off; GTV CEC
    active-source-lost rule = `none`).
  - n=3 per cell, codec order rotated per repetition, device order
    alternated.
- **Presented frame rate:**
  - **Bbox:** sampled every 20 s inside each task window from the
    player's SurfaceView frame timestamps
    (`dumpsys SurfaceFlinger --latency`).
  - **GTV:** cannot be read this way; its MediaTek decoders present
    through a sideband path (0 frames in the compositor). H.264 and AV1
    were checked by eye on the panel (Ben, smooth). HEVC was not
    eye-checked.

## 2. Scope statement

Device layer only: each streaming box's own wall-plug draw above its
own idle. The panel is metered as context and excluded from every ΔW.
Network, CDN, and the panel's own consumption are excluded. One content
family (Meridian), one operating point per codec (the C11 1080p
matched-VMAF files), two boxes metered, two more (Fire TV, GTV) used
for mechanism reproduction. **Sink state and output mode per cell:**
every metered cell is `panel:HDMI_1` (GTV, 60 Hz UI plane) or
`panel:HDMI_2` (Bbox, 50 Hz UI plane), panel lit. The July-condition arm
has the GTV cabled to HDMI_1 with the panel showing the Bbox. Encode
side is out of scope (Pouli et al. #4941).

## 3. Findings

### F1 — With playback verified, hardware decode on both boxes costs +0.25 to +0.51 W for every covered codec

- **Claim:** at Meridian 1080p59.94, panel lit, the player verified
  PLAYING and the hardware decoder logged, the marginal power is:

  | Device | H.264 | HEVC | AV1 |
  |---|---|---|---|
  | GTV (MT8696) | +0.468 W (sd 0.107) | +0.506 W (sd 0.040) | +0.427 W (sd 0.041) |
  | Bbox (Marvell) | +0.331 W (sd 0.025) | +0.249 W (sd 0.043) | see F2 |

  - Decoders logged:
    - GTV: `c2.mtk.avc` / `c2.mtk.hevc` / `c2.mtk.av1`.
    - Bbox: `OMX.Berlin.video_decoder.avc` / `.hevc`.
  - Bbox presented fps for H.264 and HEVC: 49.9–50.0 in every sample.
  - The codec spread on each box (0.08 W on the GTV, 0.08 W on the Bbox)
    is smaller than the decode cost itself. The ±0.2 W "noise floor"
    band in Figure 8's caption does not contain any verified
    hardware-decode cell.
- **Traffic Light:** 🟢 Repeatable. n=3 per cell, 17 of 18 rows 🟢 (one
  🟡, Bbox HEVC), sd ≤0.107 W, and playback evidence on every row.
- **Confounds:**
  - One content family only.
  - GTV HEVC was not eye-checked; its evidence is the PLAYING state,
    the hardware decoder, and a power level matching the other codecs.
  - The Bbox presents at 50 Hz from 59.94 fps content, so its numbers
    include frame-rate conversion.
  - Box idle levels differ from July (GTV baseline 1.18–1.24 W today
    against 1.38–1.45 W in July).

### F2 — The Bbox's AV1 row is a failed real-time playback: ~5 fps presented, no hardware decoder

- **Claim:** Meridian AV1 on the Bbox reads **+1.773 W** (sd 0.029, n=3,
  screen) and **+1.765 W** (sd 0.024, n=3, headless with the panel on
  the Bbox).
  - The player reports PLAYING throughout.
  - No video decoder is allocated (software path: Marvell Berlin has no
    AV1 block).
  - Presented frame rate is **4.7–5.2 fps** in every sample of all six
    rows, against 50 fps for H.264/HEVC on the same box. Ben saw the
    slideshow on the panel.
  - The row passes every gate the harness has (PLAYING, alive, 🟢
    confidence). The same trap was found on the W5 (S77).
- **Traffic Light:** 🟢 Repeatable, for "the Bbox cannot play 1080p60
  AV1 in real time, and the row measures that failure". n=6 rows, 8–9
  fps samples per row, sd 0.03 W.
- **Consequence for citable numbers:**
  - C11's "AV1 +1.4 W on an operator CPE with no AV1 block" and the C17
    Bbox AV1 rows (+1.18 to +1.33 W) are the power of a software decoder
    running roughly 10× short of real time. They are **not** a cost of
    watching AV1 on that box; watching was not possible.
  - Whether a lower-rate AV1 stream (e.g. 1080p30, or 720p) plays in
    real time on this box is unmeasured.
- **Confounds:** the SurfaceFlinger read counts frames presented by the
  player's surface. It agrees with the eye check and with the H.264
  control (50 fps) on the same box.

### F3 — July's H.264 rows (Fire TV, GTV) and the GTV's sequential AV1 rows were a paused player, not decode

- **Claim:** every C11 H.264 row on the Fire TV and the GTV (18 rows,
  all three contents, parallel and sequential) sits at idle-level power
  from the first task sample:
  - GTV about 1.42 W, its idle; Fire TV about 1.30 W.
  - Playing today on the same boxes draws 1.67–1.85 W.

  The mechanism, from the harness fix record (wattlab `fec0065`,
  2026-08-16, 16 days after C11):
  - Just Player launched by VIEW intent without `--ei position 0`
    resumes PAUSED at a remembered position when the previous play of
    that file was interrupted.
  - The July harness neither sent `position 0` nor checked PLAYING.
  - H.264 was the only codec served as the 60-minute file, and the C11
    duration study had just played those files for 59 minutes, during
    which the GTV slept (20-minute sleep timer) and the Fire TV
    screensaved (5 minutes).
  - The GTV's sequential AV1 rows followed the parallel AV1 rows in
    which it fell asleep mid-file (F4). They sit flat at idle
    (1.41–1.42 W).
- **Reproduction (today, both boxes, n=1 per box):** play the 60-minute
  H.264 file, put the box to sleep mid-play, wake it, then relaunch with
  the July command. Watts come from the rig's 3 s plug poll.

  | Step | GTV mean W (n polls) | player | Fire TV mean W (n polls) | player |
  |---|---|---|---|---|
  | idle, home screen (after wake) | 1.500 (14) | — | 1.638 (14) | — |
  | **July relaunch, no `position 0`** | **1.459 (26)** | **PAUSED** | **1.398 (28)** | **PAUSED** |
  | today's relaunch, `position 0` | 1.853 (19) | PLAYING | 1.805 (19) | PLAYING |

  The July launch comes up PAUSED at or below idle; the fixed launch
  plays. On the Fire TV the paused screen draws less than the home
  screen, which is the sign of July's −0.12 to −0.20 W. The size of that
  difference today is not resolved: the home-screen idle sd is 0.55 W
  over 14 polls.
- **Traffic Light:** 🟡 Early Insight. The mechanism was reproduced
  once per box (below the n=3 bar). The July signature is uniform across
  all 18 H.264 rows plus the sequential AV1 rows. That the July rows are
  not decode measurements is supported independently by their
  idle-level traces.
- **Confounds:** the reproduction interrupts playback with a forced
  sleep, not with the July timers themselves.

### F4 — The GTV's parallel AV1 rows (−0.39 to −0.41 W) are a box that fell asleep about 9 s into playback; the trigger is unidentified

- **Claim:** in all three C11 `B_all` AV1 rows:
  - The GTV draws 1.7–2.1 W (playing) for the first ~3–4 s of the task
    window, about 9 s after launch.
  - It then falls to 1.1 W and holds 0.98–1.02 W to the end.
  - Its steady sleep level, measured today, is 0.8–1.1 W (mWakefulness
    = Asleep).

  The Lab-E trace shows no C2 event at the drop (flat 47 W on Meridian),
  so the drop is not tied to the C2 changing input. Setting the GTV's
  CEC rule back to the July `standby_now` and switching the panel away
  during AV1 playback did **not** make it sleep today (1.872 W, awake,
  90 s). The GTV reports its CEC state as inactive, so it may never have
  been the active source.
- **Traffic Light:** 🟡 for "asleep" (level matches, 3 of 3 July rows);
  🔴 Need More Data for the trigger.
- **Confounds:** GTV firmware and player build differ between July
  (Just Player 0.212-legacy) and today, not recorded per date. The
  20-minute inattentive sleep timer, already overdue in July, is an
  untested candidate.

### F5 — Panel standby does not explain Figure 8 (item 1a, query of existing data)

- **Claim:** of the 253 Fire TV / GTV / Bbox rows in C11 `B_*`, C17
  (`20260817b9c0de`), C18 (`20260818ae7ba7b0`) and F9 (`f9d026082401`),
  **all ran headless, so none carries a Lab-E context trace.**
  - Lab-E is on record only where the C2 was a concurrent device in the
    same job: C11 `B_all` (27 rows) and C17 (87 rows). In those rows the
    C2 was lit, playing natively on its own input, with no standby
    reading and no baseline-to-task transition.
  - C11 `B_seq` (27), C18 (89) and F9 (20) have no Lab-E record at all.
  - Splitting C11 by panel record changes nothing that Figure 8 shows,
    except GTV AV1, where the split is the F4 sleep:

    | C11 cell | ΔW, C2 lit (n=3) | ΔW, no record (n=3) |
    |---|---|---|
    | Fire TV H.264 | −0.155 | −0.156 |
    | Fire TV HEVC | +0.399 | +0.362 |
    | Fire TV AV1 | +0.388 | +0.373 |
    | GTV HEVC | +0.411 | +0.499 |
    | GTV AV1 | −0.398 | +0.037 |
    | Bbox AV1 | +1.329 | +1.389 |
- **Traffic Light:** 🟡 Early Insight. Half the rows have no panel
  record; the split rests on n=3 per half.
- **Also:** Figure 8 was n=2 per content family (one parallel plus one
  sequential run), below the n=3 bar.

### F6 — Whether the GTV's input is on screen makes no difference to its AV1 decode cost, with the CEC rule pinned

- **Claim:** GTV AV1 with its input on screen reads +0.427 W (sd 0.041,
  n=3); cabled but unwatched (panel on the Bbox, the July-condition arm)
  it reads +0.447 W (sd 0.071, n=3). Every row was PLAYING and flat,
  with no sleep.
- **Traffic Light:** 🟢 Repeatable (n=3 each, all rows 🟢, difference
  0.02 W < sd).
- **Confounds:** today's harness pins CEC active-source-lost to `none`
  and the sleep timers off. The July condition is reproduced for the
  sink, not for those settings.

## 4. Anomalies and open questions

- **Not every negative is explained by playback failure.**
  - **C17 Bbox, 10 rows (−0.03 to −0.40 W), 7 of them Kranjska:**
    PLAYING was recorded mid-window. The August logger never captured
    the Bbox's video decoder name (audio only, on every C17 Bbox row,
    positive or negative), so there is no further playback evidence.
    Candidate explanation: a genuine near-zero marginal on dark content
    against a home-screen baseline that draws more. **Resolving run:**
    Bbox × Kranjska × H.264/HEVC/VP9, n=3, screen mode, fps sampled.
  - **F9 Fire TV, 2 of 11 rows (−0.46, −0.24 W):** PLAYING recorded, but
    the baselines are contaminated (2.2–2.4 W against a ~1.4 W idle;
    one baseline falling from 2.24 to 1.44 W within its 20 samples).
    This is a baseline defect, not a playback failure. The F9 amendment
    in the C11 digest should say so or drop the two rows.
  - **C17 Fire TV Kranjska HEVC (−0.127 W):** PAUSED mid-window (after
    the August fix; the player paused after a verified start). Invalid
    row.
  - **C11 Bbox H.264 (−0.749 W):** the idle guard timed out at 30 s with
    the baseline still falling (7.53 → 6.24 W over the task). Other C11
    Bbox H.264/HEVC negatives sit inside the Bbox's known idle drift
    (C11 Q9).
- **Figure 8's caption band (±0.2 W) is wrong for hardware decode**, and
  so are the Fire TV H.264 and GTV AV1 bars. The Fire TV and GTV HEVC
  and AV1 C11 bars look valid (1.7–2.1 W while playing). The Pi 5 rows
  (software decode, `ffmpeg` to null) are unaffected by the Just Player
  defect.
- **The 2026-08-30 figure sweep's "checked, clean" verdict on the codec
  matrix (RUN_QUEUE, 2026-08-30 block) is overturned.** It tested window
  length against the sleep and screensaver thresholds, which was correct
  for those timers, but the pre-fix harness could also start a row
  PAUSED, which window length does not reveal.
- **Every software-fallback cell in the paper now needs a frame-rate
  check before it is cited as a decode cost:**
  - Bbox AV1 (C11, C17): answered, fails (F2).
  - W5 AV1 (S77): known, fails (1.3–1.7 fps).
  - Apple TV AV1/VP9 (C19, C24): unanswered (handoff item 3).
- **Idle levels moved since July:** GTV baseline 1.41 → 1.18–1.24 W;
  Fire TV home screen 1.45 → 1.64–1.67 W (noisy). Firmware, launcher,
  or sink state; not investigated. Cross-campaign absolute watts on
  these boxes should not be compared.
- **The GTV's presented frame rate is not remotely measurable** (sideband
  video path). Any future GTV row that needs an fps check needs eyes on
  the panel, or a capture device.
- **Rig state left by this campaign:** GTV on HDMI_1 (sink
  `panel:HDMI_1`), W5 on a dummy (`dummy`). Live `settings.json`
  (`rig_hdmi_inputs`, `rig_sinks`) matches. Rows from other campaigns
  after 2026-09-27 must record their sink accordingly.

## 5. Figure manifest

- `figures/fig_c25_codec_matrix.{svg,png}`. **Replaces Figure 8**
  (`fig_c11_f7_f11_codec_matrix`, retired: removed from the working
  repository, kept and marked RETIRED in the public evidence pack's
  `figures/` for the record; the correction is in the paper's Table 2). It shows marginal decode power by codec on the GTV and the
  Bbox: Meridian 1080p59.94, playback verified, panel lit, n=3 per bar.
  Hollow diamonds show the same cells as C11 measured them. The hatched
  bar is software decode at ~5 fps.

      /srv/data/owl/figenv/bin/python figures/make_c25_figures.py

  The draft's image link (`drafts/04-findings.md` Figure 8) needs
  re-pointing, which is a writing-desk task. The figure covers two
  boxes and one content family, not Figure 8's four boxes × three
  families: the full one-campaign re-run of every Figure 8 cell
  (handoff 1b) was not run.

## 6. Provenance

- **Raw data (GoS1 only):**
  - `/srv/data/owl/results/decode/2026-09-27_{job}.json` (21 envelopes,
    batch `20260927d1a6`; job ids in the CSV).
  - `/srv/data/owl/campaign_2026-09-27_rediag/{jobs,fps,repro}.jsonl`.
  - C11 `/srv/data/owl/campaign_2026-07-31/results.jsonl` plus envelopes.
- **Scripts (this repo), all run on GoS1:**
  - `analysis/c25_fig8_panel_state.py` (F5):
    `python3 analysis/c25_fig8_panel_state.py [--csv OUT]`.
  - `analysis/c25_rediag_feeder.py` (F1, F2, F6): ran the 21 rows.
  - `analysis/c25_rediag_summary.py` (F1, F2, F6, and the CSV):
    `python3 analysis/c25_rediag_summary.py --csv digests/2026-09-c25-decode-rediag.csv`.
  - `analysis/c25_repro_july_negatives.py` (F3, F4):
    `python3 analysis/c25_repro_july_negatives.py t1:gtv t2`, then
    `... t1:firestick`.
  - F4 sleep level: GTV `input keyevent KEYCODE_SLEEP`, rig plug poll,
    20 reads at 3 s (0.76–1.17 W; the first two reads were in
    transition).
- **Code:** wattlab `d242579` (harness protocol v3, keep-awake and
  PLAYING check from `fec0065`). Mechanism record: wattlab `fec0065`
  commit message.
- **Summary CSV:** `digests/2026-09-c25-decode-rediag.csv` (one row per
  arm × device × codec; summary statistics only).
- **Analysis date:** 2026-09-27.
