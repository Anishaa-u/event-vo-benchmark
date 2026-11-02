# Event-based VO benchmark: complete data pack

Every value collected in this project, generated from the experiment folders in C:\capstone. Raw files (full-rate trajectories, logs, 10 Hz profiles) are in the event-vo-benchmark repository; this file summarises all of them.

Test machine: Intel Core i7-1255U (10 cores, 12 threads), 15.7 GB RAM (~7.7 GB to containers), Windows 11, Docker Desktop 4.97 on WSL 2. Evaluation: nearest-timestamp association within 0.02 s, Umeyama alignment, ATE = RMS position error, RPE = RMS translation error over 1 s windows (m and % of distance), coverage = % of ground-truth samples with an estimate within 0.1 s.

# Leaderboard (all algorithms)

| algorithm | sequence | alignment | runs | runs_completed | coverage_mean_percent | ate_mean_m | ate_sd_m | rpe_1s_mean_percent | sim3_scale_mean | cpu_mean_percent_one_core | peak_memory_mb | playback_rate | real_time | commit | configuration | evaluator | hardware |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| evo | boxes_6dof | sim3 | 3 | 0 | 7.900 | 0.302 | 0.051 | 93.727 | 0.127 | 513 | 831 | 0.5x | no | 14c7291 | authors' default, untuned | independent (this project) | i7-1255U laptop, Docker/WSL2 |
| evo | shapes_6dof | sim3 | 3 | 0 | 9.733 | 0.199 | 0.011 | 83.505 | 0.147 | 312 | 749 | 0.5x | no | 14c7291 | authors' default, untuned | independent (this project) | i7-1255U laptop, Docker/WSL2 |
| esvo | flying1 | se3 | 3 | 3 | 99.567 | 0.227 | 0.044 | 21.493 | 1.081 | 335 | 1625 | 0.25x | no | 1639a43 | authors' default, untuned | independent (this project) | i7-1255U laptop, Docker/WSL2 |
| esvo | flying3 | se3 | 3 | 3 | 99.300 | 0.355 | 0.029 | 32.026 | 0.983 | 290 | 1620 | 0.25x | no | 1639a43 | authors' default, untuned | independent (this project) | i7-1255U laptop, Docker/WSL2 |
| esvio_chen2023 | flying1 | se3 | 3 | 3 | 100.000 | 0.187 | 0.005 | 14.821 | 1.077 | 135 | 764 | 0.25x | no | b9e5aee | authors' default, untuned | independent (this project) | i7-1255U laptop, Docker/WSL2 |
| esvio_chen2023 | flying3 | se3 | 3 | 3 | 98.967 | 0.264 | 0.034 | 23.642 | 1.043 | 180 | 900 | 0.25x | no | b9e5aee | authors' default, untuned | independent (this project) | i7-1255U laptop, Docker/WSL2 |

# ESVO (Zhou et al., 2021)

Primary alignment: SE3 (requirement R4). All values below are original data from this project.

### Per sequence (summary.csv)
| sequence | alignment | runs | runs_ok | ate_mean_m | ate_sd_m | rpe_1s_mean_percent | coverage_mean_percent | sim3_scale_mean |
|---|---|---|---|---|---|---|---|---|
| flying1 | se3 | 3 | 3 | 0.2270 | 0.0442 | 21.4933 | 99.5667 | 1.0809 |
| flying3 | se3 | 3 | 3 | 0.3550 | 0.0291 | 32.0265 | 99.3000 | 0.9829 |

### Per run (results.csv)
| sequence | run | alignment | estimated_poses | associated_poses | coverage_percent | status | ate_se3_m | ate_sim3_m | sim3_scale | rpe_1s_rmse_m | rpe_1s_percent |
|---|---|---|---|---|---|---|---|---|---|---|---|
| flying1 | 1 | se3 | 2171 | 2128 | 99.6000 | ok | 0.2079 | 0.1824 | 1.0742 | 0.0995 | 19.4857 |
| flying1 | 2 | se3 | 2358 | 2308 | 99.7000 | ok | 0.1956 | 0.1452 | 1.0976 | 0.0973 | 18.9575 |
| flying1 | 3 | se3 | 2363 | 2324 | 99.4000 | ok | 0.2776 | 0.2609 | 1.0709 | 0.1529 | 26.0365 |
| flying3 | 1 | se3 | 2325 | 2312 | 98.3000 | ok | 0.3560 | 0.3558 | 1.0107 | 0.1875 | 28.9415 |
| flying3 | 2 | se3 | 2341 | 2328 | 99.9000 | ok | 0.3255 | 0.3245 | 0.9753 | 0.1288 | 24.9041 |
| flying3 | 3 | se3 | 1797 | 1785 | 99.7000 | ok | 0.3836 | 0.3817 | 0.9628 | 0.2185 | 42.2337 |

### Per sequence (esvo_summary.csv)
| sequence | runs | ate_se3_mean_m | ate_se3_sd_m | rpe_1s_mean_percent | coverage_mean_percent | sim3_scale_mean |
|---|---|---|---|---|---|---|
| flying1 | 3 | 0.2270 | 0.0442 | 21.4933 | 99.5667 | 1.0809 |
| flying3 | 3 | 0.3550 | 0.0291 | 32.0265 | 99.3000 | 0.9829 |

### Per run (esvo_results.csv)
| sequence | run | associated_poses | coverage_percent | ate_se3_m | ate_sim3_m | sim3_scale | rpe_1s_rmse_m | rpe_1s_percent |
|---|---|---|---|---|---|---|---|---|
| flying1 | 1 | 2128 | 99.6000 | 0.2079 | 0.1824 | 1.0742 | 0.0995 | 19.4857 |
| flying1 | 2 | 2308 | 99.7000 | 0.1956 | 0.1452 | 1.0976 | 0.0973 | 18.9575 |
| flying1 | 3 | 2324 | 99.4000 | 0.2776 | 0.2609 | 1.0709 | 0.1529 | 26.0365 |
| flying3 | 1 | 2312 | 98.3000 | 0.3560 | 0.3558 | 1.0107 | 0.1875 | 28.9415 |
| flying3 | 2 | 2328 | 99.9000 | 0.3255 | 0.3245 | 0.9753 | 0.1288 | 24.9041 |
| flying3 | 3 | 1785 | 99.7000 | 0.3836 | 0.3817 | 0.9628 | 0.2185 | 42.2337 |

### Experiment record (notes, verbatim)

```
ESVO pilot - experiment notes
=============================
Hardware
  CPU: 12th Gen Intel(R) Core(TM) i7-1255U
  Cores / threads: 10 / 12
  RAM: 15.7 GB
  OS: Microsoft Windows 11 Home build 26200
  Docker engine: 29.9.2 (Docker Desktop 4.97.0, WSL 2 backend)

Data (ESVO project page, edited upenn stereo dataset, Google Drive)
  indoor_flying1_edited.bag  655 MB
  indoor_flying3_edited.bag  627 MB
  Downloaded: 2026-11-02

Setup changes
  Dockerfile: removed separate rpg_dvs_ros clone (already in ESVO dependencies.yaml)
  Dockerfile: added rosdep install step (first build failed: image_geometry missing)
  Base image osrf/ros:noetic-desktop (Ubuntu 20.04, ROS Noetic). Container sees 12 threads, ~7.7 GB RAM (WSL 2 default)

ESVO commit: 1639a43ca3c5411b73a083c654f1aef73d8e0319 (HKUST-Aerial-Robotics/ESVO, master)

Config changes (everything else is ESVO's shipped upenn configuration)
  cfg/tracking/tracking_upenn.yaml
    SAVE_TRAJECTORY: False -> True
    PATH_TO_SAVE_TRAJECTORY: /home/zhouyi/... -> /tmp/esvo_result/ (copied to runs/<seq>_run<k>.txt)
  launch/system/system_upenn_headless.launch = system_upenn.launch with rqt_gui and rviz removed (no display)
  Sync timer (global_timer): 50 Hz -> 25 Hz, to match 0.25x playback (keeps 100 Hz time surfaces in bag time)
  Bag playback: rosbag play -r 0.25 --clock (ESVO default upenn launcher uses -r 0.5)
  Ground truth: /davis/left/pose (motion capture), 2112 poses (flying1), 2119 poses (flying3)

Procedure fix
  ESVO only saves on ESVO_SYSTEM_STATUS=TERMINATE, but its tracking loop sleeps on sim time, which
  stops when the bag ends. clock_keeper.py continues /clock from the bag end time so the save happens.

Pilot at ESVO default rate (0.5x, 50 Hz sync), flying1, kept in runs/pilot_0.5x/
  TS_left 43.7 Hz (target ~100 Hz): two time-surface nodes at ~96% of a core each, could not keep up
  Only 523 poses saved (~21 Hz) vs ~2100-2400 (~90 Hz) in the 0.25x runs: tracker updated far less often
  14 "resetRegProblem RESET fails for no enough events" warnings (main 0.25x runs: 205-370, non-fatal)
  ATE (SE3) 0.882 m, RPE 69.5%, coverage 98.2%, Sim(3) scale 0.747
  -> laptop cannot run ESVO at the authors' default rate; main runs use 0.25x (requirement R6: non-real-time, recorded)

Runs (0.25x): see runs/run_log.txt, esvo_results.csv, esvo_summary.csv

Results (0.25x, 3 runs per sequence)
flying1_run1 | rate 0.25x, sync 25 Hz | wall 105.7 s (start 1793611014.750538524, end 1793611120.466170095) | TS_left 99.314 Hz | poses 2171 | Samples: 1053  Mean CPU (% of one core): 366.3  Peak memory: 1625 MB  Logged for 112.7 s
flying1_run2 | rate 0.25x, sync 25 Hz | wall 105.5 s (start 1793611157.418949215, end 1793611262.950595602) | TS_left 99.950 Hz | poses 2358 | Samples: 1065  Mean CPU (% of one core): 330.7  Peak memory: 1625 MB  Logged for 112.6 s
flying1_run3 | rate 0.25x, sync 25 Hz | wall 105.5 s (start 1793611285.064269014, end 1793611390.611334645) | TS_left 100.019 Hz | poses 2363 | Samples: 1067  Mean CPU (% of one core): 307.5  Peak memory: 1623 MB  Logged for 112.3 s
flying3_run1 | rate 0.25x, sync 25 Hz | wall 102.1 s (start 1793611412.219403052, end 1793611514.297565090) | TS_left 99.916 Hz | poses 2325 | Samples: 1039  Mean CPU (% of one core): 279.1  Peak memory: 1620 MB  Logged for 108.6 s
flying3_run2 | rate 0.25x, sync 25 Hz | wall 101.6 s (start 1793611535.777666736, end 1793611637.403167764) | TS_left 99.952 Hz | poses 2341 | Samples: 1023  Mean CPU (% of one core): 287.6  Peak memory: 1617 MB  Logged for 107.4 s
flying3_run3 | rate 0.25x, sync 25 Hz | wall 101.4 s (start 1793611658.028417128, end 1793611759.459841974) | TS_left 99.992 Hz | poses 1797 | Samples: 1037  Mean CPU (% of one core): 304.7  Peak memory: 1620 MB  Logged for 110.2 s
  No run lost tracking or crashed; all six saved trajectories with 98-100% coverage. The 'RESET fails for no enough events' warnings (205-370 per run) are non-fatal, ESVO continues.
```

