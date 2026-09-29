#!/usr/bin/env python3
"""Item 5f (SMPTE #4951 review checks, 2026-09-30): each client device's OWN
idle coefficients vs the host coefficients the rig applies.

The client rig (decode_bench/bench.py) calls confidence.confidence() with no
device-specific settings, so the host's calibrated
    c_idle  = variance_idle_pct        (mean of within-baseline-window CVs)
    c_drift = variance_idle_drift_pct  (CV across baseline-window means)
are applied as percentages of each device's own w_base. This script computes
the same two estimators from each device's stored per-run baselines
(runs[].raw_baseline_w in results/decode/*.json), exactly as the host
calibration does (video.py run_variance_calibration: _cv = sample sd / mean
x 100; c_idle = mean of per-window CVs; c_drift = CV of window means), then
re-flags every run under (a) the host coefficients in force on its date
(results/variance/history.jsonl) and (b) the device's own coefficients.

c_drift is computed two ways: per batch (the host analogue: one calibration
session, windows minutes apart; batches with >= 4 baselines, median
reported) and across all of a device's baselines (weeks apart: sessions,
firmware, sink and ambient all differ — an upper bound, not the analogue).

Usage (on GoS1, repo root):
    python3 analysis/device_idle_coeffs.py [--json out.json]
"""
import glob, json, os, statistics, sys, collections, datetime, argparse

# wattlab repo checkout on the measurement host (GoS1: ~/wattlab)
WATTLAB = os.environ.get("WATTLAB_DIR", os.path.expanduser("~/wattlab"))

sys.path.insert(0, WATTLAB + "/wattlab_service")
import confidence as owl_confidence  # noqa: E402

RES = WATTLAB + "/results/decode/*.json"
HIST = WATTLAB + "/results/variance/history.jsonl"
FOCUS = {"20260927d1a6": "C25", "20260927c26b": "C26",
         "3e54b322a9b4": "C27 W5", "4b94ea5075f3": "C27 GTV comparator"}


def cv(v):
    if len(v) < 2:
        return None
    m = sum(v) / len(v)
    if abs(m) < 0.001:
        return None
    return statistics.stdev(v) / m * 100


def host_eras():
    eras = []
    for line in open(HIST):
        h = json.loads(line)
        eras.append((h["ts"], h["variance_idle_pct"], h["variance_idle_drift_pct"]))
    return sorted(eras)


def host_at(ts, eras):
    cur = None
    for t, ci, cd in eras:
        if t <= ts:
            cur = (ci, cd, t[:10])
    return cur


def flag(row, c_idle, c_drift):
    s = {"variance_idle_pct": c_idle, "variance_idle_drift_pct": c_drift,
         "conf_green_polls": 9, "conf_yellow_polls": 4,
         "conf_positive_green": 0.95, "conf_positive_yellow": 0.80}
    b, t = row["raw_baseline_w"], row["raw_task_w"]
    return owl_confidence.confidence(row["delta_w"], len(t), statistics.mean(b),
                                     baseline_samples_w=b, task_samples_w=t, s=s)


