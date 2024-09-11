import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray


class PublisherForwardVelocity(Node):
    def __init__(self):
        super().__init__("publisher_forward_velocity_controller")
        # Declare all parameters
        self.declare_parameter("controller_name", "forward_velocity_controller")

        # Read parameters
        controller_name = self.get_parameter("controller_name").value

        publish_topic = "/" + controller_name + "/" + "commands"

        self.get_logger().info(
            f'Publishing velocity goals on topic "{publish_topic}"\n'
        )

        self.publisher_ = self.create_publisher(Float64MultiArray, publish_topic, 1)

        self.subscription = self.create_subscription(
            Float64MultiArray,
            'control_velocity',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        # self.get_logger().info(f'Publishing: "{msg.data}"')
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    publisher_forward_velocity = PublisherForwardVelocity()

    rclpy.spin(publisher_forward_velocity)
    publisher_forward_velocity.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