### Run log (one line per run)

```
flying1_run1 | rate 0.25x, sync 25 Hz | wall 105.7 s (start 1793611014.750538524, end 1793611120.466170095) | TS_left 99.314 Hz | poses 2171 | Samples: 1053  Mean CPU (% of one core): 366.3  Peak memory: 1625 MB  Logged for 112.7 s
flying1_run2 | rate 0.25x, sync 25 Hz | wall 105.5 s (start 1793611157.418949215, end 1793611262.950595602) | TS_left 99.950 Hz | poses 2358 | Samples: 1065  Mean CPU (% of one core): 330.7  Peak memory: 1625 MB  Logged for 112.6 s
flying1_run3 | rate 0.25x, sync 25 Hz | wall 105.5 s (start 1793611285.064269014, end 1793611390.611334645) | TS_left 100.019 Hz | poses 2363 | Samples: 1067  Mean CPU (% of one core): 307.5  Peak memory: 1623 MB  Logged for 112.3 s
flying3_run1 | rate 0.25x, sync 25 Hz | wall 102.1 s (start 1793611412.219403052, end 1793611514.297565090) | TS_left 99.916 Hz | poses 2325 | Samples: 1039  Mean CPU (% of one core): 279.1  Peak memory: 1620 MB  Logged for 108.6 s
flying3_run2 | rate 0.25x, sync 25 Hz | wall 101.6 s (start 1793611535.777666736, end 1793611637.403167764) | TS_left 99.952 Hz | poses 2341 | Samples: 1023  Mean CPU (% of one core): 287.6  Peak memory: 1617 MB  Logged for 107.4 s
flying3_run3 | rate 0.25x, sync 25 Hz | wall 101.4 s (start 1793611658.028417128, end 1793611759.459841974) | TS_left 99.992 Hz | poses 1797 | Samples: 1037  Mean CPU (% of one core): 304.7  Peak memory: 1620 MB  Logged for 110.2 s
```

### Efficiency per run (10 Hz profiles; CPU summed over the algorithm's processes, % of one core)

| run | samples | duration s | mean CPU % | median CPU % | p95 CPU % | max CPU % | mean RSS MB | peak RSS MB |
|---|---|---|---|---|---|---|---|---|
| flying1_run1 | 1053 | 112.7 | 366.3 | 373.6 | 601.1 | 721.0 | 1428 | 1625 |
| flying1_run2 | 1065 | 112.6 | 330.7 | 329.0 | 565.1 | 715.4 | 1433 | 1625 |
| flying1_run3 | 1067 | 112.3 | 307.5 | 300.2 | 547.0 | 690.8 | 1429 | 1623 |
| flying3_run1 | 1039 | 108.6 | 279.1 | 271.6 | 511.4 | 690.0 | 1403 | 1620 |
| flying3_run2 | 1023 | 107.4 | 287.6 | 281.2 | 510.2 | 708.7 | 1415 | 1617 |
| flying3_run3 | 1037 | 110.2 | 304.7 | 273.1 | 589.1 | 719.2 | 1419 | 1620 |

### Error statistics per run (after SE3 alignment)

| run | estimate span s | GT path length m | est poses | est rate Hz | mean err m | median err m | p95 err m | max err m | final err m |
|---|---|---|---|---|---|---|---|---|---|
| flying1_run1 | 25.8 | 11.66 | 2171 | 84 | 0.190 | 0.183 | 0.382 | 0.516 | 0.494 |
| flying1_run2 | 25.8 | 11.69 | 2358 | 91 | 0.184 | 0.179 | 0.315 | 0.406 | 0.332 |
| flying1_run3 | 25.7 | 11.64 | 2363 | 92 | 0.241 | 0.210 | 0.582 | 1.126 | 0.707 |
| flying3_run1 | 24.5 | 10.41 | 2325 | 95 | 0.345 | 0.329 | 0.482 | 0.843 | 0.429 |
| flying3_run2 | 24.8 | 10.57 | 2341 | 94 | 0.314 | 0.305 | 0.451 | 0.636 | 0.323 |
| flying3_run3 | 24.8 | 10.54 | 1797 | 73 | 0.362 | 0.347 | 0.672 | 0.815 | 0.691 |
| flying1_run1 (pilot_0.5x) | 25.4 | 11.45 | 523 | 21 | 0.672 | 0.382 | 2.035 | 2.493 | 1.980 |

### Position error over time (m, every 2 s from the start of ground truth)

| t_s | flying1_run1 | flying1_run2 | flying1_run3 | flying3_run1 | flying3_run2 | flying3_run3 | flying1_run1 (pilot_0.5x) |
|---|---|---|---|---|---|---|---|
| 2 | 0.279 | 0.241 | 0.368 | 0.279 | 0.241 | 0.311 | 1.906 |
| 4 | 0.126 | 0.127 | 0.166 | 0.362 | 0.384 | 0.403 | 0.516 |
| 6 | 0.183 | 0.216 | 0.240 | 0.444 | 0.401 | 0.394 | 0.408 |
| 8 | 0.209 | 0.238 | 0.227 | 0.494 | 0.279 | 0.271 | 0.373 |
| 10 | 0.255 | 0.242 | 0.269 | 0.338 | 0.362 | 0.470 | 0.382 |
| 12 | 0.134 | 0.127 | 0.125 | 0.251 | 0.246 | 0.279 | 0.290 |
| 14 | 0.088 | 0.091 | 0.115 | 0.287 | 0.168 | 0.275 | 0.257 |
| 16 | 0.100 | 0.121 | 0.105 | 0.381 | 0.377 | 0.664 | 0.181 |
| 18 | 0.190 | 0.170 | 0.203 | 0.302 | 0.458 | 0.779 | 0.638 |
| 20 | 0.230 | 0.155 | 0.280 | 0.259 | 0.310 | 0.416 | 0.622 |
| 22 | 0.175 | 0.147 | 0.206 | 0.269 | 0.290 | 0.284 | 0.861 |
| 24 | 0.208 | 0.227 | 0.249 | 0.310 | 0.275 | 0.429 | 1.323 |

### Trajectories of the main runs, downsampled to 1 Hz (metres, estimate after alignment)

**flying1_run1**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.0 | -0.247 | -1.234 | 0.528 | -0.116 | -1.212 | 0.902 |
| 2.0 | -0.140 | -1.524 | 0.986 | -0.040 | -1.500 | 1.238 |
| 3.0 | -0.055 | -1.889 | 1.371 | 0.031 | -1.879 | 1.517 |
| 4.0 | -0.124 | -2.139 | 1.566 | -0.063 | -2.083 | 1.647 |
| 5.0 | -0.361 | -2.337 | 1.822 | -0.266 | -2.296 | 1.870 |
| 6.0 | -0.721 | -2.687 | 2.407 | -0.624 | -2.564 | 2.323 |
| 7.0 | -0.914 | -3.168 | 3.102 | -0.810 | -3.054 | 2.972 |
| 8.0 | -0.770 | -3.428 | 3.511 | -0.685 | -3.378 | 3.329 |
| 9.0 | -0.546 | -3.461 | 3.625 | -0.478 | -3.466 | 3.375 |
| 10.0 | -0.412 | -3.407 | 3.509 | -0.408 | -3.398 | 3.252 |
| 11.0 | -0.385 | -3.209 | 3.240 | -0.377 | -3.173 | 3.056 |
| 12.0 | -0.387 | -2.867 | 2.817 | -0.375 | -2.797 | 2.699 |
| 13.0 | -0.566 | -2.620 | 2.478 | -0.554 | -2.536 | 2.472 |
| 14.0 | -0.701 | -2.543 | 2.297 | -0.681 | -2.468 | 2.327 |
| 15.0 | -0.556 | -2.603 | 2.210 | -0.587 | -2.520 | 2.217 |
| 16.0 | -0.285 | -2.567 | 2.153 | -0.359 | -2.499 | 2.106 |
| 17.0 | -0.067 | -2.326 | 1.913 | -0.185 | -2.297 | 1.888 |
| 18.0 | 0.122 | -2.157 | 1.538 | -0.073 | -2.159 | 1.516 |
| 19.0 | 0.360 | -2.161 | 1.138 | 0.118 | -2.162 | 1.179 |
| 20.0 | 0.529 | -2.006 | 0.966 | 0.295 | -2.058 | 0.917 |
| 21.0 | 0.527 | -1.821 | 0.860 | 0.330 | -1.907 | 0.818 |
| 22.0 | 0.146 | -1.563 | 0.713 | 0.037 | -1.697 | 0.681 |
| 23.0 | -0.339 | -1.226 | 0.426 | -0.314 | -1.413 | 0.430 |
| 24.0 | -0.837 | -0.949 | 0.096 | -0.775 | -1.132 | 0.172 |
| 25.0 | -1.262 | -0.719 | -0.312 | -1.190 | -0.895 | -0.311 |

