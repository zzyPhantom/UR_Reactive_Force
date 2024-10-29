#todo: 可操作雅各比矩阵由于环境冲突使用不了机器人工具箱所以被注释掉

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, Float64MultiArray
from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import JointState

import time
import pickle
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
# import roboticstoolbox as rtb

# 节点参数
FPS = 60

# IK的参数
err_k = 5  # 阻尼最小二乘法误差系数
k_positioncon = 100  # 位置约束增益
k_vel = 50      # 速度增益
k_slack = 1000   # 宽容量增益
k_err = 1    # 位置误差到期望末端速度的变换
k_wheel = 0.1   # 轮子速度增益
Pi = 0.6   # influence distance in which to activate the damper
Ps = 0.1  # stopping distance
force_gain = 0.01  # 力控制增益
max_step = 0.02   # 路径规划中的最大步长
kalman_des_vel_gain = 1.5  # 卡尔曼滤波器中期望速度对预测加速度的影响
plot_axis = 2  # 绘制轴朝向（基坐标系）

# 一些初始化数据
vel_old = np.zeros(6)  # 用来存储上一步的速度
last_eef_vel = np.zeros(6)  # 用来存储上一步的末端速度
# trolley_position = [0.5, 0.0, 0.8, 0.0, 0.0, 0.0]  # 用来存储视觉读取的目标位姿(ur5)
trolley_position = [0.5, 0.0, 0.5, 0.0, 0.0, 0.0]  # 用来存储视觉读取的目标位姿(ur10)
force_predict = []   # 用来存储历史加速度力数据
eef_pos = np.eye(4)          # 用来存储目前的末端位姿
qpos = np.zeros(6)           # 用来存储目前的关节位置
qvel = np.zeros(6)           # 用来存储目前的关节速度
eef_vel = np.zeros(6)        # 用来存储目前的末端速度
des_eef_vel = np.zeros(6)    # 用来存储目标末端速度
p_control_target = np.zeros(3) # 用来存储目标位置的暂时位置
force_control_sign = False  # 用来记录是否开启力控制

#定义机器人模型
# link_lengths = [0.1807, 0.6127, 0.5716, 0.1742, 0.1199, 0.1166] # UR10e链长
link_lengths = [0.1273, 0.6120, 0.5723, 0.1640, 0.1157, 0.0922] # UR10链长
# link_lengths = [0.0892, 0.4250, 0.3923, 0.1092, 0.0947, 0.0823] # UR5链长
car_params = [0.1, 0.1, 1] # 小车参数（左轮半径，右轮半径，轴距）

# E1 = rtb.ET.tx(-0.4)
# E2 = rtb.ET.tx()
# E3 = rtb.ET.Rz()
# E4 = rtb.ET.tx(0.4)
# E5 = rtb.ET.Rz()
# E6 = rtb.ET.tz(link_lengths[0])
# E7 = rtb.ET.Ry()
# E8 = rtb.ET.tz(link_lengths[1])
# E9 = rtb.ET.Ry()
# E10 = rtb.ET.tz(link_lengths[2])
# E11 = rtb.ET.Ry()
# E12 = rtb.ET.ty(link_lengths[3])
# E13 = rtb.ET.Rz()
# E14 = rtb.ET.tz(link_lengths[4])
# E15 = rtb.ET.Ry()
# E16 = rtb.ET.ty(link_lengths[5])
# ur10m = E5 * E6 * E7 * E8 * E9 * E10 * E11 * E12 * E13 * E14 * E15 * E16

Tbase = np.eye(4)
Tbase[0:3, 3] = [0, 0, 0]
Ttool = np.eye(4)
Ttool[0:3, 3] = [0.0, 0, 0]

# 读取末端工具和末端传感器的矫正数据
mass_file_path = '/home/zzy/ur_real/src/gravity_compensation/gravity_compensation/data.pkl'
try:
    with open(mass_file_path, 'rb') as f:
        filedata = pickle.load(f)
    if isinstance(filedata, dict):
        mass_params = filedata.get('mass')