def load():
    rows = []
    for f in sorted(glob.glob(RES)):
        a = json.load(open(f))
        for r in a.get("runs") or []:
            if not isinstance(r.get("device"), str) or not r.get("raw_baseline_w") \
                    or not r.get("raw_task_w") or "delta_w" not in r:
                continue
            r = dict(r)
            r["_file"] = f
            r["_saved"] = a.get("saved_at") or f.split("/")[-1][:10]
            r["_batch"] = a.get("batch_id") or ("date:" + f.split("/")[-1][:10])
            rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()
    eras = host_eras()
    rows = load()
    bydev = collections.defaultdict(list)
    for r in rows:
        bydev[r["device"]].append(r)

    out = {}
    print("device    n_base_win n_samples  w_base_med  dates                  "
          "c_idle_own  c_drift_batch_med [n_batches]  c_drift_all  dup%")
    for d, rs in sorted(bydev.items()):
        wins = [r["raw_baseline_w"] for r in rs]
        cvs = [c for c in (cv(w) for w in wins) if c is not None]
        c_idle = statistics.mean(cvs)
        means = [statistics.mean(w) for w in wins]
        byb = collections.defaultdict(list)
        for r in rs:
            byb[r["_batch"]].append(statistics.mean(r["raw_baseline_w"]))
        bd = [cv(v) for v in byb.values() if len(v) >= 4]
        bd = [x for x in bd if x is not None]
        c_drift_b = statistics.median(bd) if bd else None
        c_drift_all = cv(means)
        dup = sum(sum(1 for i in range(1, len(w)) if w[i] == w[i - 1]) for w in wins)
        pairs = sum(len(w) - 1 for w in wins)
        dates = sorted(r["_saved"][:10] for r in rs)
        wb = statistics.median(means)
        out[d] = dict(n_windows=len(wins), n_samples=sum(len(w) for w in wins),
                      w_base_median=round(wb, 3), first=dates[0], last=dates[-1],
                      c_idle_own_pct=round(c_idle, 3),
                      c_idle_own_p90_pct=round(sorted(cvs)[int(0.9 * len(cvs))], 3),
                      c_drift_batch_median_pct=round(c_drift_b, 3) if c_drift_b else None,
                      c_drift_batch_p90_pct=round(sorted(bd)[int(0.9 * len(bd))], 3) if bd else None,
                      n_batches=len(bd), c_drift_all_pct=round(c_drift_all, 3),
                      dup_pct=round(100 * dup / pairs, 1))
        o = out[d]
        print(f"{d:9} {o['n_windows']:10} {o['n_samples']:9} {wb:10.3f}  "
              f"{o['first']}..{o['last']}  {o['c_idle_own_pct']:9.3f}  "
              f"{o['c_drift_batch_median_pct'] if o['c_drift_batch_median_pct'] is not None else '—':>12} "
              f"[{o['n_batches']}]  {o['c_drift_all_pct']:10.3f}  {o['dup_pct']:5.1f}")

    # Re-flag under host-era vs device-own coefficients.
    print("\nHost eras (history.jsonl):", [(t[:10], ci, cd) for t, ci, cd in eras])
    trans = collections.Counter()
    repro = collections.Counter()
    focus_lines = []
    for r in rows:
        d = r["device"]
        h = host_at(r["_saved"], eras)
        if h is None:
            continue
        own = out[d]
        own_drift = own["c_drift_batch_median_pct"] if own["c_drift_batch_median_pct"] is not None \
            else own["c_drift_all_pct"]
        fh = flag(r, h[0], h[1])
        fo = flag(r, own["c_idle_own_pct"], own_drift)
        stored = (r.get("confidence") or {}).get("flag")
        repro["match" if stored == fh["flag"] else "differ"] += 1
        trans[(d, fh["flag"], fo["flag"])] += 1
        tag = FOCUS.get(r["_batch"])
        if tag:
            focus_lines.append((tag, d, r["run"], round(r["delta_w"], 3), stored,
                                fh["flag"], fh["ci_delta_w_95"], fo["flag"], fo["ci_delta_w_95"]))
    print("stored flag reproduced by host-era recompute:", dict(repro))
    print("\nflag transitions host-era -> device-own (device, host, own): count")
    for k, v in sorted(trans.items()):
        if k[1] != k[2]:
            print("  ", k, v)
    print("  unchanged:", sum(v for k, v in trans.items() if k[1] == k[2]),
          "changed:", sum(v for k, v in trans.items() if k[1] != k[2]))
    print("\nC25/C26/C27 rows: tag device run dW stored | host flag CI | own flag CI")
    for x in sorted(focus_lines):
        print("  ", *x)
    if args.json:
        json.dump({"devices": out, "eras": eras,
                   "transitions": {"|".join(k): v for k, v in trans.items()},
                   "focus": focus_lines}, open(args.json, "w"), indent=1)


if __name__ == "__main__":
    main()