**flying1_run2**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.0 | -0.247 | -1.234 | 0.528 | -0.114 | -1.368 | 0.788 |
| 2.0 | -0.140 | -1.524 | 0.986 | -0.017 | -1.631 | 1.161 |
| 3.0 | -0.055 | -1.889 | 1.371 | 0.055 | -1.960 | 1.453 |
| 4.0 | -0.124 | -2.139 | 1.566 | -0.002 | -2.171 | 1.585 |
| 5.0 | -0.361 | -2.337 | 1.822 | -0.236 | -2.357 | 1.822 |
| 6.0 | -0.718 | -2.683 | 2.400 | -0.597 | -2.512 | 2.353 |
| 7.0 | -0.914 | -3.168 | 3.102 | -0.810 | -3.036 | 2.963 |
| 8.0 | -0.770 | -3.428 | 3.511 | -0.696 | -3.336 | 3.307 |
| 9.0 | -0.549 | -3.461 | 3.625 | -0.515 | -3.439 | 3.401 |
| 10.0 | -0.412 | -3.407 | 3.509 | -0.410 | -3.364 | 3.271 |
| 11.0 | -0.385 | -3.209 | 3.240 | -0.382 | -3.135 | 3.051 |
| 12.0 | -0.387 | -2.867 | 2.817 | -0.383 | -2.779 | 2.731 |
| 13.0 | -0.568 | -2.618 | 2.475 | -0.544 | -2.523 | 2.466 |
| 14.0 | -0.701 | -2.543 | 2.297 | -0.684 | -2.464 | 2.334 |
| 15.0 | -0.556 | -2.603 | 2.210 | -0.589 | -2.517 | 2.209 |
| 16.0 | -0.285 | -2.567 | 2.153 | -0.370 | -2.481 | 2.161 |
| 17.0 | -0.067 | -2.326 | 1.913 | -0.196 | -2.281 | 1.910 |
| 18.0 | 0.120 | -2.157 | 1.542 | -0.052 | -2.163 | 1.540 |
| 19.0 | 0.358 | -2.161 | 1.141 | 0.120 | -2.130 | 1.185 |
| 20.0 | 0.520 | -2.027 | 0.974 | 0.368 | -2.012 | 0.985 |
| 21.0 | 0.527 | -1.821 | 0.860 | 0.335 | -1.841 | 0.904 |
| 22.0 | 0.146 | -1.563 | 0.713 | 0.046 | -1.630 | 0.802 |
| 23.0 | -0.335 | -1.230 | 0.430 | -0.314 | -1.356 | 0.522 |
| 24.0 | -0.837 | -0.949 | 0.096 | -0.758 | -1.097 | 0.248 |
| 25.0 | -1.262 | -0.719 | -0.312 | -1.200 | -0.872 | -0.264 |

**flying1_run3**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.0 | -0.247 | -1.234 | 0.528 | 0.036 | -1.247 | 1.051 |
| 2.0 | -0.141 | -1.521 | 0.981 | 0.038 | -1.513 | 1.303 |
| 3.0 | -0.055 | -1.887 | 1.368 | 0.080 | -1.887 | 1.494 |
| 4.0 | -0.124 | -2.139 | 1.566 | 0.009 | -2.056 | 1.619 |
| 5.0 | -0.361 | -2.337 | 1.822 | -0.226 | -2.233 | 1.849 |
| 6.0 | -0.718 | -2.683 | 2.400 | -0.586 | -2.484 | 2.412 |
| 7.0 | -0.914 | -3.168 | 3.102 | -0.806 | -3.000 | 3.008 |
| 8.0 | -0.770 | -3.428 | 3.511 | -0.692 | -3.372 | 3.305 |
| 9.0 | -0.549 | -3.461 | 3.625 | -0.494 | -3.472 | 3.337 |
| 10.0 | -0.412 | -3.407 | 3.509 | -0.417 | -3.413 | 3.240 |
| 11.0 | -0.385 | -3.217 | 3.247 | -0.360 | -3.191 | 3.023 |
| 12.0 | -0.388 | -2.863 | 2.813 | -0.365 | -2.804 | 2.696 |
| 13.0 | -0.564 | -2.622 | 2.480 | -0.533 | -2.548 | 2.487 |
| 14.0 | -0.701 | -2.542 | 2.298 | -0.674 | -2.441 | 2.346 |
| 15.0 | -0.551 | -2.604 | 2.209 | -0.598 | -2.505 | 2.239 |
| 16.0 | -0.285 | -2.567 | 2.153 | -0.370 | -2.508 | 2.141 |
| 17.0 | -0.067 | -2.326 | 1.913 | -0.223 | -2.325 | 1.892 |
| 18.0 | 0.127 | -2.156 | 1.525 | -0.084 | -2.186 | 1.515 |
| 19.0 | 0.365 | -2.160 | 1.132 | 0.044 | -2.207 | 1.133 |
| 20.0 | 0.529 | -2.006 | 0.966 | 0.246 | -2.085 | 0.903 |
| 21.0 | 0.527 | -1.821 | 0.860 | 0.276 | -1.921 | 0.838 |
| 22.0 | 0.146 | -1.563 | 0.713 | -0.017 | -1.674 | 0.736 |
| 23.0 | -0.339 | -1.226 | 0.426 | -0.373 | -1.364 | 0.516 |
| 24.0 | -0.841 | -0.946 | 0.092 | -0.801 | -1.028 | 0.334 |
| 25.0 | -1.262 | -0.719 | -0.312 | -1.145 | -0.932 | -0.223 |

**flying3_run1**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.0 | 0.169 | -1.300 | 0.639 | 0.411 | -1.580 | 0.851 |
| 2.0 | 0.317 | -1.518 | 0.882 | 0.378 | -1.783 | 0.945 |
| 3.0 | 0.454 | -1.775 | 1.215 | 0.558 | -2.149 | 1.352 |
| 4.0 | 0.557 | -1.967 | 1.440 | 0.624 | -2.306 | 1.545 |
| 5.0 | 0.421 | -2.180 | 1.859 | 0.524 | -2.567 | 1.889 |
| 6.0 | 0.187 | -2.428 | 2.257 | 0.304 | -2.852 | 2.197 |
| 7.0 | -0.205 | -2.645 | 2.564 | -0.087 | -3.083 | 2.513 |
| 8.0 | -0.657 | -2.736 | 2.755 | -0.505 | -3.204 | 2.705 |
| 9.0 | -1.033 | -2.775 | 2.709 | -0.820 | -3.194 | 2.691 |
| 10.0 | -1.057 | -2.725 | 2.720 | -0.719 | -2.701 | 2.713 |
| 11.0 | -0.802 | -2.750 | 2.750 | -0.721 | -2.483 | 2.730 |
| 12.0 | -0.465 | -2.709 | 2.683 | -0.444 | -2.459 | 2.654 |
| 13.0 | -0.101 | -2.652 | 2.487 | -0.151 | -2.414 | 2.491 |
| 14.0 | 0.360 | -2.549 | 2.204 | 0.209 | -2.305 | 2.201 |
| 15.0 | 0.784 | -2.327 | 1.848 | 0.556 | -2.074 | 1.838 |
| 16.0 | 1.019 | -2.244 | 1.442 | 0.735 | -1.979 | 1.474 |
| 17.0 | 0.913 | -2.038 | 1.260 | 0.633 | -1.818 | 1.304 |
| 18.0 | 0.562 | -2.079 | 1.231 | 0.370 | -1.849 | 1.274 |
| 19.0 | 0.462 | -2.198 | 1.459 | 0.315 | -2.040 | 1.450 |
| 20.0 | 0.475 | -2.396 | 2.013 | 0.343 | -2.181 | 1.929 |
| 21.0 | 0.118 | -2.604 | 2.324 | 0.032 | -2.377 | 2.221 |
| 22.0 | -0.303 | -2.677 | 2.386 | -0.394 | -2.428 | 2.327 |
| 23.0 | -0.764 | -2.688 | 2.486 | -0.811 | -2.435 | 2.480 |
| 24.0 | -1.191 | -2.819 | 2.394 | -1.191 | -2.501 | 2.386 |

**flying3_run2**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.0 | 0.167 | -1.297 | 0.637 | 0.134 | -1.136 | 0.698 |
| 2.0 | 0.317 | -1.518 | 0.882 | 0.210 | -1.303 | 0.882 |
| 3.0 | 0.455 | -1.777 | 1.217 | 0.387 | -1.488 | 1.290 |
| 4.0 | 0.557 | -1.967 | 1.440 | 0.515 | -1.592 | 1.504 |
| 5.0 | 0.428 | -2.171 | 1.846 | 0.405 | -1.802 | 1.910 |
| 6.0 | 0.181 | -2.432 | 2.265 | 0.161 | -2.029 | 2.256 |
| 7.0 | -0.205 | -2.645 | 2.564 | -0.239 | -2.278 | 2.547 |
| 8.0 | -0.657 | -2.736 | 2.755 | -0.651 | -2.465 | 2.695 |
| 9.0 | -1.033 | -2.775 | 2.709 | -0.904 | -2.515 | 2.613 |
| 10.0 | -1.057 | -2.725 | 2.720 | -0.748 | -2.603 | 2.577 |
| 11.0 | -0.811 | -2.749 | 2.750 | -0.570 | -2.647 | 2.637 |
| 12.0 | -0.465 | -2.709 | 2.683 | -0.253 | -2.609 | 2.609 |
| 13.0 | -0.105 | -2.653 | 2.489 | 0.078 | -2.560 | 2.506 |
| 14.0 | 0.365 | -2.547 | 2.200 | 0.506 | -2.491 | 2.267 |
| 15.0 | 0.784 | -2.327 | 1.848 | 0.608 | -2.569 | 1.934 |
| 16.0 | 1.019 | -2.244 | 1.442 | 0.805 | -2.521 | 1.582 |
| 17.0 | 0.917 | -2.039 | 1.261 | 0.761 | -2.440 | 1.360 |
| 18.0 | 0.560 | -2.081 | 1.232 | 0.492 | -2.537 | 1.307 |
| 19.0 | 0.462 | -2.198 | 1.459 | 0.417 | -2.627 | 1.537 |
| 20.0 | 0.475 | -2.396 | 2.013 | 0.386 | -2.690 | 2.038 |
| 21.0 | 0.118 | -2.604 | 2.324 | -0.001 | -2.871 | 2.317 |
| 22.0 | -0.303 | -2.677 | 2.386 | -0.405 | -2.958 | 2.343 |
| 23.0 | -0.764 | -2.688 | 2.486 | -0.833 | -2.970 | 2.437 |
| 24.0 | -1.184 | -2.815 | 2.396 | -1.152 | -3.085 | 2.330 |

**flying3_run3**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.0 | 0.167 | -1.297 | 0.637 | -0.068 | -1.334 | 0.655 |
| 2.0 | 0.317 | -1.518 | 0.882 | 0.030 | -1.422 | 0.970 |
| 3.0 | 0.455 | -1.777 | 1.217 | 0.272 | -1.644 | 1.493 |
| 4.0 | 0.557 | -1.968 | 1.444 | 0.412 | -1.706 | 1.710 |
| 5.0 | 0.421 | -2.180 | 1.859 | 0.333 | -1.883 | 2.112 |
| 6.0 | 0.184 | -2.430 | 2.261 | 0.160 | -2.108 | 2.485 |
| 7.0 | -0.205 | -2.645 | 2.564 | -0.190 | -2.382 | 2.816 |
| 8.0 | -0.657 | -2.736 | 2.755 | -0.572 | -2.606 | 2.988 |
| 9.0 | -1.033 | -2.775 | 2.709 | -0.808 | -2.734 | 2.936 |
| 10.0 | -1.055 | -2.726 | 2.721 | -0.900 | -2.715 | 2.310 |
| 11.0 | -0.802 | -2.750 | 2.750 | -0.688 | -2.677 | 2.387 |
| 12.0 | -0.465 | -2.709 | 2.683 | -0.384 | -2.711 | 2.417 |
| 13.0 | -0.101 | -2.652 | 2.487 | -0.056 | -2.758 | 2.349 |
| 14.0 | 0.365 | -2.547 | 2.200 | 0.377 | -2.825 | 2.172 |
| 15.0 | 0.788 | -2.324 | 1.844 | 0.824 | -2.781 | 1.906 |
| 16.1 | 1.029 | -2.235 | 1.419 | 1.057 | -2.898 | 1.548 |
| 17.0 | 0.909 | -2.037 | 1.260 | 1.055 | -2.817 | 1.300 |
| 18.1 | 0.537 | -2.095 | 1.243 | 0.766 | -2.832 | 1.274 |
| 19.0 | 0.465 | -2.204 | 1.476 | 0.624 | -2.836 | 1.476 |
| 20.1 | 0.452 | -2.409 | 2.050 | 0.522 | -2.790 | 1.945 |
| 21.1 | 0.096 | -2.615 | 2.332 | 0.095 | -2.832 | 2.145 |
| 22.0 | -0.303 | -2.677 | 2.386 | -0.311 | -2.795 | 2.123 |
| 23.0 | -0.768 | -2.688 | 2.486 | -0.742 | -2.690 | 2.130 |
| 24.0 | -1.187 | -2.817 | 2.395 | -1.048 | -2.740 | 1.963 |

