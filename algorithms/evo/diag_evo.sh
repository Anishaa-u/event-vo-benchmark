#!/bin/bash
# Diagnostic: start EVO, play a bag, and report topic rates for the bootstrap (SVO) and tracker.
#   bash diag_evo.sh <launch file> <bag> <rate> [extra roslaunch args]
LAUNCH_FILE=$1; BAG=$2; RATE=$3; shift 3
source /catkin_ws/devel/setup.bash
export PYTHONUNBUFFERED=1
roslaunch dvs_tracking $LAUNCH_FILE auto_trigger:=true "$@" > /tmp/diag_launch.log 2>&1 &
sleep 10
rosbag play $BAG -r $RATE -q -u 40 &
PLAY=$!
sleep 25
for t in /dvs/events /events/image_raw /svo/pose_cam/0 /dvs_mapping/pointcloud /evo/pose; do
  printf "%-26s " $t; timeout 6 rostopic hz $t 2>/dev/null | grep -m1 "average rate" || echo "no messages"
done
rosparam get /svo/ 2>/dev/null | grep -i "cam0_topic"
wait $PLAY
sleep 2
grep -aiE "died|error|bootstrap|svo|init" /tmp/diag_launch.log | sed 's/\x1b\[[0-9;]*m//g' | grep -v "Found parameter" | sort | uniq -c | sort -rn | head -15
pkill -f roslaunch; sleep 3; bash /work/stop_evo.sh > /dev/null
