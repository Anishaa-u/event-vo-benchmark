# ESVO on ROS Noetic (Ubuntu 20.04), which the ESVO README lists as supported.
# Build:  docker build -t esvo .
FROM osrf/ros:noetic-desktop

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
      python3-catkin-tools python3-vcstool python3-psutil python3-numpy \
      git autoconf automake libtool \
      libgoogle-glog-dev libgflags-dev libyaml-cpp-dev libeigen3-dev libpcl-dev \
      ros-noetic-pcl-ros ros-noetic-cv-bridge ros-noetic-image-transport \
      ros-noetic-tf ros-noetic-tf-conversions ros-noetic-camera-info-manager \
      ros-noetic-rqt-reconfigure tmux nano \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws/src

# ESVO and its listed dependencies (dependencies.yaml includes rpg_dvs_ros, which provides dvs_msgs)
RUN git clone https://github.com/HKUST-Aerial-Robotics/ESVO.git \
 && vcs-import < ESVO/dependencies.yaml

WORKDIR /catkin_ws
# Install every ROS dependency the cloned packages declare (e.g. image_geometry)
RUN apt-get update && apt-get install -y ros-noetic-image-geometry \
 && (rosdep update --rosdistro noetic || true) \
 && rosdep install --from-paths src --ignore-src --rosdistro noetic -r -y \
 && rm -rf /var/lib/apt/lists/*
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    catkin config --extend /opt/ros/noetic --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    catkin build dvs_msgs esvo_time_surface esvo_core"

# Record the exact ESVO commit used, for the report's provenance requirement (R9)
RUN cd /catkin_ws/src/ESVO && git rev-parse HEAD > /catkin_ws/ESVO_COMMIT.txt

RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc
WORKDIR /work
