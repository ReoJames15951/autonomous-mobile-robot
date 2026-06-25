# 🤖 Autonomous Mobile Robot (AMR) using ROS2

[![ROS2](https://img.shields.io/badge/ROS2-Kilted-blue.svg)]
[![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04-E95420.svg)]
[![Language](https://img.shields.io/badge/Python-3.12-yellow.svg)]
[![License](https://img.shields.io/badge/License-MIT-green.svg)]

---

## Overview

This project is a **ROS2-based Autonomous Mobile Robot (AMR)** developed as part of my robotics engineering portfolio.

The objective of this project is to build a warehouse-style differential drive robot capable of:

- Autonomous navigation
- Sensor integration
- Localization
- Mapping
- Path planning
- Real-world deployment

The software architecture follows industry-standard ROS2 practices and is designed to be easily transferable to real hardware such as Raspberry Pi or NVIDIA Jetson platforms.

---

# Project Features

## Robot Description

- Differential Drive Robot
- Modular Xacro Robot Description
- URDF Robot Model
- TF Tree
- RViz Visualization

---

## Motion Control

- Differential Drive Kinematics
- Wheel Encoder Simulation
- Joint State Publisher
- Encoder-based Odometry
- Velocity Command Interface (`/cmd_vel`)

---

## Localization

- Odometry Publisher
- IMU Simulation
- Extended Kalman Filter (EKF)
- Robot Localization Package
- Filtered Odometry

---

## Mapping

- LiDAR Simulation
- LaserScan Publisher
- SLAM Toolbox Integration
- Occupancy Grid Mapping

---

## Visualization

- RViz2
- Robot Model
- TF Frames
- Laser Scan Visualization
- Occupancy Map

---

# Software Stack

| Component | Version |
|------------|----------|
| Ubuntu | 24.04 |
| ROS2 | Kilted |
| Python | 3.12 |
| RViz2 | Latest |
| SLAM Toolbox | Latest |
| Robot Localization | Latest |

---

# Robot Architecture

```
                   +-------------------+
                   |    /cmd_vel       |
                   +---------+---------+
                             |
                             v
                 wheel_encoder_sim.py
                             |
                             v
                    /joint_states
                             |
                             v
                  diff_drive_odom.py
                             |
                             v
                           /odom
                             |
               +-------------+-------------+
               |                           |
               |                           |
               v                           v
          imu_sim.py                robot_state_publisher
               |                           |
               +-------------+-------------+
                             |
                             v
                 robot_localization (EKF)
                             |
                             v
                 /odometry/filtered
                             |
                             |
                             v
                     lidar_sim.py
                             |
                             v
                           /scan
                             |
                             v
                     SLAM Toolbox
                             |
                             v
                           /map
```

---

# TF Tree

```
map
│
└── odom
      │
      └── base_footprint
              │
              └── base_link
                    │
                    ├── left_wheel
                    ├── right_wheel
                    └── lidar_link
```

---

# Package Structure

```
amr_ws/
│
├── amr_description
│   ├── URDF/Xacro
│   ├── Robot Description
│   └── RViz Launch Files
│
├── amr_control
│   ├── Differential Drive Controller
│   ├── Wheel Encoder Simulator
│   ├── IMU Simulator
│   ├── LiDAR Simulator
│   ├── Encoder Odometry
│   └── EKF Configuration
│
└── amr_bringup
    ├── Robot Launch
    ├── SLAM Launch
    └── System Bringup
```

---

# ROS2 Topics

| Topic | Description |
|---------|-------------|
| `/cmd_vel` | Velocity Commands |
| `/joint_states` | Wheel Encoder States |
| `/odom` | Encoder Odometry |
| `/imu/data` | Simulated IMU |
| `/odometry/filtered` | EKF Output |
| `/scan` | LiDAR Scan |
| `/map` | Occupancy Grid |

---

# Implemented Algorithms

- Differential Drive Kinematics
- Wheel Encoder Odometry
- Extended Kalman Filter (EKF)
- Laser Scan Simulation
- Occupancy Grid Mapping
- ROS2 TF Transform Tree

---

# Launch

## Build

```bash
cd ~/amr_ws
colcon build --symlink-install
source install/setup.bash
```

---

## Launch Robot

```bash
ros2 launch amr_bringup amr.launch.py
```

---

## Launch SLAM

```bash
ros2 launch amr_bringup slam.launch.py
```

---

## Teleoperation

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

# Screenshots

## Robot Model

to be added

---

## TF Tree

to be added

---

## Laser Scan

to be added

---

## Occupancy Grid
to be added

---

# Future Improvements

- Gazebo / Ignition Simulation
- Nav2 Navigation Stack
- Dynamic Obstacle Avoidance
- AMCL Localization
- Autonomous Docking
- Camera Integration
- Intel RealSense Support
- RPLidar Integration
- ESP32 Motor Controller
- Raspberry Pi Deployment
- NVIDIA Jetson Deployment
- Multi-Robot Communication
- Cloud Dashboard

---

# Hardware Compatibility

Designed to run on:

- Raspberry Pi 5
- NVIDIA Jetson Orin Nano
- ESP32
- RPLidar A1
- Intel RealSense D435i
- Differential Drive Mobile Robot

---

# Learning Outcomes

This project demonstrates practical experience with:

- ROS2
- Robot Description (URDF/Xacro)
- Differential Drive Robots
- Wheel Encoder Odometry
- Sensor Simulation
- Robot Localization
- TF Transform Tree
- SLAM
- RViz
- Mobile Robotics

---

# Repository Status

Current Progress

- ✅ Robot Description
- ✅ Differential Drive
- ✅ Encoder Simulation
- ✅ Odometry
- ✅ EKF Localization
- ✅ LiDAR Simulation
- ✅ SLAM Toolbox
- 🔄 Navigation2 (In Progress)
- 🔄 Gazebo Integration (Planned)
- 🔄 Real Hardware Deployment (Planned)

---

# Author
Reo James

Robotics | ROS2 | Autonomous Systems | Computer Vision | Embedded Systems

---

## License

This project is licensed under the MIT License.
