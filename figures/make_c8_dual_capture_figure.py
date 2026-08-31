#!/usr/bin/env python3
"""fig_c8_dual_capture.png — the REM 10-min energy-signature sequence seen by
the bench (1 s, mW) and by REM's two paths on the same plug, per arm.
Run on GoS1: /srv/data/owl/figures-venv/bin/python figures/make_c8_dual_capture_figure.py
Inputs (raw, stay on GoS1): decode-bench per-run JSONs, LEM CSV, gos_rem export
(/srv/data/owl/r2-dual-capture/). Output: figures/fig_c8_dual_capture.png
"""
import glob, json, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

D = '/srv/data/owl/r2-dual-capture/'
BENCH = '/srv/data/owl/decode-bench/results/'
OUT = '/home/gos/dev/smpte-4951/figures/fig_c8_dual_capture.png'
# job ids: (rep-2 headless signature on GTV+Pi 400, first C2 signature job)
ARMS = [('gtv', '7d82cb7d', 'Lab-D', 'Google TV Streamer, Ethernet, headless decode (LAN path: LEM 10 s → REM field API)'),
        ('pi400', '7d82cb7d', 'Lab-B', 'Raspberry Pi 400, software decode (cloud path: TP-Link cloud → REM, 10 s, integer W)'),
        ('c2', sys.argv[1] if len(sys.argv) > 1 else '75d7e183', 'Lab-E', 'LG C2 OLED, native playback, panel metered (LAN path: LEM 10 s → REM)')]
SEG = [(0, 90, 'timer/black'), (90, 120, 'white'), (120, 151, 'black'), (151, 540, 'Meridian content'), (540, 599, 'black')]
SKIP = {'gtv': 8, 'pi400': 8, 'c2': 5}


def epoch(s, fmt=None):
    return (pd.to_datetime(s, utc=True, format=fmt) - pd.Timestamp(0, tz='UTC')).dt.total_seconds()


lem = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(D + 'lem/r2_*_combined.csv'))])
lem['t'] = epoch(lem['timestamp'])
rem = pd.read_csv(D + 'rem_rows.csv'); rem['t'] = epoch(rem['time'], 'ISO8601')

fig, axes = plt.subplots(len(ARMS), 1, figsize=(11, 9.5), sharex=True)
for ax, (dev, job, alias, title) in zip(axes, ARMS):
    fs = glob.glob(BENCH + f'ui-*-{job}-{dev}.json')
    if not fs:
        ax.set_title(title + ' — (no data)'); continue
    r = json.load(open(fs[0]))['rows'][0]
    t = np.array(r['raw_task_t']); w = np.array(r['raw_task_w'])
    tl = t[0] - SKIP[dev]; trel = t - tl
    for a, b, lab in SEG:
        ax.axvspan(a, b, color=('white' if lab == 'white' else ('0.85' if 'black' in lab else '0.95')), alpha=0.6, lw=0)
    ax.plot(trel, w, lw=0.8, color='C0', label='bench 1 s / mW (local)')
    src = rem if dev == 'pi400' else lem
    col = 'power_watts' if dev == 'pi400' else 'power_w'
    d = src[(src.alias == alias) & (src.t >= t[0] - 5) & (src.t <= t[-1] + 5)]
    lab = 'REM cloud 10 s / 1 W' if dev == 'pi400' else 'LEM 10 s / mW (in REM via field API)'
    ax.step(d.t - tl, d[col], where='post', lw=1.4, color='C3', label=lab)
    if dev != 'pi400':
        ax.step(d.t - tl, np.floor(d[col]), where='post', lw=1.0, color='C1', ls='--', label='same trace at 1 W (floor) — what the cloud path would report')
    ax.axhline(r['w_base'], color='0.4', ls=':', lw=1, label=f'bench idle baseline {r["w_base"]:.2f} W')
    ax.set_title(title, fontsize=10); ax.set_ylabel('W'); ax.legend(fontsize=8, loc='upper right', ncol=2)
    ax.grid(alpha=0.3)
axes[-1].set_xlabel('clip time (s) — REM 10-min signature: timer/black · white · black · content · black tail')
fig.suptitle('R2 dual capture (C8): one playback, two readers per plug — 2026-08-25, decode rig protocol v3, keep_awake pinned', fontsize=11)
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(OUT, dpi=160)
print('wrote', OUT)
