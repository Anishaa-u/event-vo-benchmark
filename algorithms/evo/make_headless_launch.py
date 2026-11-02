"""Create headless copies of EVO's launch files for bag playback in a container without a display.

  rpg_headless.launch        = live.launch (EVO's template, set up for the DAVIS-ijrr camera of
                               the RPG Event Camera Dataset) without rqt_gui/svo_gui, rqt_evo,
                               rviz, dvs_renderer and dvs_reconstruction
  flyingroom_headless.launch = flyingroom.launch with the same visualisation nodes removed

These nodes only draw images or GUIs; tracking, mapping and bootstrapping are unchanged.
Python 2 and 3 compatible (ROS Melodic).
    python make_headless_launch.py
"""

import re

LAUNCH_DIR = "/catkin_ws/src/rpg_dvs_evo_open/dvs_tracking/launch/"
VIS_NODES = ["svo_gui", "rqt_evo", "rviz", "dvs_renderer_left", "dvs_reconstruction"]


def strip(text):
    for name in VIS_NODES:
        # self-closing <node ... /> or <node ...>...</node>
        text = re.sub(r'\s*<node[^>]*name="%s"[^>]*/>' % name, "", text)
        text = re.sub(r'\s*<node[^>]*name="%s"[^>]*>.*?</node>' % name, "", text, flags=re.S)
    return text


for src, dst in [("live.launch", "rpg_headless.launch"),
                 ("flyingroom.launch", "flyingroom_headless.launch")]:
    with open(LAUNCH_DIR + src) as f:
        text = strip(f.read())
    with open(LAUNCH_DIR + dst, "w") as f:
        f.write(text)
    remaining = [n for n in VIS_NODES if 'name="%s"' % n in text]
    print("Wrote %s (visualisation nodes left: %s)" % (dst, remaining or "none"))
