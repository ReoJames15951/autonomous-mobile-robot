#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist


class ImuSimulator(Node):
    """
    Simulated IMU publisher.

    The node estimates robot heading from commanded
    angular velocity and publishes orientation,
    angular velocity and linear acceleration.
    """

    def __init__(self):

        super().__init__("imu_sim")

        self.heading = 0.0

        self.linear_velocity = 0.0
        self.angular_velocity = 0.0

        self.last_linear_velocity = 0.0

        self.last_time = self.get_clock().now()

        self.publisher = self.create_publisher(
            Imu,
            "/imu/data",
            10,
        )

        self.create_subscription(
            Twist,
            "/cmd_vel",
            self.cmd_vel_callback,
            10,
        )

        self.create_timer(
            0.02,
            self.publish_imu,
        )

        self.get_logger().info(
            "IMU Simulator Started"
        )

    def cmd_vel_callback(self, msg):

        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    def publish_imu(self):

        now = self.get_clock().now()

        dt = (
            now - self.last_time
        ).nanoseconds / 1e9

        if dt <= 0.0:
            return

        self.last_time = now

        self.heading += self.angular_velocity * dt

        linear_acceleration = (
            self.linear_velocity -
            self.last_linear_velocity
        ) / dt

        self.last_linear_velocity = self.linear_velocity

        imu = Imu()

        imu.header.stamp = now.to_msg()

        imu.header.frame_id = "base_link"

        imu.orientation.x = 0.0
        imu.orientation.y = 0.0
        imu.orientation.z = math.sin(
            self.heading / 2.0
        )
        imu.orientation.w = math.cos(
            self.heading / 2.0
        )

        imu.angular_velocity.x = 0.0
        imu.angular_velocity.y = 0.0
        imu.angular_velocity.z = self.angular_velocity

        imu.linear_acceleration.x = linear_acceleration
        imu.linear_acceleration.y = 0.0
        imu.linear_acceleration.z = 0.0

        self.publisher.publish(imu)


def main(args=None):

    rclpy.init(args=args)

    node = ImuSimulator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":
    main()
