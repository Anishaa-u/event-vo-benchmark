"""Generate fill.json (placeholder text for the report) from the experiment result files, so that
every number in the report comes from the data. Hand-written prose lives in prose.json.
    python fill_values.py
"""

import csv
import json
import os
import re

ROOT = r"C:\capstone"
HERE = os.path.join(ROOT, "report")


def results(kit):
    p = os.path.join(ROOT, kit, "results.csv")
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def run_log(kit):
    out = {}
    p = os.path.join(ROOT, kit, "runs", "run_log.txt")
    if os.path.exists(p):
        for line in open(p):
            name = line.split(" |")[0].strip()
            poses = re.search(r"poses (\d+)", line)
            cpu = re.search(r"Mean CPU \(% of one core\): ([\d.]+)", line)
            mem = re.search(r"Peak memory: (\d+)", line)
            out[name] = (poses.group(1) if poses else "", cpu.group(1) if cpu else "", mem.group(1) if mem else "")
    return out


def table(header, rows):
    return "\n".join(["| " + " | ".join(header) + " |"] + ["| " + " | ".join(r) + " |" for r in rows])


def f(x, n=3):
    try:
        return f"{float(x):.{n}f}"
    except (TypeError, ValueError):
        return "n/a"


def main():
    fill = {}
    # EVO
    log = run_log("evo_kit")
    rows = []
    for r in results("evo_kit"):
        name = f"{r['sequence']}_run{r['run']}"
        poses, cpu, mem = log.get(name, ("", "", ""))
        rows.append([r["sequence"], r["run"], poses, f(r["coverage_percent"], 1), "Yes",
                     f(r["ate_sim3_m"]), f(r["sim3_scale"], 2), f(r["rpe_1s_percent"], 0),
                     f(cpu, 0), mem])
    fill["EVO_MAIN_TABLE"] = table(["Sequence", "Run", "Poses", "Coverage (%)", "Tracker crashed",
                                    "ATE, Sim(3) (m)", "Sim(3) scale", "RPE over 1 s (%)",
                                    "Mean CPU (%)", "Peak memory (MB)"], rows)
    # ESVIO
    log = run_log("esvio_kit")
    rows = []
    for r in results("esvio_kit"):
        name = f"{r['sequence']}_run{r['run']}"
        poses, cpu, mem = log.get(name, ("", "", ""))
        seq = "indoor_" + r["sequence"]
        rows.append([seq, r["run"], poses, f(r["coverage_percent"], 1), f(r["ate_se3_m"]),
                     f(r["ate_sim3_m"]), f(r["sim3_scale"], 3), f(r["rpe_1s_percent"], 1), f(cpu, 0), mem])
    if rows:
        fill["ESVIO_MAIN_TABLE"] = table(["Sequence", "Run", "Poses", "Coverage (%)", "ATE, SE(3) (m)",
                                          "ATE, Sim(3) (m)", "Sim(3) scale", "RPE over 1 s (%)",
                                          "Mean CPU (%)", "Peak memory (MB)"], rows)
    # leaderboard summary table
    lb = os.path.join(ROOT, "leaderboard.csv")
    if os.path.exists(lb):
        names = {"evo": "EVO", "esvo": "ESVO", "esvio_chen2023": "ESVIO"}
        seqs = {"flying1": "MVSEC indoor_flying1", "flying3": "MVSEC indoor_flying3",
                "shapes_6dof": "RPG shapes_6dof", "boxes_6dof": "RPG boxes_6dof"}
        rows = []
        for r in csv.DictReader(open(lb)):
            done = int(r["runs_completed"] or 0)
            ate = f"{float(r['ate_mean_m']):.3f} ± {float(r['ate_sd_m']):.3f}" if done else "Not meaningful (failed)"
            rows.append([names[r["algorithm"]], seqs.get(r["sequence"], r["sequence"]),
                         f"{r['runs_completed']} of {r['runs']}", f(r["coverage_mean_percent"], 1),
                         ate + (" (Sim(3))" if r["alignment"] == "sim3" and done else ""),
                         f(r["rpe_1s_mean_percent"], 0) if done else "n/a",
                         f"{float(r['cpu_mean_percent_one_core'])/100:.1f}", r["peak_memory_mb"],
                         r["playback_rate"].replace("x", " times")])
        fill["SUMMARY_TABLE"] = table(["Algorithm", "Sequence", "Runs completed", "Mean coverage (%)",
                                       "ATE, mean ± SD (m)", "RPE over 1 s (%)", "Mean CPU (cores)",
                                       "Peak memory (MB)", "Playback"], rows)
    prose = os.path.join(HERE, "prose.json")
    if os.path.exists(prose):
        fill.update(json.load(open(prose, encoding="utf-8")))
    json.dump(fill, open(os.path.join(HERE, "fill.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("filled:", ", ".join(sorted(fill)))


if __name__ == "__main__":
    main()
