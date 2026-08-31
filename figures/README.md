figures generated on GoS1 land here (SVG preferred)

## fig_architecture.svg / .png — the framework architecture (draft, 2026-08-25)

Hand-authored, not generated from data, so it has no reproduction command.
Edit the SVG; the PNG is a render of it.

Palette taken from the GoS deck (`GoS_Deck.pptx.svg`): navy #1f2236,
green #68a06a (dark #56895a, light #b6d3ac), blue #7fb3d5, greys #f6f6f6
/ #e7e6e6 / #aeb3c4. Inverted to a light ground for print; the deck's
dark navy ground is a screen style and costs ink in a journal.

Render (no rsvg/inkscape on the MacBook, so via the preview engine):

    cd <scratch>
    printf '<html><body style="margin:0;background:#fff"><div style="width:1000px;height:563px"><img src="ABS/PATH/figures/fig_architecture.svg" width="1000"></div></body></html>' > w.html
    qlmanage -t -s 2000 -o . w.html
    sips -c 1126 2000 w.html.png --out figures/fig_architecture.png

For submission this needs a proper 600-dpi render (rsvg-convert or
Inkscape on GoS1), or the SVG supplied directly if the author kit takes it.

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
