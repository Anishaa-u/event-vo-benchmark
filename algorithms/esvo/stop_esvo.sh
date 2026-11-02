#!/bin/bash
# Stop every ROS/ESVO process left in the container (e.g. after an interrupted run).
for pat in profile_esvo clock_keeper roslaunch esvo_ rosmaster rostopic rosout "rosbag play"; do
  pkill -9 -f "$pat" 2>/dev/null
done
sleep 1
echo "Remaining ESVO processes: $(pgrep -fc 'esvo_|rosmaster')"
