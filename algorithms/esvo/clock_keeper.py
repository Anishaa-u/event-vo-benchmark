"""Keep /clock advancing after the bag ends, starting from the bag's end time.

ESVO's tracking loop sleeps on simulated time and only saves its trajectory once it
reads ESVO_SYSTEM_STATUS = TERMINATE, which it cannot do if /clock has stopped.
    python3 clock_keeper.py <bag end time in seconds>
"""

import sys
import time

import rospy
from rosgraph_msgs.msg import Clock

rospy.init_node("clock_keeper", disable_signals=True)
pub = rospy.Publisher("/clock", Clock, queue_size=10)
t = float(sys.argv[1])
while True:
    t += 0.01
    pub.publish(Clock(clock=rospy.Time.from_sec(t)))
    time.sleep(0.01)
