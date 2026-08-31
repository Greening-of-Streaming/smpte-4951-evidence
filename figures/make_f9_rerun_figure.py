#!/usr/bin/env python3
"""fig_c11_f9_duration_v2 — F9 duration study RE-RUN (2026-08-24, keep_awake
pinned, batch f9d026082401). Replaces fig_c11_f9_duration, whose long-window
STB legs were sleep-timer artefacts (C11 F9 amendment).

Source: /srv/data/owl/results/decode/2026-08-24_<job>.json on GoS1.
Command: /srv/data/owl/figures-venv/bin/python make_f9_rerun_figure.py   (run on GoS1)
Style: follows make_c11_figures.py (dataviz reference palette; filled=green,
open=yellow, X=red; text wears text tokens, never series color).
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DECODE = Path("/srv/data/owl/results/decode")
# valid rows only — discards per campaign_2026-08-24_r16b/NOTES.txt
VALID = {"9393f686": ["gtv"], "139f4979": ["gtv"],
         "a7dff199": ["gtv", "firestick"], "8f9719be": ["gtv", "firestick"],
         "454086d3": ["gtv", "firestick"], "7f195277": ["gtv", "firestick"],
         "8141abb4": ["gtv", "firestick"], "0f4f7cd4": ["firestick"],
         "924ae582": ["firestick", "pi5"], "b4264c56": ["pi5"],
         "0c73392a": ["gtv", "firestick"], "1e8d2132": ["pi5"],
         "0a88b387": ["pi5"]}
DEV_COLOR = {"pi5": "#2a78d6", "firestick": "#eb6834", "gtv": "#1baf7a"}
DEV_LABEL = {"pi5": "Pi 5 (sw decode, headless)",
             "firestick": "Fire TV Stick 4K (panel dark)",
             "gtv": "Google TV Streamer"}
TEXT_1, TEXT_2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e5e4e0", "#ffffff"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9,
    "text.color": TEXT_1, "axes.edgecolor": GRID, "axes.labelcolor": TEXT_2,
    "xtick.color": TEXT_2, "ytick.color": TEXT_2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "axes.axisbelow": True, "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "svg.fonttype": "none"})

pts = {}   # dev -> list[(window, dw, flag)]
for jid, devs in VALID.items():
    d = json.load(open(DECODE / f"2026-08-24_{jid}.json"))
    for dev in devs:
        for r in d["devices"][dev]["rows"]:
            fl = (r.get("confidence") or {}).get("label", "")
            flag = {"repeatable": "green", "early insight": "yellow"}.get(fl.lower(), "red")
            pts.setdefault(dev, []).append((r["window_s"], r["delta_w"], flag))

durs = [30, 300, 1200, 3540]
fig, ax = plt.subplots(figsize=(7.6, 4.1))
for dev in ("pi5", "gtv", "firestick"):
    col = DEV_COLOR[dev]
    rows = sorted(pts.get(dev, []))
    means = {d: [y for x, y, f in rows if x == d] for d in durs}
    xs = [d for d in durs if means[d]]
    ax.plot(xs, [sum(means[d]) / len(means[d]) for d in xs],
            color=col, lw=1.6, zorder=3)
    for x, y, fl in rows:
        mfc = col if fl == "green" else "#ffffff"
        mark = "o" if fl != "red" else "X"
        ax.plot([x], [y], marker=mark, ms=5.5 if fl != "red" else 6.5,
                mfc=mfc, mec=col, mew=1.2, ls="none", zorder=4)
ax.set_xscale("log"); ax.set_xticks(durs)
ax.set_xticklabels(["30 s", "5 m", "20 m", "59 m"], fontsize=8)
ax.minorticks_off()
ax.axhline(0, color=TEXT_2, lw=0.7, zorder=2)
ax.set_ylabel("ΔW over device idle (W)")
ax.set_xlabel("sampled window (log scale) — BBB H.264 1080p60, HTTP,\n"
              "keep_awake pinned, n=2 per duration", fontsize=8)
handles = [plt.Line2D([], [], color=DEV_COLOR[d], lw=1.6, label=DEV_LABEL[d])
           for d in ("pi5", "gtv", "firestick")]
handles += [plt.Line2D([], [], color=TEXT_2, ls="none", marker="o", mfc=TEXT_2,
                       label="filled = Repeatable"),
            plt.Line2D([], [], color=TEXT_2, ls="none", marker="o",
                       mfc="#ffffff", label="open = Early Insight"),
            plt.Line2D([], [], color=TEXT_2, ls="none", marker="X",
                       mfc="#ffffff", label="X = Need More Data")]
fig.legend(handles=handles, frameon=False, fontsize=7.5, loc="upper center",
           bbox_to_anchor=(0.5, 0.15), ncol=2)
fig.suptitle("Real signals are green in seconds and flat through 59 min;\n"
             "a small margin flickers at every duration — repeats beat length",
             fontsize=9.5, x=0.02, ha="left", color=TEXT_1)
fig.tight_layout(rect=(0, 0.22, 1, 0.87))
for ext in ("svg", "png"):
    fig.savefig(HERE / f"fig_c11_f9_duration_v2.{ext}", dpi=180)
print("saved fig_c11_f9_duration_v2.{svg,png}")
