#!/bin/bash
# One ESVO run on an upenn sequence, end to end. Run inside the container from /work:
#     bash run_esvo.sh flying1 1
# Plays the edited bag at RATE (default 0.25x; ESVO's own upenn default is 0.5x), with the
# sync timer at 100*RATE Hz so time surfaces stay at 100 Hz in bag time, as ESVO's README
# requires. Profiles CPU and memory, logs the time-surface rate, then saves the
# trajectory to runs/<seq>_run<k>.txt.
SEQ=$1; RUN=$2
RATE=${RATE:-0.25}
SYNC_HZ=$(python3 -c "print(round(100 * $RATE))")
BAG=/work/data/indoor_${SEQ}_edited.bag
OUT=/work/runs; TMP=/tmp/esvo_result/
NAME=${SEQ}_run${RUN}
source /catkin_ws/devel/setup.bash
mkdir -p $OUT/logs; rm -rf $TMP; mkdir -p $TMP

# Setup: save the trajectory to $TMP (ESVO writes result.txt there on TERMINATE)
CFG=/catkin_ws/src/ESVO/esvo_core/cfg/tracking/tracking_upenn.yaml
sed -i "s|^SAVE_TRAJECTORY:.*|SAVE_TRAJECTORY: True|; s|^PATH_TO_SAVE_TRAJECTORY:.*|PATH_TO_SAVE_TRAJECTORY: \"$TMP\"|" $CFG
LAUNCH_FILE=/catkin_ws/src/ESVO/esvo_core/launch/system/system_upenn_headless.launch
sed -i -E "s|pub -s -r [0-9.]+ /sync|pub -s -r $SYNC_HZ /sync|" $LAUNCH_FILE

roslaunch esvo_core system_upenn_headless.launch > $OUT/logs/${NAME}_esvo.log 2>&1 &
LAUNCH=$!
sleep 8

python3 /work/profile_esvo.py $OUT/${NAME}_profile.csv > $OUT/logs/${NAME}_profile.txt 2>&1 &
PROF=$!
(sleep 15; timeout 20 rostopic hz /TS_left) > $OUT/logs/${NAME}_ts_hz.txt 2>&1 &

START=$(date +%s.%N)
rosbag play $BAG -r $RATE --clock -q
END=$(date +%s.%N)

# Bag finished: keep sim time moving, ask ESVO to stop and save
BAG_END=$(python3 -c "import rosbag; print(rosbag.Bag('$BAG').get_end_time())")
python3 /work/clock_keeper.py $BAG_END &
CLOCK=$!
rosparam set /ESVO_SYSTEM_STATUS TERMINATE
for i in $(seq 1 60); do
  [ -s $TMP/result.txt ] && grep -q "Saving trajectory" $OUT/logs/${NAME}_esvo.log && sleep 2 && break
  sleep 1
done

kill -TERM $PROF; wait $PROF
kill $CLOCK; kill -TERM $LAUNCH; sleep 5
bash /work/stop_esvo.sh > /dev/null

if [ -s $TMP/result.txt ]; then
  cp $TMP/result.txt $OUT/$NAME.txt
  POSES=$(wc -l < $OUT/$NAME.txt)
else
  POSES=0
fi
HZ=$(grep "average rate" $OUT/logs/${NAME}_ts_hz.txt | tail -1 | awk '{print $3}')
SUMMARY=$(grep "Mean CPU" $OUT/logs/${NAME}_profile.txt)
LINE="$NAME | rate ${RATE}x, sync ${SYNC_HZ} Hz | wall $(python3 -c "print(f'{$END - $START:.1f}')") s (start $START, end $END) | TS_left ${HZ:-n/a} Hz | poses $POSES | $SUMMARY"
echo "$LINE" | tee -a $OUT/run_log.txt