except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
    mass_params = np.zeros(6)
    print(f"加载矫正数据时发生错误: {e}, 默认矫正数据为None")

mass_square_sum = mass_params[0]**2 + mass_params[1]**2 + mass_params[2]**2
eef_mass = [np.sqrt(mass_square_sum)] # 末端工具参数（重量）

force_init = np.zeros(3) # 用来存储传感器零点力数据
force_init[0] = -mass_params[3] # 传感器x方向零点力
force_init[1] = mass_params[5] # 传感器y方向零点力
force_init[2] = -mass_params[4]  # 传感器z方向零点力
# force_init[0] = 0 # 传感器x方向零点力
# force_init[1] = 0 # 传感器y方向零点力
# force_init[2] = 0 # 传感器z方向零点力

# 定义卡尔曼滤波器

# 初始化预测的状态和协方差矩阵
state_matrix_pred = np.zeros((6, 1))  # [v_x, v_y, v_z, a_x, a_y, a_z]
covariance_matrix_pred = np.eye(6)

# 卡尔曼滤波器预测阶段
def kalman_predict(x, P, v_desired, v_current, dt):
    # 状态转移矩阵 A
    A = np.array([[1, 0, 0, dt, 0, 0],
                [0, 1, 0, 0, dt, 0],
                [0, 0, 1, 0, 0, dt],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1]])
    # 控制矩阵 B
    B = np.array([[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [kalman_des_vel_gain, 0, 0],
                [0, kalman_des_vel_gain, 0],
                [0, 0, kalman_des_vel_gain]])
    Q = np.eye(6) * 1e-4  # 示例噪声

    # 状态预测，加入速度期望的影A
    v_error = v_desired - v_current
    x_pred = A @ x + B @ v_error.reshape(-1, 1)
    P_pred = A @ P @ A.T + Q
    return x_pred, P_pred

# 卡尔曼滤波器更新阶段
def kalman_update(x_pred, P_pred, z):
    # 观测矩阵 H
    H = np.array([[1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0]])
    # 测量噪声协方差矩阵
    R = np.eye(3) * 0.01  # 示例观测噪声

    y = z.reshape(-1, 1) - H @ x_pred  # 创新
    S = H @ P_pred @ H.T + R  # 创新协方差
    K = P_pred @ H.T @ np.linalg.inv(S)  # 卡尔曼增益
    x_new = x_pred + K @ y  # 状态更新
    P_new = (np.eye(6) - K @ H) @ P_pred  # 协方差更新
    return x_new, P_new

def transform_to_xyzrpy(T):
    # 提取平移部分
    x, y, z = T[0, 3], T[1, 3], T[2, 3]
    
    # 提取旋转矩阵部分
    R = T[:3, :3]
    
    # 计算欧拉角
    sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    
    singular = sy < 1e-6
    
    if not singular:
        roll = np.arctan2(R[2, 1], R[2, 2])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = np.arctan2(R[1, 0], R[0, 0])
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = 0

    return np.array([x, y, z, roll, pitch, yaw])

def get_target_position(force, p_change = np.zeros(6)):
    # 更新目标位姿
    global force_predict, last_time, state_matrix_pred, covariance_matrix_pred, last_eef_vel, p_control_target
    p_target = np.zeros(6)  # 用来存储目标位姿

    dt = time.time() - last_time

    # 更新卡尔曼滤波器状态并预测下一状态
    state_matrix, convariance_matrix = kalman_update(state_matrix_pred, covariance_matrix_pred, eef_vel[:3])
    state_matrix_pred, covariance_matrix_pred = kalman_predict(state_matrix, convariance_matrix, des_eef_vel[:3], eef_vel[:3], dt)

    # 计算加速度
    # eef_acc_force = ((des_eef_vel[:3] - eef_vel[:3]) / dt) * (eef_mass[0] / 9.8)  # 使用计算出的加速度(根据目标速度)
    # force_predict_SIZE = 4

    # eef_acc_force = ((eef_vel[:3] - last_eef_vel[:3]) / dt) * (eef_mass[0] / 9.8) * 0.7 # 使用计算出的加速度（根据真实速度变化量）
    # force_predict_SIZE = 3

    eef_acc_force = state_matrix_pred[3:].flatten() * (eef_mass[0] / 9.8) # 使用卡尔曼预测的加速度
    force_predict_SIZE = 1
    
    last_time = time.time()
    last_eef_vel = eef_vel

    # 将力数据存入列表，如果力历史记录已满，删除最早的力数据
    force_predict.append(eef_acc_force)
    if len(force_predict) > force_predict_SIZE:
        force_predict.pop(0)

    # # 将速度数据存入列表，如果力历史记录已满，删除最早的力数据(测使用)
    # force_predict.append(des_eef_vel[:3])
    # if len(force_predict) > force_predict_SIZE:
    #     force_predict.pop(0)

    # # 计算平均力
    # avg_force = np.mean(force_predict, axis=0)

    #计算位置变化是否过大过大则减缓变化(渐进距离法)
    target_pos = np.array(p_change[0:3])

    # 计算两点之间的距离
    distance = np.linalg.norm(target_pos - p_control_target)

    # 如果距离超过最大移动距离，则按比例缩小
    if distance > max_step:
        direction = (target_pos - p_control_target) / distance  # 单位方向向量
        p_control_target = p_control_target + direction * max_step    # 按比例缩小移动
    else:
        p_control_target = target_pos  # 距离在允许范围内，直接移动到目标点

    # 测试用直接使用给定速度
    # p_control_target = p_change[0:3]

    if force_control_sign == False:
        p_target[0] = p_control_target[0]
        p_target[1] = p_control_target[1]
        p_target[2] = p_control_target[2]

    if force_control_sign == True:
        p_target[0] = p_control_target[0] - force_gain * (force[0] - force_predict[0][0])
        p_target[1] = p_control_target[1] - force_gain * (force[1] - force_predict[0][1])
        p_target[2] = p_control_target[2] - force_gain * (force[2] - force_predict[0][2])
    
    p_target[3:] = [0.0 + p_change[3], 0.0 + p_change[4], np.pi/2 + p_change[5]]
    # p_target[3:] = [0.0, 0.0, np.pi/2]

    # #计算位置变化是否过大过大则减缓变化(渐进距离法)
    # target_pos = np.array(p_target[0:3])

    # # 计算两点之间的距离
    # distance = np.linalg.norm(target_pos - p_control_target)

    # # 如果距离超过最大移动距离，则按比例缩小
    # if distance > max_step:
    #     direction = (target_pos - p_control_target) / distance  # 单位方向向量
    #     p_control_target = p_control_target + direction * max_step    # 按比例缩小移动
    # else:
    #     p_control_target = target_pos  # 距离在允许范围内，直接移动到目标点

    # p_target[0:3] = p_control_target[:]

    # 回传力数据到F/T显示部分
    force_data = [force[0] - force_predict[0][0], force[1] - force_predict[0][1], force[2] - force_predict[0][2]]
    # force_data = [force[0], force[1], force[2]]
    # force_data = [force_predict[0][0], force_predict[0][1], force_predict[0][2]]
    # force_data = eef_acc_force[:3]
    # force_data = des_eef_vel
    # force_data = p_change
    # vel_error = (eef_vel[:3] - force_predict[0][:3])
    # force_data = des_eef_vel[:3]
    # force_data = vel_error
    force_data = [p_control_target[0], p_change[0], force[2] - force_predict[0][2]]
    force_data = [force_predict[0][0], force_predict[0][1], force_predict[0][2]]

    return p_target, force_data

def homogeneous_matrix_to_array(H):
    """Convert a homogeneous matrix to an array"""
    # Extract position (translation part)
    position = H[:3, 3]

    # Extract rotation (rotation matrix part)
    rotation_matrix = H[:3, :3]

    # Convert rotation matrix to Euler angles (XYZ convention)
    euler_angles = Rotation.from_matrix(rotation_matrix).as_euler('xyz')

    # Combine position and euler angles into a single array
    p_rpy_array = np.concatenate((position, euler_angles))

    return p_rpy_array

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

def Ryd(q):
    Sq = np.sin(q)
    Cq = np.cos(q)
    
    T = np.array([
        [-Sq, 0, Cq, 0],
        [0, 0, 0, 0],
        [-Cq, 0, -Sq, 0],
        [0, 0, 0, 0]
    ])
    
    return T

def Rydd(q):
    Sq = np.sin(q)
    Cq = np.cos(q)
    
    T = np.array([
        [-Cq, 0, -Sq, 0],
        [0, 0, 0, 0],
        [Sq, 0, -Cq, 0],
        [0, 0, 0, 0]
    ])
    
    return T

def Rzd(q):
    Sq = np.sin(q)
    Cq = np.cos(q)
    
    T = np.array([
        [-Sq, -Cq, 0, 0],
        [Cq, -Sq, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    
    return T

def Rzdd(q):
    Sq = np.sin(q)
    Cq = np.cos(q)
    
    T = np.array([
        [-Cq, Sq, 0, 0],
        [-Sq, -Cq, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    
    return T

def Txd(s):
    T = np.array([
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])
    
    return T

def Hwl(dql):
    Sq = np.sin(dql*car_params[0])
    Cq = np.cos(dql*car_params[0])
    Sql = np.sin(-dql*car_params[0]/car_params[2])
    Cql = np.cos(-dql*car_params[0]/car_params[2])

    T = np.array([
        [Cql, -Sql, 0, Cq/2],
        [Sql, Cql, 0, Sq/2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])

    return T

def Hwr(dqr):
    Sq = np.sin(dqr*car_params[1])
    Cq = np.cos(dqr*car_params[1])
    Sqr = np.sin(dqr*car_params[1]/car_params[2])
    Cqr = np.cos(dqr*car_params[1]/car_params[2])

    T = np.array([
        [Cqr, -Sqr, 0, Cq/2],
        [Sqr, Cqr, 0, Sq/2],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ])

    return T

def vec(matrix):

    return matrix.flatten(order='F')

def Jcol(T):
    # Extract the Jacobian column from the transformation matrix T
    J = np.array([T[0, 3], T[1, 3], T[2, 3], T[2, 1], T[0, 2], T[1, 0]]).reshape((-1,1))
    return J

def quaternion_to_rotation_matrix(q):

    q_w, q_x, q_y, q_z = q
    R = np.array([
        [1 - 2*(q_y**2 + q_z**2), 2*(q_x*q_y - q_z*q_w), 2*(q_x*q_z + q_y*q_w)],
        [2*(q_x*q_y + q_z*q_w), 1 - 2*(q_x**2 + q_z**2), 2*(q_y*q_z - q_x*q_w)],
        [2*(q_x*q_z - q_y*q_w), 2*(q_y*q_z + q_x*q_w), 1 - 2*(q_x**2 + q_y**2)]
    ])
    return R

def homogeneous_matrix(xyz, quaternion):

    x, y, z = xyz
    R = quaternion_to_rotation_matrix(quaternion)
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [x, y, z]
    return T

def FK(q):
    # Forward Kinematics calculation
    L = link_lengths
    H = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]), 
            np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), 
            np.dot(Rz(q[4]), np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))

    return H

def Jacobian(q):
    # Calculate forward kinematics
    H = FK(q[:6])
    R = H[:3, :3]  # Rotation matrix part
    L = link_lengths

    # 1st column of Jacobian
    J1p = np.dot(Tbase, np.dot(Rzd(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]),
           np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), np.dot(Rz(q[4]),
           np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))
    J1r = np.dot(J1p, np.vstack((np.hstack((np.linalg.inv(R), np.zeros((3, 1)))), np.array([[0, 0, 0, 1]]))))
    J1 = Jcol(J1r)

    # 2nd column of Jacobian
    J2p = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ryd(q[1]), np.dot(Tz(L[1]),
           np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), np.dot(Rz(q[4]),
           np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))
    J2r = np.dot(J2p, np.vstack((np.hstack((np.linalg.inv(R), np.zeros((3, 1)))), np.array([[0, 0, 0, 1]]))))
    J2 = Jcol(J2r)

    # 3rd column of Jacobian
    J3p = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]),
           np.dot(Ryd(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), np.dot(Rz(q[4]),
           np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))
    J3r = np.dot(J3p, np.vstack((np.hstack((np.linalg.inv(R), np.zeros((3, 1)))), np.array([[0, 0, 0, 1]]))))
    J3 = Jcol(J3r)

    # 4th column of Jacobian
    J4p = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]),
           np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ryd(q[3]), np.dot(Ty(L[3]), np.dot(Rz(q[4]),
           np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))
    J4r = np.dot(J4p, np.vstack((np.hstack((np.linalg.inv(R), np.zeros((3, 1)))), np.array([[0, 0, 0, 1]]))))
    J4 = Jcol(J4r)

    # 5th column of Jacobian
    J5p = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]),
           np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), np.dot(Rzd(q[4]),
           np.dot(Tz(L[4]), np.dot(Ry(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))
    J5r = np.dot(J5p, np.vstack((np.hstack((np.linalg.inv(R), np.zeros((3, 1)))), np.array([[0, 0, 0, 1]]))))
    J5 = Jcol(J5r)

    # 6th column of Jacobian
    J6p = np.dot(Tbase, np.dot(Rz(q[0]), np.dot(Tz(L[0]), np.dot(Ry(q[1]), np.dot(Tz(L[1]),
           np.dot(Ry(q[2]), np.dot(Tz(L[2]), np.dot(Ry(q[3]), np.dot(Ty(L[3]), np.dot(Rz(q[4]),
           np.dot(Tz(L[4]), np.dot(Ryd(q[5]), np.dot(Ty(L[5]), Ttool)))))))))))))
    J6r = np.dot(J6p, np.vstack((np.hstack((np.linalg.inv(R), np.zeros((3, 1)))), np.array([[0, 0, 0, 1]]))))
    J6 = Jcol(J6r)

    # Combine columns to form the full Jacobian
    J = np.concatenate((J1, J2, J3, J4, J5, J6), axis=1)

    return J

# def Manipulability_Jacobian(q, jacob):
#     # Manipulability Jacobian
#     q = [q[0], q[1], q[2], q[3], q[4], q[5]]
#     He = ur10m.hessiane(q)
#     He = np.array([np.concatenate((layer[:, 2:], layer[:, :2]), axis=1) for layer in He])
#     # 定义 J, H1, H2, ..., Hn 和 m
#     J = jacob

#     # 计算 JJ^T 和它的逆矩阵
#     JJ_T = np.dot(J, J.T)
#     JJ_T_inv = np.linalg.inv(JJ_T)
#     vec_JJ_T_inv = vec(JJ_T_inv)

#     # 计算行列式
#     det_JJ_T = np.linalg.det(JJ_T)

#     # 计算行列式的平方根
#     m = np.sqrt(det_JJ_T)

#     # 计算每一项并存储在列表中
#     MJ = []
#     for H in He:
#         JH_T = np.dot(J, H.T)
#         vec_JH_T = vec(JH_T).T
#         result = m * np.dot(vec_JH_T, vec_JJ_T_inv)
#         MJ.append(result)

#     # 将结果转换为数组或所需的形状
#     MJ = np.array(MJ)

#     return MJ

# 关节逆运动学计算函数
def compute_inverse_kinematics(p_goal):
    global vel_old

    # 使用 mujoco 的 ik_solver
    q_current = np.array(qpos) # 保证不修改原始输入的值
    q_current[1] += np.pi/2
    q_current[3] += np.pi/2
    q_updated = q_current[:6]  

    p_curr_H = FK(q_current[:6])
    # p_curr = homogeneous_matrix_to_array(p_curr_H)  # 获取当前末端位置
    p_curr = p_curr_H
    
    err = np.zeros(6)
    err[:3] = p_goal[:3] - p_curr_H[:3, 3]  # 计算位置误差

    rot_curr = p_curr_H[:3, :3]  # 计算旋转误差（矩阵形式）
    rot_goal = Rotation.from_euler('xyz', p_goal[3:]).as_matrix()
    rot_err = np.dot(rot_goal, rot_curr.T)    # 计算旋转矩阵的相对旋转
    euler_err = Rotation.from_matrix(rot_err).as_euler('xyz')
    err[3:] = euler_err

    jacob = Jacobian(q_current)  # 计算雅可比矩阵
    # Mjacob = Manipulability_Jacobian(q_current, jacob)  # 计算可操纵性雅各比矩阵

    # Quadratic Programmming
    # 初始猜测值
    q0 = vel_old
    slack0 = np.zeros(6)
    x0 = np.concatenate([q0, slack0])
    I = np.eye(len(q0))
    err_vel = err * k_err  # 末端的期望速度
    Sjacob = np.concatenate([jacob, np.eye(len(slack0))], axis=1)
    SI = np.concatenate([np.concatenate([np.eye(len(q0)) * k_vel, np.zeros((len(q0), len(slack0)))], axis=1), np.concatenate([np.zeros((len(slack0), len(q0))), np.eye(len(slack0)) * k_slack], axis=1)], axis=0)

    # 最小化问题包含松弛量
    cons = ({'type': 'eq', 'fun': lambda x: np.dot(Sjacob, x.reshape(-1,1)).flatten() - err_vel},
            {'type': 'ineq', 'fun': lambda x: ((np.pi/2 - q_updated[1] * np.sign(q_updated[1])) - Ps)/(Pi - Ps) * k_positioncon - x[1] * np.sign(q_updated[1])})
            # {'type': 'ineq', 'fun': lambda x: ((0.6 - q_updated[3] * np.sign(q_updated[3])) - Ps)/(Pi - Ps) * k_positioncon - x[3] * np.sign(q_updated[3])})
    obj = lambda x: (np.dot(np.dot(x, SI), x.reshape(-1,1)) / 2)[0] #+ np.dot(Mjacob.T, x[:6].reshape(-1,1))[0]
    bounds = [(-1, 1), (-1, 1), (-1, 1), (-1, 1), (-1, 1), (-1, 1), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
    q_vel = minimize(obj, x0, constraints=cons, bounds=bounds)

    q_updated[:6] = q_vel.x[:6]  # 更新关节角速度（速度控制）

    eef_vel_updated = np.dot(jacob, q_updated[:6])  # 计算期望末端速度
    eef_vel_now = np.dot(jacob, qvel[:6])  # 计算末端速度

    return q_updated, p_curr, eef_vel_updated, eef_vel_now

def calculate_eef_pos():
    global p_control_target
    q_current = np.array(qpos) # 更新末端状态
    q_current[1] += np.pi/2
    q_current[3] += np.pi/2 
    eef_pos = FK(q_current[:6])
    p_control_target = eef_pos[:3, 3]

class JointVelocityIK(Node):
    def __init__(self):
        super().__init__("joint_velocity_IK")
        # Declare all parameters
        self.declare_parameter("FPS", FPS)
        # self.stop = False
        # self.collision_stop = True
        self.force_data = np.zeros(3) # 用来存储当前力数据
        self.run_sign = True  # 用来通知其他节点IK是否在运行
        self.received_first_message = False  # 是否初始化了关节姿态

        global last_time
        last_time = time.time()
        self.iniT = time.time()    # 用来记录开始运行的时间

        self.data_list = []  # 用于显示最近几秒的数据
        self.save_data = []  # 用于存储数据
        self.plot_duration = 15
        # 初始化图像
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')  # 初始化折线
        self.ax.set_xlim(0, self.plot_duration)  # x轴范围
        # 启动动画
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=500)  # 每秒更新一次

        # 每一秒存储一次保存的数据
        self.timer = self.create_timer(1, self.save_data_callback)

        # Read parameters
        wait_sec_between_publish = 1 / self.get_parameter("FPS").value

        self.publisher_ = self.create_publisher(Float64MultiArray, "control_velocity_unswiched", 1)
                # 发布停止信号
        self.run_publisher = self.create_publisher(Bool, 'run_sign', 1)

        self.timer = self.create_timer(wait_sec_between_publish, self.timer_callback)
        self.get_logger().info('velocity publisher created')

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.get_logger().info('joint state subscriber created')

        self.trolley_subscription = self.create_subscription(
            Float64MultiArray,
            '/ArUco_pos',
            self.trolley_position_callback,
            10)
        self.trolley_subscription
        self.get_logger().info('trolley position subscriber created')  

        self.ft_sensor_subscription = self.create_subscription(
            WrenchStamped,
            '/ft_wrench',
            self.ft_sensor_callback,
            10)
        self.ft_sensor_subscription
        self.get_logger().info('F/T sensor subscriber created')  

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
        self.get_logger().info('stop signal subscriber created')

        self.get_logger().info('使用的末端公具重力参数为:{}'.format(eef_mass))

    def save_data_callback(self):
        data_file_path = '/home/zzy/ur_real/save_data_1.pkl'
        with open(data_file_path, "wb") as file:
            pickle.dump(self.save_data, file)

    def update_plot(self, frame):
        # 更新折线图
        if self.data_list:
            times, values = zip(*self.data_list)
            times = [t - times[0] for t in times]  # 调整时间以显示最近5秒
            self.line.set_data(times, values)
            self.ax.set_xlim(0, self.plot_duration)
            # 自动调整y轴范围
            self.ax.relim()  # 重新计算数据范围
            self.ax.autoscale_view()  # 自动缩放视图
        return self.line,

    def stop_callback(self, msg):
        self.stop = bool(msg.data)

    def trolley_position_callback(self, msg):
        global trolley_position
        trolley_position = msg.data

    def ft_sensor_callback(self, msg):
        # 从 WrenchStamped 消息中提取力
        force = msg.wrench.force

        # 提取 x, y, z 方向的力值
        force_x = force.x - force_init[0]
        force_y = force.y - force_init[1]
        force_z = force.z - force_init[2]
        data = np.array([-force_x, -force_z, force_y]).reshape(3, 1)
        # print('none_d',force)
        # 定义重力加速度
        g = 9.81  # m/s^2, eef_mass[0]是工具重力，若输入质量则需要乘g

        # 计算工具重力在基座标系下的力
        tool_gravity_base = np.array([0.0, 0.0, eef_mass[0]]).reshape(3, 1)

        # 将工具重力转换到末端坐标系
        R_eef = eef_pos[:3, :3]  # 从齐次变换矩阵中提取旋转矩阵
        tool_gravity_eef = np.zeros(3)
        tool_gravity_eef = np.dot(R_eef.T, tool_gravity_base)# np.dot(R_eef, np.dot(Rz(-np.pi/2)[:3, :3], Ry(np.pi)[:3, :3])))

        # 计算工具重心产生的力矩
        # tool_gravity_eef[3:] = np.cross(tool_com, tool_gravity_eef[:3])

        # 减去工具重力的影响
        corrected_data = data - tool_gravity_eef.reshape(3, 1)
        print("data",data)
        print("gravity_predict",tool_gravity_eef)

        #转回基座标系
        self.force_data = np.dot(R_eef, corrected_data)

    def listener_callback(self, msg):
        global qpos, qvel

        if not self.received_first_message:
            self.received_first_message = True  # 设置标志为 True
            calculate_eef_pos()
            self.get_logger().info('Received first joint state message!')
        
        qpos[1:] = msg.position[:5]
        qpos[0] = msg.position[5]

        qvel[1:] = msg.velocity[:5]
        qvel[0] = msg.velocity[5]

    def collision_stop_callback(self, msg):
        self.collision_stop = bool(msg.data)

    def timer_callback(self):
        global eef_pos, des_eef_vel, eef_vel, force_control_sign

        msg = Float64MultiArray()
        msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        force_data_display = [0.0, 0.0, 0.0]

        if time.time() - self.iniT <= 0.5:
            calculate_eef_pos()
            _, force_data_display = get_target_position(self.force_data, [p_control_target[0], p_control_target[1], p_control_target[2], 0.0-1.57, 0.0, 0.0])

        if time.time() - self.iniT > 0.5 and time.time() - self.iniT <= 5:
            p_target, force_data_display = get_target_position(self.force_data, [-trolley_position[0]-0.5, -trolley_position[1], trolley_position[2], 0.0-1.57, 0.0, 0.0])
            IK, eef_pos, des_eef_vel, eef_vel = compute_inverse_kinematics(p_target)

            # 设置小数点精度
            precision = 6
            data_list = [round(value, precision) for value in IK]
            msg.data = data_list

        if time.time() - self.iniT > 5 and time.time() - self.iniT <= 10:

            p_target, force_data_display = get_target_position(self.force_data, [-trolley_position[0]+0.5, -trolley_position[1], trolley_position[2]+0.3, -trolley_position[4]-1.57, trolley_position[3], trolley_position[5]])
            IK, eef_pos, des_eef_vel, eef_vel = compute_inverse_kinematics(p_target)

            # 设置小数点精度
            precision = 6
            data_list = [round(value, precision) for value in IK]
            msg.data = data_list

        if time.time() - self.iniT > 10:# and time.time() - self.iniT <= 15:
            force_control_sign = True
            # p_target = get_target_position(force_data, [np.sin(time.time()), 0, 0])
            # p_target = get_target_position(force_data, [0.2, 0.0, 0.0, 0.0, 0.0, 0.0])
            p_target, force_data_display = get_target_position(self.force_data, [-trolley_position[0]-0.2*np.sin(time.time()), -trolley_position[1], trolley_position[2]-0.3, -trolley_position[4]-1.57, trolley_position[3], trolley_position[5]])
            IK, eef_pos, des_eef_vel, eef_vel = compute_inverse_kinematics(p_target)

            # 设置小数点精度
            precision = 6
            data_list = [round(value, precision) for value in IK]
            msg.data = data_list

        # F/T传感器数据显示部分
        # 存储时间戳和数据
        current_time = time.time()
        self.data_list.append((current_time, force_data_display[plot_axis]))  
        self.save_data.append((current_time - self.iniT, force_data_display[0]))#, force_data_display[1]))  
        # 清除超过5秒的数据
        self.data_list = [(t, data) for t, data in self.data_list if current_time - t <= self.plot_duration]

        self.publisher_.publish(msg)
        self.run_publisher.publish(Bool(data=self.run_sign))


def main(args=None):
    rclpy.init(args=args)

    joint_velocity_IK = JointVelocityIK()

    while rclpy.ok():
        rclpy.spin_once(joint_velocity_IK)
        plt.pause(0.01)  # 绘图刷新
    # rclpy.spin(joint_velocity_IK)

    # 发送静止关节速度
    msg = Float64MultiArray()
    msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    joint_velocity_IK.publisher_.publish(msg)
    rclpy.spin_once(joint_velocity_IK)

    joint_velocity_IK.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
