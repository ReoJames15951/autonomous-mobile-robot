#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LidarSimulator(Node):
    """
    Simulates a 360° planar LiDAR in a square room.
    """

    def __init__(self):

        super().__init__("lidar_sim")

        self.publisher = self.create_publisher(
            LaserScan,
            "/scan",
            10,
        )

        self.create_timer(
            0.10,
            self.publish_scan,
        )

        self.get_logger().info(
            "LiDAR Simulator Started"
        )

    def publish_scan(self):

        scan = LaserScan()

        scan.header.stamp = (
            self.get_clock().now().to_msg()
        )

        scan.header.frame_id = "lidar_link"

        scan.angle_min = -math.pi
        scan.angle_max = math.pi

        scan.angle_increment = math.radians(1.0)

        scan.range_min = 0.12
        scan.range_max = 10.0

        count = int(
            (
                scan.angle_max
                - scan.angle_min
            )
            / scan.angle_increment
        )

        room_x = 2.0
        room_y = 2.0

        ranges = []

        for i in range(count):

            angle = (
                scan.angle_min
                + i * scan.angle_increment
            )

            dx = math.cos(angle)
            dy = math.sin(angle)

            candidates = []

            if abs(dx) > 1e-6:

                candidates.append(room_x / abs(dx))

            if abs(dy) > 1e-6:

                candidates.append(room_y / abs(dy))

            distance = min(candidates)

            distance = min(
                distance,
                scan.range_max,
            )

            ranges.append(distance)

        scan.ranges = ranges

        self.publisher.publish(scan)


def main(args=None):

    rclpy.init(args=args)

    node = LidarSimulator()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":

    main()
