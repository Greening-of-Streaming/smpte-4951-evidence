#!/usr/bin/env python3
"""make_c11_figures.py — C11 decode-rig figure candidates for SMPTE #4951.

Runs ON GoS1 (reads the campaign raw store; raw data never leaves the box —
only these rendered figures are committed). Reproduce with:

    /srv/data/owl/figenv/bin/python figures/make_c11_figures.py

Outputs (SVG + 300-dpi PNG side by side, light mode / print):
  fig_c11_f1_ladder          — cross-silicon playback ladder (C11 F1)
  fig_c11_f7_f11_codec_matrix — codec x silicon ΔW matrix (C11 F7/F11)
  fig_c11_f9_duration        — ΔW + confidence vs window length (C11 F9)

Sources:
  /srv/data/owl/campaign_2026-07-31/results.jsonl   (08-01 66-cell campaign)
  /srv/data/owl/results/decode/*_{357b087d,606d5ad3,d99775a0,ea55f33b}.json
                                                    (F1 screen-mode ladder)
"""
import glob
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
CAMPAIGN = Path("/srv/data/owl/campaign_2026-07-31/results.jsonl")
DECODE_DIR = Path("/srv/data/owl/results/decode")

# dataviz reference palette (light mode), categorical slots 1-3 in fixed
# order: H.264 -> blue, HEVC -> orange, AV1 -> aqua. First three slots
# validate all-pairs; text wears text tokens, never series color.
C_H264, C_HEVC, C_AV1 = "#2a78d6", "#eb6834", "#1baf7a"
CODEC_COLOR = {"h264": C_H264, "h265": C_HEVC, "av1": C_AV1}
CODEC_LABEL = {"h264": "H.264", "h265": "HEVC", "av1": "AV1"}
TEXT_1, TEXT_2, GRID = "#0b0b0b", "#52514e", "#e5e4e0"
SURFACE = "#ffffff"
# Device series (F9 lines, adjacent pairlist): slots 1-5.
DEV_COLOR = {"pi5": "#2a78d6", "firestick": "#eb6834", "gtv": "#1baf7a",
             "bbox": "#eda100", "c2": "#e87ba4"}
DEV_LABEL = {"pi5": "Pi 5 (sw decode)", "firestick": "Fire TV Stick 4K",
             "gtv": "Google TV Streamer", "bbox": "Bbox 4K (operator CPE)",
             "c2": "LG C2 (native)"}

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "text.color": TEXT_1, "axes.edgecolor": GRID, "axes.labelcolor": TEXT_2,
    "xtick.color": TEXT_2, "ytick.color": TEXT_2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "svg.fonttype": "none",
})


def load_campaign():
    """results.jsonl rows; duplicated cell keys = re-runs, last wins."""
    by_key = {}
    with open(CAMPAIGN) as f:
        for line in f:
            r = json.loads(line)
            by_key[r["cell"]["key"]] = r
    return by_key


def flag_of(row):
    lab = ((row.get("confidence") or {}).get("label") or "").lower()
    if "repeatable" in lab:
        return "green"
    if "early" in lab:
        return "yellow"
    return "red"


def save(fig, stem):
    for ext, kw in (("svg", {}), ("png", {"dpi": 300})):
        fig.savefig(HERE / f"{stem}.{ext}", bbox_inches="tight", **kw)
    plt.close(fig)
    print(f"wrote {stem}.svg/.png")


# --- F1: cross-silicon playback ladder --------------------------------------

def fig_f1():
    runs = []  # (label, run_id)
    spec = [("Google TV Streamer\n(hw decode, local file)", "357b087d"),
            ("Pi 400 — hw decode\n(v4l2m2m-copy)", "606d5ad3"),
            ("Pi 400 — sw decode", "d99775a0"),
            ("Pi 5 — sw decode\n(no hw block)", "ea55f33b")]
    for label, rid in spec:
        path = glob.glob(str(DECODE_DIR / f"*_{rid}.json"))[0]
        env = json.load(open(path))
        row = env["runs"][0]
        runs.append((label, row["delta_w"],
                     (row.get("confidence") or {}).get("ci_delta_w_95")))
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ys = range(len(runs))[::-1]
    base = runs[0][1]
    for y, (label, dw, ci) in zip(ys, runs):
        ax.barh(y, dw, height=0.55, color=C_H264, zorder=3)
        if ci:
            ax.plot(ci, [y, y], color=TEXT_1, lw=1.0, zorder=4,
                    solid_capstyle="butt")
        anchor = max(dw, ci[1]) if ci else dw
        ax.annotate(f"+{dw:.2f} W", (anchor, y), xytext=(6, 0),
                    textcoords="offset points", va="center", color=TEXT_1,
                    fontsize=9, fontweight="bold")
        if dw != base:
            ax.annotate(f"{dw / base:.1f}x", (0.03, y), va="center",
                        color="#ffffff", fontsize=8, fontweight="bold",
                        zorder=5)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in runs], fontsize=8.5)
    ax.set_xlabel("ΔW over device idle (W)")
    ax.set_xlim(0, 2.45)
    ax.grid(axis="y", visible=False)
    ax.set_title("Same clip, same protocol: playback power by silicon\n"
                 "BBB 1080p60 H.264 · display attached · marker-verified · "
                 "all rows Repeatable (green)", fontsize=9, loc="left", color=TEXT_1)
    save(fig, "fig_c11_f1_ladder")


# --- F7/F11: codec x silicon matrix ------------------------------------------

