"""Sample CPU and memory of all ESVO processes while a run is in progress.

Run inside the container in its own terminal BEFORE starting the bag, then press
Ctrl+C once ESVO has saved its trajectory.
    python3 profile_esvo.py runs/flying1_run1_profile.csv
Writes one row per sample and prints the summary used for the efficiency table.
"""

import csv
import signal
import sys
import time

import psutil

INTERVAL_S = 0.1


def _stop(*_):
    raise KeyboardInterrupt


# Background jobs in a script ignore SIGINT, so run_esvo.sh stops the profiler with SIGTERM
signal.signal(signal.SIGTERM, _stop)


def esvo_processes():
    procs = []
    for p in psutil.process_iter(["cmdline"]):
        cmd = " ".join(p.info.get("cmdline") or [])
        if "esvo_core" in cmd or "esvo_time_surface" in cmd:
            procs.append(p)
    return procs


def main(out_path):
    rows, primed = [], set()
    start = time.time()
    print("Profiling ESVO processes. Press Ctrl+C after the trajectory is saved.")
    try:
        while True:
            cpu, rss = 0.0, 0
            for p in esvo_processes():
                try:
                    if p.pid not in primed:
                        p.cpu_percent(None)   # first call only sets the baseline
                        primed.add(p.pid)
                        continue
                    cpu += p.cpu_percent(None)
                    rss += p.memory_info().rss
                except psutil.NoSuchProcess:
                    pass
            rows.append({"t_s": round(time.time() - start, 3),
                         "cpu_percent_one_core": round(cpu, 1),
                         "rss_mb": round(rss / 1e6, 1)})
            time.sleep(INTERVAL_S)
    except KeyboardInterrupt:
        pass

    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["t_s", "cpu_percent_one_core", "rss_mb"])
        w.writeheader()
        w.writerows(rows)
    active = [r for r in rows if r["cpu_percent_one_core"] > 0]
    if active:
        mean_cpu = sum(r["cpu_percent_one_core"] for r in active) / len(active)
        peak_mb = max(r["rss_mb"] for r in rows)
        print(f"Samples: {len(rows)}  Mean CPU (% of one core): {mean_cpu:.1f}  "
              f"Peak memory: {peak_mb:.0f} MB  Logged for {rows[-1]['t_s']:.1f} s")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "esvo_profile.csv")
