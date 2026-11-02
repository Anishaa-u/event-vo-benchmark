# event-vo-benchmark

A standardised evaluation framework for event-based visual odometry, with original results for
EVO, ESVO and ESVIO run under one protocol on one machine.

41030 Engineering Capstone, University of Technology Sydney, Spring 2026.
Anisha Uddin. Supervisor: Dr Teresa Vidal Calleja.

## What is here

| Folder | Contents | Framework requirement |
| --- | --- | --- |
| `datasets/registry.yaml` | Every sequence used, with sensor configuration, resolution, IMU, ground-truth topic and download source | R1, R2 |
| `algorithms/<id>/` | Dockerfile (pinned commit), headless launch generator, run and stop scripts for each algorithm | R9, R10, R11 |
| `adapters/` | Converters from each algorithm's output to TUM trajectory format | R11 |
| `evaluate/` | Timestamp association, SE(3)/Sim(3) alignment, ATE, RPE and tracking coverage | R3, R4, R5 |
| `profile/` | CPU and memory sampling at 10 Hz for any set of processes | R6, R7 |
| `results/<id>/` | Notes, per-run and summary CSVs, data pack, and `runs/` with every trajectory, ground truth, profile and log | R8, R9 |
| `results/leaderboard.csv` | One row per algorithm and sequence, with provenance, playback rate and coverage | R9, R11 |
| `tools/` | Scripts that build the data packs, this repository and the report | |

Algorithm identifiers (R10): `evo` (Rebecq et al., 2017), `esvo` (Zhou et al., 2021),
`esvio_chen2023` (Chen et al., 2023, arclab-hku/ESVIO). The ESVIO of Liu et al. (2023) is a
different system and is not included.

## Reproducing a run

1. Download the bags listed in `datasets/registry.yaml` into the kit's `data/` folder.
2. Build the container: `docker build -t <id> algorithms/<id>`.
3. Start it with the kit mounted at `/work`, run `make_headless_launch.py` once, then
   `bash run_<id>.sh <sequence> <run>` for each repeat.
4. Evaluate on the host: `python evaluate/evaluate_runs.py --align se3` (stereo and
   stereo-inertial) or `--align sim3` (monocular).

Bag files are not stored here because of their size (0.3 to 1.6 GB each).

## Test machine

Intel Core i7-1255U (10 cores, 12 threads), 15.7 GB RAM (about 7.7 GB available to Docker),
Windows 11 with Docker Desktop 4.97 on WSL 2.
