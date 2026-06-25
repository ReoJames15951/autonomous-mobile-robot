#!/usr/bin/env python3

"""
Display Launch File

This launch file starts:

• Robot State Publisher
• Joint State Publisher GUI
• RViz2

Author : Felix
Project: Autonomous Mobile Robot (AMR)
"""

import os

import xacro

from launch import LaunchDescription

from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_path = get_package_share_directory("amr_description")

    xacro_file = os.path.join(
        package_path,
        "urdf",
        "amr.urdf.xacro"
    )

    robot_description = xacro.process_file(
        xacro_file
    ).toxml()

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[
            {
                "robot_description": robot_description
            }
        ]
    )

    joint_state_publisher = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        output="screen"
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        output="screen"
    )

    return LaunchDescription([

        robot_state_publisher,

        joint_state_publisher,

        rviz

    ])
