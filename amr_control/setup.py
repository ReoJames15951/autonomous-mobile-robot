from setuptools import find_packages, setup
from glob import glob
import os

package_name = "amr_control"

setup(
    name=package_name,
    version="1.0.0",

    packages=find_packages(exclude=["test"]),

    data_files=[

        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),

        (
            os.path.join("share", package_name),
            ["package.xml"],
        ),

        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.py"),
        ),

        (
            os.path.join("share", package_name, "config"),
            glob("config/*.yaml"),
        ),
    ],

    install_requires=[
        "setuptools",
    ],

    zip_safe=True,

    maintainer="Felix",

    maintainer_email="reojames3378@gmail.com",

    description=(
        "Control package for the Autonomous Mobile Robot "
        "(AMR) using ROS2."
    ),

    license="MIT",

    tests_require=["pytest"],

    entry_points={

        "console_scripts": [

            "diff_drive_odom = amr_control.diff_drive_odom:main",

            "wheel_encoder_sim = amr_control.wheel_encoder_sim:main",

            "imu_sim = amr_control.imu_sim:main",

            "lidar_sim = amr_control.lidar_sim:main",

        ],

    },
)
