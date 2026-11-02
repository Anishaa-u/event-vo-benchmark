#!/bin/bash
# One ESVIO run on an MVSEC indoor_flying sequence, end to end. Run inside the container from /work:
#     bash run_esvio.sh flying1 1
# Plays the same edited bag used for ESVO at RATE (default 1.0, real time), profiles CPU and
# memory, logs the IMU and feature rates, then saves the odometry trajectory (no loop closure)
# to runs/<seq>_run<k>.txt and the loop-closed trajectory to runs/loop/<seq>_run<k>.txt.
SEQ=$1; RUN=$2
RATE=${RATE:-1.0}
BAG=/work/data/indoor_${SEQ}_edited.bag
OUT=/work/runs; TMP=/tmp/esvio_result
NAME=${SEQ}_run${RUN}
source /catkin_ws/devel/setup.bash
mkdir -p $OUT/logs $OUT/loop; rm -rf $TMP; mkdir -p $TMP

roslaunch esvio_estimator esvio_mvsec_flying_headless.launch > $OUT/logs/${NAME}_esvio.log 2>&1 &
LAUNCH=$!
sleep 8

python3 /work/profile_procs.py $OUT/${NAME}_profile.csv stereo_event_tracker stereo_image_tracker \
    stereo_esvio_estimator pose_graph/pose_graph > $OUT/logs/${NAME}_profile.txt 2>&1 &
PROF=$!

START=$(date +%s.%N)
rosbag play $BAG -r $RATE -q
END=$(date +%s.%N)
sleep 5

kill -TERM $PROF; wait $PROF
kill -INT $LAUNCH 2>/dev/null; kill -TERM $LAUNCH; sleep 5
bash /work/stop_esvio.sh > /dev/null

if [ -s $TMP/esvio_result_no_loop.csv ]; then
  python3 /work/esvio_csv_to_tum.py $TMP/esvio_result_no_loop.csv $OUT/$NAME.txt > /dev/null
  POSES=$(wc -l < $OUT/$NAME.txt)
else
  POSES=0
fi
[ -s $TMP/esvio_result_loop.txt ] && cp $TMP/esvio_result_loop.txt $OUT/loop/$NAME.txt
RESPAWNS=$(grep -c "respawning" $OUT/logs/${NAME}_esvio.log)
SUMMARY=$(grep "Mean CPU" $OUT/logs/${NAME}_profile.txt)
LINE="$NAME | rate ${RATE}x | wall $(python3 -c "print(f'{$END - $START:.1f}')") s (start $START, end $END) | poses $POSES | respawns $RESPAWNS | $SUMMARY"
echo "$LINE" | tee -a $OUT/run_log.txt
