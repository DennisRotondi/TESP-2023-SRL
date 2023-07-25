cmake_minimum_required(VERSION 3.0.2)
project(tesp_server)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
   CATKIN_DEPENDS rospy std_msgs
   CATKIN_DEPENDS message_runtime
)

catkin_install_python(PROGRAMS src/server.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)
