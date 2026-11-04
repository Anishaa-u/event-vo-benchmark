"""Assemble a self-contained working folder for one algorithm, ready to mount into its container.

    python tools/prepare_workdir.py esvo work/esvo
    python tools/prepare_workdir.py evo work/evo
    python tools/prepare_workdir.py esvio_chen2023 work/esvio

The folder gets the algorithm's Dockerfile and run scripts, the shared profiler, adapters and
evaluator, and empty data/ and runs/ folders. Put the bags listed in datasets/registry.yaml into
data/ (and, for esvio_chen2023, the original MVSEC bags into data_orig/), then follow README.md.
"""

import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = {
    "esvo": ["profile/profile_esvo.py", "evaluate/evaluation.py", "evaluate/evaluate_runs.py",
             "evaluate/evaluate_esvo.py"],
    "evo": ["profile/profile_procs.py", "adapters/record_pose.py", "adapters/bag_pose_to_tum.py",
            "evaluate/evaluation.py", "evaluate/evaluate_runs.py"],
    "esvio_chen2023": ["profile/profile_procs.py", "adapters/esvio_csv_to_tum.py", "algorithms/esvo/bag_groundtruth_to_tum.py",
                       "evaluate/evaluation.py", "evaluate/evaluate_runs.py"],
}


def main(algo, dst):
    if algo not in SHARED:
        sys.exit(f"Unknown algorithm '{algo}'. Choose one of: {', '.join(SHARED)}")
    src = os.path.join(REPO, "algorithms", algo)
    os.makedirs(dst, exist_ok=True)
    n = 0
    for dirpath, _, files in os.walk(src):
        for f in files:
            s = os.path.join(dirpath, f)
            d = os.path.join(dst, os.path.relpath(s, src))
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(s, d)
            n += 1
    for rel in SHARED[algo]:
        shutil.copy2(os.path.join(REPO, rel), os.path.join(dst, os.path.basename(rel)))
        n += 1
    for sub in ("data", "runs") + (("data_orig",) if algo == "esvio_chen2023" else ()):
        os.makedirs(os.path.join(dst, sub), exist_ok=True)
    print(f"Prepared {dst} for {algo} ({n} files). Next: put the bags in {dst}/data, then see README.md.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
