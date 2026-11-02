# EVO (Rebecq et al. 2017, rpg_dvs_evo_open) on ROS Melodic (Ubuntu 18.04), as its README specifies.
# Build:  docker build -t evo .
FROM osrf/ros:melodic-desktop

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
      python-catkin-tools python-vcstool python-psutil python-numpy python3-psutil \
      git autoconf automake libtool \
      ros-melodic-sophus ros-melodic-pcl-ros ros-melodic-eigen-conversions \
      ros-melodic-camera-info-manager ros-melodic-image-view ros-melodic-image-geometry \
      libfftw3-dev libglew-dev libopencv-dev libyaml-cpp-dev \
      libgoogle-glog-dev libgflags-dev \
    && rm -rf /var/lib/apt/lists/*

ARG EVO_COMMIT=14c72916b40c2d5fbd7197b772198c3ca75f4cbe
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws
RUN catkin config --init --mkdirs --extend /opt/ros/melodic --merge-devel \
      --cmake-args -DCMAKE_BUILD_TYPE=Release
WORKDIR /catkin_ws/src
# dependencies.yaml uses SSH URLs; switch them to HTTPS so no GitHub key is needed.
# zurich-eye's gflags_catkin clones a gflags branch that no longer exists; use ethz-asl's (as ESVO does)
RUN git clone https://github.com/uzh-rpg/rpg_dvs_evo_open.git \
 && cd rpg_dvs_evo_open && git checkout $EVO_COMMIT && cd .. \
 && sed -i 's|git@github.com:|https://github.com/|' rpg_dvs_evo_open/dependencies.yaml \
 && sed -i 's|zurich-eye/gflags_catkin|ethz-asl/gflags_catkin|; s|zurich-eye/glog_catkin|ethz-asl/glog_catkin|' \
      rpg_dvs_evo_open/dependencies.yaml \
 && vcs-import < rpg_dvs_evo_open/dependencies.yaml

# Live-camera drivers need libcaer and are not used for bag playback
RUN touch rpg_dvs_ros/davis_ros_driver/CATKIN_IGNORE rpg_dvs_ros/dvs_ros_driver/CATKIN_IGNORE \
          rpg_dvs_ros/dvxplorer_ros_driver/CATKIN_IGNORE 2>/dev/null; true

WORKDIR /catkin_ws
RUN apt-get update && (rosdep update --rosdistro melodic || true) \
 && rosdep install --from-paths src --ignore-src --rosdistro melodic -r -y \
 && rm -rf /var/lib/apt/lists/*
RUN /bin/bash -c "source /opt/ros/melodic/setup.bash && catkin build dvs_tracking"

RUN cd /catkin_ws/src/rpg_dvs_evo_open && git rev-parse HEAD > /catkin_ws/EVO_COMMIT.txt
RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc
WORKDIR /work
