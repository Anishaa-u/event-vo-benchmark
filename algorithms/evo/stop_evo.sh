#!/bin/bash
# Stop every ROS/EVO process left in the container (e.g. after an interrupted run).
for pat in profile_procs roslaunch "rosbag record" "rosbag play" record_ svo_node dvs_mapping dvs_tracking \
           dvs_bootstrapping trigger_map_expansion pose_to_tf tf_to_camera snakify rosmaster rosout; do
  pkill -9 -f "$pat" 2>/dev/null
done
sleep 1
echo "Remaining EVO processes: $(pgrep -fc 'dvs_|svo_node|rosmaster')"
