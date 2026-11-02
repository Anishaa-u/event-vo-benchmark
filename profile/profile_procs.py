"""Sample CPU and memory of every process whose command line contains one of the given patterns.

Same method as profile_esvo.py (0.1 s interval, CPU as % of one core, summed RSS), so results
are comparable across algorithms. Stop with Ctrl+C or SIGTERM.
    python3 profile_procs.py out.csv pattern1 [pattern2 ...]
"""

import csv
import signal
import sys
import time

import psutil

INTERVAL_S = 0.1


def _stop(*_):
    raise KeyboardInterrupt


# Background jobs in a script ignore SIGINT, so run scripts stop the profiler with SIGTERM
signal.signal(signal.SIGTERM, _stop)


def matching_processes(patterns):
    procs = []
    for p in psutil.process_iter(["cmdline"]):
        cmd = " ".join(p.info.get("cmdline") or [])
        if any(pat in cmd for pat in patterns) and "profile_procs" not in cmd:
            procs.append(p)
    return procs


def main(out_path, patterns):
    rows, primed = [], set()
    start = time.time()
    print("Profiling processes matching", patterns)
    try:
        while True:
            cpu, rss = 0.0, 0
            for p in matching_processes(patterns):
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
    main(sys.argv[1], sys.argv[2:])
