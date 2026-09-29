#!/usr/bin/env python3
"""C28 R8 (2026-09-30): host calibration provenance and what moves under it.

1. The host variance-calibration history (results/variance/history.jsonl).
2. An independent check of the two calibration nights (2026-07-07 and
   2026-09-05): both were step 0 of an in-app overnight benchmark, which then
   ran 20 /video all-codecs jobs with the same settings. Those jobs persist
   their 5 x 1 s baseline windows and thermals, so c_idle (mean within-window
   CV) and c_drift (CV of window means) can be recomputed per night, all
   windows and without hot (post-CPU-encode) baselines.
3. Re-flags the stored decode rows the paper cites (C11 F9 re-run / Figure 5,
   C17, C25, C26, C27) under the July (2.38/1.12) and September (2.46/1.90)
   host coefficients, with wattlab's own confidence() (settings passed
   explicitly, so the live settings.json is not read).
4. Encode rows (S53, VP9, C17 parity, R14) store no raw samples; bounds the
   effect of the September drift term on them from the stored SE:
   p+ >= Phi(dW / (SE_stored + (1.90 - c_drift_then)/100 * W_base)).

Run on GoS1:  python3 analysis/c28_r8_calibration.py
"""
import glob
import json
import os
import statistics as st
import sys
from collections import Counter, defaultdict

from scipy.stats import norm

WATTLAB = os.environ.get("WATTLAB_DIR", os.path.expanduser("~/wattlab"))
sys.path.insert(0, WATTLAB + "/wattlab_service")
import confidence as owl_confidence  # noqa: E402

DEC = "/srv/data/owl/results/decode"
JUL, SEP = (2.38, 1.12), (2.46, 1.90)
BENCH = {"2026-07-07": "e121c415", "2026-09-05": "591d63c9"}
F9_VALID = {"9393f686": ["gtv"], "139f4979": ["gtv"],
            "a7dff199": ["gtv", "firestick"], "8f9719be": ["gtv", "firestick"],
            "454086d3": ["gtv", "firestick"], "7f195277": ["gtv", "firestick"],
            "8141abb4": ["gtv", "firestick"], "0f4f7cd4": ["firestick"],
            "924ae582": ["firestick", "pi5"], "b4264c56": ["pi5"],
            "0c73392a": ["gtv", "firestick"], "1e8d2132": ["pi5"],
            "0a88b387": ["pi5"]}          # = figures/make_f9_rerun_figure.py VALID
BATCHES = {"20260817b9c0de": "C17", "20260927d1a6": "C25", "20260927c26b": "C26",
           "3e54b322a9b4": "C27 W5", "4b94ea5075f3": "C27 GTV comparator"}


def cv(v):
    return st.stdev(v) / st.mean(v) * 100 if len(v) > 1 else None


def flag(r, c):
    s = {"variance_idle_pct": c[0], "variance_idle_drift_pct": c[1],
         "conf_green_polls": 9, "conf_yellow_polls": 4,
         "conf_positive_green": 0.95, "conf_positive_yellow": 0.80}
    b, t = r["raw_baseline_w"], r["raw_task_w"]
    return owl_confidence.confidence(r["delta_w"], len(t), st.mean(b),
                                     baseline_samples_w=b, task_samples_w=t, s=s)


