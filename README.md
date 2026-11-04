# event-vo-benchmark

This is the evaluation framework from my 41030 Engineering Capstone at UTS (2026, supervisor Dr Teresa Vidal Calleja). It's for comparing event-based visual odometry algorithms fairly. Each algorithm runs in its own Docker container at a fixed code version, the bag is played at a recorded rate, CPU and memory are logged while it runs, and every trajectory is scored with the same evaluation code.

So far it has EVO, ESVO and ESVIO in it, each run 3 times on 2 sequences on my laptop. You can use it to evaluate your own trajectories, rerun any of the three algorithms, or add a new algorithm (see CONTRIBUTING.md).

## Results

Laptop: i7-1255U (10 cores), about 7.7 GB of RAM available to Docker. 3 runs per algorithm and sequence. The full numbers are in `results/leaderboard.csv`, each algorithm's folder in `results/`, and `results/ALL_RESULTS_DATA_PACK.md`.

| Algorithm | Sequence | Runs completed | Coverage | ATE (mean ± SD) | CPU | Peak memory | Playback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ESVIO | MVSEC indoor_flying1 | 3/3 | 100% | 0.187 ± 0.005 m | 1.4 cores | 0.76 GB | 0.25x (real time also worked, 0.184 m) |
| ESVIO | MVSEC indoor_flying3 | 3/3 | 99% | 0.264 ± 0.034 m | 1.8 cores | 0.90 GB | 0.25x |
| ESVO | MVSEC indoor_flying1 | 3/3 | 99.6% | 0.227 ± 0.044 m | 3.4 cores | 1.6 GB | 0.25x (couldn't keep up at 0.5x) |
| ESVO | MVSEC indoor_flying3 | 3/3 | 99.3% | 0.355 ± 0.029 m | 2.9 cores | 1.6 GB | 0.25x |
| EVO | RPG shapes_6dof | 0/3 | 9.7% | crashed | 3.1 cores | 0.75 GB | 0.5x |
| EVO | RPG boxes_6dof | 0/3 | 7.9% | crashed | 5.1 cores | 0.83 GB | 0.5x |

ATE uses SE(3) alignment for the stereo methods and Sim(3) for EVO because it's monocular. I counted a run as completed if it covered at least 90% of the sequence and the fitted scale was between 0.5 and 2. `results/<algorithm>/NOTES.txt` has everything I had to change to get each one building and running, plus the pilot runs. One thing worth knowing: ESVIO fails on the ESVO-edited MVSEC bags because they start mid-flight, but works on the original MVSEC bags.

ESVIO here is the one by Chen, Guan and Lu (2023), arclab-hku/ESVIO. There's another ESVIO by Liu et al. (2023) but it doesn't have code you can build.

## Folders

- `datasets/registry.yaml`: every sequence (file, where to download it, sensor, resolution, IMU, ground truth topic) and every algorithm (paper, code, commit, ROS version, sensors needed, alignment)
- `algorithms/<name>/`: Dockerfile and the run/stop scripts for that algorithm
- `adapters/`: scripts that convert each algorithm's output to TUM format
- `evaluate/`: `evaluation.py` (alignment, ATE, RPE) and `evaluate_runs.py` (matching poses, coverage, failed runs, summaries)
- `profile/`: `profile_procs.py`, logs CPU and memory of the algorithm's processes every 0.1 s
- `results/`: notes, CSVs, trajectories, ground truth, profiles and logs for every run
- `tools/`: `prepare_workdir.py` sets up a folder for running one algorithm; the other scripts made the leaderboard and figures for my report

## Evaluating your own trajectories

You only need Python 3 and NumPy for this. Put your files in TUM format (`timestamp x y z qx qy qz qw`, timestamps in seconds) like this:

```
my_eval/runs/gt_flying1.txt        ground truth
my_eval/runs/flying1_run1.txt      your trajectory, run 1
my_eval/runs/flying1_run2.txt      run 2, and so on
```

Then from `my_eval`:

```
python path/to/evaluate/evaluate_runs.py --align se3     # stereo / visual-inertial
python path/to/evaluate/evaluate_runs.py --align sim3    # monocular
```

You get `results.csv` (one row per run) and `summary.csv` (mean and SD per sequence) with ATE (SE(3) and Sim(3)), the fitted scale, RPE over 1 s windows and coverage. Poses are matched to ground truth within 0.02 s, and coverage is the percentage of ground truth samples that have an estimate within 0.1 s.

## Rerunning EVO, ESVO or ESVIO

You need Docker (Docker Desktop with at least 8 GB of memory is fine), about 25 GB of disk space (each image is 4-8 GB and the bags are 0.3-1.9 GB each), and Python 3 with NumPy for the evaluation. Build one image at a time, because building two at once crashed Docker for me.

1. Set up a folder for the algorithm:
   ```
   python tools/prepare_workdir.py esvo work/esvo      # or evo work/evo, esvio_chen2023 work/esvio
   ```
2. Download the bags into its `data/` folder:
   - ESVO: `indoor_flying1_edited.bag` and `indoor_flying3_edited.bag` from the ESVO project page (edited upenn dataset, Google Drive folder `1FbABakLVcWAGsA7E5CN11vVovdWQfDEx`)
   - ESVIO: the same two edited bags (for the ground truth), plus `indoor_flying1_data.bag` and `indoor_flying3_data.bag` from https://visiondata.cis.upenn.edu/mvsec/indoor_flying/ into `data_orig/`
   - EVO: `shapes_6dof.bag` and `boxes_6dof.bag` from https://rpg.ifi.uzh.ch/datasets/davis/
3. Build and start the container:
   ```
   cd work/esvo
   docker build -t esvo .
   docker run -d --name esvo -v "$(pwd):/work" esvo sleep infinity     # PowerShell: -v "${PWD}:/work"
   docker exec -it esvo bash
   ```
4. Inside the container, run the setup once and get the ground truth:
   ```
   cd /work
   python3 make_headless_launch.py      # for EVO it's python, not python3 (ROS Melodic)
   python3 bag_groundtruth_to_tum.py data/indoor_flying1_edited.bag runs/gt_flying1.txt /davis/left/pose
   python3 bag_groundtruth_to_tum.py data/indoor_flying3_edited.bag runs/gt_flying3.txt /davis/left/pose
   # EVO: python bag_pose_to_tum.py data/shapes_6dof.bag runs/gt_shapes_6dof.txt /optitrack/davis
   ```
5. Run each sequence 3 times, e.g. `bash run_esvo.sh flying1 1`, then runs 2 and 3:
   - `run_esvo.sh`: defaults to 0.25x with the sync timer at 25 Hz
   - `run_esvio.sh`: defaults to the original bag at 0.25x (`RATE=1.0` for real time)
   - `run_evo.sh`: defaults to EVO's flyingroom config with the RPG calibration, frame bootstrapping, 0.5x

   Each run saves the trajectory to `runs/<sequence>_run<k>.txt`, the CPU/memory profile to `runs/<sequence>_run<k>_profile.csv`, the log to `runs/logs/`, and adds a line to `runs/run_log.txt`. You can change settings with environment variables, e.g. `RATE=0.5 bash run_esvo.sh flying1 1`, but write down anything you change.
6. Back on your own computer, in the same folder:
   ```
   python evaluate_runs.py --align se3      # --align sim3 for EVO
   ```

## Rules I used

These came out of the report (R1-R11):

1. Keep a list of which sequences each algorithm can actually run on.
2. Name the exact version of each sequence (the edited and original MVSEC bags are different).
3. Report ATE (RMS, metres) and RPE together, with units.
4. SE(3) alignment for stereo/visual-inertial, Sim(3) for monocular.
5. Always report coverage with ATE, and keep failed runs.
6. Record the playback rate and the rate the algorithm actually managed.
7. Record CPU and memory, and the hardware.
8. At least 3 runs per algorithm and sequence.
9. Record who ran it, the commit, the config and every change.
10. Give each algorithm a unique name linked to its paper and code.
11. One container per algorithm, adapters, and one shared results table.

The algorithms' own code isn't in this repo. The Dockerfiles download it from the authors' repositories when you build, so it stays under the authors' licences. The same goes for the datasets.
