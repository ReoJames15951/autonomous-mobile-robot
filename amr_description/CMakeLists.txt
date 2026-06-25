cmake_minimum_required(VERSION 3.8)
project(amr_description)

###########################################################
# Compiler Settings
###########################################################

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

###########################################################
# Dependencies
###########################################################

find_package(ament_cmake REQUIRED)

###########################################################
# Install Files
###########################################################

install(
  DIRECTORY
    launch
    urdf
  DESTINATION
    share/${PROJECT_NAME}
)

###########################################################
# Export Package
###########################################################

ament_package()
