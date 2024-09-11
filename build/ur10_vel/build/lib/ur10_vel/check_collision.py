import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetStateValidity
from sensor_msgs.msg import JointState
from rclpy.callback_groups import ReentrantCallbackGroup
from std_msgs.msg import Bool, Float64MultiArray
import numpy as np


class StateValidity(Node):
    def __init__(self):
        super().__init__('collision_checker_node')

        # 订阅关节状态
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.jointStatesCB,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('joint state subscriber created')

        # 订阅关节速度
        self.velsubscription = self.create_subscription(
            Float64MultiArray,
            '/control_velocity',
            self.jointvelCB,
            10)
        self.velsubscription  # prevent unused variable warning
        self.get_logger().info('joint vel subscriber created')

        # 发布停止信号
        self.publisher = self.create_publisher(Bool, 'collision_stop_sign', 1)
        self.collision = True

        self.cb_group = ReentrantCallbackGroup()
        self.client = self.create_client(GetStateValidity, 'check_state_validity', callback_group=self.cb_group)
        
        # 准备与MoveIt接口的消息
        self.request = GetStateValidity.Request()
        self.request.robot_state.joint_state.name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        self.request.robot_state.joint_state.position = [0.0, -1.5, 0.0, -1.5, 0.0, 0.0]
        self.request.group_name = 'ur_manipulator'
        self.joint_vel = np.zeros(6)

        # 等待服务可用
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.get_logger().info('service is available')

        # 定时器用于检查状态
        self.timer = self.create_timer(0.01, self.call_service, callback_group=self.cb_group)

    async def call_service(self):
        try:
            future = self.client.call_async(self.request)
            result = await future

            if result.valid:
                # self.get_logger().info('Robot not in collision, all ok!')
                self.collision = False
            else:
                # self.get_logger().warn('Robot in collision!')
                self.collision = True

        finally:
            i = 1

    def jointStatesCB(self, msg):
        # 更新机器人状态
        joint_del_position = [x * 0.1 for x in self.joint_vel]  # 保证0.5秒后不会碰撞
        # print("del_position",joint_del_position)
        self.request.robot_state.joint_state.position = [msg.position[5]+joint_del_position[0], msg.position[0]+joint_del_position[1], msg.position[1]+joint_del_position[2], msg.position[2]+joint_del_position[3], msg.position[3]+joint_del_position[4], msg.position[4]+joint_del_position[5]]
        self.publisher.publish(Bool(data=self.collision))

    def jointvelCB(self, msg):
        # 更新机器人速度
        self.joint_vel = msg.data

def main(args=None):
    rclpy.init(args=args)
    collision_checker_node = StateValidity()

    while rclpy.ok():
        rclpy.spin_once(collision_checker_node)

    collision_checker_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()