def fig_f7(by_key):
    devices = ["pi5", "firestick", "gtv", "bbox"]   # C2 excluded (F8: panel
    # baseline unstable; its rows diverge and are explicitly uncitable)
    fams = ["bbb", "meridian", "kranjska"]
    codecs = ["h264", "h265", "av1"]
    # per device x codec: family means over the parallel + sequential runs
    vals = {}
    for dev in devices:
        for cod in codecs:
            fam_means = []
            for fam in fams:
                pts = []
                for key in (f"B_all_{fam}_{cod}", f"B_seq_{fam}_{cod}_{dev}"):
                    row = (by_key.get(key) or {}).get("rows", {}).get(dev)
                    if row and row.get("delta_w") is not None:
                        pts.append(row["delta_w"])
                if pts:
                    fam_means.append(sum(pts) / len(pts))
            vals[(dev, cod)] = fam_means
    fig, ax = plt.subplots(figsize=(6.4, 3.1))
    width, gap = 0.24, 0.04
    for gi, dev in enumerate(devices):
        for ci, cod in enumerate(codecs):
            x = gi + (ci - 1) * (width + gap)
            fam_means = vals[(dev, cod)]
            mean = sum(fam_means) / len(fam_means)
            ax.bar(x, mean, width=width, color=CODEC_COLOR[cod], zorder=3)
            ax.plot([x] * len(fam_means), fam_means, ls="none", marker="o",
                    ms=3.4, mfc="white", mec=TEXT_1, mew=0.7, zorder=4)
            if mean > 0.28:
                ax.annotate(f"{mean:.1f}", (x, max([mean] + fam_means)),
                            xytext=(0, 5), textcoords="offset points",
                            ha="center", fontsize=7.5, color=TEXT_2)
    ax.axhspan(-0.2, 0.2, color=GRID, alpha=0.55, zorder=1)
    ax.annotate("±0.2 W\nnoise floor", (0.5, 0), fontsize=7,
                color=TEXT_2, ha="center", va="center")
    ax.set_xticks(range(len(devices)))
    short = {"pi5": "Pi 5 (sw decode)", "firestick": "Fire TV Stick",
             "gtv": "Google TV", "bbox": "Bbox 4K (CPE)"}
    ax.set_xticklabels([short[d] for d in devices], fontsize=8.5)
    ax.set_ylabel("ΔW over device idle (W)")
    ax.grid(axis="x", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=CODEC_COLOR[c])
               for c in codecs]
    ax.legend(handles, [CODEC_LABEL[c] for c in codecs], frameon=False,
              fontsize=8.5, loc="upper right", ncol=3)
    ax.set_title("Codec cost is a property of silicon coverage\n"
                 "1080p matched-VMAF (~92–93) · 150 s cells · dots = content "
                 "families (mean of parallel + sequential runs)",
                 fontsize=9, loc="left", color=TEXT_1)
    save(fig, "fig_c11_f7_f11_codec_matrix")


# --- F9: confidence vs run length --------------------------------------------

def fig_f9(by_key):
    durs = [30, 300, 1200, 3540]
    fams = ["bbb", "meridian", "kranjska"]
    # C2 excluded: its panel-signed rows (+16 / −3 W, F8) are a different
    # finding and an order of magnitude off this axis.
    devices = ["pi5", "firestick", "gtv", "bbox"]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.9), sharey=True)
    flag_mfc = {"green": None, "yellow": "#ffffff", "red": "#ffffff"}
    for ax, fam in zip(axes, fams):
        for dev in devices:
            xs, ys, flags = [], [], []
            for d in durs:
                row = ((by_key.get(f"A_dur{d}_{fam}") or {})
                       .get("rows", {}).get(dev))
                if row and row.get("delta_w") is not None:
                    xs.append(d)
                    ys.append(row["delta_w"])
                    flags.append(flag_of(row))
            col = DEV_COLOR[dev]
            ax.plot(xs, ys, color=col, lw=1.6, zorder=3)
            for x, y, fl in zip(xs, ys, flags):
                mfc = col if fl == "green" else "#ffffff"
                mark = "o" if fl != "red" else "X"
                ax.plot([x], [y], marker=mark, ms=5.5 if fl != "red" else 6.5,
                        mfc=mfc, mec=col, mew=1.2, zorder=4)
        ax.set_xscale("log")
        ax.set_xticks(durs)
        ax.set_xticklabels(["30 s", "5 m", "20 m", "59 m"], fontsize=8)
        ax.minorticks_off()
        ax.axhline(0, color=TEXT_2, lw=0.7, zorder=2)
        ax.set_title(fam.capitalize() if fam != "bbb" else "Big Buck Bunny",
                     fontsize=9, color=TEXT_1)
    axes[0].set_ylabel("ΔW over device idle (W)")
    axes[1].set_xlabel("sampled window (log scale) — H.264 1080p, HTTP delivery")
    handles = [plt.Line2D([], [], color=DEV_COLOR[d], lw=1.6,
                          label=DEV_LABEL[d]) for d in devices]
    handles += [plt.Line2D([], [], color=TEXT_2, ls="none", marker="o",
                           mfc=TEXT_2, label="filled = Repeatable (green)"),
                plt.Line2D([], [], color=TEXT_2, ls="none", marker="o",
                           mfc="#ffffff", label="open = Early Insight (yellow)"),
                plt.Line2D([], [], color=TEXT_2, ls="none", marker="X",
                           mfc="#ffffff", label="X = Need More Data (red)")]
    fig.legend(handles=handles, frameon=False, fontsize=7.5,
               loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=4)
    fig.suptitle("A real signal is confident at 30 s; a null cannot be "
                 "rescued by run length; small margins degrade over an hour",
                 fontsize=9.5, x=0.02, ha="left", color=TEXT_1)
    fig.tight_layout(rect=(0, 0.02, 1, 0.93))
    save(fig, "fig_c11_f9_duration")


if __name__ == "__main__":
    by_key = load_campaign()
    fig_f1()
    fig_f7(by_key)
    fig_f9(by_key)
