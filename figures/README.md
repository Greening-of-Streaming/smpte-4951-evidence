figures generated on GoS1 land here (SVG preferred)

## fig_c25_codec_matrix.svg / .png — Figure 7: marginal decode power, playback verified (2026-09-27)

C25 (`digests/2026-09-c25-decode-rediag.md`). GTV and Bbox × H.264 /
HEVC / AV1, Meridian 1080p59.94, screen mode (display lit on the box's
own input), player verified PLAYING, n=3 per bar (batch
`20260927d1a6`). The hatched bar is the Bbox's software AV1 decode,
presenting ~5 fps. The July C11 values (hollow diamonds in the first
render) were removed on 2026-09-27 at Ben's request: withdrawn results
are reported once, in Table 2. The committed render (600 dpi) was made
on the MacBook from the published digest CSV:

    python3 figures/make_c25_figures.py --csv digests/2026-09-c25-decode-rediag.csv

The same figure from GoS1's raw store:

    /srv/data/owl/figenv/bin/python figures/make_c25_figures.py

## fig_c11_f7_f11_codec_matrix.svg / .png — RETIRED 2026-09-27

The old Figure 8 (C11 codec × silicon matrix, `make_c11_figures.py`
`fig_f7`). Its H.264 and GTV AV1 cells were paused-player or
sleeping-box rows (C25 F3/F4), and its ±0.2 W band does not contain
hardware decode. Replaced by `fig_c25_codec_matrix`. History in git.
`make_c11_figures.py` still regenerates it if run; do not re-add it.

## fig_architecture.svg / .png — RETIRED 2026-09-27

Replaced by `fig_measurement.svg` (Figure 1) and `fig_owl_architecture.svg`
(Section 3); the all-in-one drawing was too dense and its PNG render was
clipped. History in git.

## fig_sequence.svg / .png — the test sequence at two cadences (2026-08-26)

Composed on the MacBook from slides 2 and 3 of
`sources/2026-03_simon-jones_rem-tv-settings-v1.pptx` (Simon Jones,
March 2026), exported by Ben with background graphics and slide numbers
hidden. The SVG embeds the two cropped panels as data URIs, so it is
self-contained; the PNG is a render of it.

    # crop each exported slide to its content (sips takes -c H W, offset Y X)
    sips -c 1240 2980 --cropOffset 210 80 Slide2.png --out pa.png
    sips -c 1100 2980 --cropOffset 210 80 Slide3.png --out pb.png
    # build the SVG with both panels base64-embedded, then render it
    # (external image refs do not load in SVG-as-image, hence data URIs)
    qlmanage -t -s 3000 -o . wseq.html      # wrapper: 1000x1000 flex-centered
    sips -c 2535 3000 wseq.html.png --out figures/fig_sequence.png

Edit the SVG's text and geometry directly; to change the crops, redo the
sips step and rebuild. Full-resolution slide exports are not in the
repo — re-export from the .pptx in `sources/`.

## fig_deck_ladder.png — bitrate ladder, four boxes (deck figure, 2026-09-10)

Not a paper figure. Made for the IBC 2026 deck (slide 5, "no knee").
Data transcribed from the wattlab lab doc
`docs/intra_content_sync_2026-09-03.md` §5f (batch `bae281b52f90`,
n=3, wattlab commit 42a41b6); not yet a C-numbered campaign. Rendered on
the MacBook:

    /Applications/Xcode.app/Contents/Developer/usr/bin/python3 figures/make_deck_ladder_figure.py

## fig_measurement.svg / .pdf / .png — Figure 1 candidate: the measurement architecture (2026-09-27)

Hand-authored SVG from Ben's sketch (`sources/collection.pptx`): the
measured devices behind one plug each, the plug read two ways (vendor
cloud at 10 s / integer watts; LEM on the participant's LAN down to 1 s /
milliwatts, back-filled into the REM store), the November 2025 server
PDU path, and the measurement boundary. OWL appears only as a footnote;
its own diagram is a separate figure. Replaces the single all-in-one
`fig_architecture.svg`, whose PNG render was clipped.

Render on the MacBook (LibreOffice for the vector PDF, poppler for the
600 dpi line-art PNG; qlmanage is no longer used because it clipped):

    cd <scratch> && cp figures/fig_measurement.svg . \
      && soffice --headless --convert-to pdf fig_measurement.svg \
      && pdftoppm -r 600 -png -singlefile fig_measurement.pdf fig_measurement \
      && cp fig_measurement.pdf fig_measurement.png <repo>/figures/

LibreOffice substitutes fonts by name; the SVG names Arial first so the
render matches the deck.

## fig_owl_architecture.svg / .pdf / .png — OWL: host and client decode rig (2026-09-27)

Hand-authored SVG for Section 3 (the "Figure 5, to be produced" placeholder
in `drafts/03-owl.md`): the measurement host behind two P110 meters in
series, the dedicated measurement mode, the per-run envelope (idle guard,
baseline, workload, confidence flag) and the results store; the client
decode rig as eight metered slots per Table 1 plus one generic slot for
devices added since (Xiaomi Gen 2 and Gen 3 at the time of drawing), the LG C2 in its own slot
as both shared display and device under test, the bench LAN carrying
content from the origin on the host and per-device control, and the
marker head every clip carries. Same render command as fig_measurement:

    cd <scratch> && cp figures/fig_owl_architecture.svg . \
      && soffice --headless --convert-to pdf fig_owl_architecture.svg \
      && pdftoppm -r 600 -png -singlefile fig_owl_architecture.pdf fig_owl_architecture \
      && cp fig_owl_architecture.pdf fig_owl_architecture.png <repo>/figures/

