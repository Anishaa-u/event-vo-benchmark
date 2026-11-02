"""Write every geometry_msgs/PoseStamped on a topic straight to a TUM file, flushing each line,
so poses are kept even if the algorithm crashes. Python 2 and 3 compatible (ROS Melodic).
    python record_pose.py /evo/pose out.txt
"""

import sys

import rospy
from geometry_msgs.msg import PoseStamped

out = open(sys.argv[2], "w")


def callback(msg):
    p, q = msg.pose.position, msg.pose.orientation
    out.write("%.9f %r %r %r %r %r %r %r\n" % (msg.header.stamp.to_sec(), p.x, p.y, p.z, q.x, q.y, q.z, q.w))
    out.flush()


rospy.init_node("record_pose", anonymous=True)
rospy.Subscriber(sys.argv[1], PoseStamped, callback, queue_size=1000)
rospy.spin()
out.close()
