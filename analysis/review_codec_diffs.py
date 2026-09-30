#!/usr/bin/env python3
"""Review check 2 (2026-09-30): pairwise codec differences in decode power,
Welch 95 % CIs, and the n a 0.1 W bound would need.

Sets (per device x content family; one row = one metered run, ΔW over the
run's own idle baseline unless stated):
  HW  C25 F1   batch 20260927d1a6 arm=screen  GTV H.264/HEVC/AV1, Bbox H.264/HEVC  (Meridian)
  HW  C27 F1   batch 3e54b322a9b4             W5 H.264/HEVC/VP9                   (BBB iso)
  HW  C17 F3   batch 20260817b9c0de           GTV, Fire TV x 4 codecs x 3 families (iso)
  SW  C11 F7   2026-07-31 + 2026-08-01 loop_* rows, Pi 5 (headless, software)
  SW  C24 am.  batch 20260927e7e5             Apple TV, ABSOLUTE task W (as the digest)
  SW  C26      batch 20260927c26b             Bbox 720p30 / 1080p30 AV1 vs H.264

Welch: d = m1 - m2, se = sqrt(s1^2/n1 + s2^2/n2), df Welch-Satterthwaite.
n for a 0.1 W bound: smallest equal n per cell such that
|d_obs| + t(.975, 2n-2) * s_pooled * sqrt(2/n) < 0.1 W   (observed d and sd
held fixed); 'none' if |d_obs| >= 0.1 W; also n0 = the same with d = 0.

Two modes:
  on GoS1, from the raw store (and write the per-run table the pack carries):
    python3 analysis/review_codec_diffs.py --export digests/2026-09-review-checks-runs.csv \
        --csv digests/2026-09-review-checks.csv
  anywhere, from the public evidence pack's per-run table (no GoS1 access):
    python3 analysis/review_codec_diffs.py --runs digests/2026-09-review-checks-runs.csv
Both modes print the same cells and intervals. Needs scipy.

The per-run table also carries rows kept out of the comparison by design
(Bbox AV1 at 1080p59.94, C25 F2; W5 AV1, C27 F2: failed playback), with
in_comparison = no, so Figure 7 can be drawn from the same file.
"""
import argparse
import csv
import glob
import itertools
import json
import math
import re
import statistics as st
from collections import defaultdict

from scipy import stats

DEC = "/srv/data/owl/results/decode"
FPS_LOGS = ("/srv/data/owl/campaign_2026-09-27_rediag/fps.jsonl",
            "/srv/data/owl/campaign_2026-09-27_c26/fps.jsonl")
EYE = {("C25 F1", "gtv", "h264"): "eye-checked (cell)", ("C25 F1", "gtv", "av1"): "eye-checked (cell)",
       ("C24 am. (abs W)", "atv", None): "eye-checked (every row)"}
FIELDS = ["set", "decode_class", "device", "content", "codec", "job_id", "n_baseline", "n_task",
          "w_base_w", "w_task_w", "delta_w_w", "value_w", "value_basis", "flag", "valid",
          "in_comparison", "presented_fps", "fps_source", "note"]
BOUND = 0.1


def env(pattern):
    for f in sorted(glob.glob(f"{DEC}/{pattern}")):
        yield json.load(open(f))


def parse_tpl(t):
    m = re.match(r"loop_([a-z]+?)(iso)?_(h264|h265|av1|vp9)$", t)
    return (m.group(1), m.group(3)) if m else (None, None)


