"""Convert ESVIO's esvio_result_no_loop.csv (time in ns, x, y, z, qw, qx, qy, qz, vx, vy, vz)
to TUM format (time in s, x, y, z, qx, qy, qz, qw).
    python3 esvio_csv_to_tum.py esvio_result_no_loop.csv out.txt
"""

import sys

n = 0
with open(sys.argv[1]) as f, open(sys.argv[2], "w") as out:
    for line in f:
        parts = [p for p in line.strip().split(",") if p]
        if len(parts) < 8 or not parts[0][0].isdigit():
            continue
        t, x, y, z, qw, qx, qy, qz = (float(p) for p in parts[:8])
        out.write(f"{t * 1e-9:.9f} {x} {y} {z} {qx} {qy} {qz} {qw}\n")
        n += 1
print(f"Wrote {n} poses to {sys.argv[2]}")
