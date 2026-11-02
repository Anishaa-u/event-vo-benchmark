"""Bundle every result from the three experiment kits into ONE small Markdown file,
ALL_RESULTS_DATA_PACK.md, for upload. Re-run after each new set of runs.
    python make_data_packs.py
"""

import csv
import glob
import os
import re
import sys

import numpy as np

ROOT = r"C:\capstone"
sys.path.insert(0, os.path.join(ROOT, "evo_kit"))
from evaluate_runs import associate, load_tum  # noqa: E402
from evaluation import align, apply  # noqa: E402

KITS = [
    # name, kit folder, alignment, notes file, log suffix
    ("ESVO (Zhou et al., 2021)", os.path.join(ROOT, "esvo_pilot_kit"), "se3", "NOTES.txt", "_esvo.log"),
    ("EVO (Rebecq et al., 2017)", os.path.join(ROOT, "evo_kit"), "sim3", "NOTES.txt", "_evo.log"),
    ("ESVIO (Chen et al., 2023)", os.path.join(ROOT, "esvio_kit"), "se3", "NOTES.txt", "_esvio.log"),
]
out = []
w = out.append


def read(p):
    with open(p, encoding="utf-8-sig", errors="ignore") as f:
        return f.read().strip()


def csv_table(path, fmt=4):
    rows = list(csv.reader(open(path)))
    head, body = rows[0], rows[1:]

    def f(x):
        try:
            v = float(x)
            return x if v.is_integer() and "." not in x else f"{v:.{fmt}f}"
        except ValueError:
            return x
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    lines += ["| " + " | ".join(f(x) for x in r) + " |" for r in body]
    return "\n".join(lines)


def traj(est_path, gt_path, mode):
    t_e, p_e = load_tum(est_path)
    t_g, p_g = load_tum(gt_path)
    if len(t_e) < 10:
        return None
    ie, ig = associate(t_e, t_g)
    if len(ie) < 10:
        return None
    est, gt, t = p_e[ie], p_g[ig], t_e[ie]
    s, R, tr = align(est, gt, with_scale=(mode == "sim3"))
    al = apply(est, s, R, tr)
    return t, al, gt, np.linalg.norm(al - gt, axis=1), t_e, t_g[0]


