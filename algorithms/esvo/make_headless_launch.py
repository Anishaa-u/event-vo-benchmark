"""Create system_upenn_headless.launch: ESVO's system_upenn.launch without rqt_gui and rviz,
which need a display the container does not have. Nothing else is changed.
    python3 make_headless_launch.py
"""

import re

LAUNCH_DIR = "/catkin_ws/src/ESVO/esvo_core/launch/system/"

with open(LAUNCH_DIR + "system_upenn.launch") as f:
    text = f.read()
text = re.sub(r"\s*<!-- Visualization -->.*?(?=</launch>)", "\n", text, flags=re.S)
with open(LAUNCH_DIR + "system_upenn_headless.launch", "w") as f:
    f.write(text)
print("Wrote", LAUNCH_DIR + "system_upenn_headless.launch")