## fig_loop.svg / .pdf / .png — Figure 6: the dual-track loop (2026-09-27)

Hand-authored SVG for the opening of Section 4: the two tracks as
nodes, the hand-offs in each direction (§4.3), the instrument-scale
axle (C8 F2), and the three turns as a timeline (November 2025, July
2026, the queued operator-box campaign) with their statuses. Its
insertion renumbered the device-class ladder from Figure 7 to Figure 9;
the codec matrix stays Figure 8, which also restores order-of-first-
reference numbering in §4.2. Same render command as fig_measurement,
with `fig_loop` in place of the name.

## 2026-09-27 text edits to fig_loop and fig_owl_architecture (V1.0 alignment)

Found while building the talk deck: both hand-authored SVGs still carried
pre-V1.0 wording. fig_loop: "panel luminance, 60 to 130 W" -> "display
luminance, 10 to 25 W under content"; Cycle 1 bench line no longer quotes an
encode ratio absent from the paper ("NVENC 2.5 to 4.4 times"), cites [3]
instead; Cycle 2 bench line drops the withdrawn "1.2 to 1.4 W in software
fallback (AV1 on an operator box)" for "over 1 W in software, or the stream
does not play"; turn 3 reads "failed playback, or a cost" and "hardware AV1
across vendors". fig_owl_architecture: Table 1 is nine devices, not eight;
generic slot "W5, Xiaomi Gen 3, others" (Gen 2 retired); "panel" -> "display".
Re-rendered with the render command above (soffice, pdftoppm -r 600).

## deck/ — charts for the SMPTE MTS 2026 talk (not paper figures)

`deck_scale`, `deck_w5`, `deck_software`, `deck_rungs`, `deck_trap`,
`deck_network`: every value typed in from its digest, tagged in the script.

    python3 figures/deck/make_deck_figures.py

`deck_c8_two_panels.png` is the top two panels of `fig_c8_dual_capture.png`
(PIL crop, rows 6.8%–65.5% of the height, truncated to whole pixels; used by
talks/mts2026/build_deck.py, slide 7). Scripted 2026-09-30; the script
reproduces the earlier hand crop of the 160-dpi figure pixel for pixel. Now
6600×3346 from the 600-dpi Figure 3:

    python3 figures/deck/make_c8_two_panels.py

## fig_c8_dual_capture.png / .svg — Figure 3: R2 dual capture (C8), 600 dpi (2026-09-30)

Rendered on GoS1 from the raw store: bench per-run JSONs, the LEM CSV and
the REM export under `/srv/data/owl/r2-dual-capture/`. Jobs: `7d82cb7d`
(GTV, Pi 400) and C2 `75d7e183`.

    /srv/data/owl/figures-venv/bin/python figures/make_c8_dual_capture_figure.py 75d7e183

`--dpi` defaults to 600 (it was a hard-coded 160 until 2026-09-30, i.e.
1760×1520 px). The PNG is now 6600×5700 px: 11 × 9.5 in at 600 dpi,
about 1,015 dpi as placed at 6.5 in. The script also writes an SVG, so
later edits need no raw store. Same data and text as before: `--dpi 160`
reproduces the previously committed PNG byte for byte, and all 46 SVG text
labels match.

## 2026-09-28 text edits to fig_c11_f9_duration_v2 (Figure 6), from Dom's review

Title "green in seconds" -> "confident within seconds" (Dom's comment on the
V1.0 Doc). Legend relabelled: the markers are per-run confidence flags, not
the paper's Traffic Light finding statuses ("filled: confident run / open:
marginal run / X: run not distinguishable from idle"). "panel dark" ->
"display dark"; "keep_awake pinned" -> "sleep timers pinned"; em-dashes out.
Edited in both the SVG and make_f9_rerun_figure.py (so a GoS1 re-render
matches); PNG re-rendered from the SVG on the MacBook, data unchanged:

    soffice --headless --convert-to pdf fig_c11_f9_duration_v2.svg \
      && pdftoppm -r 300 -png -singlefile fig_c11_f9_duration_v2.pdf fig_c11_f9_duration_v2


## 2026-09-28 figure renumbering

The never-produced Figure 2 placeholder was dropped from §2.2 (Ben, 2026-09-28);
Figures 3–8 became 2–7: sequence 2, dual capture 3, OWL architecture 4,
window length 5, loop 6, codec matrix 7. Headings above updated where they
named a number.

## 2026-09-30 — talk deck master moved to Drive

Ben edited the MTS 2026 deck in Google Slides (Affiliate Members slide,
backup slide 26, retitled slides), so the Drive copy
`SMPTE-4951/SMPTE-4951_MTS2026.pptx` is now the master and
`talks/mts2026/build_deck.py` is historical: rebuilding would drop his
edits. Changes are applied to the Drive master by scripts such as
`talks/mts2026/edit_deck_2026-09-30.py`. Added: `deck/make_qr.py`
(`qr_github.png`, `qr_website.png`: segno, error correction H, GS badge in
the centre, both verified to decode at 150 px). `deck_rungs.png`: the
1080p60 label now reads "~5 of 60 fps" (content rate), matching the paper.
