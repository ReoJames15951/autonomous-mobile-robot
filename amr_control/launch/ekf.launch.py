#!/usr/bin/env python3
"""
ekf.launch.py

Launch file for the Extended Kalman Filter (EKF).

This launch file starts the robot_localization EKF node
using the configuration defined in config/ekf.yaml.
"""

import os

from launch import LaunchDescription

from launch_ros.actions import Node

from ament_index_python.packages import (
    get_package_share_directory,
)


def generate_launch_description():

    package_path = get_package_share_directory(
        "amr_control"
    )

    ekf_config = os.path.join(
        package_path,
        "config",
        "ekf.yaml",
    )

    ekf_node = Node(

        package="robot_localization",

        executable="ekf_node",

        name="ekf_filter_node",

        output="screen",

        parameters=[
            ekf_config,
        ],
    )

    return LaunchDescription([

        ekf_node,

    ])
