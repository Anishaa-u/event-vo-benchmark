"""Evaluate saved ESVO trajectories against ground truth with the project's own
evaluation module (evaluation.py, Sections 3.2 and 4.1 of the report).

Runs on any computer with Python and NumPy, no ROS needed.
    python evaluate_esvo.py
It looks for runs/<sequence>_run<k>.txt (ESVO output) and runs/gt_<sequence>.txt,
and writes esvo_results.csv and esvo_summary.csv.

Metrics per run (requirements R3 to R5 of the framework):
  ATE RMSE after SE(3) alignment (m), plus Sim(3) ATE and fitted scale as a scale check
  RPE: RMSE of translation error over 1.0 s windows (m), and as % of distance travelled
  Coverage: % of ground-truth time with an associated estimate
"""

import csv
import glob
import os
import re

import numpy as np

from evaluation import align, apply, ate_rmse

MAX_DT = 0.02        # s, maximum timestamp difference for association
RPE_WINDOW = 1.0     # s


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
    a = np.array(rows)
    return a[:, 0], a[:, 1:4]


def associate(t_est, t_gt):
    idx = np.searchsorted(t_gt, t_est)
    idx = np.clip(idx, 1, len(t_gt) - 1)
    left, right = t_gt[idx - 1], t_gt[idx]
    idx = np.where(np.abs(t_est - left) <= np.abs(t_est - right), idx - 1, idx)
    ok = np.abs(t_gt[idx] - t_est) <= MAX_DT
    return np.nonzero(ok)[0], idx[ok]


def coverage(t_est, t_gt, gap=0.1):
    """Share of ground-truth samples that have an estimate within `gap` seconds."""
    idx = np.clip(np.searchsorted(t_est, t_gt), 1, len(t_est) - 1)
    nearest = np.minimum(np.abs(t_est[idx] - t_gt), np.abs(t_est[idx - 1] - t_gt))
    return 100.0 * np.mean(nearest <= gap)


def rpe_time(t, est, gt, window=RPE_WINDOW):
    j = np.searchsorted(t, t + window)
    valid = j < len(t)
    i, j = np.nonzero(valid)[0], j[valid]
    d_est, d_gt = est[j] - est[i], gt[j] - gt[i]
    err = np.linalg.norm(d_est - d_gt, axis=1)
    dist = np.linalg.norm(d_gt, axis=1)
    rmse = float(np.sqrt(np.mean(err ** 2)))
    pct = float(100.0 * np.sum(err) / np.sum(dist)) if np.sum(dist) > 0 else float("nan")
    return rmse, pct


def evaluate_run(est_path, gt_path):
    t_e, p_e = load_tum(est_path)
    t_g, p_g = load_tum(gt_path)
    ie, ig = associate(t_e, t_g)
    if len(ie) < 10:
        raise RuntimeError(f"Only {len(ie)} poses associated. Check timestamps in {est_path}")
    est, gt, t = p_e[ie], p_g[ig], t_e[ie]
    s, R, tr = align(est, gt, with_scale=False)
    al = apply(est, s, R, tr)
    s3, R3, tr3 = align(est, gt, with_scale=True)
    rpe_m, rpe_pct = rpe_time(t, al, gt)
    return {
        "associated_poses": len(ie),
        "coverage_percent": round(coverage(t_e, t_g), 1),
        "ate_se3_m": ate_rmse(al, gt),
        "ate_sim3_m": ate_rmse(apply(est, s3, R3, tr3), gt),
        "sim3_scale": float(s3),
        "rpe_1s_rmse_m": rpe_m,
        "rpe_1s_percent": rpe_pct,
    }


def main():
    results = []
    for est_path in sorted(glob.glob("runs/*_run*.txt")):
        m = re.match(r"(.+)_run(\d+)\.txt$", os.path.basename(est_path))
        if not m:
            continue
        seq, run = m.group(1), int(m.group(2))
        gt_path = os.path.join("runs", f"gt_{seq}.txt")
        if not os.path.exists(gt_path):
            print(f"Skipping {est_path}: no {gt_path}")
            continue
        r = {"sequence": seq, "run": run, **evaluate_run(est_path, gt_path)}
        results.append(r)
        print(f"{seq} run {run}: ATE {r['ate_se3_m']:.4f} m, RPE {r['rpe_1s_percent']:.2f}%, "
              f"coverage {r['coverage_percent']:.1f}%, Sim(3) scale {r['sim3_scale']:.3f}")
    if not results:
        print("No runs found in runs/")
        return
    with open("esvo_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    summary = []
    for seq in sorted({r["sequence"] for r in results}):
        sel = [r for r in results if r["sequence"] == seq]
        ate = [r["ate_se3_m"] for r in sel]
        summary.append({
            "sequence": seq, "runs": len(sel),
            "ate_se3_mean_m": np.mean(ate),
            "ate_se3_sd_m": np.std(ate, ddof=1) if len(ate) > 1 else 0.0,
            "rpe_1s_mean_percent": np.mean([r["rpe_1s_percent"] for r in sel]),
            "coverage_mean_percent": np.mean([r["coverage_percent"] for r in sel]),
            "sim3_scale_mean": np.mean([r["sim3_scale"] for r in sel]),
        })
    with open("esvo_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)
    print("\nSummary")
    for s in summary:
        print(f"{s['sequence']}: {s['runs']} runs, ATE {s['ate_se3_mean_m']*100:.1f} cm "
              f"(sd {s['ate_se3_sd_m']*100:.1f} cm), coverage {s['coverage_mean_percent']:.0f}%")


if __name__ == "__main__":
    main()
