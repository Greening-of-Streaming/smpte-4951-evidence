#!/usr/bin/env python3
"""make_coupling_figures.py — Tier-3 coupling figures (C13/C14/C15/C16).

Numbers are the campaign means from the digests (raw stores under
/srv/data/owl/campaign_2026-08-0{8,9}_r1{1,2,3,6}/ — see each digest's
provenance). Reproduce with:

    /srv/data/owl/figenv/bin/python figures/make_coupling_figures.py

Outputs (SVG + 300-dpi PNG, light/print):
  fig_coupling_ledgers  — R11 vs R12 mirrored ledgers (C13/C14)
  fig_effort_ladder     — R13 encode Wh vs decode ΔW per corner (C15)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TEXT_1, TEXT_2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e5e4e0", "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "text.color": TEXT_1, "axes.edgecolor": GRID, "axes.labelcolor": TEXT_2,
    "xtick.color": TEXT_2, "ytick.color": TEXT_2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "svg.fonttype": "none",
})


def save(fig, stem):
    for ext, kw in (("svg", {}), ("png", {"dpi": 300})):
        fig.savefig(HERE / f"{stem}.{ext}", bbox_inches="tight", **kw)
    plt.close(fig)
    print(f"wrote {stem}.svg/.png")


def fig_ledgers():
    # (label, R11 FGS-on vs off delta %, R12 CABAC vs CAVLC delta %)
    # positive = the "advanced" option costs more; negative = saves.
    rows = [
        ("Encode energy\n(per title)", 115, 1),      # 2.15x -> +115%; wash -> +1%
        ("Bitrate\n(per view)", -19, -11.5),          # matched quality
        ("SW decode power\n(per view)", 26, 46),      # Pi 5
        ("HW decode power\n(per view)", 0, 0),        # in noise both
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.9), sharey=True)
    titles = [
        "AV1 film-grain synthesis ON vs OFF\n(R11 · Nocturne 1080p60 · CRF 25)",
        "H.264 CABAC vs CAVLC\n(R12 · BBB 1080p60 · 8 Mb/s matched)",
    ]
    for ax, col, title in zip(axes, (1, 2), titles):
        ys = range(len(rows))[::-1]
        for y, r in zip(ys, rows):
            v = r[col]
            color = ORANGE if v > 2 else (AQUA if v < -2 else GRID)
            ax.barh(y, v, height=0.55, color=color, zorder=3)
            lab = f"{v:+.0f}%" if abs(v) > 2 else "≈0"
            ax.annotate(lab, (v, y),
                        xytext=(6 if v >= 0 else -6, 0),
                        textcoords="offset points", va="center",
                        ha="left" if v >= 0 else "right",
                        fontsize=8.5, fontweight="bold", color=TEXT_1)
        ax.axvline(0, color=TEXT_2, lw=0.8)
        ax.set_yticks(list(ys))
        ax.set_yticklabels([r[0] for r in rows], fontsize=8)
        ax.set_xlim(-60, 135)
        ax.grid(axis="y", visible=False)
        ax.set_title(title, fontsize=8.5, loc="left", color=TEXT_1)
    axes[0].set_xlabel("change when the flag is ON (%)")
    axes[1].set_xlabel("change CABAC vs CAVLC (%)")
    fig.suptitle("One encoder flag moves energy between boundaries — "
                 "and the viewer-side term exists only in software",
                 fontsize=9.5, x=0.02, ha="left", color=TEXT_1)
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    save(fig, "fig_coupling_ledgers")


def fig_effort():
    # R13 corners: (label, encode Wh/min, Pi5 decode W, kbps)
    corners = [("refs1/bf0\n(fast-decode)", 0.216, 1.034, 3995),
               ("refs4/bf3\n(x264 default)", 0.292, 1.155, 3808),
               ("refs16/bf8\n(max effort)", 0.498, 1.255, 3646)]
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    for (label, enc, dec, kbps), mstyle in zip(corners, ("o", "s", "D")):
        ax.plot([enc], [dec], marker=mstyle, ms=9, mfc=BLUE, mec=TEXT_1,
                mew=0.8, ls="none", zorder=4)
        ax.annotate(f"{label}\n{kbps} kb/s", (enc, dec), xytext=(10, -4),
                    textcoords="offset points", fontsize=7.5, color=TEXT_2)
    ax.plot([c[1] for c in corners], [c[2] for c in corners],
            color=BLUE, lw=1.2, alpha=0.5, zorder=3)
    ax.set_xlabel("encode energy (Wh per content-minute, GoS1)")
    ax.set_ylabel("Pi 5 software decode ΔW (W)")
    ax.set_xlim(0.15, 0.62)
    ax.set_ylim(0.95, 1.35)
    ax.set_title("Encoder effort leaks to the software decoder\n"
                 "x264 CRF 21, BBB 1080p60, equal quality (NEG spread 0.32) — "
                 "up-and-right = worse on BOTH sides",
                 fontsize=8.5, loc="left", color=TEXT_1)
    save(fig, "fig_effort_ladder")


if __name__ == "__main__":
    fig_ledgers()
    fig_effort()
