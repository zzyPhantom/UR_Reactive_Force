import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float64MultiArray
import threading


class StateValidity(Node):
    def __init__(self):
        super().__init__('keyboard_checker_node')

        # 发布停止信号
        self.publisher = self.create_publisher(Bool, 'stop_sign', 1)
        self.stop_sign = False

        threading.Thread(target=self.wait_for_input, daemon=True).start()

    def wait_for_input(self):
        while True:
            key = input("Press 'q' to toggle the value: ")
            if key == 'q':
                self.stop_sign = not self.stop_sign
                self.get_logger().info(f"Variable value is now {self.stop_sign}")
                self.publisher.publish(Bool(data=self.stop_sign))


def main(args=None):
    rclpy.init(args=args)
    keyboard_checker_node = StateValidity()

    while rclpy.ok():
        rclpy.spin_once(keyboard_checker_node)

    keyboard_checker_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()