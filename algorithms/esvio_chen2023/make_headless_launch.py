"""Create esvio_mvsec_flying_headless.launch: ESVIO's esvio_mvsec_flying.launch without rviz and
without the gnome-terminal launch prefix, which need a display the container does not have.
Also points output_path at /tmp/esvio_result. Nothing else is changed.
    python3 make_headless_launch.py
"""

import re

LAUNCH_DIR = "/catkin_ws/src/ESVIO/esvio_estimator/launch/"
CONFIG = "/catkin_ws/src/ESVIO/config/esvio_mvsec_flying/esvio.yaml"

with open(LAUNCH_DIR + "esvio_mvsec_flying.launch") as f:
    text = f.read()
text = text.replace(' launch-prefix="gnome-terminal -x"', "")
text = re.sub(r'\s*<node name="rvizvisualisation".*?/>', "", text, flags=re.S)
with open(LAUNCH_DIR + "esvio_mvsec_flying_headless.launch", "w") as f:
    f.write(text)
print("Wrote", LAUNCH_DIR + "esvio_mvsec_flying_headless.launch")

with open(CONFIG) as f:
    cfg = f.read()
cfg = re.sub(r'^output_path:.*$', 'output_path: "/tmp/esvio_result"', cfg, flags=re.M)
with open(CONFIG, "w") as f:
    f.write(cfg)
print("Set output_path in", CONFIG)
