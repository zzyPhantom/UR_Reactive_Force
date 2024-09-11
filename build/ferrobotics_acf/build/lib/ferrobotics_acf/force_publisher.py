
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
import socket
import sys

bytes_args = ()
if sys.version_info.major >= 3:
    bytes_args = ("ASCII",)


class Force_Publisher(Node):
    def __init__(self):
        super().__init__('force_publisher')

        self.get_params()
        self.ros_setup()

    def get_params(self):
        self.declare_parameter("force", 10.0)
        
        # Retrieve the parameter as a double (float) value
        self.force = self.get_parameter("force").get_parameter_value().double_value

    def ros_setup(self):

        self.force_pub = self.create_publisher(Float32, "/ACF/force", 10)
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        msg = Float32()
        msg.data = float(self.force)
        self.force_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    force_publisher = Force_Publisher()
    rclpy.spin(force_publisher)

    force_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
