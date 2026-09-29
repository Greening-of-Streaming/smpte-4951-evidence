#!/usr/bin/env python3
"""make_c25_figures.py — C25 figure for SMPTE #4951 (replaces Figure 8's
C11 codec matrix, fig_c11_f7_f11_codec_matrix, now in git history only).

Two ways to reproduce it:

  on GoS1, from the raw store:
    /srv/data/owl/figenv/bin/python figures/make_c25_figures.py
  anywhere, from the published digest CSV:
    python3 figures/make_c25_figures.py --csv digests/2026-09-c25-decode-rediag.csv

The CSV mode rebuilds each n=3 cell's repeats from its mean, min and max
(middle repeat = 3*mean - min - max, exact up to the CSV's 1 mW rounding).
The two modes draw the same bars.

Output (SVG + 600-dpi PNG, light mode / print):
  fig_c25_codec_matrix — GTV + Bbox x H.264/HEVC/AV1, Meridian 1080p59.94,
      screen mode (display lit on the box's own input), player verified
      PLAYING, n=3 per cell (batch 20260927d1a6). The July C11 values are
      no longer drawn (withdrawn, Table 2; digest C25 F3-F4).

Sources:
  raw:  /srv/data/owl/campaign_2026-09-27_rediag/jobs.jsonl
        /srv/data/owl/results/decode/*_{job}.json   (batch 20260927d1a6)
  csv:  digests/2026-09-c25-decode-rediag.csv (arm = screen)
"""
import argparse
import csv
import glob
import json
import statistics as st
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CAMP = Path("/srv/data/owl/campaign_2026-09-27_rediag")
DEC = Path("/srv/data/owl/results/decode")

# Same codec palette as make_c11_figures.py (dataviz reference slots 1-3;
# validated all-pairs; AV1 green is < 3:1 on white -> every bar is
# direct-labelled with its value).
CODEC_COLOR = {"h264": "#2a78d6", "h265": "#eb6834", "av1": "#1baf7a"}
CODEC_LABEL = {"h264": "H.264", "h265": "HEVC", "av1": "AV1"}
TEXT_1, TEXT_2, GRID = "#0b0b0b", "#52514e", "#e5e4e0"
SURFACE = "#ffffff"
DEVICES = ["gtv", "bbox"]
DEV_LABEL = {"gtv": "Google TV Streamer\n(MediaTek MT8696)",
             "bbox": "Bbox 4K operator CPE\n(Marvell Berlin)"}
CODECS = ["h264", "h265", "av1"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "text.color": TEXT_1, "axes.edgecolor": GRID, "axes.labelcolor": TEXT_2,
    "xtick.color": TEXT_2, "ytick.color": TEXT_2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "svg.fonttype": "none",
})


def c25_cells():
    cells = {}
    for line in open(CAMP / "jobs.jsonl"):
        j = json.loads(line)
        if j["arm"] != "screen" or j["status"] != "done":
            continue
        env = json.load(open(glob.glob(str(DEC / f"*_{j['job_id']}.json"))[0]))
        for r in env["runs"]:
            cells.setdefault((r["device"], j["codec"]), []).append(r["delta_w"])
    return cells


def csv_cells(path):
    cells = {}
    for r in csv.DictReader(open(path)):
        if r["arm"] != "screen":
            continue
        mean, lo, hi = (float(r[k]) for k in ("mean_dw_w", "min_dw_w", "max_dw_w"))
        assert int(r["n"]) == 3
        cells[(r["device"], r["codec"])] = [lo, round(3 * mean - lo - hi, 3), hi]
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="digest CSV instead of the GoS1 raw store")
    args = ap.parse_args()
    new = csv_cells(args.csv) if args.csv else c25_cells()
    fig, ax = plt.subplots(figsize=(6.4, 3.3))
    width, gap = 0.24, 0.04
    for gi, dev in enumerate(DEVICES):
        for ci, cod in enumerate(CODECS):
            x = gi + (ci - 1) * (width + gap)
            v = new[(dev, cod)]
            m = st.mean(v)
            sw = dev == "bbox" and cod == "av1"
            ax.bar(x, m, width=width, color=CODEC_COLOR[cod], zorder=3,
                   hatch="////" if sw else None, edgecolor=SURFACE,
                   linewidth=0.0)
            ax.plot([x] * len(v), v, ls="none", marker="o", ms=3.4,
                    mfc="white", mec=TEXT_1, mew=0.7, zorder=4)
            ax.annotate(f"{m:+.2f}", (x, max(v)), xytext=(0, 4),
                        textcoords="offset points", ha="center",
                        fontsize=7.5, color=TEXT_2)
    ax.axhline(0, color=TEXT_2, lw=0.8, zorder=2)
    ax.annotate("software decode —\nplays at ~5 fps\n(output 50 fps)",
                (1 + width + gap, 1.77), xytext=(18, -32),
                textcoords="offset points", fontsize=7, color=TEXT_2,
                ha="left", arrowprops={"arrowstyle": "-", "color": TEXT_2,
                                       "lw": 0.6})
    ax.set_xticks(range(len(DEVICES)))
    ax.set_xticklabels([DEV_LABEL[d] for d in DEVICES], fontsize=8.5)
    ax.set_xlim(-0.55, 1.95)
    ax.set_ylabel("ΔW over device idle (W)")
    ax.grid(axis="x", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=CODEC_COLOR[c])
               for c in CODECS]
    handles += [plt.Line2D([], [], ls="none", marker="o", ms=3.4,
                           mfc="white", mec=TEXT_1, mew=0.7)]
    labels = [CODEC_LABEL[c] for c in CODECS] + ["repeat (n=3)"]
    ax.legend(handles, labels, frameon=False, fontsize=7.5,
              loc="upper left", ncol=1)
    ax.set_title("Marginal decode power, playback verified\n"
                 "Meridian 1080p59.94 · 150 s windows · display lit on the "
                 "box's input · bars = mean of 3", fontsize=9, loc="left",
                 color=TEXT_1)
    for ext, kw in (("svg", {}), ("png", {"dpi": 600})):
        fig.savefig(HERE / f"fig_c25_codec_matrix.{ext}",
                    bbox_inches="tight", **kw)
    print("wrote fig_c25_codec_matrix.svg/.png")


if __name__ == "__main__":
    main()