def main():
    print("== 1. host calibration history ==")
    for l in open(WATTLAB + "/results/variance/history.jsonl"):
        h = json.loads(l)
        print(f"  {h['ts'][:16]}  c_idle {h['variance_idle_pct']:5.2f}  c_drift "
              f"{h['variance_idle_drift_pct']:5.2f}  pairs {h['runs']:3}  w_base_mean "
              f"{h.get('w_base_mean')}  kernel {h['kernel']}"
              + ("  AMBIENT NOTE" if h.get("ambient_note") else ""))

    print("\n== 2. the two calibration nights, re-estimated from the benchmark's own video jobs ==")
    for day, bid in BENCH.items():
        b = json.load(open(f"{WATTLAB}/results/benchmark/{day}_{bid}.json"))
        jobs = [s["result_ref"]["job_id"] for s in b["steps"]
                if s["kind"] == "video" and s.get("result_ref")]
        wins, cpu_b, gpu_b = [], [], []
        for j in jobs:
            d = json.load(open(glob.glob(f"{WATTLAB}/results/video/*_{j}.json")[0]))
            for codec, byp in d["codecs"].items():
                for prof, e in byp.items():
                    if not isinstance(e, dict) or "energy" not in e:
                        continue
                    w = e["energy"].get("baseline_samples_w")
                    if w:
                        wins.append((codec, prof, w))
                    th = e.get("thermals") or {}
                    if th.get("cpu_base") is not None:
                        cpu_b.append(th["cpu_base"])
                        gpu_b.append(th["gpu_base"])
        floor = st.median(st.mean(w) for _, _, w in wins)
        for label, keep in (("all windows", lambda m: True),
                            ("no hot windows (< floor+4 W)", lambda m: m < floor + 4)):
            ws = [w for _, _, w in wins if keep(st.mean(w))]
            ci = st.mean(c for c in (cv(w) for w in ws) if c is not None)
            cd = cv([st.mean(w) for w in ws])
            print(f"  {day} bench {bid}: {len(jobs)} video jobs, {label:28} windows {len(ws):3}"
                  f"  floor {floor:6.2f} W  c_idle {ci:5.2f}  c_drift {cd:5.2f}")
        print(f"  {day}   idle temps at baseline: CPU Tctl median {st.median(cpu_b):.1f} C"
              f" (range {min(cpu_b):.1f}-{max(cpu_b):.1f}), GPU median {st.median(gpu_b):.1f} C")

    print("\n== 3. decode rows re-flagged: July vs September host coefficients ==")
    rows = []
    for f in sorted(glob.glob(f"{DEC}/*.json")):
        d = json.load(open(f))
        tag = BATCHES.get(d.get("batch_id"))
        if f.split("/")[-1].startswith("2026-08-24_") and d["job_id"] in F9_VALID:
            tag = "C11 F9 (Figure 5)"
        if not tag:
            continue
        for r in d["runs"]:
            if tag.startswith("C11") and r["device"] not in F9_VALID[d["job_id"]]:
                continue
            if r.get("raw_baseline_w") and r.get("raw_task_w"):
                rows.append((tag, d["job_id"], r))
    trans = defaultdict(Counter)
    for tag, jid, r in rows:
        fj, fs = flag(r, JUL), flag(r, SEP)
        stored = (r.get("confidence") or {}).get("flag")
        trans[tag][(stored, fj["flag"], fs["flag"])] += 1
        if fj["flag"] != fs["flag"]:
            print(f"  CHANGES {tag} job {jid} {r['device']} window {r.get('window_s')} s"
                  f" dW {r['delta_w']:+.3f}: Jul {fj['flag']} p+ {fj['confidence_positive']:.3f}"
                  f" -> Sep {fs['flag']} p+ {fs['confidence_positive']:.3f}")
    for tag, c in trans.items():
        print(f"  {tag:20} rows {sum(c.values()):3}  (stored, Jul, Sep): " +
              ", ".join(f"{k[0]}{k[1]}{k[2]} x{v}" for k, v in sorted(c.items())))

    print("\n== 4. encode rows: September drift term added to the stored SE ==")
    arts = {"S53+ext": "calibration/encode_parity_nvenc_24c_2026-06-20_plus_ext.json",
            "VP9": "diagnostics/encode_parity_nvenc_24c_2026-08-09.json",
            "C17": "diagnostics/encode_parity_nvenc_24c_2026-08-17.json"}
    enc = []
    for k, p in arts.items():
        enc += [(k, r) for r in json.load(open(f"{WATTLAB}/results/{p}"))["rows"]]
    enc += [("R14", json.loads(l)) for l in
            open("/srv/data/owl/campaign_2026-08-29_tier3/r14/stage_b_results.jsonl")]
    worst = None
    for k, r in enc:
        c = r.get("confidence") or {}
        se = c.get("se_final_w")
        if se is None or r.get("delta_w") is None:
            continue
        wb = r.get("w_base") or 79.0
        extra = max(0.0, (SEP[1] - 1.03) / 100 * wb)   # worst case: the lowest pre-Sep c_drift
        p = norm.cdf(r["delta_w"] / (se + extra))
        if worst is None or p < worst[0]:
            worst = (p, k, r["delta_w"], se, extra)
    print(f"  {len(enc)} encode rows; lowest p+ after adding the Sep drift term: {worst[0]:.6f}"
          f" ({worst[1]}, dW {worst[2]} W, SE {worst[3]} + {worst[4]:.2f} W)")

    print("\n== 5. the numbers for section 3.2 ==")
    for name, (ci, cd), wb in (("July (07-07, 30 pairs)", JUL, 75.59),
                               ("September (09-05, 20 pairs)", SEP, 78.36)):
        for base in (wb, 79.0, 101.0):
            fl = cd / 100 * base
            print(f"  {name:28} W_base {base:6.2f}: SE_drift floor {fl:.2f} W,"
                  f" dW for p+>=0.95 {1.645 * fl:.2f} W")


if __name__ == "__main__":
    main()
