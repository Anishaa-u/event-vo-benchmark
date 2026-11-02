"""Figures for the final report. Run from C:\\capstone\\report:
    python make_figures.py            (all figures whose data exists)
"""

import glob
import os
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = r"C:\capstone"
sys.path.insert(0, os.path.join(ROOT, "evo_kit"))
from evaluate_runs import associate, load_tum  # noqa: E402
from evaluation import align, apply  # noqa: E402

OUT = os.path.join(ROOT, "report", "figures")
os.makedirs(OUT, exist_ok=True)
BLUE, ORANGE, GREEN, GREY = "#2F6DB3", "#E07B39", "#3A9E5F", "#6B6B6B"
ALGO_COLOR = {"EVO": ORANGE, "ESVO": BLUE, "ESVIO": GREEN}
plt.rcParams.update({"font.family": "Calibri", "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False})


def fig_pipeline():
    fig, ax = plt.subplots(figsize=(10, 3.3))
    ax.set_xlim(-1.5, 101.5)
    ax.set_ylim(-0.5, 31.5)
    ax.axis("off")
    boxes = [  # x, width, label, colour
        (0, 15, "Benchmark bag\nregistry\n(R1, R2)", "#EDEDED"),
        (20, 17, "Algorithm container\npinned commit,\nown ROS (R9-R11)", "#D9E2F3"),
        (42, 17, "Headless run script\nauthors' config,\nplayback rate (R6)", "#D9E2F3"),
        (64, 13, "Adapter\nto TUM\ntrajectory", "#E2EFDA"),
        (82, 18, "Evaluator\nalign SE(3)/Sim(3)\nATE, RPE,\ncoverage (R3-R5)", "#E2EFDA"),
    ]
    y, h = 15, 15
    for x, wd, label, color in boxes:
        ax.add_patch(FancyBboxPatch((x, y), wd, h, boxstyle="round,pad=0.4", fc=color, ec=GREY, lw=1))
        ax.text(x + wd / 2, y + h / 2, label, ha="center", va="center", fontsize=8.6)
    for (x0, w0, *_), (x1, *_) in zip(boxes, boxes[1:]):
        ax.annotate("", xy=(x1 - 0.6, y + h / 2), xytext=(x0 + w0 + 0.6, y + h / 2),
                    arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.2))
    ax.add_patch(FancyBboxPatch((42, 1), 17, 8, boxstyle="round,pad=0.4", fc="#FFF2CC", ec=GREY, lw=1))
    ax.text(50.5, 5, "Profiler, 10 Hz\nCPU, memory (R7)", ha="center", va="center", fontsize=8.6)
    ax.annotate("", xy=(50.5, y - 0.6), xytext=(50.5, 9.6), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.add_patch(FancyBboxPatch((82, 1), 18, 8, boxstyle="round,pad=0.4", fc="#FCE4D6", ec=GREY, lw=1))
    ax.text(91, 5, "Results table, repo\n3 repeats,\nprovenance (R8, R9)", ha="center", va="center", fontsize=8.6)
    ax.annotate("", xy=(91, 9.6), xytext=(91, y - 0.6), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1))
    ax.annotate("", xy=(81.4, 5), xytext=(59.6, 5), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1))
    fig.savefig(os.path.join(OUT, "fig_pipeline.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)


def errors(kit, mode, pattern="*_run*.txt"):
    runs = os.path.join(ROOT, kit, "runs")
    res = {}
    for e in sorted(glob.glob(os.path.join(runs, pattern))):
        m = re.match(r"(.+)_run(\d+)\.txt$", os.path.basename(e))
        gt = os.path.join(runs, f"gt_{m.group(1)}.txt")
        t_e, p_e = load_tum(e)
        t_g, p_g = load_tum(gt)
        if len(t_e) < 10:
            continue
        ie, ig = associate(t_e, t_g)
        if len(ie) < 10:
            continue
        s, R, tr = align(p_e[ie], p_g[ig], with_scale=(mode == "sim3"))
        err = np.linalg.norm(apply(p_e[ie], s, R, tr) - p_g[ig], axis=1)
        res[(m.group(1), int(m.group(2)))] = (t_e[ie] - t_g[0], err)
    return res


def fig_error_over_time(panels, name):
    """panels: list of (title, {label: (t, err, color, style)})"""
    fig, axes = plt.subplots(1, len(panels), figsize=(5 * len(panels), 3.2), sharey=False)
    axes = np.atleast_1d(axes)
    for ax, (title, series) in zip(axes, panels):
        for label, (t, err, color, style) in series.items():
            ax.plot(t, err, color=color, ls=style, lw=1.2, label=label)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Time from start of sequence (s)")
        ax.set_ylabel("Position error after alignment (m)")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=7.5, frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_pipeline()
    print("figures in", OUT, os.listdir(OUT))
