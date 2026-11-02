"""Build leaderboard.csv: one row per algorithm and sequence, combining accuracy (summary.csv),
efficiency (per-run profiles) and run conditions, with provenance (requirements R9, R11).
    python make_leaderboard.py
"""

import csv
import glob
import os

import numpy as np

ROOT = r"C:\capstone"
ENTRIES = [
    # algorithm id, kit, summary file, alignment, playback, commit, sequence prefix map
    ("evo", "evo_kit", "summary.csv", "sim3", None, "14c7291"),
    ("esvo", "esvo_pilot_kit", "summary.csv", "se3", "0.25x", "1639a43"),
    ("esvio_chen2023", "esvio_kit", "summary.csv", "se3", None, "b9e5aee"),
]
FIELDS = ["algorithm", "sequence", "alignment", "runs", "runs_completed", "coverage_mean_percent",
          "ate_mean_m", "ate_sd_m", "rpe_1s_mean_percent", "sim3_scale_mean", "cpu_mean_percent_one_core",
          "peak_memory_mb", "playback_rate", "real_time", "commit", "configuration", "evaluator", "hardware"]


def playback_rate(kit, seq):
    rates = set()
    p = os.path.join(kit, "runs", "run_log.txt")
    if os.path.exists(p):
        for line in open(p):
            if line.startswith(seq + "_run") and "rate " in line:
                rates.add(line.split("rate ")[1].split("x")[0].strip())
    return "/".join(sorted(rates)) + "x" if rates else ""


def completed(kit, seq):
    """Runs that neither stopped nor diverged: coverage >= 90% and fitted Sim(3) scale in [0.5, 2]."""
    n = 0
    p = os.path.join(kit, "results.csv")
    if not os.path.exists(p):
        return ""
    for r in csv.DictReader(open(p)):
        if r["sequence"] != seq or r.get("status", "ok") != "ok":
            continue
        if float(r["coverage_percent"]) >= 90 and 0.5 <= float(r["sim3_scale"]) <= 2:
            n += 1
    return str(n)


def main():
    rows = []
    for algo, kitname, summ, align, rate, commit in ENTRIES:
        kit = os.path.join(ROOT, kitname)
        p = os.path.join(kit, summ)
        if not os.path.exists(p):
            continue
        for s in csv.DictReader(open(p)):
            seq = s["sequence"]
            cpu, mem = [], []
            for prof in glob.glob(os.path.join(kit, "runs", f"{seq}_run*_profile.csv")):
                a = np.genfromtxt(prof, delimiter=",", names=True)
                if a.size < 2:
                    continue
                c = a["cpu_percent_one_core"][a["cpu_percent_one_core"] > 0]
                if c.size:
                    cpu.append(c.mean())
                    mem.append(a["rss_mb"].max())
            pr = playback_rate(kit, seq) or rate or ""
            rows.append({
                "algorithm": algo, "sequence": seq, "alignment": align,
                "runs": s.get("runs", ""), "runs_completed": completed(kit, seq),
                "coverage_mean_percent": s.get("coverage_mean_percent", ""),
                "ate_mean_m": s.get("ate_mean_m", ""), "ate_sd_m": s.get("ate_sd_m", ""),
                "rpe_1s_mean_percent": s.get("rpe_1s_mean_percent", ""),
                "sim3_scale_mean": s.get("sim3_scale_mean", ""),
                "cpu_mean_percent_one_core": f"{np.mean(cpu):.0f}" if cpu else "",
                "peak_memory_mb": f"{np.max(mem):.0f}" if mem else "",
                "playback_rate": pr, "real_time": "yes" if pr.startswith("1.0") else "no",
                "commit": commit, "configuration": "authors' default, untuned",
                "evaluator": "independent (this project)",
                "hardware": "i7-1255U laptop, Docker/WSL2",
            })
    with open(os.path.join(ROOT, "leaderboard.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r["algorithm"], r["sequence"], r["runs_completed"], r["ate_mean_m"], r["coverage_mean_percent"],
              r["cpu_mean_percent_one_core"], r["peak_memory_mb"], r["playback_rate"])


if __name__ == "__main__":
    main()
