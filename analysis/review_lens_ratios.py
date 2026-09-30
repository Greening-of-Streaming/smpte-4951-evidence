#!/usr/bin/env python3
"""Review check 1 (2026-09-30): encoder ratios under the marginal and
attributional accounting lenses.

  marginal       Wh/min = dW * dt / 3600 / (content_s / 60)       (stored)
  attributional  Wh/min = (W_base + dW) * dt / 3600 / (content_s / 60)

W_base is the row's own measured baseline where the row stores one (C17,
R14, the 33 S53 extension rows); otherwise the nominal 79 W post-swap idle
floor used by wattlab's attributional_retrofit.py (labelled `nominal`).
Cells = mean over reps. Pairwise ratios are formed only inside a comparable
group (same set, same clip, same target bitrate / rung).

Multiplier m = attr/marg = 1 + W_base/dW, so ratio_attr/ratio_marg =
m_a/m_b: ratios are unchanged only where two rows share the same dW.

Two modes:
  on GoS1, from the stored parity artifacts (and write the per-row table):
    python3 analysis/review_lens_ratios.py --export digests/2026-09-review-checks-lens-runs.csv \
        --csv digests/2026-09-review-checks-lens.csv
  anywhere, from the public evidence pack's per-row table (no GoS1 access):
    python3 analysis/review_lens_ratios.py --rows digests/2026-09-review-checks-lens-runs.csv
Both modes print the same multipliers, shifts and flips.
"""
import argparse
import csv
import itertools
import json
import os
import statistics as st
from collections import defaultdict

# wattlab repo checkout on the measurement host (GoS1: ~/wattlab)
WATTLAB = os.environ.get("WATTLAB_DIR", os.path.expanduser("~/wattlab"))

W_NOMINAL = 79.0
HOT_W = 84.0   # row baseline >= 5 W above the nominal floor = hot (under-counts dW)
S53 = WATTLAB + "/results/calibration/encode_parity_nvenc_24c_2026-06-20_plus_ext.json"
VP9 = WATTLAB + "/results/diagnostics/encode_parity_nvenc_24c_2026-08-09.json"
C17 = WATTLAB + "/results/diagnostics/encode_parity_nvenc_24c_2026-08-17.json"
R14 = "/srv/data/owl/campaign_2026-08-29_tier3/r14/stage_b_results.jsonl"


def per_min(w, dt, cs):
    return w * dt / 3600 / (cs / 60)


def rows():
    out = []
    for tag, path in (("S53", S53), ("VP9", VP9), ("C17", C17)):
        for r in json.load(open(path))["rows"]:
            if not r.get("content_s") or r.get("delta_w") is None:
                continue
            wb = r.get("w_base")
            rung = r.get("rung") or "sweep"
            grp_set = "S53+VP9" if tag in ("S53", "VP9") else "C17"
            key = (grp_set, r["clip"], rung, r["height"], r["target_bitrate_kbps"])
            hw = "nvenc" if r.get("encoder_kind") == "gpu" or r["profile"].startswith("gpu") else "cpu"
            out.append(dict(set=grp_set, src=tag, group=key,
                            cell=f"{r['codec']}/{r['profile']}", hw=hw,
                            dw=r["delta_w"], dt=r["delta_t_s"], cs=r["content_s"],
                            wb=wb if wb is not None else W_NOMINAL,
                            wb_src="row" if wb is not None else "nominal"))
    for line in open(R14):
        r = json.loads(line)
        out.append(dict(set="R14", src="R14", group=("R14", "bbb", "crf", 1080, "crf"),
                        cell=r["arm"], hw="cpu", dw=r["delta_w"], dt=r["delta_t_s"],
                        cs=r["content_s"], wb=r["w_base"], wb_src="row"))
    return derive(out)


ROW_FIELDS = ["set", "source_artifact", "clip", "rung", "height", "target_kbps", "cell",
              "encoder_hw", "delta_w_w", "delta_t_s", "content_s", "w_base_w", "w_base_source"]


