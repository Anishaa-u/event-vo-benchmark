# ESVIO (Chen et al. 2023, arclab-hku/ESVIO) on ROS Noetic (Ubuntu 20.04), as its README specifies.
# Build:  docker build -t esvio .
FROM osrf/ros:noetic-desktop

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
      python3-catkin-tools python3-psutil python3-numpy \
      git unzip autoconf automake libtool \
      libgoogle-glog-dev libgflags-dev libeigen3-dev libsuitesparse-dev libatlas-base-dev \
      libyaml-cpp-dev libpcl-dev \
      ros-noetic-cv-bridge ros-noetic-image-transport ros-noetic-tf ros-noetic-pcl-ros \
      ros-noetic-image-geometry ros-noetic-camera-info-manager \
    && rm -rf /var/lib/apt/lists/*

ARG ESVIO_COMMIT=b9e5aee7db647b70cee6f1128e2f49f47107ca84
RUN mkdir -p /catkin_ws/src
WORKDIR /catkin_ws
RUN catkin config --init --mkdirs --extend /opt/ros/noetic --merge-devel \
      --cmake-args -DCMAKE_BUILD_TYPE=Release
WORKDIR /catkin_ws/src
RUN git clone https://github.com/arclab-hku/ESVIO.git \
 && cd ESVIO && git checkout $ESVIO_COMMIT

# Live-camera drivers need libcaer / dv libraries and are not used for bag playback
RUN cd ESVIO/dependences/rpg_dvs_ros \
 && for d in davis_ros_driver dvs_ros_driver dvxplorer_ros_driver dvs_calibration dvs_calibration_gui; do \
      [ -d $d ] && touch $d/CATKIN_IGNORE; done; true

WORKDIR /catkin_ws
RUN apt-get update && (rosdep update --rosdistro noetic || true) \
 && rosdep install --from-paths src --ignore-src --rosdistro noetic -r -y \
 && rm -rf /var/lib/apt/lists/*
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    catkin build esvio_estimator feature_tracker pose_graph"

RUN cd /catkin_ws/src/ESVIO && git rev-parse HEAD > /catkin_ws/ESVIO_COMMIT.txt
RUN echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc
WORKDIR /work
