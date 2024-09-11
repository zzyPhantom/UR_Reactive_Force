#todo: 可操作雅各比矩阵由于环境冲突使用不了机器人工具箱所以被注释掉； 传感器部分未移植

import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, Float64MultiArray
from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import JointState

import time
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
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

# 一些初始化数据
vel_old = np.zeros(6)  # 用来存储上一步的速度
trolley_position = [0.0, 0.0, 1.0, 3.14, 0.0, 0.0]  # 用来存储视觉读取的目标位姿
force_history = []   # 用来存储历史力数据
FORCE_HISTORY_SIZE = 2   # 用来计算平均力的历史记录长度
force_data = np.zeros(3)
eef_pos = np.zeros(3)
qpos = np.zeros(6)
iniT = time.time()

#定义机器人模型
# link_lengths = [0.1807, 0.6127, 0.5716, 0.1742, 0.1199, 0.1166] # UR10e链长
link_lengths = [0.1807, 0.6127, 0.5716, 0.1742, 0.1199, 0.1166] # UR5链长
car_params = [0.1, 0.1, 1] # 小车参数（左轮半径，右轮半径，轴距）
eef_params = [1.5] # 末端工具参数（重量）

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
    global force_history
    p_target = np.zeros(6)  # 用来存储目标位姿

    # force = d.sensor('eef_force').data.copy()

    # 如果力历史记录还没满，直接添加新数据
    if len(force_history) < FORCE_HISTORY_SIZE:
        force_history.append(force)
    else:
    # 如果力历史记录已满，删除最早的力数据，然后添加新数据
        force_history.pop(0)
        force_history.append(force)

    # 计算平均力
    avg_force = np.mean(force_history, axis=0)

    p_target[0] = 0.5 + p_change[0] + 0.05 * (force[2]+29.0) -0.2
    p_target[1] = 0.0 + p_change[1] - 0.05 * (force[1]-21.5)
    p_target[2] = 1.0 + p_change[2] + 0.05 * (force[0]) +0.1

    p_target[3:] = [0.0 + p_change[3], 0.0 + p_change[4], -np.pi/2 + p_change[5]]

    return p_target

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

# def force_sensor_data(H_eef, ddT):
    
#     data = d.sensor('eef_force').data.copy()

#     # 定义重力加速度
#     g = 9.81  # m/s^2

#     # 计算工具重力在基座标系下的力
#     tool_gravity_base = np.array([0, 0, eef_params[0] * g])
#     #先不计算加速度产生的力（此方法需要验证）
#     # tool_extForce_base = tool_gravity_base - np.array([ddT[0], ddT[1], ddT[2]]) * eef_params[0]

#     # 将工具重力转换到末端坐标系
#     R_eef = H_eef[:3, :3]  # 从齐次变换矩阵中提取旋转矩阵
#     tool_gravity_eef = np.zeros(3)
#     tool_gravity_eef = np.dot(tool_gravity_base, np.dot(R_eef, np.dot(Rz(-np.pi/2)[:3, :3], Ry(np.pi)[:3, :3])))

#     # 计算工具重心产生的力矩
#     # tool_gravity_eef[3:] = np.cross(tool_com, tool_gravity_eef[:3])

#     # 减去工具重力的影响
#     corrected_data = data - tool_gravity_eef

#     # print ('m',tool_gravity_eef)
#     # print('r',d.sensor('eef_tool_acc').data)

#     #转回基座标系
#     corrected_data_base = np.dot(R_eef.T, corrected_data)

#     return corrected_data_base

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
    p_curr = homogeneous_matrix_to_array(p_curr_H)  # 获取当前末端位置
    
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

    ddT = 0.0

    return q_updated, p_curr

class JointVelocityIK(Node):
    def __init__(self):
        super().__init__("joint_velocity_IK")
        # Declare all parameters
        self.declare_parameter("FPS", FPS)
        # self.stop = False
        # self.collision_stop = True
        self.run_sign = True

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

    def stop_callback(self, msg):
        self.stop = bool(msg.data)

    def trolley_position_callback(self, msg):
        global trolley_position
        trolley_position = msg.data

    def ft_sensor_callback(self, msg):
        global force_data
        # 从 WrenchStamped 消息中提取力
        force = msg.wrench.force

        # 提取 x, y, z 方向的力值
        force_x = force.x
        force_y = force.y
        force_z = force.z
        force_data = [force_x, force_y, force_z]

    def listener_callback(self, msg):
        global qpos
        qpos[1:] = msg.position[:5]
        qpos[0] = msg.position[5]

    def collision_stop_callback(self, msg):
        self.collision_stop = bool(msg.data)

    def timer_callback(self):
        global force_data, eef_pos

        msg = Float64MultiArray()

        if time.time() - iniT <= 2:
            msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]   # 速度控制用

        if time.time() - iniT > 2 and time.time() - iniT <= 10:
            p_target = get_target_position(force_data, [0.2, 0.0, 0.0, 0.0, 0.0, 0.0])
            IK, eef_pos = compute_inverse_kinematics(p_target)

            # 设置小数点精度
            precision = 6
            data_list = [round(value, precision) for value in IK]
            msg.data = data_list

        if time.time() - iniT > 10:
            # p_target = get_target_position(force_data, [np.sin(time.time()), 0, 0])
            p_target = get_target_position(force_data, [0.2, 0.0, 0.0, 0.0, 0.0, 0.0])
            # p_target = get_target_position(force_data, [trolley_position[0], trolley_position[1], trolley_position[2], trolley_position[3]-3.14, -trolley_position[4], -trolley_position[5]])
            IK, eef_pos = compute_inverse_kinematics(p_target)

            # 设置小数点精度
            precision = 6
            data_list = [round(value, precision) for value in IK]
            msg.data = data_list

        self.publisher_.publish(msg)
        self.run_publisher.publish(Bool(data=self.run_sign))


def main(args=None):
    rclpy.init(args=args)

    joint_velocity_IK = JointVelocityIK()

    rclpy.spin(joint_velocity_IK)

    # 发送停止信号
    msg = Float64MultiArray()
    msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    joint_velocity_IK.publisher_.publish(msg)
    rclpy.spin_once(joint_velocity_IK)

    joint_velocity_IK.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
