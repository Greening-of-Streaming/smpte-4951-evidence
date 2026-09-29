#!/usr/bin/env python3
"""C26 summary: batch 20260927c26b (feeder c26_bbox_rungs_feeder.py); arm = rung.

Per arm x device x codec: n, mean/sd dW, flags, box task W, Lab-E context,
sink, decoder, midwindow player state, and (Bbox) presented fps from the
feeder's SurfaceFlinger samples taken inside each job's task window.

Run on GoS1:  python3 analysis/c26_summary.py [--csv OUT.csv]
"""
import argparse
import csv
import glob
import json
import statistics as st
from collections import defaultdict

DEC = "/srv/data/owl/results/decode"
CAMP = "/srv/data/owl/campaign_2026-09-27_c26"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv")
    a = ap.parse_args()
    jobs = [json.loads(l) for l in open(f"{CAMP}/jobs.jsonl")]
    fps = defaultdict(list)
    try:
        for l in open(f"{CAMP}/fps.jsonl"):
            r = json.loads(l)
            fps[r["job_id"]].append(r)
    except FileNotFoundError:
        pass
    cells = defaultdict(list)
    for j in jobs:
        f = glob.glob(f"{DEC}/*_{j['job_id']}.json")
        if not f:
            continue
        d = json.load(open(f[0]))
        for r in d["runs"]:
            t0 = r["raw_task_t"][0] if r.get("raw_task_t") else None
            t1 = r["raw_task_t"][-1] if r.get("raw_task_t") else None
            fv = [x["fps"] for x in fps.get(j["job_id"], [])
                  if x.get("fps") and t0 and t0 <= x["t"] <= t1] \
                if r["device"] == "bbox" else []
            cells[(j["arm"], r["device"], j["codec"])].append({
                "job": j["job_id"], "dw": r["delta_w"],
                "flag": r["confidence"]["flag"], "w_base": r["w_base"],
                "w_task": r["w_task"], "ctx_base": r.get("context_base_w"),
                "ctx_task": r.get("context_task_w"), "sink": r.get("sink"),
                "awake": r.get("panel_awake"),
                "dec": ",".join(r["provenance"].get("decoders_allocated")
                                or []) or "none",
                "state": r["provenance"].get("playback_state_midwindow"),
                "fps": round(st.mean(fv), 1) if fv else None})
    out = []
    for k in sorted(cells):
        v = cells[k]
        dws = [x["dw"] for x in v]
        row = {"arm": k[0], "device": k[1], "codec": k[2], "n": len(v),
               "mean_dw_w": round(st.mean(dws), 3),
               "sd_dw_w": round(st.stdev(dws), 3) if len(v) > 1 else None,
               "min_dw_w": min(dws), "max_dw_w": max(dws),
               "flags": "".join(x["flag"] for x in v),
               "mean_w_base": round(st.mean(x["w_base"] for x in v), 3),
               "mean_w_task": round(st.mean(x["w_task"] for x in v), 3),
               "sink": "/".join(sorted({str(x["sink"]) for x in v})),
               "panel_awake": "/".join(sorted({str(x["awake"]) for x in v})),
               "decoder": "/".join(sorted({x["dec"] for x in v})),
               "player_state": "/".join(sorted({str(x["state"]) for x in v})),
               "presented_fps": "/".join(str(x["fps"]) for x in v)
               if k[1] == "bbox" else "eye-checked" if k[1] == "gtv" else "",
               "jobs": " ".join(x["job"] for x in v)}
        out.append(row)
        print(" | ".join(f"{c}={row[c]}" for c in row))
    if a.csv:
        with open(a.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)


if __name__ == "__main__":
    main()
