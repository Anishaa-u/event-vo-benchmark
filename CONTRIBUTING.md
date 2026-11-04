# Adding an algorithm

If you want to add another algorithm, this is what I did for the three that are already in here. The point is that every result is produced the same way so they can be compared.

1. **Add it to `datasets/registry.yaml`** with a unique name (like `esvio_chen2023`), the paper and DOI, the code repo and exact commit, the ROS version, which sensors it needs and whether to use `se3` or `sim3` alignment. Only run it on sequences that have the right sensors.
2. **Write a Dockerfile** in `algorithms/<name>/` that clones the authors' code at that commit and builds it. If you have to fix anything to get it to build, do it in the Dockerfile with a comment saying why.
3. **Write a run script** based on `run_esvo.sh`, `run_evo.sh` or `run_esvio.sh`. It should:
   - use the authors' config and only change what you have to (saving the trajectory, removing anything that needs a display, the playback rate), and note every change
   - copy the bag into the container before playing it
   - start `profile_procs.py` with the algorithm's process names
   - save the trajectory as `runs/<sequence>_run<k>.txt` in TUM format (add a converter to `adapters/` if needed) and keep it even if the algorithm crashes
   - stop everything at the end and add a line to `runs/run_log.txt`

   Then add the files it needs to `tools/prepare_workdir.py`.
4. **Run it.** Do a pilot run first to find the fastest playback rate it can keep up with, then 3 runs per sequence with the same settings. Keep every run, even the ones that fail.
5. **Evaluate** with `python evaluate_runs.py --align se3` (or `sim3`).
6. **Add the results** as `results/<name>/` with `NOTES.txt` (hardware, commit, everything you changed, the pilot runs), `results.csv`, `summary.csv` and the `runs/` folder, and add your rows to `results/leaderboard.csv`. If you used different hardware that's fine, just say what it was.