def kit_section(name, kit, mode, notes, log_suffix):
    runs = os.path.join(kit, "runs")
    w(f"# {name}")
    w("")
    if not glob.glob(os.path.join(runs, "*_run*.txt")):
        w("No runs recorded yet.")
        w("")
        if os.path.exists(os.path.join(kit, notes)):
            w("```")
            w(read(os.path.join(kit, notes)))
            w("```")
            w("")
        return
    w(f"Primary alignment: {mode.upper()} (requirement R4). All values below are original data from this project.")
    w("")
    for res, label in (("summary.csv", "Per sequence"), ("results.csv", "Per run"),
                       ("esvo_summary.csv", "Per sequence"), ("esvo_results.csv", "Per run")):
        p = os.path.join(kit, res)
        if os.path.exists(p):
            w(f"### {label} ({res})")
            w(csv_table(p))
            w("")
    if os.path.exists(os.path.join(kit, notes)):
        w("### Experiment record (notes, verbatim)")
        w("")
        w("```")
        w(read(os.path.join(kit, notes)))
        w("```")
        w("")
    if os.path.exists(os.path.join(runs, "run_log.txt")):
        w("### Run log (one line per run)")
        w("")
        w("```")
        w(read(os.path.join(runs, "run_log.txt")))
        w("```")
        w("")

    w("### Efficiency per run (10 Hz profiles; CPU summed over the algorithm's processes, % of one core)")
    w("")
    w("| run | samples | duration s | mean CPU % | median CPU % | p95 CPU % | max CPU % | mean RSS MB | peak RSS MB |")
    w("|---|---|---|---|---|---|---|---|---|")
    for p in sorted(glob.glob(os.path.join(runs, "*_profile.csv"))):
        a = np.genfromtxt(p, delimiter=",", names=True)
        if a.size < 2:
            continue
        cpu = a["cpu_percent_one_core"][a["cpu_percent_one_core"] > 0]
        if cpu.size == 0:
            continue
        nm = os.path.basename(p).replace("_profile.csv", "")
        w(f"| {nm} | {len(a)} | {a['t_s'][-1]:.1f} | {cpu.mean():.1f} | {np.median(cpu):.1f} | "
          f"{np.percentile(cpu, 95):.1f} | {cpu.max():.1f} | {a['rss_mb'].mean():.0f} | {a['rss_mb'].max():.0f} |")
    w("")

    ests = sorted(glob.glob(os.path.join(runs, "*_run*.txt")))
    for sub in sorted(glob.glob(os.path.join(runs, "*", ""))):
        if os.path.basename(os.path.dirname(sub)) in ("logs", "loop", "raw", "runs"):
            continue
        ests += sorted(glob.glob(os.path.join(sub, "*_run*.txt")))
    cache = {}
    w(f"### Error statistics per run (after {mode.upper()} alignment)")
    w("")
    w("| run | estimate span s | GT path length m | est poses | est rate Hz | mean err m | median err m | p95 err m | max err m | final err m |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for e in ests:
        m = re.match(r"(.+)_run(\d+)\.txt$", os.path.basename(e))
        if not m:
            continue
        seq = m.group(1)
        gt_path = os.path.join(runs, f"gt_{seq}.txt")
        if not os.path.exists(gt_path):
            continue
        cond = os.path.basename(os.path.dirname(e))
        nm = os.path.basename(e)[:-4] + (f" ({cond})" if cond != "runs" else "")
        r = traj(e, gt_path, mode)
        if r is None:
            w(f"| {nm} | failed | | | | | | | | |")
            continue
        t, al, gt, err, t_e, t0 = r
        cache[nm] = (t - t0, al, gt, err)
        plen = np.sum(np.linalg.norm(np.diff(gt, axis=0), axis=1))
        span = t_e[-1] - t_e[0]
        w(f"| {nm} | {span:.1f} | {plen:.2f} | {len(t_e)} | {len(t_e)/max(span, 1e-9):.0f} | {err.mean():.3f} | "
          f"{np.median(err):.3f} | {np.percentile(err, 95):.3f} | {err.max():.3f} | {err[-1]:.3f} |")
    w("")
    if cache:
        # keep the over-time tables readable: main runs plus at most a few condition runs
        names = [n for n in cache if "(" not in n] + [n for n in cache if "(" in n][:4]
        w("### Position error over time (m, every 2 s from the start of ground truth)")
        w("")
        w("| t_s | " + " | ".join(names) + " |")
        w("|---|" + "---|" * len(names))
        tmax = max(v[0][-1] for v in cache.values())
        for g in np.arange(0, tmax + 2, 2.0):
            cells = []
            for n in names:
                rel, _, _, err = cache[n]
                cells.append(f"{np.interp(g, rel, err):.3f}" if rel[0] <= g <= rel[-1] else "")
            if any(cells):
                w(f"| {g:.0f} | " + " | ".join(cells) + " |")
        w("")
        w("### Trajectories of the main runs, downsampled to 1 Hz (metres, estimate after alignment)")
        for n in [n for n in names if "(" not in n]:
            rel, al, gt, _ = cache[n]
            w("")
            w(f"**{n}**")
            w("")
            w("| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |")
            w("|---|---|---|---|---|---|---|")
            for g in np.arange(np.ceil(rel[0]), rel[-1], 1.0):
                i = min(np.searchsorted(rel, g), len(rel) - 1)
                w(f"| {rel[i]:.1f} | " + " | ".join(f"{v:.3f}" for v in gt[i]) + " | " +
                  " | ".join(f"{v:.3f}" for v in al[i]) + " |")
        w("")
    logs = sorted(glob.glob(os.path.join(runs, "logs", "*" + log_suffix)))
    if logs:
        w("### Log summaries")
        w("")
        for lg in logs:
            txt = open(lg, errors="ignore").read()
            lines = [l.rstrip() for l in txt.splitlines() if l.strip()]
            w(f"- {os.path.basename(lg)}: {len(lines)} lines; last lines: `" +
              " / ".join(l[:120] for l in lines[-3:]).replace("`", "'") + "`")
        w("")


def main():
    w("# Event-based VO benchmark: complete data pack")
    w("")
    w("Every value collected in this project, generated from the experiment folders in C:\\capstone. "
      "Raw files (full-rate trajectories, logs, 10 Hz profiles) are in the event-vo-benchmark repository; "
      "this file summarises all of them.")
    w("")
    w("Test machine: Intel Core i7-1255U (10 cores, 12 threads), 15.7 GB RAM (~7.7 GB to containers), "
      "Windows 11, Docker Desktop 4.97 on WSL 2. Evaluation: nearest-timestamp association within 0.02 s, "
      "Umeyama alignment, ATE = RMS position error, RPE = RMS translation error over 1 s windows "
      "(m and % of distance), coverage = % of ground-truth samples with an estimate within 0.1 s.")
    w("")
    lb = os.path.join(ROOT, "leaderboard.csv")
    if os.path.exists(lb):
        w("# Leaderboard (all algorithms)")
        w("")
        w(csv_table(lb, 3))
        w("")
    for k in KITS:
        kit_section(*k)
    dst = os.path.join(ROOT, "ALL_RESULTS_DATA_PACK.md")
    with open(dst, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(dst, f"{os.path.getsize(dst)/1024:.0f} KB")


if __name__ == "__main__":
    main()
