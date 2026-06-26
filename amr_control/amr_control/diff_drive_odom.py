#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class DiffDriveOdometry(Node):
    """
    Differential Drive Odometry Node.
    """

    def __init__(self):

        super().__init__("diff_drive_odom")

        # -----------------------------------------------------
        # Robot Parameters

        self.declare_parameter("wheel_radius", 0.05)
        self.declare_parameter("wheel_separation", 0.30)

        self.wheel_radius = (
            self.get_parameter("wheel_radius").value
        )

        self.wheel_separation = (
            self.get_parameter("wheel_separation").value
        )

        # -----------------------------------------------------
        # Robot Pose
        # -----------------------------------------------------

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.prev_left = None
        self.prev_right = None

        # -----------------------------------------------------
        # ROS Interfaces
        # -----------------------------------------------------

        self.create_subscription(
            JointState,
            "/joint_states",
            self.joint_callback,
            10,
        )

        self.odom_pub = self.create_publisher(
            Odometry,
            "/odom",
            10,
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info(
            "Differential Drive Odometry Started"
        )

    # ---------------------------------------------------------
    # Joint State Callback
    # ---------------------------------------------------------

    def joint_callback(self, msg: JointState):

        try:
            left = msg.position[
                msg.name.index("left_wheel_joint")
            ]

            right = msg.position[
                msg.name.index("right_wheel_joint")
            ]

        except ValueError:
            return

        if self.prev_left is None:

            self.prev_left = left
            self.prev_right = right

            return

        # ---------------------------------------------
        # Wheel Displacements
        # ---------------------------------------------

        d_left = (
            left - self.prev_left
        ) * self.wheel_radius

        d_right = (
            right - self.prev_right
        ) * self.wheel_radius

        self.prev_left = left
        self.prev_right = right

        # ---------------------------------------------
        # Differential Drive Kinematics
        # ---------------------------------------------

        d_center = (
            d_left + d_right
        ) / 2.0

        d_theta = (
            d_right - d_left
        ) / self.wheel_separation

        self.theta += d_theta

        self.x += d_center * math.cos(self.theta)

        self.y += d_center * math.sin(self.theta)

        self.publish_odom(msg.header.stamp)

    # ---------------------------------------------------------
    # Publish Odometry
    # ---------------------------------------------------------

    def publish_odom(self, stamp):

        qz = math.sin(self.theta / 2.0)
        qw = math.cos(self.theta / 2.0)

        tf = TransformStamped()

        tf.header.stamp = stamp

        tf.header.frame_id = "odom"

        tf.child_frame_id = "base_footprint"

        tf.transform.translation.x = self.x
        tf.transform.translation.y = self.y
        tf.transform.translation.z = 0.0

        tf.transform.rotation.z = qz
        tf.transform.rotation.w = qw

        self.tf_broadcaster.sendTransform(tf)

        odom = Odometry()

        odom.header.stamp = stamp

        odom.header.frame_id = "odom"

        odom.child_frame_id = "base_footprint"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y

        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        self.odom_pub.publish(odom)


def main(args=None):

    rclpy.init(args=args)

    node = DiffDriveOdometry()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    finally:

        node.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":
    main()
