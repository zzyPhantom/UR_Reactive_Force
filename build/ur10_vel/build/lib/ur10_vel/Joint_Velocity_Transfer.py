import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float64MultiArray

class StateValidity(Node):
    def __init__(self):
        super().__init__('keyboard_checker_node')
        self.stop = False
        self.collision_stop = True
        self.run = False
        self.last_velocity = Float64MultiArray()

        self.stop_subscription = self.create_subscription(
            Float64MultiArray,
            'control_velocity_unswiched',
            self.publisher_callback,
            10)
        self.stop_subscription  

        self.collision_stop_subscription = self.create_subscription(
            Bool,
            '/collision_stop_sign',
            self.collision_stop_callback,
            10)
        self.collision_stop_subscription  
        self.stop_subscription = self.create_subscription(
            Bool,
            '/stop_sign',
            self.stop_callback,
            10)
        self.stop_subscription
        self.stop_subscription = self.create_subscription(
            Bool,
            '/run_sign',
            self.run_callback,
            10)
        self.stop_subscription  

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.publisher_ = self.create_publisher(Float64MultiArray, "control_velocity", 1)

    def stop_callback(self, msg):
        self.stop = bool(msg.data)

    def collision_stop_callback(self, msg):
        self.collision_stop = bool(msg.data)

    def run_callback(self, msg):
        self.run = bool(msg.data)

    def publisher_callback(self, msg):
        if self.collision_stop == True:
            msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 碰撞停止
            self.get_logger().info("stop move: collision")

        if self.stop == True:
            msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 停止
            self.get_logger().info("stop move: keyboard")

        self.last_velocity = msg
        self.publisher_.publish(msg)

    def timer_callback(self):
        if self.run == False:
            self.last_velocity.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 停止
            self.get_logger().info("stop move: IK not running")

        self.publisher_.publish(self.last_velocity)
        self.run = False
        

def main(args=None):
    rclpy.init(args=args)
    keyboard_checker_node = StateValidity()

    while rclpy.ok():
        rclpy.spin_once(keyboard_checker_node)

    keyboard_checker_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()