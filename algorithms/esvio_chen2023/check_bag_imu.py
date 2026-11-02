"""Print IMU, image and event timing and the mean accelerometer reading of a bag (diagnostic)."""

import sys

import numpy as np
import rosbag

bag = rosbag.Bag(sys.argv[1])
first = {}
acc, stamps = [], {}
for topic, msg, t in bag.read_messages(topics=["/davis/left/imu", "/davis/left/image_raw",
                                               "/davis/right/image_raw", "/davis/left/events"]):
    st = msg.header.stamp.to_sec() if hasattr(msg, "header") else t.to_sec()
    stamps.setdefault(topic, []).append(st)
    if topic == "/davis/left/imu" and len(acc) < 2000:
        a = msg.linear_acceleration
        acc.append([a.x, a.y, a.z])
for k, v in stamps.items():
    v = np.array(v)
    print(f"{k}: n={len(v)} first={v[0]:.3f} last={v[-1]:.3f} rate={len(v)/(v[-1]-v[0]):.1f} Hz "
          f"non-monotonic={int(np.sum(np.diff(v) < 0))}")
acc = np.array(acc)
print("mean accel first 2000 IMU samples:", acc.mean(axis=0).round(3), "norm", np.linalg.norm(acc.mean(axis=0)).round(3))