### Log summaries

- flying1_run1_esvo.log: 767 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- flying1_run2_esvo.log: 923 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- flying1_run3_esvo.log: 927 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- flying3_run1_esvo.log: 823 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- flying3_run2_esvo.log: 807 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- flying3_run3_esvo.log: 597 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`

# EVO (Rebecq et al., 2017)

Primary alignment: SIM3 (requirement R4). All values below are original data from this project.

### Per sequence (summary.csv)
| sequence | alignment | runs | runs_ok | ate_mean_m | ate_sd_m | rpe_1s_mean_percent | coverage_mean_percent | sim3_scale_mean |
|---|---|---|---|---|---|---|---|---|
| boxes_6dof | sim3 | 3 | 3 | 0.3018 | 0.0513 | 93.7268 | 7.9000 | 0.1271 |
| shapes_6dof | sim3 | 3 | 3 | 0.1992 | 0.0112 | 83.5050 | 9.7333 | 0.1468 |

### Per run (results.csv)
| sequence | run | alignment | estimated_poses | associated_poses | coverage_percent | status | ate_se3_m | ate_sim3_m | sim3_scale | rpe_1s_rmse_m | rpe_1s_percent |
|---|---|---|---|---|---|---|---|---|---|---|---|
| boxes_6dof | 1 | sim3 | 296 | 296 | 6.5000 | ok | 0.4539 | 0.2508 | 0.2973 | 0.3948 | 86.0055 |
| boxes_6dof | 2 | sim3 | 326 | 326 | 6.8000 | ok | 1.7370 | 0.3012 | 0.0508 | 0.4488 | 97.4243 |
| boxes_6dof | 3 | sim3 | 596 | 596 | 10.4000 | ok | 2.4826 | 0.3534 | 0.0331 | 0.4858 | 97.7505 |
| shapes_6dof | 1 | sim3 | 178 | 178 | 14.0000 | ok | 1.4323 | 0.1907 | 0.0644 | 0.2793 | 90.1520 |
| shapes_6dof | 2 | sim3 | 66 | 66 | 6.9000 | ok | 0.4010 | 0.2119 | 0.2284 | 0.2843 | 81.3465 |
| shapes_6dof | 3 | sim3 | 86 | 86 | 8.3000 | ok | 0.7663 | 0.1948 | 0.1475 | 0.2861 | 79.0166 |

### Experiment record (notes, verbatim)

```
EVO (Rebecq et al., 2017) - experiment notes
=============================================
Hardware: same machine as ESVO and ESVIO (Intel Core i7-1255U, 10 cores / 12 threads, 15.7 GB RAM,
Windows 11, Docker Desktop 4.97 on WSL 2). Runs made with the default WSL 2 memory (~7.7 GB),
the same as ESVO.

Algorithm
  EVO of Rebecq, Horstschaefer, Gallego & Scaramuzza (2017), IEEE RA-L, doi:10.1109/LRA.2016.2645143
  Code: uzh-rpg/rpg_dvs_evo_open, commit 14c72916b40c2d5fbd7197b772198c3ca75f4cbe
  Container: osrf/ros:melodic-desktop (Ubuntu 18.04, ROS Melodic), as the README specifies

Data (RPG Event Camera Dataset, Mueggler et al., 2017; monocular DAVIS240C, 240 x 180)
  shapes_6dof.bag  322 MB, 59.7 s, ground truth /optitrack/davis 11,862 poses
  boxes_6dof.bag   1.6 GB, 59.8 s, ground truth /optitrack/davis 11,954 poses
  evo_flyingroom.bag 564 MB, 103 s, EVO's own sample bag (functional check, no ground truth)
  Source: https://rpg.ifi.uzh.ch/datasets/davis/ and http://rpg.ifi.uzh.ch/data/EVO/code_examples/

Build changes (none affect the algorithm)
  1. dependencies.yaml uses SSH git URLs; switched to HTTPS (no GitHub key in the container).
  2. zurich-eye/gflags_catkin clones a gflags branch ('master') that no longer exists; replaced
     gflags_catkin and glog_catkin with the ethz-asl versions (the ones ESVO uses). First build failed.
  3. dvs_tracking declares dvs_ros_driver and davis_ros_driver (live-camera drivers) in package.xml
     but never uses them in code; the two <depend> lines were removed. Second build failed on this.
     Live drivers marked CATKIN_IGNORE (need libcaer, not used for bag playback).
  4. A Docker build crashed when EVO and ESVIO were compiled at the same time (out of memory).
     Builds were then run one at a time with WSL memory raised to 11 GB + 8 GB swap for building
     only; the setting was removed again before any run.

Configuration
  rpg_headless.launch = EVO's live.launch (its template for the DAVIS-ijrr camera of the RPG dataset,
    calibration parameters/calib/DAVIS-ijrr.yaml) without svo_gui, rqt_evo, rviz, dvs_renderer and
    dvs_reconstruction (visualisation and image reconstruction only; tracking/mapping unchanged)
  flyingroom_headless.launch = flyingroom.launch with the same nodes removed
  auto_trigger:=true (pipeline starts itself; no GUI button presses)
  Trajectory: /evo/pose (geometry_msgs/PoseStamped). First recorded with rosbag record (left unclosed
    when runs ended); replaced by record_pose.py, which writes TUM directly (see below)
  Evaluation: Sim(3) alignment (monocular, requirement R4)

Configuration actually used for the main runs (decided by pilots, below)
  flyingroom_headless.launch with camera_name:=DAVIS-ijrr (RPG dataset calibration) and
  bootstrap_image_topic:=/dvs/image_raw (SVO bootstrap from the DAVIS frames, which the EVO README calls
  the most reliable method). flyingroom.launch is the authors' configuration for bag playback; its
  tracker guards are min_map_size 200, min_n_keypoints 2000.
  Playback 0.5x (EVO README suggests slowing on weaker hardware; Chen et al. used 0.2 or 0.5x).
  Pose recording: record_pose.py writes /evo/pose to TUM, flushing each line (kept even if EVO crashes).