def export_rows(rs, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(ROW_FIELDS)
        for r in rs:
            g = r["group"]
            w.writerow([g[0], r["src"], g[1], g[2], g[3], g[4], r["cell"], r["hw"],
                        r["dw"], r["dt"], r["cs"], r["wb"], r["wb_src"]])


def rows_from_csv(path):
    out = []
    for x in csv.DictReader(open(path)):
        out.append(dict(set=x["set"], src=x["source_artifact"],
                        group=(x["set"], x["clip"], x["rung"], int(x["height"]),
                               int(x["target_kbps"]) if x["target_kbps"].isdigit() else x["target_kbps"]),
                        cell=x["cell"], hw=x["encoder_hw"], dw=float(x["delta_w_w"]),
                        dt=float(x["delta_t_s"]), cs=float(x["content_s"]),
                        wb=float(x["w_base_w"]), wb_src=x["w_base_source"]))
    return derive(out)


def derive(out):
    for r in out:
        r["marg"] = per_min(r["dw"], r["dt"], r["cs"])
        r["attr"] = per_min(r["wb"] + r["dw"], r["dt"], r["cs"])
        r["attr_nom"] = per_min(W_NOMINAL + r["dw"], r["dt"], r["cs"])
    return out


def cells(rs):
    by = defaultdict(list)
    for r in rs:
        by[(r["group"], r["cell"])].append(r)
    out = []
    for (g, c), v in by.items():
        out.append(dict(group=g, cell=c, hw=v[0]["hw"], n=len(v),
                        wb_src=",".join(sorted({x["wb_src"] for x in v})),
                        dw=st.mean(x["dw"] for x in v),
                        wb=st.mean(x["wb"] for x in v),
                        marg=st.mean(x["marg"] for x in v),
                        attr=st.mean(x["attr"] for x in v),
                        attr_nom=st.mean(x["attr_nom"] for x in v)))
    for c in out:
        c["mult"] = c["attr"] / c["marg"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="write the per-cell summary CSV")
    ap.add_argument("--export", help="GoS1: write the per-row table from the stored artifacts")
    ap.add_argument("--rows", help="read the per-row table instead of the stored artifacts")
    a = ap.parse_args()
    rs = rows_from_csv(a.rows) if a.rows else rows()
    if a.export:
        export_rows(rs, a.export)
        print(f"per-row table ({len(rs)} rows) -> {a.export}")
    cs = cells(rs)
    groups = defaultdict(list)
    for c in cs:
        groups[c["group"]].append(c)

    print("== multipliers (attr/marg) by set x hw ==")
    for s in ("S53+VP9", "C17", "R14"):
        for hw in ("cpu", "nvenc"):
            m = [c["mult"] for c in cs if c["group"][0] == s and c["hw"] == hw]
            d = [c["dw"] for c in cs if c["group"][0] == s and c["hw"] == hw]
            if m:
                print(f"{s:8} {hw:5} cells={len(m):3}  mult {min(m):.2f}-{max(m):.2f}"
                      f"  dW {min(d):.1f}-{max(d):.1f} W")

    pairs = []
    for g, v in groups.items():
        for x, y in itertools.combinations(v, 2):
            rm, ra = x["marg"] / y["marg"], x["attr"] / y["attr"]
            ran = x["attr_nom"] / y["attr_nom"]
            kind = x["hw"] + "-" + y["hw"] if x["hw"] == y["hw"] else "cpu-nvenc"
            pairs.append(dict(group=g, a=x["cell"], b=y["cell"], kind=kind,
                              rm=rm, ra=ra, shift=ra / rm - 1, shift_nom=ran / rm - 1,
                              flip=(x["marg"] - y["marg"]) * (x["attr"] - y["attr"]) < 0))

    print("\n== pairwise ratio shift (ratio_attr / ratio_marg - 1), by set x pair kind ==")
    for s in ("S53+VP9", "C17", "R14"):
        for kind in ("cpu-cpu", "nvenc-nvenc", "cpu-nvenc"):
            p = [q for q in pairs if q["group"][0] == s and q["kind"] == kind]
            if not p:
                continue
            w = max(p, key=lambda q: abs(q["shift"]))
            print(f"{s:8} {kind:12} pairs={len(p):4} |shift| median {st.median(abs(q['shift']) for q in p):6.1%}"
                  f"  max {abs(w['shift']):6.1%}  rank flips {sum(q['flip'] for q in p):3}"
                  f"   worst: {w['group'][1:]} {w['a']} vs {w['b']}: {w['rm']:.2f}x -> {w['ra']:.2f}x")
    print("\n== rank flips (any set) ==")
    for q in pairs:
        if q["flip"]:
            print(f"  {q['group']} {q['a']} vs {q['b']}: marg ratio {q['rm']:.3f} attr ratio {q['ra']:.3f}")
    print("\n== sensitivity: row-W_base vs nominal-79 W on rows that store W_base ==")
    for s in ("C17", "R14"):
        p = [q for q in pairs if q["group"][0] == s]
        print(f"{s:5} max |shift| row W_base {max(abs(q['shift']) for q in p):.1%}"
              f" · nominal 79 W {max(abs(q['shift_nom']) for q in p):.1%}")

    print("\n== set-wide bound: any within-set ratio shifts by at most max(m)/min(m)-1 ==")
    for s in ("S53+VP9", "C17", "R14"):
        for label, keep in (("all rows", lambda c: True),
                            ("clean W_base", lambda c: c["wb"] < HOT_W)):
            for hw in ("cpu", "all"):
                m = [c["mult"] for c in cs if c["group"][0] == s and keep(c)
                     and (hw == "all" or c["hw"] == hw)]
                if m:
                    print(f"{s:8} {label:13} {hw:4} cells={len(m):3} m {min(m):.3f}-{max(m):.3f}"
                          f"  bound {max(m)/min(m)-1:6.1%}")
    hot = [c for c in cs if c["wb"] >= HOT_W]
    print(f"\nhot-baseline cells (mean W_base >= {HOT_W} W): " +
          "; ".join(f"{c['group'][0]} {c['group'][1]} {c['group'][4]} {c['cell']} W_base {c['wb']:.1f}"
                    for c in hot))
    print("\n== rank flips among clean cells, all pairs within set x clip (any bitrate) ==")
    byclip = defaultdict(list)
    for c in cs:
        if c["wb"] < HOT_W:
            byclip[(c["group"][0], c["group"][1])].append(c)
    for k, v in sorted(byclip.items()):
        fl = [(x, y) for x, y in itertools.combinations(v, 2)
              if (x["marg"] - y["marg"]) * (x["attr"] - y["attr"]) < 0]
        big = [(x, y) for x, y in fl if abs(x["marg"] / y["marg"] - 1) > 0.05]
        print(f"  {k}: cells {len(v)} pairs {len(v)*(len(v)-1)//2} flips {len(fl)}"
              f" (marginal gap >5%: {len(big)})")
        for x, y in big:
            print(f"     {x['group'][4]} {x['cell']} {x['marg']:.4f}/{x['attr']:.4f}"
                  f"  vs  {y['group'][4]} {y['cell']} {y['marg']:.4f}/{y['attr']:.4f}")

    print("\n== S53 F4 pairs: same clip, codec, rung, bitrate; CPU / NVENC ratio (CPU over GPU) ==")
    idx = {(c["group"], c["cell"]): c for c in cs if c["group"][0] == "S53+VP9"}
    for prof in ("gpu_baseline", "gpu_tuned"):
        rm_, ra_, fl = [], [], 0
        for (g, cell), c in idx.items():
            codec, p_ = cell.split("/")
            if p_ != "cpu" or c["wb"] >= HOT_W:
                continue
            gcell = idx.get((g, f"{codec}/{prof}"))
            if not gcell or gcell["wb"] >= HOT_W:
                continue
            rm_.append(c["marg"] / gcell["marg"])
            ra_.append(c["attr"] / gcell["attr"])
            fl += (rm_[-1] - 1) * (ra_[-1] - 1) < 0
        sh = [ra / rm - 1 for rm, ra in zip(rm_, ra_)]
        print(f"  cpu vs {prof:12} pairs {len(rm_):3}  marginal {min(rm_):.2f}-{max(rm_):.2f}x"
              f"  attributional {min(ra_):.2f}-{max(ra_):.2f}x  shift {min(sh):+.1%}..{max(sh):+.1%}"
              f"  order flips {fl}")

    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["set", "clip", "rung", "height", "target_kbps", "cell", "encoder_hw", "n",
                        "w_base_src", "mean_w_base_w", "mean_delta_w_w", "marginal_wh_per_min",
                        "attributional_wh_per_min", "multiplier"])
            for c in sorted(cs, key=lambda c: (str(c["group"]), c["marg"])):
                g = c["group"]
                w.writerow([g[0], g[1], g[2], g[3], g[4], c["cell"], c["hw"], c["n"], c["wb_src"],
                            f"{c['wb']:.2f}", f"{c['dw']:.2f}", f"{c['marg']:.4f}",
                            f"{c['attr']:.4f}", f"{c['mult']:.3f}"])
        print(f"\ncsv -> {a.csv}")


if __name__ == "__main__":
    main()
