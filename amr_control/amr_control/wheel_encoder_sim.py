#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState


class WheelEncoderSimulator(Node):
    """
    Simulates left and right wheel encoder positions from
    commanded robot velocities.
    """

    def __init__(self) -> None:

        super().__init__("wheel_encoder_sim")

        # -----------------------------------------------------
        # Robot Parameters

        self.declare_parameter("wheel_radius", 0.05)
        self.declare_parameter("wheel_separation", 0.30)
        self.declare_parameter("publish_rate", 50.0)

        self.wheel_radius = (
            self.get_parameter("wheel_radius")
            .value
        )

        self.wheel_separation = (
            self.get_parameter("wheel_separation")
            .value
        )

        publish_rate = (
            self.get_parameter("publish_rate")
            .value
        )

        # -----------------------------------------------------
        # Robot State
        # -----------------------------------------------------

        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        self.left_position = 0.0
        self.right_position = 0.0

        self.last_time = self.get_clock().now()

        # -----------------------------------------------------
        # ROS Interfaces
        # -----------------------------------------------------

        self.create_subscription(
            Twist,
            "/cmd_vel",
            self.cmd_vel_callback,
            10,
        )

        self.publisher = self.create_publisher(
            JointState,
            "/joint_states",
            10,
        )

        self.create_timer(
            1.0 / publish_rate,
            self.update,
        )

        self.get_logger().info(
            "Wheel Encoder Simulator Started"
        )

    # ---------------------------------------------------------
    # Callbacks
    # ---------------------------------------------------------

    def cmd_vel_callback(self, msg: Twist) -> None:

        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    # ---------------------------------------------------------
    # Main Update Loop
    # ---------------------------------------------------------

    def update(self) -> None:

        now = self.get_clock().now()

        dt = (
            now - self.last_time
        ).nanoseconds / 1e9

        self.last_time = now

        left_speed = (
            self.linear_velocity
            - (
                self.angular_velocity
                * self.wheel_separation
                / 2.0
            )
        ) / self.wheel_radius

        right_speed = (
            self.linear_velocity
            + (
                self.angular_velocity
                * self.wheel_separation
                / 2.0
            )
        ) / self.wheel_radius

        self.left_position += left_speed * dt
        self.right_position += right_speed * dt

        msg = JointState()

        msg.header.stamp = now.to_msg()

        msg.name = [
            "left_wheel_joint",
            "right_wheel_joint",
        ]

        msg.position = [
            self.left_position,
            self.right_position,
        ]

        msg.velocity = [
            left_speed,
            right_speed,
        ]

        self.publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = WheelEncoderSimulator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":
    main()
