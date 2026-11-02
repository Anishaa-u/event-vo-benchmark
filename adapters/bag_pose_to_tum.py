"""Write a geometry_msgs/PoseStamped topic from a bag to TUM format
(timestamp tx ty tz qx qy qz qw). Used for EVO's /evo/pose output and for the RPG dataset's
/optitrack/davis ground truth. Python 2 and 3 compatible (ROS Melodic).
    python bag_pose_to_tum.py in.bag out.txt /topic
"""

import sys

import rosbag


def main(bag_path, out_path, topic):
    bag = rosbag.Bag(bag_path)
    n = 0
    with open(out_path, "w") as f:
        for _, msg, _ in bag.read_messages(topics=[topic]):
            p, q = msg.pose.position, msg.pose.orientation
            f.write("%.9f %r %r %r %r %r %r %r\n" % (msg.header.stamp.to_sec(),
                                                     p.x, p.y, p.z, q.x, q.y, q.z, q.w))
            n += 1
    bag.close()
    print("Wrote %d poses from %s to %s" % (n, topic, out_path))


if __name__ == "__main__":
    main(*sys.argv[1:4])
