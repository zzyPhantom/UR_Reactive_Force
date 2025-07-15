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

# P_obj = np.array([
#     [0.0, 0.06, 0.013],
#     [0.0, 0.0, 0.0],
#     [0.0, -0.06, 0.013]
# ]) # 电池实际坐标

# P_obj = np.array([
#     [0.0, 0.0, 0.0],
#     [0.12, 0.0, 0.0],
#     [0.0, 0.35, 0.0],
#     [0.12, 0.35, 0.0],
#     # [0.0, 0.35, 0.0]
# ]) # 电池组坐标

P_obj = np.array([
    [0.0, 0.0, 0.0],

]) # 测试坐标

pos_num = P_obj.shape[0]

#定义机器人模型
# ur5DH参数
d_vals =     [0.089159, 0,       0,        0.10915,  0.09465,  0.0823]
a_vals =     [0,       -0.425,  -0.39225,  0,        0,        0]
alpha_vals = [np.pi/2,  0,       0,        np.pi/2, -np.pi/2,  0]  
Tbase = np.eye(4)
Tbase[0:3, 3] = [0, 0, 0]
Ttool = np.eye(4)
Ttool[0:3, 3] = [0.0, -0.09, 0.2]

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

def Tx(d):
    """生成沿 X 轴平移的变换矩阵"""
    return np.array([
        [1, 0, 0, d],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

# def vec(matrix):

#     return matrix.flatten(order='F')

def compute_all_transforms(q):
    # q[1] -= np.pi/2
    # q[3] -= np.pi/2

    T_list = []
    T = Tbase
    T_list.append(T)  # T0

    for i in range(6):
        T = T @ Rz(q[i]) @ Tz(d_vals[i]) @ Rx(alpha_vals[i]) @ Tx(a_vals[i])
        T_list.append(T)

    T = T @ Ttool
    T_list[-1] = T

    return T_list

def FK(q):
    T_list = compute_all_transforms(q)
    return T_list[-1]  # 末端执行器的齐次变换矩阵

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
        # ft_data = np.array([force.x, -force.z, -force.y, torque.x, torque.y, torque.z])

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
        global R_matrix, pos

        super().__init__('get_rotation_matrix')
        R_matrix = np.eye(3)
        pos = np.zeros(3)
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
        global R_matrix, pos
        qpos = np.zeros(6)
        qpos[1:] = msg.position[:5]
        qpos[0] = msg.position[5]
        q_current = np.array(qpos) # 更新末端状态
        H = FK(q_current[:6])
        print("H",H)
        R_matrix = H[:3, :3]  # Rotation matrix part
        pos = H[:3, 3]
        self.RM_data_sign = True

def get_rotation_matrix_data(args=None):
    global R_matrix, pos

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

    if pos is not None:
        print('Position (p):')
        print(pos)

    get_RM.destroy_node()
    rclpy.shutdown()

def eef_weight(A, b):
    # 计算最小二乘解  Ax = b
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

    print("最小二乘解:", x)
    print("残差:", residuals)
    return x

def estimate_pose(P_obj, P_base):
    assert P_obj.shape == P_base.shape

    # 计算质心
    centroid_obj = np.mean(P_obj, axis=0)
    centroid_base = np.mean(P_base, axis=0)

    # 去中心化
    Q_obj = P_obj - centroid_obj
    Q_base = P_base - centroid_base

    # 求解旋转
    H = Q_obj.T @ Q_base
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # 保证是合法旋转矩阵
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T

    # 平移
    t = centroid_base - R @ centroid_obj

    # 构造齐次变换矩阵
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = t
    return T

def main():
    # rclpy.init()

    force_vectors = []  # 存储力数据
    rotation_matrices = []  # 存储旋转矩阵的逆矩阵
    pos_matrices = []  # 存储位置矩阵

    for _ in range(pos_num):
        input("按回车键继续...")
        
        get_rotation_matrix_data()
        R_inv = np.linalg.inv(R_matrix)
        I = np.eye(3)
        combined_matrix = np.hstack([R_inv, I])
        rotation_matrices.append(combined_matrix)

        pos_matrices.append(pos)
    
    # 世界坐标系下测得的末端位置
    P_base = np.array(pos_matrices)  # 来自你采集的 3 次 pos

    # 估计目标物体的世界坐标系下的位姿
    T_obj = estimate_pose(P_obj, P_base)

    print("矫正变换矩阵:")
    print(T_obj)

    data = {'pos': T_obj}
    file_path = '/home/zzy/ur_real/src/gravity_compensation/gravity_compensation/data_pos.pkl'

    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

    exit(0)

if __name__ == '__main__':
    main()
