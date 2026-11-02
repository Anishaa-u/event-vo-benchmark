#!/bin/bash
# Stop every ROS/ESVIO process left in the container (e.g. after an interrupted run).
for pat in profile_procs roslaunch stereo_event_tracker stereo_image_tracker stereo_esvio_estimator \
           pose_graph rosmaster rostopic rosout "rosbag play"; do
  pkill -9 -f "$pat" 2>/dev/null
done
sleep 1
echo "Remaining ESVIO processes: $(pgrep -fc 'stereo_e|rosmaster')"
