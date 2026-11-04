#!/bin/bash
# One EVO run on an RPG Event Camera Dataset sequence, end to end. Run inside the container from /work:
#     bash run_evo.sh shapes_6dof 1
# Defaults reproduce the reported protocol: EVO's bag-playback configuration (flyingroom_headless.launch)
# with the RPG camera calibration (EXTRA=camera_name:=DAVIS-ijrr), auto-trigger, bootstrapping from the
# sensor's frames (BOOT=frames; BOOT=events for EVO's default) and playback at RATE=0.5. Records /evo/pose,
# profiles CPU and memory, and writes the trajectory to runs/<seq>_run<k>.txt.
SEQ=$1; RUN=$2
RATE=${RATE:-0.5}
BOOT=${BOOT:-frames}
LAUNCH_FILE=${LAUNCH_FILE:-flyingroom_headless.launch}; EXTRA=${EXTRA-camera_name:=DAVIS-ijrr}
BAG=${BAG:-/tmp/$SEQ.bag}
# play from the container's own disk, not the slower Windows-mounted folder
[ -f $BAG ] || cp /work/data/$(basename $BAG) $BAG
OUT=${OUT:-/work/runs}
NAME=${SEQ}_run${RUN}
source /catkin_ws/devel/setup.bash
mkdir -p $OUT/logs $OUT/raw

if [ "$BOOT" = "frames" ]; then BOOT_ARG="bootstrap_image_topic:=/dvs/image_raw"; else BOOT_ARG=""; fi

roslaunch dvs_tracking $LAUNCH_FILE auto_trigger:=true $BOOT_ARG $EXTRA $EXTRA > $OUT/logs/${NAME}_evo.log 2>&1 &
LAUNCH=$!
sleep 10

python /work/record_pose.py /evo/pose $OUT/$NAME.txt > /dev/null 2>&1 &
REC=$!
python3 /work/profile_procs.py $OUT/${NAME}_profile.csv svo_node dvs_mapping dvs_tracking dvs_bootstrapping \
    trigger_map_expansion pose_to_tf > $OUT/logs/${NAME}_profile.txt 2>&1 &
PROF=$!
sleep 2

START=$(date +%s.%N)
rosbag play $BAG -r $RATE -q
END=$(date +%s.%N)
sleep 3

kill -INT $REC 2>/dev/null; sleep 1
kill -TERM $PROF; wait $PROF
CRASHED=$(grep -c "process has died" $OUT/logs/${NAME}_evo.log)
kill -INT $LAUNCH 2>/dev/null; sleep 5
bash /work/stop_evo.sh > /dev/null

POSES=0
[ -s $OUT/$NAME.txt ] && POSES=$(wc -l < $OUT/$NAME.txt)
SUMMARY=$(grep "Mean CPU" $OUT/logs/${NAME}_profile.txt)
WALL=$(python3 -c "print('%.1f' % ($END - $START))")
LINE="$NAME | rate ${RATE}x | bootstrap $BOOT | wall $WALL s (start $START, end $END) | poses $POSES | node crashes during run $CRASHED | $SUMMARY"
echo "$LINE" | tee -a $OUT/run_log.txt
