#!/usr/bin/env python3
"""C25 item 1a — Lab-E (LG C2) panel state behind the Figure 8 rows.

Handoff 2026-09-27 §1a. For every Fire TV / GTV / Bbox row in
  C11  /srv/data/owl/campaign_2026-07-31/results.jsonl  (B_all_*, B_seq_*)
  C17  decode batch 20260817b9c0de (2026-08-17/18)
  C18  decode batch 20260818ae7ba7b0
  F9   decode batch f9d026082401
recover the Lab-E power over the row's baseline and task windows, classify
lit (>40 W) / standby (<15 W) / other, flag baseline->task transitions, and
split each cell's ΔW by panel state. Also report each box's own task-trace
signature (flat near 1.0 W = asleep).

Lab-E sources, in order: the row's own context trace (screen-mode runs
only), else the C2's own row when the C2 ran as a concurrent device in the
same parallel job (then the panel is lit on its NATIVE input — the HDMI
box's input is not the one displayed). Otherwise: no record.

Run on GoS1:  python3 analysis/c25_fig8_panel_state.py [--csv OUT.csv]
Reads raw envelopes; writes summary rows only (no raw samples).
"""
import argparse
import csv
import glob
import json
import statistics as st
import sys
from collections import defaultdict

DEC = "/srv/data/owl/results/decode"
JUL = "/srv/data/owl/campaign_2026-07-31/results.jsonl"
BATCH = {"20260817b9c0de": "C17", "20260818ae7ba7b0": "C18",
         "f9d026082401": "F9"}
BOXES = ("firestick", "gtv", "bbox")
LIT, STANDBY = 40.0, 15.0


def state(w):
    if w is None:
        return "no_record"
    return "lit" if w > LIT else "standby" if w < STANDBY else "between"


def sig(samples):
    """Asleep signature: flat task trace near 1.0 W."""
    if not samples:
        return None, None, ""
    m, sd = st.mean(samples), st.pstdev(samples)
    return m, sd, "asleep_sig" if (m < 1.3 and sd < 0.05) else ""


def july_cells():
    cells = {}
    for line in open(JUL):
        r = json.loads(line)
        k = r["cell"]["key"]
        if k.startswith("B_"):
            cells[r["cell"]["job_id"]] = r   # re-runs: last wins (as figure)
    return cells


def parse_run(run):
    # run name like bbb_h264_loop / bbbiso_vp9_... / netpath variants
    name = run.get("run", "")
    parts = name.split("_")
    return parts[0] if parts else "", parts[1] if len(parts) > 1 else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    a = ap.parse_args()
    jul = july_cells()
    rows = []
    for f in sorted(glob.glob(f"{DEC}/2026-0[78]-*.json")):
        d = json.load(open(f))
        jid = d.get("job_id")
        tag = BATCH.get(d.get("batch_id"))
        key = None
        if not tag and jid in jul:
            tag, key = "C11", jul[jid]["cell"]["key"]
        if not tag:
            continue
        c2 = next((r for r in d.get("runs", []) if r["device"] == "c2"),
                  None)
        for r in d.get("runs", []):
            if r["device"] not in BOXES:
                continue
            if r.get("raw_context_w"):
                src = "context"
                lb = st.mean(r["raw_context_baseline_w"] or [0]) or None
                lt = st.mean(r["raw_context_w"])
            elif c2 is not None:
                src = "c2_native_concurrent"
                lb, lt = c2.get("w_base"), c2.get("w_task")
            else:
                src, lb, lt = "none", None, None
            fam, cod = parse_run(r)
            m, sd, s = sig(r.get("raw_task_w"))
            sb, st_ = state(lb), state(lt)
            rows.append({
                "set": tag, "job_id": jid, "cell": key or r.get("run"),
                "device": r["device"], "family": fam, "codec": cod,
                "window_s": r.get("window_s"), "delta_w": r.get("delta_w"),
                "box_w_base": r.get("w_base"), "box_task_mean_w": m and round(m, 3),
                "box_task_sd_w": sd and round(sd, 3), "box_signature": s,
                "labe_src": src, "labe_base_w": lb, "labe_task_w": lt,
                "labe_base_state": sb, "labe_task_state": st_,
                "transition": "yes" if (lb is not None and sb != st_) else "",
            })
    # per-set / per-device / codec split by panel state
    agg = defaultdict(list)
    for r in rows:
        ps = r["labe_task_state"] if r["labe_src"] != "none" else "no_record"
        agg[(r["set"], r["device"], r["codec"], ps)].append(r["delta_w"])
    print("set  device     codec  panel_state        n  mean_dW   min    max")
    for k in sorted(agg):
        v = [x for x in agg[k] if x is not None]
        if v:
            print(f"{k[0]:4} {k[1]:10} {k[2]:6} {k[3]:18} {len(v):2} "
                  f"{st.mean(v):+7.3f} {min(v):+6.3f} {max(v):+6.3f}")
    neg = [r for r in rows if (r["delta_w"] or 0) < 0]
    print(f"\nnegative rows: {len(neg)}")
    for r in neg:
        print(f"  {r['set']} {r['cell']:32} {r['device']:9} dW={r['delta_w']:+.3f}"
              f" box_task={r['box_task_mean_w']}±{r['box_task_sd_w']} "
              f"{r['box_signature'] or '-'} labe={r['labe_src']}:"
              f"{r['labe_base_state']}->{r['labe_task_state']}")
    tr = [r for r in rows if r["transition"]]
    print(f"\nLab-E baseline->task transitions: {len(tr)}")
    src = defaultdict(int)
    for r in rows:
        src[(r["set"], r["labe_src"])] += 1
    print("\nLab-E evidence per set:", dict(src))
    if a.csv:
        with open(a.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
