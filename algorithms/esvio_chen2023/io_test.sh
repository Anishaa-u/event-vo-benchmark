#!/bin/bash
# Compare bag read speed from the Windows-mounted folder and from the container's own disk,
# and time a 1x rosbag play from each (no algorithm running).
source /opt/ros/noetic/setup.bash
BAG=/work/data/indoor_flying1_edited.bag
t() { python3 -c "import time; print(time.time())"; }
s=$(t); cat $BAG > /dev/null; e=$(t)
python3 -c "print('windows share read: %.1f MB/s' % (655/($e-$s)))"
cp $BAG /tmp/f1.bag
s=$(t); cat /tmp/f1.bag > /dev/null; e=$(t)
python3 -c "print('container disk read: %.1f MB/s' % (655/($e-$s)))"
roscore > /dev/null 2>&1 &
sleep 3
for src in $BAG /tmp/f1.bag; do
  s=$(t); rosbag play $src -q > /dev/null 2>&1; e=$(t)
  python3 -c "print('rosbag play 1x from $src: %.1f s for a 26 s bag' % ($e-$s))"
done
pkill -f roscore; pkill -f rosmaster
