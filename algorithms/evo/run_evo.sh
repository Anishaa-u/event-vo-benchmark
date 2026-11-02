#!/bin/bash
# One EVO run on an RPG Event Camera Dataset sequence, end to end. Run inside the container from /work:
#     bash run_evo.sh shapes_6dof 1
# Uses EVO's DAVIS-ijrr template (rpg_headless.launch) with auto-trigger and bootstrapping from the
# sensor's frames (BOOT=frames, the method EVO's README calls most reliable) or from events
# (BOOT=events, EVO's default). Plays the bag at RATE (default 1.0), records /evo/pose, profiles CPU
# and memory, and writes the trajectory to runs/<seq>_run<k>.txt.
SEQ=$1; RUN=$2
RATE=${RATE:-1.0}
BOOT=${BOOT:-frames}
LAUNCH_FILE=${LAUNCH_FILE:-rpg_headless.launch}
BAG=${BAG:-/work/data/$SEQ.bag}
OUT=/work/runs
NAME=${SEQ}_run${RUN}
source /catkin_ws/devel/setup.bash
mkdir -p $OUT/logs $OUT/raw

if [ "$BOOT" = "frames" ]; then BOOT_ARG="bootstrap_image_topic:=/dvs/image_raw"; else BOOT_ARG=""; fi

roslaunch dvs_tracking $LAUNCH_FILE auto_trigger:=true $BOOT_ARG > $OUT/logs/${NAME}_evo.log 2>&1 &
LAUNCH=$!
sleep 10

rosbag record -O $OUT/raw/${NAME}_pose.bag /evo/pose __name:=record_evo > /dev/null 2>&1 &
python3 /work/profile_procs.py $OUT/${NAME}_profile.csv svo_node dvs_mapping dvs_tracking dvs_bootstrapping \
    trigger_map_expansion pose_to_tf > $OUT/logs/${NAME}_profile.txt 2>&1 &
PROF=$!
sleep 2

START=$(date +%s.%N)
rosbag play $BAG -r $RATE -q
END=$(date +%s.%N)
sleep 3

rosnode kill /record_evo > /dev/null 2>&1; sleep 2
kill -TERM $PROF; wait $PROF
kill -INT $LAUNCH 2>/dev/null; sleep 5
bash /work/stop_evo.sh > /dev/null

POSES=0
if [ -s $OUT/raw/${NAME}_pose.bag ]; then
  python /work/bag_pose_to_tum.py $OUT/raw/${NAME}_pose.bag $OUT/$NAME.txt /evo/pose > /dev/null 2>&1
  [ -s $OUT/$NAME.txt ] && POSES=$(wc -l < $OUT/$NAME.txt)
fi
SUMMARY=$(grep "Mean CPU" $OUT/logs/${NAME}_profile.txt)
WALL=$(python3 -c "print('%.1f' % ($END - $START))")
LINE="$NAME | rate ${RATE}x | bootstrap $BOOT | wall $WALL s (start $START, end $END) | poses $POSES | $SUMMARY"
echo "$LINE" | tee -a $OUT/run_log.txt
