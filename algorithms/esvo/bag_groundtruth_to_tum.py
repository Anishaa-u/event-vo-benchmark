"""Extract the ground-truth pose topic from a rosbag into TUM format.

Run inside the container:
    python3 bag_groundtruth_to_tum.py /data/upenn_indoor_flying1.bag gt_flying1.txt
Optionally give the topic as a third argument. Without it, the first
geometry_msgs/PoseStamped topic in the bag is used and its name is printed.
TUM format: timestamp tx ty tz qx qy qz qw
"""

import sys

import rosbag


def main(bag_path, out_path, topic=None):
    bag = rosbag.Bag(bag_path)
    info = bag.get_type_and_topic_info().topics
    if topic is None:
        poses = [t for t, v in info.items() if v.msg_type == "geometry_msgs/PoseStamped"]
        if not poses:
            print("No PoseStamped topic found. Topics in this bag:")
            for t, v in info.items():
                print(f"  {t}  ({v.msg_type})")
            sys.exit(1)
        topic = poses[0]
    print(f"Using ground-truth topic {topic}")
    n = 0
    with open(out_path, "w") as f:
        for _, msg, _ in bag.read_messages(topics=[topic]):
            p, q = msg.pose.position, msg.pose.orientation
            f.write(f"{msg.header.stamp.to_sec():.9f} {p.x} {p.y} {p.z} {q.x} {q.y} {q.z} {q.w}\n")
            n += 1
    bag.close()
    print(f"Wrote {n} poses to {out_path}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
