from threading import Thread

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node

import random
import numpy as np
from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import JointState
import time
import pickle

from tf2_ros import Buffer, TransformListener
from scipy.spatial.transform import Rotation as R

from pymoveit2 import MoveIt2, MoveIt2State
from pymoveit2.robots import lbr as ur5


#定义机器人模型
# link_lengths = [0.1807, 0.6127, 0.5716, 0.1742, 0.1199, 0.1166] # UR10e链长
link_lengths = [0.1273, 0.6120, 0.5723, 0.1640, 0.1157, 0.0922] # UR10链长
# link_lengths = [0.0892, 0.4250, 0.3923, 0.1092, 0.0947, 0.0823] # UR5链长
Tbase = np.eye(4)
Tbase[0:3, 3] = [0, 0, 0]
Ttool = np.eye(4)
Ttool[0:3, 3] = [0.0, 0, 0]

def Rz(q):
    """生成绕 Z 轴旋转的变换矩阵"""
    cq = np.cos(q)
    sq = np.sin(q)
    return np.array([
        [cq, -sq, 0, 0],
        [sq, cq, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def Ry(q):
    """生成绕 Y 轴旋转的变换矩阵"""
    cq = np.cos(q)
    sq = np.sin(q)
    return np.array([
        [cq, 0, sq, 0],
        [0, 1, 0, 0],
        [-sq, 0, cq, 0],
        [0, 0, 0, 1]
    ])

def Rx(q):
    """生成绕 X 轴旋转的变换矩阵"""
    cq = np.cos(q)
    sq = np.sin(q)
    return np.array([
        [1, 0, 0, 0],
        [0, cq, -sq, 0],
        [0, sq, cq, 0],
        [0, 0, 0, 1]
    ])

def Tz(d):
    """生成沿 Z 轴平移的变换矩阵"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, d],
        [0, 0, 0, 1]
    ])

def Ty(d):
    """生成沿 Y 轴平移的变换矩阵"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, d],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def Tx(d):
    """生成沿 X 轴平移的变换矩阵"""
    return np.array([
        [1, 0, 0, d],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def FK(q):
    # Forward Kinematics calculation
    L = link_lengths
    H = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]), 
            np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), 
            np.dot(Rz(q[4]), np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))

    return H

def move_to_point(x, y, z, rx, ry, rz, w):
    
    rclpy.init()

    # Create node for this example
    node = Node("ex_pose_goal")

    # Declare parameters for position and orientation
    node.declare_parameter("position", [x, y, z])
    node.declare_parameter("quat_xyzw", [rx, ry, rz, w])
    node.declare_parameter("synchronous", True)
    # If non-positive, don't cancel. Only used if synchronous is False
    node.declare_parameter("cancel_after_secs", 0.0)
    # Planner ID
    node.declare_parameter("planner_id", "RRTConnectkConfigDefault")
    # Declare parameters for cartesian planning
    node.declare_parameter("cartesian", False)
    node.declare_parameter("cartesian_max_step", 0.25)
    node.declare_parameter("cartesian_fraction_threshold", 0.0)
    node.declare_parameter("cartesian_jump_threshold", 0.0)
    node.declare_parameter("cartesian_avoid_collisions", True)

    # Create callback group that allows execution of callbacks in parallel without restrictions
    callback_group = ReentrantCallbackGroup()

    # Create MoveIt 2 interface
    moveit2 = MoveIt2(
        node=node,
        joint_names=ur5.joint_names(),
        base_link_name=ur5.base_link_name(),
        end_effector_name=ur5.end_effector_name(),
        group_name=ur5.MOVE_GROUP_ARM,
        callback_group=callback_group,
    )
    moveit2.planner_id = (
        node.get_parameter("planner_id").get_parameter_value().string_value
    )

    # Spin the node in background thread(s) and wait a bit for initialization
    executor = rclpy.executors.MultiThreadedExecutor(2)
    executor.add_node(node)
    executor_thread = Thread(target=executor.spin, daemon=True, args=())
    executor_thread.start()
    node.create_rate(1.0).sleep()

    # Scale down velocity and acceleration of joints (percentage of maximum)
    moveit2.max_velocity = 0.5
    moveit2.max_acceleration = 0.5

    # Get parameters
    position = node.get_parameter("position").get_parameter_value().double_array_value
    quat_xyzw = node.get_parameter("quat_xyzw").get_parameter_value().double_array_value
    synchronous = node.get_parameter("synchronous").get_parameter_value().bool_value
    cancel_after_secs = (
        node.get_parameter("cancel_after_secs").get_parameter_value().double_value
    )
    cartesian = node.get_parameter("cartesian").get_parameter_value().bool_value
    cartesian_max_step = (
        node.get_parameter("cartesian_max_step").get_parameter_value().double_value
    )
    cartesian_fraction_threshold = (
        node.get_parameter("cartesian_fraction_threshold")
        .get_parameter_value()
        .double_value
    )
    cartesian_jump_threshold = (
        node.get_parameter("cartesian_jump_threshold")
        .get_parameter_value()
        .double_value
    )
    cartesian_avoid_collisions = (
        node.get_parameter("cartesian_avoid_collisions")
        .get_parameter_value()
        .bool_value
    )

    # Set parameters for cartesian planning
    moveit2.cartesian_avoid_collisions = cartesian_avoid_collisions
    moveit2.cartesian_jump_threshold = cartesian_jump_threshold

    # Move to pose
    node.get_logger().info(
        f"Moving to {{position: {list(position)}, quat_xyzw: {list(quat_xyzw)}}}"
    )
    moveit2.move_to_pose(
        position=position,
        quat_xyzw=quat_xyzw,
        cartesian=cartesian,
        cartesian_max_step=cartesian_max_step,
        cartesian_fraction_threshold=cartesian_fraction_threshold,
    )
    if synchronous:
        # Note: the same functionality can be achieved by setting
        # `synchronous:=false` and `cancel_after_secs` to a negative value.
        moveit2.wait_until_executed()
    else:
        # Wait for the request to get accepted (i.e., for execution to start)
        print("Current State: " + str(moveit2.query_state()))
        rate = node.create_rate(10)
        while moveit2.query_state() != MoveIt2State.EXECUTING:
            rate.sleep()

        # Get the future
        print("Current State: " + str(moveit2.query_state()))
        future = moveit2.get_execution_future()

        # Cancel the goal
        if cancel_after_secs > 0.0:
            # Sleep for the specified time
            sleep_time = node.create_rate(cancel_after_secs)
            sleep_time.sleep()
            # Cancel the goal
            print("Cancelling goal")
            moveit2.cancel_execution()

        # Wait until the future is done
        while not future.done():
            rate.sleep()

        # Print the result
        print("Result status: " + str(future.result().status))
        print("Result error code: " + str(future.result().result.error_code))

    rclpy.shutdown()
    executor_thread.join()

def random_unit_quaternion():
    """Generate a random unit quaternion."""
    u1 = random.uniform(0, 1)
    u2 = random.uniform(0, 2 * np.pi)
    u3 = random.uniform(0, 2 * np.pi)

    w = np.sqrt(1 - u1) * np.sin(u2)
    x = np.sqrt(1 - u1) * np.cos(u2)
    y = np.sqrt(u1) * np.sin(u3)
    z = np.sqrt(u1) * np.cos(u3)

    return (x, y, z, w)

def generate_random_pose(x_range, y_range, z_range):
    """Generate a random position and random orientation (quaternion)."""
    # Generate random position
    x = random.uniform(x_range[0], x_range[1])
    y = random.uniform(y_range[0], y_range[1])
    z = random.uniform(z_range[0], z_range[1])

    # Generate random quaternion orientation
    quaternion = random_unit_quaternion()

    return (x, y, z), quaternion

class getFTsensor(Node):
    def __init__(self):
        super().__init__("get_FT_sensor")
        global ft_data
        self.sensor_data_sign = False
        ft_data = np.zeros(6)

        self.ft_sensor_subscription = self.create_subscription(
            WrenchStamped,
            '/ft_wrench',
            self.ft_sensor_callback,
            10)
        self.ft_sensor_subscription
        self.get_logger().info('F/T sensor subscriber created')

        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('F/T sensor data: ' + str(ft_data))

    def ft_sensor_callback(self, msg):
        global ft_data

        # 从 WrenchStamped 消息中提取力
        force = msg.wrench.force
        torque = msg.wrench.torque

        ft_data = np.array([-force.x, -force.z, force.y, torque.x, torque.y, torque.z])

        self.sensor_data_sign = True

def get_FT_sensor_data(args=None):
    init_time = time.time()
    rclpy.init(args=args)
    get_FT_sensor = getFTsensor()
    
    while not get_FT_sensor.sensor_data_sign and time.time() - init_time < 3.0:
        rclpy.spin_once(get_FT_sensor)
        
    if get_FT_sensor.sensor_data_sign:
        print("Successfully received sensor data.")
    else:
        print("Timeout: No sensor data received within 5 seconds.")

    get_FT_sensor.destroy_node()
    rclpy.shutdown()

class GetRotationMatrix(Node):
    def __init__(self):
        global R_matrix

        super().__init__('get_rotation_matrix')
        R_matrix = np.eye(3)
        self.RM_data_sign = False

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.qpos_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('joint state subscriber created')

        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('waiting for rotation matrix')

    def qpos_callback(self, msg):
        global R_matrix
        qpos = np.zeros(6)
        qpos[1:] = msg.position[:5]
        qpos[0] = msg.position[5]
        q_current = np.array(qpos) # 更新末端状态
        q_current[1] += np.pi/2
        q_current[3] += np.pi/2 
        H = FK(q_current[:6])
        print("H",H)
        R_matrix = H[:3, :3]  # Rotation matrix part
        self.RM_data_sign = True

def get_rotation_matrix_data(args=None):
    global R_matrix

    init_time = time.time()
    rclpy.init(args=args)
    get_RM = GetRotationMatrix()

    while not get_RM.RM_data_sign and time.time() - init_time < 3.0:
        rclpy.spin_once(get_RM)
        
    if get_RM.RM_data_sign:
        print("Successfully received sensor data.")
    else:
        print("Timeout: No sensor data received within 3 seconds.")

    if R_matrix is not None:
        print('Rotation Matrix (R):')
        print(R_matrix)

    get_RM.destroy_node()
    rclpy.shutdown()

def eef_weight(A, b):
    # 计算最小二乘解  Ax = b
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

    print("最小二乘解:", x)
    print("残差:", residuals)
    return x

def main():
    rclpy.init()

    # Create node for this example
    node = Node("ex_collision_primitive")

    # Declare parameter for joint positions
    node.declare_parameter(
        "shape",
        "box",
    )
    node.declare_parameter(
        "action",
        "add",
    )
    node.declare_parameter("position", [0.0, 0.0, -0.051])
    node.declare_parameter("quat_xyzw", [0.0, 0.0, -0.7071, 0.7071])
    node.declare_parameter("dimensions", [5.0, 5.0, 0.1])

    # Create callback group that allows execution of callbacks in parallel without restrictions
    callback_group = ReentrantCallbackGroup()

    # Create MoveIt 2 interface
    moveit2 = MoveIt2(
        node=node,
        joint_names=ur5.joint_names(),
        base_link_name=ur5.base_link_name(),
        end_effector_name=ur5.end_effector_name(),
        group_name=ur5.MOVE_GROUP_ARM,
        callback_group=callback_group,
    )

    # Spin the node in background thread(s) and wait a bit for initialization
    executor = rclpy.executors.MultiThreadedExecutor(2)
    executor.add_node(node)
    executor_thread = Thread(target=executor.spin, daemon=True, args=())
    executor_thread.start()
    node.create_rate(1.0).sleep()

    # Get parameters
    shape = node.get_parameter("shape").get_parameter_value().string_value
    action = node.get_parameter("action").get_parameter_value().string_value
    position = node.get_parameter("position").get_parameter_value().double_array_value
    quat_xyzw = node.get_parameter("quat_xyzw").get_parameter_value().double_array_value
    dimensions = (
        node.get_parameter("dimensions").get_parameter_value().double_array_value
    )

    # Use the name of the primitive shape as the ID
    object_id = shape

    if action == "add":
        # Add collision primitive
        node.get_logger().info(
            f"Adding collision primitive of type '{shape}' "
            f"{{position: {list(position)}, quat_xyzw: {list(quat_xyzw)}, dimensions: {list(dimensions)}}}"
        )
        if shape == "box":
            moveit2.add_collision_box(
                id=object_id, position=position, quat_xyzw=quat_xyzw, size=dimensions
            )
        elif shape == "sphere":
            moveit2.add_collision_sphere(
                id=object_id, position=position, radius=dimensions[0]
            )
        elif shape == "cylinder":
            moveit2.add_collision_cylinder(
                id=object_id,
                position=position,
                quat_xyzw=quat_xyzw,
                height=dimensions[0],
                radius=dimensions[1],
            )
        elif shape == "cone":
            moveit2.add_collision_cone(
                id=object_id,
                position=position,
                quat_xyzw=quat_xyzw,
                height=dimensions[0],
                radius=dimensions[1],
            )
        else:
            raise ValueError(f"Unknown shape '{shape}'")
    elif action == "remove":
        # Remove collision primitive
        node.get_logger().info(f"Removing collision primitive with ID '{object_id}'")
        moveit2.remove_collision_object(id=object_id)
    elif action == "move":
        # Move collision primitive
        node.get_logger().info(
            f"Moving collision primitive with ID '{object_id}' to "
            f"{{position: {list(position)}, quat_xyzw: {list(quat_xyzw)}}}"
        )
        moveit2.move_collision(id=object_id, position=position, quat_xyzw=quat_xyzw)
    else:
        raise ValueError(
            f"Unknown action '{action}'. Valid values are 'add', 'remove', 'move'"
        )

    rclpy.shutdown()
    executor_thread.join()

    x_range = [0.4, 0.5]  # Define the range for x, y, z in meters
    y_range = [-0.1, 0.1]
    z_range = [0.4, 0.5]

    force_vectors = []  # 存储力数据
    rotation_matrices = []  # 存储旋转矩阵的逆矩阵

    for _ in range(6):
        position, quaternion = generate_random_pose(x_range, y_range, z_range)
        # Unpack the generated position and quaternion
        x, y, z = position
        qx, qy, qz, qw = quaternion
        # Call move_to_point to move the robot
        # move_to_point(x, y, z, qx, qy, qz, qw)

        input("按回车键继续...")

        get_FT_sensor_data()
        force_vectors.append([ft_data[0], ft_data[1], ft_data[2]])
        
        get_rotation_matrix_data()
        R_inv = np.linalg.inv(R_matrix)
        I = np.eye(3)
        combined_matrix = np.hstack([R_inv, I])
        rotation_matrices.append(combined_matrix)
    
    # 将 forces 列表转换为 NumPy 数组并展平成一个向量
    force_array = np.array(force_vectors)
    b = force_array.flatten()
    b = force_array.flatten().reshape(-1, 1)  # 将扁平化后的数组转换为列向量
    # 纵向拼接所有行
    A = np.vstack(rotation_matrices)

    print(A)
    print(b)

    mass_list = eef_weight(A,b)

    mass_square_sum = mass_list[0]**2 + mass_list[1]**2 + mass_list[2]**2
    eef_mass = [np.sqrt(mass_square_sum)] # 末端工具参数（重量）
    print(eef_mass)

    data = {'mass': mass_list}
    file_path = '/home/zzy/ur_real/src/gravity_compensation/gravity_compensation/data.pkl'

    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

    exit(0)

if __name__ == '__main__':
    main()
