"""Copy every script, result, log and note from the experiment kits into the git repository
C:\\capstone\\event-vo-benchmark (layout follows Appendix C of the report). Bags and cloned
third-party source are not copied; README files record where to get them.
    python sync_repo.py
"""

import os
import shutil

ROOT = r"C:\capstone"
REPO = os.path.join(ROOT, "event-vo-benchmark")

# kit folder -> algorithm id (R10: unique identifiers)
KITS = {
    "esvo": os.path.join(ROOT, "esvo_pilot_kit"),
    "evo": os.path.join(ROOT, "evo_kit"),
    "esvio_chen2023": os.path.join(ROOT, "esvio_kit"),
}
ALGO_FILES = {  # files that define how an algorithm is built and run
    "esvo": ["Dockerfile", "make_headless_launch.py", "run_esvo.sh", "stop_esvo.sh", "clock_keeper.py",
             "bag_groundtruth_to_tum.py", ".devcontainer/devcontainer.json"],
    "evo": ["Dockerfile", "make_headless_launch.py", "run_evo.sh", "stop_evo.sh", "bag_pose_to_tum.py"],
    "esvio_chen2023": ["Dockerfile", "make_headless_launch.py", "run_esvio.sh", "stop_esvio.sh"],
}
ADAPTERS = {"esvio_chen2023": ["esvio_csv_to_tum.py"], "evo": ["bag_pose_to_tum.py"]}
RESULT_FILES = ["NOTES.txt", "results.csv", "summary.csv", "esvo_results.csv", "esvo_summary.csv",
                "ESVO_DATA_PACK.md", "EVO_DATA_PACK.md", "ESVIO_DATA_PACK.md"]
SKIP_EXT = {".bag", ".active"}


def copy(src, dst):
    if os.path.isfile(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        return 1
    return 0


def copy_tree(src, dst):
    n = 0
    for dirpath, _, files in os.walk(src):
        for f in files:
            if os.path.splitext(f)[1] in SKIP_EXT:
                continue
            s = os.path.join(dirpath, f)
            n += copy(s, os.path.join(dst, os.path.relpath(s, src)))
    return n


def main():
    n = 0
    for algo, kit in KITS.items():
        if not os.path.isdir(kit):
            continue
        for f in ALGO_FILES[algo]:
            n += copy(os.path.join(kit, f), os.path.join(REPO, "algorithms", algo, f))
        for f in ADAPTERS.get(algo, []):
            n += copy(os.path.join(kit, f), os.path.join(REPO, "adapters", f))
        for f in RESULT_FILES:
            n += copy(os.path.join(kit, f), os.path.join(REPO, "results", algo, f))
        if os.path.isdir(os.path.join(kit, "runs")):
            n += copy_tree(os.path.join(kit, "runs"), os.path.join(REPO, "results", algo, "runs"))
    # shared framework components
    for f in ["evaluation.py", "evaluate_runs.py"]:
        n += copy(os.path.join(KITS["evo"], f), os.path.join(REPO, "evaluate", f))
    n += copy(os.path.join(KITS["esvo"], "evaluate_esvo.py"), os.path.join(REPO, "evaluate", "evaluate_esvo.py"))
    n += copy(os.path.join(KITS["esvio_chen2023"], "profile_procs.py"), os.path.join(REPO, "profile", "profile_procs.py"))
    n += copy(os.path.join(KITS["esvo"], "profile_esvo.py"), os.path.join(REPO, "profile", "profile_esvo.py"))
    for f in ["ALL_RESULTS_DATA_PACK.md", "make_data_packs.py", "sync_repo.py"]:
        n += copy(os.path.join(ROOT, f), os.path.join(REPO, "results" if f.endswith(".md") else "tools", f))
    for f in ["leaderboard.csv"]:
        n += copy(os.path.join(ROOT, f), os.path.join(REPO, "results", f))
    for f in ["build_report.py", "make_figures.py"]:
        n += copy(os.path.join(ROOT, "report", f), os.path.join(REPO, "tools", f))
    print(f"Copied {n} files into {REPO}")


if __name__ == "__main__":
    main()
