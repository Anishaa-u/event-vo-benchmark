"""Evaluate saved trajectories against ground truth with the project's own evaluation module
(evaluation.py). Same association, alignment and metrics as evaluate_esvo.py, generalised to
any algorithm (framework requirements R3 to R5, R8).

Runs on any computer with Python and NumPy, no ROS needed.
    python evaluate_runs.py --align se3     (stereo and stereo-inertial methods)
    python evaluate_runs.py --align sim3    (monocular methods, requirement R4)
It looks for runs/<sequence>_run<k>.txt and runs/gt_<sequence>.txt, and writes results.csv and
summary.csv. A run with too few poses to evaluate is recorded as a failure, not skipped.

Metrics per run:
  ATE RMSE after SE(3) and after Sim(3) alignment (m), and the fitted Sim(3) scale
  RPE over 1.0 s windows after the primary alignment: RMSE (m) and % of distance travelled
  Coverage: % of ground-truth samples with an estimate within 0.1 s
"""

import argparse
import csv
import glob
import os
import re

import numpy as np

from evaluation import align, apply, ate_rmse

MAX_DT = 0.02        # s, maximum timestamp difference for association
RPE_WINDOW = 1.0     # s
MIN_POSES = 10


def load_tum(path):
    rows = []
    with open(path) as f:
        for line in f:
            parts = line.replace(",", " ").split()
            if len(parts) < 4 or parts[0].startswith("#"):
                continue
            try:
                rows.append([float(x) for x in parts[:4]])
            except ValueError:
                continue
    if not rows:
        return np.zeros(0), np.zeros((0, 3))
    a = np.array(rows)
    order = np.argsort(a[:, 0])
    return a[order, 0], a[order, 1:4]


def associate(t_est, t_gt):
    idx = np.searchsorted(t_gt, t_est)
    idx = np.clip(idx, 1, len(t_gt) - 1)
    left, right = t_gt[idx - 1], t_gt[idx]
    idx = np.where(np.abs(t_est - left) <= np.abs(t_est - right), idx - 1, idx)
    ok = np.abs(t_gt[idx] - t_est) <= MAX_DT
    return np.nonzero(ok)[0], idx[ok]


def coverage(t_est, t_gt, gap=0.1):
    """Share of ground-truth samples that have an estimate within `gap` seconds."""
    if len(t_est) < 2:
        return 0.0
    idx = np.clip(np.searchsorted(t_est, t_gt), 1, len(t_est) - 1)
    nearest = np.minimum(np.abs(t_est[idx] - t_gt), np.abs(t_est[idx - 1] - t_gt))
    return 100.0 * np.mean(nearest <= gap)


def rpe_time(t, est, gt, window=RPE_WINDOW):
    j = np.searchsorted(t, t + window)
    valid = j < len(t)
    i, j = np.nonzero(valid)[0], j[valid]
    if len(i) == 0:
        return float("nan"), float("nan")
    d_est, d_gt = est[j] - est[i], gt[j] - gt[i]
    err = np.linalg.norm(d_est - d_gt, axis=1)
    dist = np.linalg.norm(d_gt, axis=1)
    rmse = float(np.sqrt(np.mean(err ** 2)))
    pct = float(100.0 * np.sum(err) / np.sum(dist)) if np.sum(dist) > 0 else float("nan")
    return rmse, pct


def evaluate_run(est_path, gt_path, primary):
    t_e, p_e = load_tum(est_path)
    t_g, p_g = load_tum(gt_path)
    ie, ig = associate(t_e, t_g) if len(t_e) else (np.zeros(0, int), np.zeros(0, int))
    base = {"estimated_poses": len(t_e), "associated_poses": len(ie),
            "coverage_percent": round(coverage(t_e, t_g), 1)}
    if len(ie) < MIN_POSES:
        return {**base, "status": "failed", "ate_se3_m": "", "ate_sim3_m": "", "sim3_scale": "",
                "rpe_1s_rmse_m": "", "rpe_1s_percent": ""}
    est, gt, t = p_e[ie], p_g[ig], t_e[ie]
    s, R, tr = align(est, gt, with_scale=False)
    al_se3 = apply(est, s, R, tr)
    s3, R3, tr3 = align(est, gt, with_scale=True)
    al_sim3 = apply(est, s3, R3, tr3)
    rpe_m, rpe_pct = rpe_time(t, al_sim3 if primary == "sim3" else al_se3, gt)
    return {**base, "status": "ok", "ate_se3_m": ate_rmse(al_se3, gt),
            "ate_sim3_m": ate_rmse(al_sim3, gt), "sim3_scale": float(s3),
            "rpe_1s_rmse_m": rpe_m, "rpe_1s_percent": rpe_pct}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--align", choices=["se3", "sim3"], default="se3")
    ap.add_argument("--runs", default="runs")
    args = ap.parse_args()
    primary_ate = "ate_sim3_m" if args.align == "sim3" else "ate_se3_m"

    results = []
    for est_path in sorted(glob.glob(os.path.join(args.runs, "*_run*.txt"))):
        m = re.match(r"(.+)_run(\d+)\.txt$", os.path.basename(est_path))
        if not m:
            continue
        seq, run = m.group(1), int(m.group(2))
        gt_path = os.path.join(args.runs, f"gt_{seq}.txt")
        if not os.path.exists(gt_path):
            print(f"Skipping {est_path}: no {gt_path}")
            continue
        r = {"sequence": seq, "run": run, "alignment": args.align,
             **evaluate_run(est_path, gt_path, args.align)}
        results.append(r)
        if r["status"] == "ok":
            print(f"{seq} run {run}: ATE ({args.align}) {r[primary_ate]:.4f} m, "
                  f"RPE {r['rpe_1s_percent']:.2f}%, coverage {r['coverage_percent']:.1f}%, "
                  f"Sim(3) scale {r['sim3_scale']:.3f}")
        else:
            print(f"{seq} run {run}: FAILED ({r['estimated_poses']} poses, "
                  f"coverage {r['coverage_percent']:.1f}%)")
    if not results:
        print(f"No runs found in {args.runs}/")
        return
    with open("results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    summary = []
    for seq in sorted({r["sequence"] for r in results}):
        sel = [r for r in results if r["sequence"] == seq]
        ok = [r for r in sel if r["status"] == "ok"]
        ate = [r[primary_ate] for r in ok]
        summary.append({
            "sequence": seq, "alignment": args.align, "runs": len(sel), "runs_ok": len(ok),
            "ate_mean_m": np.mean(ate) if ok else "",
            "ate_sd_m": np.std(ate, ddof=1) if len(ok) > 1 else (0.0 if ok else ""),
            "rpe_1s_mean_percent": np.mean([r["rpe_1s_percent"] for r in ok]) if ok else "",
            "coverage_mean_percent": np.mean([r["coverage_percent"] for r in sel]),
            "sim3_scale_mean": np.mean([r["sim3_scale"] for r in ok]) if ok else "",
        })
    with open("summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)
    print("\nSummary")
    for s in summary:
        if s["runs_ok"]:
            print(f"{s['sequence']}: {s['runs_ok']}/{s['runs']} runs ok, ATE {s['ate_mean_m']*100:.1f} cm "
                  f"(sd {s['ate_sd_m']*100:.1f} cm), coverage {s['coverage_mean_percent']:.0f}%")
        else:
            print(f"{s['sequence']}: 0/{s['runs']} runs ok, coverage {s['coverage_mean_percent']:.0f}%")


if __name__ == "__main__":
    main()