Pilots and functional check (kept in runs/pilots/)
  evo_flyingroom (EVO's own sample bag), flyingroom config, event-frame bootstrap (default), 0.7x:
    SVO "SparseImgAlign: no features to track", 0 poses; dvs_tracking died (exit -8, SIGFPE).
  evo_flyingroom, flyingroom config, frame bootstrap, 0.7x: WORKED. 3,112 poses over the 99 s bag,
    no crash, mean CPU 727% of one core, peak memory 832 MB. -> EVO itself functions in this container.
  shapes_6dof, live.launch (DAVIS-ijrr template, guards 0/0), frame bootstrap: dvs_tracking died (SIGFPE).
  shapes_6dof, live.launch with guards 200/2000, frame bootstrap, 0.5x: 31 poses, dvs_tracking died (SIGFPE).
  shapes_6dof and boxes_6dof, flyingroom config + DAVIS-ijrr, frame bootstrap, 0.5x: 96 and 366 poses,
    dvs_tracking died (SIGFPE) in both.

Main runs (0.5x, 3 per sequence): dvs_tracking crashed (SIGFPE, exit -8) in every one of the 6 runs.
  Coverage 6.5-14.0%; Sim(3) scale 0.03-0.30 and RPE 79-98% show the short tracked segments did not
  follow the true motion, so the Sim(3) ATE of the partial runs (0.19-0.35 m) is not meaningful.
  All six recorded as failures (R5). See runs/run_log.txt, results.csv.
shapes_6dof_run1 | rate 0.5x | bootstrap frames | wall 120.7 s | poses 178 | node crashes during run 1 | Samples: 1218  Mean CPU (% of one core): 375.3  Peak memory: 749 MB  Logged for 126.5 s
shapes_6dof_run2 | rate 0.5x | bootstrap frames | wall 120.5 s | poses 66 | node crashes during run 1 | Samples: 1234  Mean CPU (% of one core): 294.6  Peak memory: 710 MB  Logged for 126.3 s
shapes_6dof_run3 | rate 0.5x | bootstrap frames | wall 120.6 s | poses 86 | node crashes during run 1 | Samples: 1224  Mean CPU (% of one core): 264.9  Peak memory: 715 MB  Logged for 126.4 s
boxes_6dof_run1 | rate 0.5x | bootstrap frames | wall 122.5 s | poses 296 | node crashes during run 1 | Samples: 1229  Mean CPU (% of one core): 497.3  Peak memory: 831 MB  Logged for 128.2 s
boxes_6dof_run2 | rate 0.5x | bootstrap frames | wall 120.7 s | poses 326 | node crashes during run 1 | Samples: 1229  Mean CPU (% of one core): 475.6  Peak memory: 810 MB  Logged for 126.5 s
boxes_6dof_run3 | rate 0.5x | bootstrap frames | wall 120.9 s | poses 596 | node crashes during run 1 | Samples: 1225  Mean CPU (% of one core): 566.1  Peak memory: 830 MB  Logged for 126.7 s
```

### Run log (one line per run)

```
shapes_6dof_run1 | rate 0.5x | bootstrap frames | wall 120.7 s (start 1793628149.410922328, end 1793628270.138907010) | poses 178 | node crashes during run 1 | Samples: 1218  Mean CPU (% of one core): 375.3  Peak memory: 749 MB  Logged for 126.5 s
shapes_6dof_run2 | rate 0.5x | bootstrap frames | wall 120.5 s (start 1793628292.942919493, end 1793628413.444938411) | poses 66 | node crashes during run 1 | Samples: 1234  Mean CPU (% of one core): 294.6  Peak memory: 710 MB  Logged for 126.3 s
shapes_6dof_run3 | rate 0.5x | bootstrap frames | wall 120.6 s (start 1793628436.305376971, end 1793628556.890895321) | poses 86 | node crashes during run 1 | Samples: 1224  Mean CPU (% of one core): 264.9  Peak memory: 715 MB  Logged for 126.4 s
boxes_6dof_run1 | rate 0.5x | bootstrap frames | wall 122.5 s (start 1793628580.339358732, end 1793628702.849814806) | poses 296 | node crashes during run 1 | Samples: 1229  Mean CPU (% of one core): 497.3  Peak memory: 831 MB  Logged for 128.2 s
boxes_6dof_run2 | rate 0.5x | bootstrap frames | wall 120.7 s (start 1793628725.648177997, end 1793628846.310013644) | poses 326 | node crashes during run 1 | Samples: 1229  Mean CPU (% of one core): 475.6  Peak memory: 810 MB  Logged for 126.5 s
boxes_6dof_run3 | rate 0.5x | bootstrap frames | wall 120.9 s (start 1793628869.109354658, end 1793628989.964275578) | poses 596 | node crashes during run 1 | Samples: 1225  Mean CPU (% of one core): 566.1  Peak memory: 830 MB  Logged for 126.7 s
```

### Efficiency per run (10 Hz profiles; CPU summed over the algorithm's processes, % of one core)

| run | samples | duration s | mean CPU % | median CPU % | p95 CPU % | max CPU % | mean RSS MB | peak RSS MB |
|---|---|---|---|---|---|---|---|---|
| boxes_6dof_run1 | 1229 | 128.2 | 497.3 | 311.2 | 1148.6 | 1193.2 | 107 | 831 |
| boxes_6dof_run2 | 1229 | 126.5 | 475.6 | 223.6 | 1162.9 | 1191.7 | 96 | 810 |
| boxes_6dof_run3 | 1225 | 126.7 | 566.1 | 546.2 | 1167.0 | 1202.7 | 131 | 830 |
| evo_flyingroom_run0 | 1516 | 158.2 | 231.3 | 169.9 | 592.5 | 1168.7 | 88 | 707 |
| shapes_6dof_run1 | 1218 | 126.5 | 375.3 | 97.9 | 1153.7 | 1200.5 | 204 | 749 |
| shapes_6dof_run2 | 1234 | 126.3 | 294.6 | 75.1 | 1160.4 | 1203.6 | 154 | 710 |
| shapes_6dof_run3 | 1224 | 126.4 | 264.9 | 67.6 | 1150.5 | 1214.3 | 163 | 715 |

### Error statistics per run (after SIM3 alignment)

| run | estimate span s | GT path length m | est poses | est rate Hz | mean err m | median err m | p95 err m | max err m | final err m |
|---|---|---|---|---|---|---|---|---|---|
| boxes_6dof_run1 | 3.7 | 1.81 | 296 | 81 | 0.239 | 0.234 | 0.358 | 0.500 | 0.479 |
| boxes_6dof_run2 | 3.8 | 1.91 | 326 | 85 | 0.287 | 0.268 | 0.435 | 0.472 | 0.195 |
| boxes_6dof_run3 | 6.0 | 3.19 | 596 | 99 | 0.337 | 0.350 | 0.510 | 0.555 | 0.137 |
| shapes_6dof_run1 | 8.1 | 3.62 | 178 | 22 | 0.174 | 0.157 | 0.324 | 0.430 | 0.039 |
| shapes_6dof_run2 | 3.9 | 1.63 | 66 | 17 | 0.190 | 0.167 | 0.376 | 0.397 | 0.127 |
| shapes_6dof_run3 | 4.7 | 2.00 | 86 | 18 | 0.172 | 0.153 | 0.379 | 0.417 | 0.049 |

### Position error over time (m, every 2 s from the start of ground truth)

| t_s | boxes_6dof_run1 | boxes_6dof_run2 | boxes_6dof_run3 | shapes_6dof_run1 | shapes_6dof_run2 | shapes_6dof_run3 |
|---|---|---|---|---|---|---|
| 4 | 0.319 | 0.420 | 0.499 |  |  |  |
| 6 | 0.277 | 0.376 | 0.395 |  |  |  |
| 8 |  |  | 0.402 |  |  |  |
| 10 |  |  |  | 0.142 | 0.154 | 0.133 |
| 12 |  |  |  | 0.149 | 0.145 | 0.135 |
| 14 |  |  |  | 0.178 |  |  |
| 16 |  |  |  | 0.223 |  |  |

### Trajectories of the main runs, downsampled to 1 Hz (metres, estimate after alignment)

**boxes_6dof_run1**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 3.0 | 0.068 | 1.357 | 1.251 | 0.155 | 1.323 | 1.402 |
| 4.0 | 0.501 | 1.375 | 1.556 | 0.222 | 1.294 | 1.426 |
| 5.0 | 0.198 | 1.225 | 1.558 | 0.175 | 1.298 | 1.441 |
| 6.0 | -0.237 | 1.127 | 1.382 | -0.017 | 1.273 | 1.458 |

**boxes_6dof_run2**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 3.0 | 0.068 | 1.357 | 1.251 | 0.111 | 1.278 | 1.402 |
| 4.0 | 0.503 | 1.375 | 1.558 | 0.118 | 1.288 | 1.404 |
| 5.0 | 0.204 | 1.227 | 1.559 | 0.113 | 1.283 | 1.408 |
| 6.0 | -0.237 | 1.127 | 1.379 | 0.109 | 1.274 | 1.411 |

**boxes_6dof_run3**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 3.0 | 0.068 | 1.357 | 1.251 | 0.115 | 1.246 | 1.260 |
| 4.0 | 0.501 | 1.375 | 1.556 | 0.115 | 1.252 | 1.264 |
| 5.0 | 0.198 | 1.225 | 1.558 | 0.116 | 1.251 | 1.259 |
| 6.0 | -0.237 | 1.127 | 1.382 | 0.117 | 1.247 | 1.253 |
| 7.0 | -0.119 | 1.263 | 0.999 | 0.113 | 1.243 | 1.256 |
| 8.0 | 0.493 | 1.161 | 1.135 | 0.116 | 1.246 | 1.254 |

**shapes_6dof_run1**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 9.1 | 4.171 | 1.768 | 1.327 | 4.358 | 1.425 | 1.345 |
| 10.0 | 4.298 | 1.445 | 1.233 | 4.354 | 1.434 | 1.352 |
| 11.0 | 4.434 | 1.275 | 1.600 | 4.346 | 1.424 | 1.364 |
| 12.0 | 4.370 | 1.331 | 1.241 | 4.360 | 1.439 | 1.356 |
| 13.0 | 4.345 | 1.691 | 1.389 | 4.330 | 1.616 | 1.373 |
| 14.0 | 4.270 | 1.764 | 1.273 | 4.330 | 1.616 | 1.373 |
| 15.0 | 4.324 | 1.634 | 1.540 | 4.330 | 1.616 | 1.373 |
| 16.0 | 4.338 | 1.466 | 1.229 | 4.330 | 1.616 | 1.373 |

**shapes_6dof_run2**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 9.0 | 4.169 | 1.772 | 1.341 | 4.327 | 1.443 | 1.356 |
| 10.1 | 4.307 | 1.420 | 1.234 | 4.338 | 1.398 | 1.368 |
| 11.0 | 4.435 | 1.276 | 1.596 | 4.360 | 1.407 | 1.414 |
| 12.0 | 4.371 | 1.334 | 1.246 | 4.309 | 1.334 | 1.385 |

**shapes_6dof_run3**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 9.1 | 4.175 | 1.764 | 1.314 | 4.311 | 1.411 | 1.356 |
| 10.1 | 4.305 | 1.426 | 1.233 | 4.334 | 1.420 | 1.351 |
| 11.0 | 4.434 | 1.277 | 1.593 | 4.352 | 1.408 | 1.381 |
| 12.0 | 4.372 | 1.335 | 1.250 | 4.349 | 1.421 | 1.353 |
| 13.0 | 4.347 | 1.686 | 1.379 | 4.436 | 1.563 | 1.324 |

### Log summaries

- boxes_6dof_run1_evo.log: 468 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- boxes_6dof_run2_evo.log: 501 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- boxes_6dof_run3_evo.log: 555 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- evo_flyingroom_run0_evo.log: 330 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- shapes_6dof_run1_evo.log: 733 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- shapes_6dof_run2_evo.log: 525 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`
- shapes_6dof_run3_evo.log: 467 lines; last lines: `shutting down processing monitor... / ... shutting down processing monitor complete / [1mdone[0m`

# ESVIO (Chen et al., 2023)

Primary alignment: SE3 (requirement R4). All values below are original data from this project.

### Per sequence (summary.csv)
| sequence | alignment | runs | runs_ok | ate_mean_m | ate_sd_m | rpe_1s_mean_percent | coverage_mean_percent | sim3_scale_mean |
|---|---|---|---|---|---|---|---|---|
| flying1 | se3 | 3 | 3 | 0.1870 | 0.0051 | 14.8210 | 100.0000 | 1.0769 |
| flying3 | se3 | 3 | 3 | 0.2636 | 0.0338 | 23.6420 | 98.9667 | 1.0427 |

### Per run (results.csv)
| sequence | run | alignment | estimated_poses | associated_poses | coverage_percent | status | ate_se3_m | ate_sim3_m | sim3_scale | rpe_1s_rmse_m | rpe_1s_percent |
|---|---|---|---|---|---|---|---|---|---|---|---|
| flying1 | 1 | se3 | 980 | 378 | 100.0000 | ok | 0.1838 | 0.1565 | 1.0703 | 0.0746 | 14.7442 |
| flying1 | 2 | se3 | 980 | 378 | 100.0000 | ok | 0.1929 | 0.1647 | 1.0735 | 0.0741 | 14.8009 |
| flying1 | 3 | se3 | 980 | 378 | 100.0000 | ok | 0.1844 | 0.1422 | 1.0869 | 0.0767 | 14.9180 |
| flying3 | 1 | se3 | 1289 | 370 | 100.0000 | ok | 0.2754 | 0.2701 | 1.0564 | 0.1092 | 23.2726 |
| flying3 | 2 | se3 | 492 | 339 | 96.9000 | ok | 0.2255 | 0.2251 | 1.0138 | 0.1215 | 23.5472 |
| flying3 | 3 | se3 | 635 | 370 | 100.0000 | ok | 0.2900 | 0.2848 | 1.0579 | 0.1131 | 24.1062 |

### Experiment record (notes, verbatim)

```
ESVIO (Chen et al., 2023) - experiment notes
=============================================
Hardware: same machine as ESVO and EVO (Intel Core i7-1255U, 10 cores / 12 threads, 15.7 GB RAM,
Windows 11, Docker Desktop 4.97 on WSL 2). Runs made with the default WSL 2 memory (~7.7 GB),
the same as ESVO.

Algorithm
  ESVIO of Chen, Guan & Lu (2023), IEEE RA-L, doi:10.1109/LRA.2023.3269950 (arclab-hku/ESVIO)
  Not the ESVIO of Liu et al. (2023a, Sensors), which has no buildable public code.
  Commit: b9e5aee7db647b70cee6f1128e2f49f47107ca84
  Container: osrf/ros:noetic-desktop (Ubuntu 20.04, ROS Noetic), as the README specifies

Data: the same ESVO-edited MVSEC bags as ESVO (indoor_flying1_edited.bag, indoor_flying3_edited.bag),
  with stereo events, stereo frames and IMU (/davis/left/imu). Ground truth /davis/left/pose
  (same gt_flying1.txt / gt_flying3.txt files as ESVO).

Build changes (none affect the algorithm)
  1. Added libceres-dev (Ceres 1.14.0 on Ubuntu 20.04, the version the README requires). First build
     failed: camera_model could not find Ceres.
  2. Build camera_model before the other packages. Second build failed: esvio_estimator,
     feature_tracker and pose_graph use camera_model but do not declare it in package.xml, so
     catkin configured them first.
  3. Live-camera driver packages in dependences/rpg_dvs_ros marked CATKIN_IGNORE (need camera SDKs,
     not used for bag playback).
  4. A Docker build crashed when EVO and ESVIO were compiled at the same time (out of memory).
     Builds were then run one at a time with WSL memory raised to 11 GB + 8 GB swap for building
     only; the setting was removed again before any run.

Configuration (config/esvio_mvsec_flying/esvio.yaml and esvio_mvsec_flying.launch, shipped by the
authors for these sequences; everything else unchanged)
  output_path: /home/cpy/Datasets/output -> /tmp/esvio_result (container path)
  esvio_mvsec_flying_headless.launch = esvio_mvsec_flying.launch without rviz and without the
    gnome-terminal launch prefix on stereo_image_tracker (no display in the container)
  Trajectory evaluated: esvio_result_no_loop.csv (sliding-window odometry, no loop closure), converted
    to TUM by esvio_csv_to_tum.py (time ns -> s, quaternion reordered). Loop-closed output kept in
    runs/loop/ for reference. Odometry is used because EVO and ESVO have no loop closure.
  Estimated pose is the IMU/body frame; ground truth is the left camera. The extrinsic translation is
    ~1.8 cm, so after SE(3) alignment the lever-arm effect is at most a few millimetres.

Pilots and run conditions (all on indoor_flying1, kept in runs/)
  Edited bag, 1.0x (pilot_1.0x): ran in real time (27.3 s wall) at 4.6 cores, but the estimator diverged
    from the first second: ATE 268 m, Sim(3) scale 0.003, 370 poses.
  Edited bag, 0.5x (pilot_0.5x): ATE 0.305 m, coverage 91.9%, scale 1.104, 356 poses, 3.6 cores.
  Edited bags, 0.25x, 3 runs per sequence (edited_bags_0.25x/): flying1 ATE 0.20, 0.49, 2.10 m
    (coverage 95.3, 83.7, 83.7%; scale 1.02, 1.06, 0.34); flying3 diverged in all 3 runs
    (ATE 38.5, 63.4, 30.9 m; scale ~0.005). Logs show the initialisation estimating a negative or
    near-zero scale ("estimated scale: -0.0028"). Cause: the ESVO-edited bags start mid-flight
    (ground truth speed 0.5-0.6 m/s in the first 2 s), while VINS-style initialisation expects a start
    at rest or well-excited motion.
  Bag read check: Windows-mounted folder 10.9 MB/s uncached, container disk 134 MB/s; 1x rosbag play of
    the 26 s bag took 31-35 s from either, so playback was not I/O limited. All ESVIO and EVO runs play
    from the container disk.

Main runs: ORIGINAL MVSEC data bags (indoor_flying1_data.bag 1.28 GB, 70 s; indoor_flying3_data.bag
  1.85 GB, 94 s; https://visiondata.cis.upenn.edu/mvsec/indoor_flying/), which start ~10 s before the
  edited bags with the drone at rest. Same configuration, 0.25x (matched to ESVO), 3 runs per sequence.
  Scored over exactly the ESVO window (the edited bags' ground truth, gt_flying1/3.txt), SE(3).
  flying1: ATE 0.184, 0.193, 0.184 m; coverage 100% x3; RPE 14.7-14.9%; scale 1.07-1.09.
  flying3: ATE 0.275, 0.226, 0.290 m; coverage 100, 96.9, 100%; RPE 23.3-24.1%; scale 1.01-1.06.
  Beyond the window: flying1 all 3 runs output poses from 4.4 s to the end (70.2 s), 980 poses each.
  flying3 run 1 output to the end (1,289 poses); run 2 stopped producing poses at 44.4 s of 94 s
  (492 poses); run 3 output to 93.6 s but with gaps (635 poses). No node crashes or respawns.
flying1_run1 | rate 0.25x | wall 282.9 s | poses 980 | respawns 0 | Samples: 2691  Mean CPU (% of one core): 146.5  Peak memory: 759 MB  Logged for 287.8 s
flying1_run2 | rate 0.25x | wall 282.7 s | poses 980 | respawns 0 | Samples: 2711  Mean CPU (% of one core): 127.3  Peak memory: 761 MB  Logged for 287.5 s
flying1_run3 | rate 0.25x | wall 282.7 s | poses 980 | respawns 0 | Samples: 2696  Mean CPU (% of one core): 132.0  Peak memory: 764 MB  Logged for 287.5 s
flying3_run1 | rate 0.25x | wall 379.1 s | poses 1289 | respawns 0 | Samples: 3557  Mean CPU (% of one core): 147.9  Peak memory: 870 MB  Logged for 384.0 s
flying3_run2 | rate 0.25x | wall 401.2 s | poses 492 | respawns 0 | Samples: 998  Mean CPU (% of one core): 232.6  Peak memory: 900 MB  Logged for 406.0 s
flying3_run3 | rate 0.25x | wall 401.2 s | poses 635 | respawns 0 | Samples: 1491  Mean CPU (% of one core): 159.5  Peak memory: 852 MB  Logged for 406.1 s

Real-time check on the ORIGINAL bag (indoor_flying1, one run each, runs/pilot_orig_1.0x and _0.5x)
  1.0x: wall 72.7 s for the 70 s bag, 4.5 cores, 790 MB, 871 poses, ATE 0.184 m, coverage 100%, RPE 15.2%
  0.5x: wall 141.8 s, 2.7 cores, 766 MB, 980 poses, ATE 0.184 m, coverage 100%, RPE 14.4%
  -> ESVIO runs in real time on this laptop with the same accuracy as at 0.25x. The 1.0x divergence on
     the edited bag was caused by the mid-flight start, not by CPU starvation.
```

### Run log (one line per run)

```
flying1_run1 | rate 0.25x | wall 282.9 s (start 1793629411.422962202, end 1793629694.336502317) | poses 980 | respawns 0 | Samples: 2691  Mean CPU (% of one core): 146.5  Peak memory: 759 MB  Logged for 287.8 s
flying1_run2 | rate 0.25x | wall 282.7 s (start 1793629714.757857830, end 1793629997.478169636) | poses 980 | respawns 0 | Samples: 2711  Mean CPU (% of one core): 127.3  Peak memory: 761 MB  Logged for 287.5 s
flying1_run3 | rate 0.25x | wall 282.7 s (start 1793630017.471826761, end 1793630300.122992304) | poses 980 | respawns 0 | Samples: 2696  Mean CPU (% of one core): 132.0  Peak memory: 764 MB  Logged for 287.5 s
flying3_run1 | rate 0.25x | wall 379.1 s (start 1793630320.182944858, end 1793630699.295554079) | poses 1289 | respawns 0 | Samples: 3557  Mean CPU (% of one core): 147.9  Peak memory: 870 MB  Logged for 384.0 s
flying3_run2 | rate 0.25x | wall 401.2 s (start 1793630720.657268060, end 1793631121.878268874) | poses 492 | respawns 0 | Samples: 998  Mean CPU (% of one core): 232.6  Peak memory: 900 MB  Logged for 406.0 s
flying3_run3 | rate 0.25x | wall 401.2 s (start 1793631141.919809866, end 1793631543.154995899) | poses 635 | respawns 0 | Samples: 1491  Mean CPU (% of one core): 159.5  Peak memory: 852 MB  Logged for 406.1 s
```

### Efficiency per run (10 Hz profiles; CPU summed over the algorithm's processes, % of one core)

| run | samples | duration s | mean CPU % | median CPU % | p95 CPU % | max CPU % | mean RSS MB | peak RSS MB |
|---|---|---|---|---|---|---|---|---|
| flying1_run1 | 2691 | 287.8 | 146.5 | 143.9 | 240.9 | 423.1 | 687 | 759 |
| flying1_run2 | 2711 | 287.5 | 127.3 | 124.8 | 213.8 | 471.0 | 687 | 761 |
| flying1_run3 | 2696 | 287.5 | 132.0 | 131.1 | 219.9 | 442.9 | 690 | 764 |
| flying3_run1 | 3557 | 384.0 | 147.9 | 140.7 | 268.4 | 809.5 | 740 | 870 |
| flying3_run2 | 998 | 406.0 | 232.6 | 164.1 | 669.1 | 866.0 | 661 | 900 |
| flying3_run3 | 1491 | 406.1 | 159.5 | 134.4 | 323.5 | 967.6 | 665 | 852 |

### Error statistics per run (after SE3 alignment)

| run | estimate span s | GT path length m | est poses | est rate Hz | mean err m | median err m | p95 err m | max err m | final err m |
|---|---|---|---|---|---|---|---|---|---|
| flying1_run1 | 65.8 | 11.71 | 980 | 15 | 0.167 | 0.180 | 0.272 | 0.381 | 0.164 |
| flying1_run2 | 65.8 | 11.71 | 980 | 15 | 0.174 | 0.186 | 0.287 | 0.401 | 0.167 |
| flying1_run3 | 65.8 | 11.71 | 980 | 15 | 0.170 | 0.188 | 0.263 | 0.364 | 0.204 |
| flying3_run1 | 86.6 | 10.60 | 1289 | 15 | 0.244 | 0.212 | 0.551 | 0.604 | 0.604 |
| flying3_run2 | 37.0 | 10.59 | 492 | 13 | 0.190 | 0.157 | 0.469 | 0.575 | 0.575 |
| flying3_run3 | 86.2 | 10.60 | 635 | 7 | 0.254 | 0.222 | 0.610 | 0.663 | 0.663 |
| flying1_run1 (edited_bags_0.25x) | 24.7 | 11.06 | 368 | 15 | 0.159 | 0.118 | 0.356 | 0.809 | 0.365 |
| flying1_run2 (edited_bags_0.25x) | 21.8 | 9.73 | 325 | 15 | 0.407 | 0.346 | 1.049 | 1.195 | 0.558 |
| flying1_run3 (edited_bags_0.25x) | 21.9 | 9.75 | 326 | 15 | 1.724 | 1.678 | 3.572 | 7.543 | 7.543 |
| flying3_run1 (edited_bags_0.25x) | 16.7 | 6.82 | 249 | 15 | 31.423 | 29.532 | 81.551 | 102.827 | 102.827 |
| flying3_run2 (edited_bags_0.25x) | 23.6 | 10.03 | 352 | 15 | 58.493 | 58.209 | 112.401 | 120.580 | 120.580 |
| flying3_run3 (edited_bags_0.25x) | 22.7 | 9.64 | 339 | 15 | 26.612 | 24.599 | 64.872 | 78.727 | 78.727 |
| flying1_run1 (pilot_0.5x) | 23.9 | 10.60 | 356 | 15 | 0.260 | 0.217 | 0.569 | 1.008 | 0.465 |
| flying1_run1 (pilot_1.0x) | 24.8 | 11.18 | 370 | 15 | 257.463 | 265.902 | 363.147 | 365.183 | 343.375 |
| flying1_run1 (pilot_orig_0.5x) | 65.8 | 11.71 | 980 | 15 | 0.168 | 0.156 | 0.298 | 0.322 | 0.319 |
| flying1_run1 (pilot_orig_1.0x) | 58.5 | 11.72 | 871 | 15 | 0.166 | 0.160 | 0.337 | 0.365 | 0.347 |

### Position error over time (m, every 2 s from the start of ground truth)

| t_s | flying1_run1 | flying1_run2 | flying1_run3 | flying3_run1 | flying3_run2 | flying3_run3 | flying1_run1 (edited_bags_0.25x) | flying1_run2 (edited_bags_0.25x) | flying1_run3 (edited_bags_0.25x) | flying3_run1 (edited_bags_0.25x) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.380 | 0.399 | 0.363 |  |  |  |  |  |  |  |
| 2 | 0.170 | 0.199 | 0.161 | 0.275 | 0.068 | 0.268 | 0.429 |  |  |  |
| 4 | 0.115 | 0.102 | 0.119 | 0.373 | 0.137 | 0.378 | 0.235 |  |  |  |
| 6 | 0.187 | 0.189 | 0.189 | 0.295 | 0.222 | 0.311 | 0.098 | 0.397 | 0.499 |  |
| 8 | 0.211 | 0.235 | 0.212 | 0.174 | 0.251 | 0.182 | 0.126 | 0.798 | 2.346 |  |
| 10 | 0.239 | 0.256 | 0.240 | 0.147 | 0.122 | 0.148 | 0.074 | 1.107 | 2.276 | 39.671 |
| 12 | 0.114 | 0.129 | 0.119 | 0.145 | 0.061 | 0.147 | 0.059 | 0.033 | 0.683 | 34.338 |
| 14 | 0.048 | 0.037 | 0.044 | 0.146 | 0.083 | 0.148 | 0.119 | 0.297 | 0.660 | 22.791 |
| 16 | 0.093 | 0.090 | 0.093 | 0.080 | 0.183 | 0.075 | 0.103 | 0.131 | 0.750 | 14.633 |
| 18 | 0.207 | 0.210 | 0.204 | 0.172 | 0.201 | 0.187 | 0.120 | 0.335 | 1.965 | 3.411 |
| 20 | 0.271 | 0.275 | 0.262 | 0.217 | 0.252 | 0.227 | 0.046 | 0.431 | 2.441 | 14.360 |
| 22 | 0.201 | 0.201 | 0.201 | 0.338 | 0.280 | 0.341 | 0.005 | 0.310 | 1.581 | 40.023 |
| 24 | 0.067 | 0.079 | 0.080 | 0.564 | 0.545 | 0.630 | 0.250 | 0.099 | 1.196 | 78.964 |

### Trajectories of the main runs, downsampled to 1 Hz (metres, estimate after alignment)

**flying1_run1**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 0.0 | -0.409 | -0.963 | 0.182 | -0.240 | -0.983 | 0.516 |
| 1.0 | -0.247 | -1.234 | 0.528 | -0.103 | -1.254 | 0.784 |
| 2.1 | -0.135 | -1.536 | 1.006 | -0.013 | -1.548 | 1.126 |
| 3.0 | -0.055 | -1.889 | 1.371 | 0.021 | -1.876 | 1.371 |
| 4.0 | -0.130 | -2.149 | 1.573 | -0.052 | -2.117 | 1.494 |
| 5.0 | -0.364 | -2.339 | 1.826 | -0.261 | -2.272 | 1.739 |
| 6.0 | -0.733 | -2.699 | 2.430 | -0.616 | -2.620 | 2.289 |
| 7.1 | -0.912 | -3.188 | 3.130 | -0.780 | -3.080 | 2.986 |
| 8.0 | -0.761 | -3.434 | 3.519 | -0.659 | -3.317 | 3.369 |
| 9.0 | -0.549 | -3.461 | 3.625 | -0.490 | -3.341 | 3.458 |
| 10.1 | -0.406 | -3.400 | 3.488 | -0.399 | -3.275 | 3.289 |
| 11.0 | -0.385 | -3.209 | 3.240 | -0.377 | -3.104 | 3.071 |
| 12.0 | -0.389 | -2.856 | 2.804 | -0.390 | -2.802 | 2.710 |
| 13.0 | -0.568 | -2.618 | 2.475 | -0.546 | -2.584 | 2.415 |
| 14.0 | -0.702 | -2.543 | 2.295 | -0.669 | -2.546 | 2.260 |
| 15.1 | -0.542 | -2.607 | 2.206 | -0.534 | -2.648 | 2.210 |
| 16.0 | -0.271 | -2.558 | 2.143 | -0.344 | -2.606 | 2.191 |
| 17.1 | -0.052 | -2.310 | 1.895 | -0.159 | -2.402 | 1.990 |
| 18.0 | 0.126 | -2.156 | 1.529 | -0.018 | -2.279 | 1.616 |
| 19.0 | 0.360 | -2.161 | 1.138 | 0.208 | -2.286 | 1.258 |
| 20.0 | 0.531 | -2.002 | 0.964 | 0.373 | -2.116 | 1.153 |
| 21.0 | 0.515 | -1.810 | 0.856 | 0.358 | -1.909 | 1.043 |
| 22.0 | 0.135 | -1.557 | 0.709 | -0.026 | -1.613 | 0.819 |
| 23.1 | -0.359 | -1.211 | 0.413 | -0.483 | -1.249 | 0.489 |
| 24.0 | -0.837 | -0.949 | 0.096 | -0.887 | -0.989 | 0.110 |
| 25.1 | -1.280 | -0.710 | -0.329 | -1.301 | -0.765 | -0.398 |

**flying1_run2**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 0.0 | -0.409 | -0.963 | 0.182 | -0.205 | -1.024 | 0.515 |
| 1.0 | -0.247 | -1.234 | 0.528 | -0.077 | -1.290 | 0.794 |
| 2.1 | -0.135 | -1.536 | 1.006 | -0.003 | -1.574 | 1.147 |
| 3.0 | -0.055 | -1.889 | 1.371 | 0.031 | -1.898 | 1.396 |
| 4.0 | -0.130 | -2.149 | 1.573 | -0.044 | -2.131 | 1.517 |
| 5.0 | -0.364 | -2.339 | 1.826 | -0.248 | -2.284 | 1.753 |
| 6.0 | -0.733 | -2.699 | 2.430 | -0.607 | -2.622 | 2.294 |
| 7.1 | -0.912 | -3.188 | 3.130 | -0.779 | -3.074 | 2.971 |
| 8.0 | -0.761 | -3.434 | 3.519 | -0.660 | -3.307 | 3.339 |
| 9.0 | -0.549 | -3.461 | 3.625 | -0.492 | -3.331 | 3.437 |
| 10.1 | -0.406 | -3.400 | 3.488 | -0.399 | -3.262 | 3.278 |
| 11.0 | -0.385 | -3.209 | 3.240 | -0.376 | -3.091 | 3.058 |
| 12.0 | -0.389 | -2.856 | 2.804 | -0.387 | -2.796 | 2.697 |
| 13.0 | -0.568 | -2.618 | 2.475 | -0.541 | -2.584 | 2.413 |
| 14.0 | -0.702 | -2.543 | 2.295 | -0.676 | -2.549 | 2.267 |
| 15.1 | -0.542 | -2.607 | 2.206 | -0.537 | -2.644 | 2.208 |
| 16.0 | -0.271 | -2.558 | 2.143 | -0.346 | -2.598 | 2.188 |
| 17.1 | -0.052 | -2.310 | 1.895 | -0.163 | -2.395 | 1.993 |
| 18.0 | 0.126 | -2.156 | 1.529 | -0.020 | -2.273 | 1.627 |
| 19.0 | 0.360 | -2.161 | 1.138 | 0.204 | -2.277 | 1.268 |
| 20.0 | 0.531 | -2.002 | 0.964 | 0.365 | -2.110 | 1.156 |
| 21.0 | 0.515 | -1.810 | 0.856 | 0.353 | -1.908 | 1.041 |
| 22.0 | 0.135 | -1.557 | 0.709 | -0.028 | -1.615 | 0.817 |
| 23.1 | -0.359 | -1.211 | 0.413 | -0.490 | -1.240 | 0.484 |
| 24.0 | -0.837 | -0.949 | 0.096 | -0.910 | -0.973 | 0.106 |
| 25.1 | -1.280 | -0.710 | -0.329 | -1.324 | -0.751 | -0.403 |

**flying1_run3**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 0.0 | -0.409 | -0.963 | 0.182 | -0.254 | -0.973 | 0.505 |
| 1.0 | -0.247 | -1.234 | 0.528 | -0.113 | -1.242 | 0.770 |
| 2.1 | -0.135 | -1.536 | 1.006 | -0.024 | -1.533 | 1.117 |
| 3.0 | -0.055 | -1.889 | 1.371 | 0.016 | -1.864 | 1.368 |
| 4.0 | -0.130 | -2.149 | 1.573 | -0.055 | -2.107 | 1.490 |
| 5.0 | -0.364 | -2.339 | 1.826 | -0.264 | -2.267 | 1.734 |
| 6.0 | -0.733 | -2.699 | 2.430 | -0.617 | -2.621 | 2.285 |
| 7.1 | -0.912 | -3.188 | 3.130 | -0.779 | -3.082 | 2.983 |
| 8.0 | -0.761 | -3.434 | 3.519 | -0.657 | -3.317 | 3.368 |
| 9.0 | -0.549 | -3.461 | 3.625 | -0.488 | -3.340 | 3.460 |
| 10.1 | -0.406 | -3.400 | 3.488 | -0.396 | -3.271 | 3.291 |
| 11.0 | -0.385 | -3.209 | 3.240 | -0.374 | -3.099 | 3.070 |
| 12.0 | -0.389 | -2.856 | 2.804 | -0.392 | -2.797 | 2.706 |
| 13.0 | -0.568 | -2.618 | 2.475 | -0.552 | -2.581 | 2.409 |
| 14.0 | -0.702 | -2.543 | 2.295 | -0.681 | -2.548 | 2.254 |
| 15.1 | -0.542 | -2.607 | 2.206 | -0.544 | -2.645 | 2.195 |
| 16.0 | -0.271 | -2.558 | 2.143 | -0.354 | -2.599 | 2.177 |
| 17.1 | -0.052 | -2.310 | 1.895 | -0.171 | -2.392 | 1.977 |
| 18.0 | 0.126 | -2.156 | 1.529 | -0.030 | -2.268 | 1.601 |
| 19.0 | 0.360 | -2.161 | 1.138 | 0.199 | -2.275 | 1.245 |
| 20.0 | 0.531 | -2.002 | 0.964 | 0.364 | -2.104 | 1.139 |
| 21.0 | 0.515 | -1.810 | 0.856 | 0.348 | -1.897 | 1.029 |
| 22.0 | 0.135 | -1.557 | 0.709 | -0.039 | -1.606 | 0.802 |
| 23.1 | -0.359 | -1.211 | 0.413 | -0.528 | -1.243 | 0.474 |
| 24.0 | -0.837 | -0.949 | 0.096 | -0.870 | -1.017 | 0.120 |
| 25.1 | -1.280 | -0.710 | -0.329 | -1.215 | -0.839 | -0.297 |

**flying3_run1**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.1 | 0.177 | -1.308 | 0.648 | 0.022 | -1.347 | 0.913 |
| 2.0 | 0.327 | -1.538 | 0.903 | 0.119 | -1.614 | 1.061 |
| 3.0 | 0.455 | -1.777 | 1.217 | 0.238 | -1.878 | 1.339 |
| 4.0 | 0.557 | -1.969 | 1.447 | 0.284 | -2.079 | 1.676 |
| 5.0 | 0.421 | -2.180 | 1.859 | 0.180 | -2.218 | 2.010 |
| 6.0 | 0.178 | -2.434 | 2.269 | -0.024 | -2.413 | 2.468 |
| 7.0 | -0.223 | -2.650 | 2.575 | -0.304 | -2.551 | 2.716 |
| 8.0 | -0.675 | -2.737 | 2.758 | -0.646 | -2.607 | 2.868 |
| 9.1 | -1.042 | -2.773 | 2.706 | -0.992 | -2.623 | 2.734 |
| 10.1 | -1.043 | -2.724 | 2.724 | -1.001 | -2.590 | 2.698 |
| 11.1 | -0.784 | -2.750 | 2.749 | -0.730 | -2.635 | 2.776 |
| 12.0 | -0.462 | -2.709 | 2.681 | -0.399 | -2.619 | 2.778 |
| 13.0 | -0.101 | -2.652 | 2.487 | -0.038 | -2.559 | 2.606 |
| 14.0 | 0.374 | -2.544 | 2.194 | 0.395 | -2.482 | 2.324 |
| 15.0 | 0.798 | -2.319 | 1.832 | 0.809 | -2.273 | 1.913 |
| 16.0 | 1.020 | -2.242 | 1.438 | 1.096 | -2.261 | 1.397 |
| 17.1 | 0.896 | -2.034 | 1.257 | 0.930 | -2.167 | 1.252 |
| 18.0 | 0.560 | -2.081 | 1.232 | 0.599 | -2.215 | 1.131 |
| 19.1 | 0.466 | -2.206 | 1.480 | 0.460 | -2.390 | 1.308 |
| 20.0 | 0.471 | -2.398 | 2.019 | 0.427 | -2.558 | 1.886 |
| 21.0 | 0.107 | -2.610 | 2.328 | 0.184 | -2.626 | 2.093 |
| 22.1 | -0.308 | -2.676 | 2.387 | -0.116 | -2.672 | 2.122 |
| 23.0 | -0.783 | -2.688 | 2.486 | -0.449 | -2.664 | 2.127 |
| 24.1 | -1.202 | -2.823 | 2.389 | -0.903 | -2.793 | 1.910 |

**flying3_run2**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.1 | 0.177 | -1.308 | 0.648 | 0.143 | -1.265 | 0.742 |
| 2.0 | 0.327 | -1.538 | 0.903 | 0.265 | -1.511 | 0.917 |
| 3.0 | 0.455 | -1.777 | 1.217 | 0.405 | -1.741 | 1.215 |
| 4.0 | 0.557 | -1.969 | 1.447 | 0.502 | -1.958 | 1.575 |
| 5.0 | 0.421 | -2.180 | 1.859 | 0.350 | -2.082 | 1.916 |
| 6.0 | 0.178 | -2.434 | 2.269 | 0.132 | -2.311 | 2.444 |
| 7.0 | -0.223 | -2.650 | 2.575 | -0.221 | -2.523 | 2.778 |
| 8.1 | -0.684 | -2.738 | 2.759 | -0.660 | -2.628 | 2.986 |
| 9.1 | -1.042 | -2.773 | 2.706 | -1.057 | -2.671 | 2.848 |
| 10.1 | -1.043 | -2.724 | 2.724 | -1.046 | -2.618 | 2.772 |
| 11.0 | -0.796 | -2.750 | 2.749 | -0.765 | -2.666 | 2.796 |
| 12.1 | -0.454 | -2.708 | 2.678 | -0.513 | -2.704 | 2.643 |
| 13.1 | -0.064 | -2.645 | 2.471 | -0.102 | -2.616 | 2.493 |
| 14.1 | 0.402 | -2.534 | 2.174 | 0.339 | -2.515 | 2.222 |
| 15.1 | 0.807 | -2.313 | 1.820 | 0.682 | -2.304 | 1.874 |
| 16.1 | 1.033 | -2.230 | 1.410 | 1.091 | -2.371 | 1.540 |
| 17.0 | 0.913 | -2.038 | 1.260 | 0.857 | -2.179 | 1.368 |
| 18.1 | 0.544 | -2.090 | 1.239 | 0.483 | -2.246 | 1.116 |
| 19.0 | 0.464 | -2.201 | 1.468 | 0.360 | -2.414 | 1.299 |
| 20.1 | 0.449 | -2.411 | 2.055 | 0.315 | -2.555 | 1.907 |
| 21.1 | 0.096 | -2.615 | 2.332 | 0.077 | -2.698 | 2.136 |
| 22.1 | -0.308 | -2.676 | 2.387 | -0.212 | -2.746 | 2.152 |
| 23.0 | -0.764 | -2.688 | 2.486 | -0.505 | -2.768 | 2.165 |
| 24.1 | -1.209 | -2.826 | 2.387 | -0.850 | -2.942 | 1.987 |

**flying3_run3**

| t_s | gt_x | gt_y | gt_z | est_x | est_y | est_z |
|---|---|---|---|---|---|---|
| 1.1 | 0.177 | -1.308 | 0.648 | 0.025 | -1.335 | 0.924 |
| 2.0 | 0.327 | -1.538 | 0.903 | 0.126 | -1.607 | 1.060 |
| 3.0 | 0.455 | -1.777 | 1.217 | 0.241 | -1.880 | 1.333 |
| 4.0 | 0.557 | -1.969 | 1.447 | 0.277 | -2.078 | 1.677 |
| 5.0 | 0.421 | -2.180 | 1.859 | 0.172 | -2.214 | 2.018 |
| 6.0 | 0.178 | -2.434 | 2.269 | -0.043 | -2.403 | 2.476 |
| 7.0 | -0.223 | -2.650 | 2.575 | -0.319 | -2.541 | 2.722 |
| 8.0 | -0.675 | -2.737 | 2.758 | -0.662 | -2.599 | 2.874 |
| 9.1 | -1.042 | -2.773 | 2.706 | -1.010 | -2.620 | 2.732 |
| 10.1 | -1.043 | -2.724 | 2.724 | -1.020 | -2.586 | 2.691 |
| 11.1 | -0.784 | -2.750 | 2.749 | -0.746 | -2.631 | 2.777 |
| 12.0 | -0.462 | -2.709 | 2.681 | -0.414 | -2.611 | 2.781 |
| 13.0 | -0.101 | -2.652 | 2.487 | -0.051 | -2.553 | 2.608 |
| 14.0 | 0.374 | -2.544 | 2.194 | 0.383 | -2.479 | 2.326 |
| 15.0 | 0.798 | -2.319 | 1.832 | 0.801 | -2.274 | 1.914 |
| 16.0 | 1.020 | -2.242 | 1.438 | 1.089 | -2.267 | 1.401 |
| 17.1 | 0.896 | -2.034 | 1.257 | 0.930 | -2.190 | 1.245 |
| 18.0 | 0.560 | -2.081 | 1.232 | 0.593 | -2.229 | 1.123 |
| 19.1 | 0.466 | -2.206 | 1.480 | 0.452 | -2.405 | 1.298 |
| 20.0 | 0.471 | -2.398 | 2.019 | 0.420 | -2.562 | 1.879 |
| 21.0 | 0.107 | -2.610 | 2.328 | 0.172 | -2.633 | 2.087 |
| 22.1 | -0.308 | -2.676 | 2.387 | -0.130 | -2.676 | 2.105 |
| 23.0 | -0.783 | -2.688 | 2.486 | -0.433 | -2.674 | 2.116 |
| 24.1 | -1.202 | -2.823 | 2.389 | -0.791 | -2.799 | 1.908 |

### Log summaries

- flying1_run1_esvio.log: 181 lines; last lines: `terminate called without an active exception / terminate called without an active exception / terminate called without an active exception`
- flying1_run2_esvio.log: 181 lines; last lines: `terminate called without an active exception / terminate called without an active exception / terminate called without an active exception`
- flying1_run3_esvio.log: 181 lines; last lines: `terminate called without an active exception / terminate called without an active exception / terminate called without an active exception`
- flying3_run1_esvio.log: 276 lines; last lines: `terminate called without an active exception / terminate called without an active exception / terminate called without an active exception`
- flying3_run2_esvio.log: 279 lines; last lines: `terminate called without an active exception / terminate called without an active exception / terminate called without an active exception`
- flying3_run3_esvio.log: 279 lines; last lines: `terminate called without an active exception / terminate called without an active exception / terminate called without an active exception`