def collect():
    rows = []  # dict(set, cls, device, content, codec, value, job, flag, ok, use, ...)
    fps = defaultdict(list)
    for path in FPS_LOGS:
        for l in open(path):
            x = json.loads(l)
            if x.get("fps") is not None:
                fps[x["job_id"]].append(x)

    def add(setname, cls, d, r, content, codec, value=None, use=True, note=""):
        prov = r.get("provenance") or {}

        def playing(x):
            return x is None or x == "PLAYING" or (isinstance(x, dict) and x.get("state") == "Playing")
        # C17's own rule (campaign_2026-08-17_vp9b/analyze_night.py): the Fire TV
        # end-of-window probe returns False on live rows, so a flat trace to the end counts
        w = r.get("raw_task_w") or []
        flat = len(w) >= 300 and abs(st.mean(w[-60:]) - st.mean(w[len(w) // 3:2 * len(w) // 3])) <= 0.15
        ok = ((r.get("alive_at_window_end") is not False or flat)
              and playing(r.get("playback_state_at_end"))
              and playing(prov.get("playback_state_midwindow")))
        t = r.get("raw_task_t") or []
        fv = [x["fps"] for x in fps.get(d["job_id"], [])
              if r["device"] == "bbox" and t and t[0] <= x["t"] <= t[-1]]
        eye = EYE.get((setname, r["device"], codec)) or EYE.get((setname, r["device"], None), "")
        rows.append(dict(set=setname, cls=cls, device=r["device"], content=content,
                         codec=codec, value=r["delta_w"] if value is None else value,
                         basis="delta_w" if value is None else "w_task (absolute)",
                         job=d["job_id"], flag=r["confidence"]["flag"], ok=ok, use=use,
                         note=note, n_base=len(r.get("raw_baseline_w") or []), n_task=len(w),
                         w_base=r["w_base"], w_task=r["w_task"], delta_w=r["delta_w"],
                         fps=round(st.mean(fv), 2) if fv else None,
                         fps_src="SurfaceFlinger, in window" if fv else eye,
                         dec=",".join(prov.get("decoders_allocated") or []) or "-"))

    # C25 F1 (screen arm only)
    jobs = {j["job_id"]: j for j in map(json.loads, open(
        "/srv/data/owl/campaign_2026-09-27_rediag/jobs.jsonl"))}
    for d in env("2026-09-27_*.json"):
        if d.get("batch_id") != "20260927d1a6" or jobs.get(d["job_id"], {}).get("arm") != "screen":
            continue
        for r in d["runs"]:
            c, k = parse_tpl(d["template"])
            if r["device"] == "bbox" and k == "av1":   # software, ~5 fps (C25 F2)
                add("C25 F1", "sw-fail", d, r, c, k, use=False,
                    note="software decode, ~5 of 59.94 frames/s: failed playback (C25 F2)")
                continue
            add("C25 F1", "hw", d, r, c, k)
    # C27 F1 (AV1 excluded: 1.7 fps failed playback, C27 F2)
    for d in env("2026-09-22_*.json"):
        if d.get("batch_id") == "3e54b322a9b4":
            for r in d["runs"]:
                c, k = parse_tpl(d["template"])
                if k == "av1":
                    add("C27 F1", "sw-fail", d, r, c, k, use=False,
                        note="in-app software AV1, 1.3-1.7 frames/s in same-session probes: failed playback (C27 F2)")
                else:
                    add("C27 F1", "hw", d, r, c, k)
    # C17 F3
    for d in env("2026-08-1[78]_*.json"):
        if d.get("batch_id") == "20260817b9c0de":
            for r in d["runs"]:
                if r["device"] in ("gtv", "firestick"):
                    c, k = parse_tpl(d["template"])
                    add("C17 F3", "hw", d, r, c, k)
    # C11 F7 Pi 5 software
    for d in list(env("2026-07-31_*.json")) + list(env("2026-08-01_*.json")):
        c, k = parse_tpl(d["template"])
        if not k:
            continue
        for r in d["runs"]:
            if r["device"] == "pi5":
                add("C11 F7", "sw", d, r, c, k)
    # C24 amendment, Apple TV, absolute task W
    for d in env("2026-09-27_*.json"):
        if d.get("batch_id") == "20260927e7e5":
            for r in d["runs"]:
                if r["device"] == "atv":
                    c, k = parse_tpl(d["template"])
                    add("C24 am. (abs W)", "sw", d, r, c, k, value=r["w_task"])
    # C26 Bbox rungs
    cj = {j["job_id"]: j for j in map(json.loads, open(
        "/srv/data/owl/campaign_2026-09-27_c26/jobs.jsonl"))}
    for d in env("2026-09-27_*.json"):
        if d.get("batch_id") == "20260927c26b" and d["job_id"] in cj:
            j = cj[d["job_id"]]
            for r in d["runs"]:
                add("C26", "sw" if j["arm"] == "720p30" else "sw-fail", d, r,
                    f"meridian{j['arm']}", j["codec"])
    return rows


def export_runs(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        for r in rows:
            w.writerow([r["set"], r["cls"], r["device"], r["content"], r["codec"], r["job"],
                        r["n_base"], r["n_task"], f"{r['w_base']:.3f}", f"{r['w_task']:.3f}",
                        f"{r['delta_w']:.3f}", f"{r['value']:.3f}", r["basis"], r["flag"],
                        "yes" if r["ok"] else "no", "yes" if r["use"] else "no",
                        "" if r["fps"] is None else r["fps"], r["fps_src"], r["note"]])


def from_runs(path):
    rows = []
    for x in csv.DictReader(open(path)):
        rows.append(dict(set=x["set"], cls=x["decode_class"], device=x["device"],
                         content=x["content"], codec=x["codec"], job=x["job_id"],
                         value=float(x["value_w"]), flag=x["flag"], ok=x["valid"] == "yes",
                         use=x["in_comparison"] == "yes"))
    return rows


def welch(a, b):
    n1, n2 = len(a), len(b)
    m1, m2 = st.mean(a), st.mean(b)
    v1, v2 = st.variance(a), st.variance(b)
    se = math.sqrt(v1 / n1 + v2 / n2)
    df = (v1 / n1 + v2 / n2) ** 2 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1)) \
        if se > 0 else n1 + n2 - 2
    t = stats.t.ppf(0.975, df)
    d = m1 - m2
    sp = math.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
    return d, se, df, d - t * se, d + t * se, sp


def n_needed(d, sp, bound=BOUND):
    room = bound - abs(d)
    if room <= 0:
        return None
    for n in range(2, 100000):
        if stats.t.ppf(0.975, 2 * n - 2) * sp * math.sqrt(2 / n) < room:
            return n
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="write the per-pair summary CSV")
    ap.add_argument("--export", help="GoS1: write the per-run table from the raw store")
    ap.add_argument("--runs", help="read the per-run table instead of the raw store")
    a = ap.parse_args()
    rows = from_runs(a.runs) if a.runs else collect()
    if a.export:
        export_runs(rows, a.export)
        print(f"per-run table ({len(rows)} rows) -> {a.export}")
    rows = [r for r in rows if r["use"]]
    bad = [r for r in rows if not r["ok"]]
    print(f"rows {len(rows)}; excluded (not PLAYING / not alive): {len(bad)}")
    for r in bad:
        print(f"   excluded {r['set']} {r['device']} {r['content']} {r['codec']} job {r['job']} {r['value']:.3f}")
    cells = defaultdict(list)
    for r in rows:
        if r["ok"]:
            cells[(r["set"], r["cls"], r["device"], r["content"], r["codec"])].append(r)

    print("\n== cells ==")
    for k in sorted(cells):
        v = [x["value"] for x in cells[k]]
        flags = "".join(x["flag"] for x in cells[k])
        print(f"{k[0]:16} {k[2]:9} {k[3]:16} {k[4]:5} n={len(v)} mean {st.mean(v):+.3f}"
              f" sd {st.stdev(v) if len(v) > 1 else float('nan'):.3f} {flags}")

    out = []
    groups = defaultdict(list)
    for k in cells:
        groups[k[:4]].append(k)
    for g, ks in sorted(groups.items()):
        for k1, k2 in itertools.combinations(sorted(ks, key=lambda k: k[4]), 2):
            a1 = [x["value"] for x in cells[k1]]
            a2 = [x["value"] for x in cells[k2]]
            if len(a1) < 2 or len(a2) < 2:
                out.append(dict(set=g[0], cls=g[1], device=g[2], content=g[3],
                                pair=f"{k1[4]}-{k2[4]}", n1=len(a1), n2=len(a2),
                                d=st.mean(a1) - st.mean(a2), note="n<2, no CI"))
                continue
            d, se, df, lo, hi, sp = welch(a1, a2)
            out.append(dict(set=g[0], cls=g[1], device=g[2], content=g[3],
                            pair=f"{k1[4]}-{k2[4]}", n1=len(a1), n2=len(a2), d=d, se=se,
                            df=df, lo=lo, hi=hi, absmax=max(abs(lo), abs(hi)), sp=sp,
                            n_obs=n_needed(d, sp), n_zero=n_needed(0.0, sp), note=""))

    print("\n== pairwise differences (W), Welch 95 % CI ==")
    print(f"{'set':16} {'device':9} {'content':16} {'pair':10} {'n':5} {'diff':>7} "
          f"{'95% CI':>18} {'df':>5} {'max|CI|':>7} {'sd_p':>6} {'n@obs':>6} {'n@0':>5}")
    for o in out:
        if o["note"]:
            print(f"{o['set']:16} {o['device']:9} {o['content']:16} {o['pair']:10} "
                  f"{o['n1']}/{o['n2']}  {o['d']:+.3f}  ({o['note']})")
            continue
        print(f"{o['set']:16} {o['device']:9} {o['content']:16} {o['pair']:10} {o['n1']}/{o['n2']:<3}"
              f" {o['d']:+.3f} [{o['lo']:+.3f}, {o['hi']:+.3f}] {o['df']:5.1f} {o['absmax']:7.3f}"
              f" {o['sp']:6.3f} {str(o['n_obs'] or 'none'):>6} {str(o['n_zero']):>5}")

    hw = [o for o in out if o["cls"] == "hw" and not o["note"]]
    big = max(hw, key=lambda o: abs(o["d"]))
    wide = max(hw, key=lambda o: o["absmax"])
    print(f"\nHW-covered set: {len(hw)} pairs;"
          f" largest |point| {big['d']:+.3f} W ({big['set']} {big['device']} {big['content']} {big['pair']});"
          f" largest |CI bound| {wide['absmax']:.3f} W ({wide['set']} {wide['device']} {wide['content']} {wide['pair']})")
    print(f"  pairs with |point| >= 0.1 W: {sum(abs(o['d']) >= BOUND for o in hw)};"
          f" pairs whose CI excludes 0: {sum(o['lo'] > 0 or o['hi'] < 0 for o in hw)};"
          f" pairs whose whole CI lies inside ±0.1 W: {sum(o['absmax'] < BOUND for o in hw)}")
    for s in ("C25 F1", "C27 F1", "C17 F3"):
        v = [o for o in hw if o["set"] == s]
        print(f"  {s}: pairs {len(v)}; |point| max {max(abs(o['d']) for o in v):.3f};"
              f" |CI| max {max(o['absmax'] for o in v):.3f}; CI inside ±0.1: "
              f"{sum(o['absmax'] < BOUND for o in v)}/{len(v)}; median n@0 "
              f"{st.median(o['n_zero'] for o in v if o['n_zero'])}")

    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["set", "decode_class", "device", "content", "codec_pair", "n1", "n2",
                        "diff_w", "ci95_lo_w", "ci95_hi_w", "welch_df", "max_abs_ci_w",
                        "pooled_sd_w", "n_per_cell_for_0p1w_bound_at_obs_diff",
                        "n_per_cell_for_0p1w_bound_if_true_diff_0", "note"])
            for o in out:
                w.writerow([o["set"], o["cls"], o["device"], o["content"], o["pair"], o["n1"], o["n2"],
                            f"{o['d']:.3f}", *(f"{o[k]:.3f}" if k in o else "" for k in ("lo", "hi")),
                            f"{o['df']:.1f}" if "df" in o else "",
                            f"{o['absmax']:.3f}" if "absmax" in o else "",
                            f"{o['sp']:.3f}" if "sp" in o else "",
                            o.get("n_obs") or ("none" if "sp" in o else ""), o.get("n_zero", ""),
                            o["note"]])
        print(f"csv -> {a.csv}")


if __name__ == "__main__":
    main()
