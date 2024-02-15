# ROS2 Humble installation on Ubuntu 23.10

  ```
  sudo apt install software-properties-common
  sudo add-apt-repository universe 
  ```
  ```
  sudo apt update && sudo apt install curl -y
  sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
  ```
  ```
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
  ```
  ```
  sudo apt update && sudo apt install -y \
  python3-flake8-docstrings \
  python3-pip \
  python3-pytest-cov \
  ```
  ```
  sudo apt install -y git colcon python3-rosdep2 vcstool wget python3-flake8-docstrings python3-pip python3-pytest-cov \
  python3-flake8-blind-except python3-flake8-builtins python3-flake8-class-newline python3-flake8-comprehensions \
  python3-flake8-deprecated python3-flake8-import-order python3-flake8-quotes python3-pytest-repeat python3-pytest-rerunfailures python3-vcstools
  ```
  ```
  mkdir -p ~/ros2_humble/src
  cd ~/ros2_humble
  vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos src
  ```
  ```
  sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
  ```
  ```
  sudo apt upgrade
  sudo rosdep init
  rosdep update
  rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers ignition-math6 ignition-cmake2 python3-catkin-pkg-modules python3-vcstool python3-rosdistro-modules"
  ```
  ```
  colcon build --symlink-install
  ```
  In case of failed build see [link](https://github.com/ros-tooling/libstatistics_collector/pull/165)
