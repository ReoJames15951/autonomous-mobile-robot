#!/usr/bin/env python3

"""
amr.launch.py
Main bringup launch file for the Autonomous Mobile Robot.

Starts:
• Robot Description
• Robot State Publisher
• Wheel Encoder Simulator
• Differential Drive Odometry
• IMU Simulator
• LiDAR Simulator
• Extended Kalman Filter
• RViz2

Author:
    Felix
"""

import os

import xacro

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    ############################################################
    # Launch Arguments
    ############################################################

    use_rviz = LaunchConfiguration("use_rviz")

    declare_rviz = DeclareLaunchArgument(
        "use_rviz",
        default_value="true",
        description="Launch RViz",
    )

    ############################################################
    # Robot Description
    ############################################################

    description_path = get_package_share_directory(
        "amr_description"
    )

    xacro_file = os.path.join(
        description_path,
        "urdf",
        "amr.urdf.xacro",
    )

    robot_description = xacro.process_file(
        xacro_file
    ).toxml()

    ############################################################
    # EKF Configuration
    ############################################################

    control_path = get_package_share_directory(
        "amr_control"
    )

    ekf_config = os.path.join(
        control_path,
        "config",
        "ekf.yaml",
    )

    ############################################################
    # Nodes
    ############################################################

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description
            }
        ],
    )

    wheel_encoder = Node(
        package="amr_control",
        executable="wheel_encoder_sim",
        output="screen",
    )

    diff_drive = Node(
        package="amr_control",
        executable="diff_drive_odom",
        output="screen",
    )

    imu = Node(
        package="amr_control",
        executable="imu_sim",
        output="screen",
    )

    lidar = Node(
        package="amr_control",
        executable="lidar_sim",
        output="screen",
    )

    ekf = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        output="screen",
        parameters=[ekf_config],
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="screen",
        condition=IfCondition(use_rviz),
    )

    ############################################################
    # Launch Description
    ############################################################

    return LaunchDescription([

        declare_rviz,

        robot_state_publisher,

        wheel_encoder,

        diff_drive,

        imu,

        lidar,

        ekf,

        rviz,

    ])
