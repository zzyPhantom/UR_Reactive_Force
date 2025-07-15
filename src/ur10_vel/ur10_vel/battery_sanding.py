#todo: 可操作雅各比矩阵由于环境冲突使用不了机器人工具箱所以被注释掉

import rclpy
from rclpy.node import Node
import signal

from std_msgs.msg import Bool, Float64MultiArray
from geometry_msgs.msg import WrenchStamped
from sensor_msgs.msg import JointState

import pickle
import numpy as np
from scipy.spatial.transform import Rotation
from scipy.optimize import minimize
from scipy.interpolate import CubicSpline
# import roboticstoolbox as rtb

# 电池单元中心序列
centers = [
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0],
    [0.0, -0.0, -0.0]

    # [0.0, 0.0, 0.0],
    # [0.0, -0.05, -0.0],
    # [0.0, -0.10, -0.0],
    # [0.0, -0.15, -0.0],
    # [0.0, -0.20, -0.0],
    # [0.0, -0.25, -0.0],
    # [0.0, -0.30, -0.0],
    # [0.0, -0.35, -0.0]
]
# 动作时长
duration_dict = {
            'approach': 8,
            'grind': 16,
            'press': 3,
            'lift': 2,
            'move_next': 4,
            'retreat': 4
        }
F_target_preset = 2  # 力目标

Force_vector = [0, 0, 1, 0, 0, 0]    # 力目标向量(基坐标系)
# trolley_position = [0.0, 0.0, 0.0, -np.pi/2, 0, 0]  # 打磨工具横向
trolley_position = [0.0, -0.0, 0.0, np.pi, 0, np.pi]  # 底座相对初始坐标

# 控制器总速率
FPS = 30

# 一些初始化数据
last_eef_vel = np.zeros(6)  # 用来存储上一步的末端速度
trolley_position_display = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 用来存储视觉读取位姿（显示）
eef_pos = np.eye(4)          # 用来存储目前的末端位姿
qpos = np.zeros(6)           # 用来存储目前的关节位置
qvel = np.zeros(6)           # 用来存储目前的关节速度
qtor = np.zeros(6)           # 用来存储目前的关节扭矩
des_eef_vel = np.zeros(6)    # 用来存储目标末端速度
p_control_target = np.zeros(3)  # 用来存储幻影目标位姿
state_matrix_pred = np.zeros((6, 1))  # 用来存储卡尔曼滤波器预测的状态[v_x, v_y, v_z, a_x, a_y, a_z]
covariance_matrix_pred = np.eye(6)  # 用来存储卡尔曼滤波器的协方差矩阵
start_time = 0.8  # 用来存储开始执行动作序列的时间
plot_axis = 2  # 绘制轴朝向（基坐标系）
display = np.zeros(3)  # 用来存储绘图数据

# ur5用参数开始
# IK的参数
k_positioncon = 100  # 位置约束增益
k_vel = 50      # 速度增益
k_slack = 1000   # 宽容量增益
k_pos = 1.0   # 平移误差增益(区分增益)
k_rot = 0.5   # 旋转误差增益
Pi = 0.6   # influence distance in which to activate the damper
Ps = 0.1  # stopping distance
max_step = 0.02   # 路径规划中的最大步长
kalman_des_vel_gain = 1.5  # 卡尔曼滤波器中期望速度对预测加速度的影响

# 导纳参数
M_k = 1
D_k = 12
K_k = 4
M = np.diag([M_k, M_k, M_k, M_k, M_k, M_k])  # 虚拟质量矩阵
D = np.diag([D_k, D_k, D_k, D_k, D_k, D_k])  # 虚拟阻尼矩阵
K = np.diag([K_k, K_k, K_k, K_k, K_k, K_k])  # 虚拟刚度矩阵
kp = 0.01  # 力误差比例项
ki = 0.003  # 力误差积分项
kd = 0.000  # 力误差微分项
beta = 0.8  # 积分项的滤波(chatgpt建议[0.7,0.9])
I_max = 10.0  # 力误差积分项的最大值(N*S)
error_threshold = 0.01  # 力误差阈值，误差小于该值时归零积分项
disturbance_threshold = 10.0  # 大扰动阈值，当误差大于该值时归零积分项
force_predict_SIZE = 1  # 平均滤波器的窗口大小

#调试用参数
M_k = 1
D_k = 20
K_k = 1
M = np.diag([M_k, M_k, M_k, M_k, M_k, M_k])  # 虚拟质量矩阵
D = np.diag([D_k, D_k, D_k, D_k, D_k, D_k])  # 虚拟阻尼矩阵
K = np.diag([K_k, K_k, K_k, K_k, K_k, K_k])  # 虚拟刚度矩阵
kp = 0.05  # 力误差比例项
ki = 0.000  # 力误差积分项
kd = 0.000  # 力误差微分项
beta = 0.8  # 积分项的滤波(chatgpt建议[0.7,0.9])
I_max = 10.0  # 力误差积分项的最大值(N*S)

# DH参数
d_vals =     [0.089159, 0,       0,        0.10915,  0.09465,  0.0823]
a_vals =     [0,       -0.425,  -0.39225,  0,        0,        0]
alpha_vals = [np.pi/2,  0,       0,        np.pi/2, -np.pi/2,  0]  
# ur5参数结束

#定义机器人模型
# link_lengths = [0.1807, 0.6127, 0.5716, 0.1742, 0.1199, 0.1166] # UR10e链长

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
Ttool[0:3, 3] = [0.0, -0.09, 0.2]

def init_params():
    # 初始化参数
    global eef_mass, force_init, time_plan, T_obj, end_time
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

    # 读取初始位置
    mass_file_path = '/home/zzy/ur_real/src/gravity_compensation/gravity_compensation/data_pos.pkl'
    try:
        with open(mass_file_path, 'rb') as f:
            filedata = pickle.load(f)
        if isinstance(filedata, dict):
            init_pos = filedata.get('pos')
    except (FileNotFoundError, EOFError, pickle.UnpicklingError) as e:
        init_pos = np.eye(4)
        print(f"加载矫正数据时发生错误: {e}, 使用默认矫正none")

    # 工件初始位置
    T_obj = np.eye(4)
    T_obj[0:3, 3] = [0.8, 0, 0.2]
    T_obj = init_pos

    # 生成动作序列
    time_plan = generate_batch_sequence(centers, start_time=start_time)
    end_time = time_plan[-1][1]  # 用来存储结束的时间 

# 定义动作序列函数
def smooth_contact_segments(original_plan, resolution=0.02):
    """
    搜索给定位置列表中的接触段，并使用样条插值函数
    """
    updated_plan = []
    i = 0
    while i < len(original_plan):
        curr = original_plan[i]
        if curr[3] == True:
            # 找前一个非接触段，获取起点
            if i == 0:
                raise ValueError("接触段不能作为 time_plan 的第一个元素")
            prev = original_plan[i - 1]
            t_start = curr[0]
            t_end = curr[1]
            p_start = np.array(prev[2])
            p_end = np.array(curr[2])
            
            # 插值时间点
            t_interp = np.arange(t_start, t_end, resolution)
            if len(t_interp) < 2 or t_interp[-1] != t_end:
                t_interp = np.append(t_interp, t_end)

            # 样条插值
            cs = CubicSpline([t_start, t_end], [p_start, p_end], axis=0)
            p_interp = cs(t_interp)

            # 构建新插值段
            for j in range(len(t_interp) - 1):
                seg = (
                    float(t_interp[j]),
                    float(t_interp[j + 1]),
                    p_interp[j].tolist(),
                    True,
                    curr[4]  # 保留当前段的力
                )
                updated_plan.append(seg)
            i += 1  # 当前段已处理
        else:
            updated_plan.append(curr)
            i += 1
    return updated_plan

def generate_grinding_sequence(center_xyz, start_time=0.5, add_return_home=False, duration_dict=None):
    """
    根据单个工件中心生成动作序列。
    """
    if duration_dict is None:
        duration_dict = {
            'approach': 8,
            'grind': 8,
            'press': 2,
            'lift': 2,
            'move_next': 4,
            'retreat': 4
        }

    x_c, y_c, z_c = center_xyz
    x_offset = 0.015
    y_offset = 0.06
    z_work = z_c #+ 0.005
    z_safe = z_c + 0.015 #+ 0.03
    z_retreat = z_c + 0.2

    t = start_time
    plan = []

    # # 横向电池
    # # 左侧抬起位置
    # plan.append((t, t + duration_dict['approach'], [x_c - x_offset, y_c + y_offset, z_safe], False, 0))
    # t += duration_dict['approach']

    # # 压下
    # plan.append((t, t + duration_dict['press'], [x_c - x_offset, y_c + y_offset, z_work], False, 0))
    # t += duration_dict['press']

    # # 左 → 右 打磨
    # plan.append((t, t + duration_dict['grind'], [x_c + x_offset, y_c + y_offset, z_work], True, F_target_preset))
    # t += duration_dict['grind']

    # # 抬起
    # plan.append((t, t + duration_dict['lift'], [x_c + x_offset, y_c + y_offset, z_safe], False, 0))
    # t += duration_dict['lift']

    # # 移动到右侧抬起位置
    # plan.append((t, t + duration_dict['move_next'], [x_c - x_offset, y_c - y_offset, z_safe], False, 0))
    # t += duration_dict['move_next']

    # # 压下
    # plan.append((t, t + duration_dict['press'], [x_c - x_offset, y_c - y_offset, z_work], False, 0))
    # t += duration_dict['press']

    # # 左 → 右 打磨（Y负）
    # plan.append((t, t + duration_dict['grind'], [x_c + x_offset, y_c - y_offset, z_work], True, F_target_preset))
    # t += duration_dict['grind']

    # # 抬起
    # plan.append((t, t + duration_dict['lift'], [x_c + x_offset, y_c - y_offset, z_safe], False, 0))
    # t += duration_dict['lift']

    # # 纵向放置的电池
    # # 抬起位置（上方）
    # plan.append((t, t + duration_dict['approach'], [x_c, y_c + x_offset, z_safe], False, 0))
    # t += duration_dict['approach']

    # # 压下
    # plan.append((t, t + duration_dict['press'], [x_c, y_c + x_offset, z_work+0.002], False, 0))
    # t += duration_dict['press']

    # # 上 → 下 打磨（x固定，y从正到负）
    # plan.append((t, t + duration_dict['grind'], [x_c, y_c - x_offset, z_work], True, F_target_preset))
    # t += duration_dict['grind']

    # # 抬起
    # plan.append((t, t + duration_dict['lift'], [x_c, y_c - x_offset, z_safe], False, 0))
    # t += duration_dict['lift']

    # # 移动到下一个打磨位置
    # plan.append((t, t + duration_dict['move_next'], [x_c - 2*y_offset, y_c + x_offset, z_safe], False, 0))
    # t += duration_dict['move_next']

    # # 压下
    # plan.append((t, t + duration_dict['press'], [x_c - 2*y_offset, y_c + x_offset, z_work+0.002], False, 0))
    # t += duration_dict['press']

    # # 上 → 下 打磨（x固定，y从正到负）
    # plan.append((t, t + duration_dict['grind'], [x_c - 2*y_offset, y_c - x_offset, z_work], True, F_target_preset))
    # t += duration_dict['grind']

    # # 抬起
    # plan.append((t, t + duration_dict['lift'], [x_c - 2*y_offset, y_c - x_offset, z_safe], False, 0))
    # t += duration_dict['lift']

    # 单独打磨一个
    # 抬起位置（上方）
    plan.append((t, t + duration_dict['approach'], [x_c, y_c + x_offset, z_safe], False, 0))
    t += duration_dict['approach']

    # 压下
    plan.append((t, t + duration_dict['press'], [x_c, y_c + x_offset, z_work+0.002], False, 0))
    t += duration_dict['press']

    # 上 → 下 打磨（x固定，y从正到负）
    plan.append((t, t + duration_dict['grind'], [x_c, y_c - x_offset, z_work], True, F_target_preset))
    t += duration_dict['grind']

    # 抬起
    plan.append((t, t + duration_dict['lift'], [x_c, y_c - x_offset, z_safe], False, 0))
    t += duration_dict['lift']

    # # 数据收集的流程
    # # 抬起位置（上方）
    # plan.append((t, t + 4, [x_c, y_c, z_safe], False, 0))
    # t += 4

    # # 压下
    # plan.append((t, t + duration_dict['press'], [x_c, y_c, z_work+0.002], False, 0))
    # t += duration_dict['press']

    # # 上 → 下 打磨（x固定，y从正到负）
    # plan.append((t, t + duration_dict['grind'], [x_c, y_c, z_work], True, F_target_preset))
    # t += duration_dict['grind']

    # # 抬起
    # plan.append((t, t + duration_dict['lift'], [x_c, y_c, z_safe], False, 0))
    # t += duration_dict['lift']

    # 是否回中位
    if add_return_home:
        plan.append((t, t + duration_dict['retreat'], [x_c, y_c, z_retreat], False, 0))
        t += duration_dict['retreat']

    return plan, t


def generate_batch_sequence(centers, start_time=0.5):
    """
    多个工件中心生成完整动作序列，默认只在最后一个回中位。
    """
    full_plan = []
    t = start_time
    for i, c in enumerate(centers):
        is_last = (i == len(centers) - 1)
        sub_plan, t = generate_grinding_sequence(c, start_time=t, add_return_home=is_last, duration_dict=duration_dict)
        full_plan.extend(sub_plan)

    time_plan = smooth_contact_segments(full_plan, resolution=0.02)
    return time_plan


# 定义卡尔曼滤波器
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

def get_target_position(dt, eef_vel, p_change = np.zeros(6)):
    # 更新目标位姿
    # global force_predict, state_matrix_pred, covariance_matrix_pred, last_eef_vel
    global p_control_target

    # # 更新卡尔曼滤波器状态并预测下一状态
    # state_matrix, convariance_matrix = kalman_update(state_matrix_pred, covariance_matrix_pred, eef_vel[:3])
    # state_matrix_pred, covariance_matrix_pred = kalman_predict(state_matrix, convariance_matrix, des_eef_vel[:3], eef_vel[:3], dt)

    # 计算加速度
    # eef_acc_force = ((des_eef_vel[:3] - eef_vel[:3]) / dt) * (eef_mass[0] / 9.8)  # 使用计算出的加速度(根据目标速度)
    # force_predict_SIZE = 4

    # eef_acc_force = ((eef_vel[:3] - last_eef_vel[:3]) / dt) * (eef_mass[0] / 9.8) * 0.7 # 使用计算出的加速度（根据真实速度变化量）
    # force_predict_SIZE = 3

    # eef_acc_force = state_matrix_pred[3:].flatten() * (eef_mass[0] / 9.8) # 使用卡尔曼预测的加速度


    # 使用位置标定将目标坐标系中的目标点转到基坐标系中
    obj_pos = np.array(p_change[0:3])
    obj_pos_hom = np.hstack((obj_pos, [1]))
    base_pos_hom = T_obj @ obj_pos_hom 
    target_pos = base_pos_hom[:3]

    # 计算位置变化是否过大过大则减缓变化(渐进距离法)
    distance = np.linalg.norm(target_pos - p_control_target)

    # 如果距离超过最大移动距离，则按比例缩小
    if distance > max_step:
        direction = (target_pos - p_control_target) / distance  # 单位方向向量
        p_control_target = p_control_target + direction * max_step    # 按比例缩小移动
    else:
        p_control_target = target_pos  # 距离在允许范围内，直接移动到目标点

    p_target = np.zeros(6)  # 用来存储目标位姿
    p_target[0] = p_control_target[0]
    p_target[1] = p_control_target[1]
    p_target[2] = p_control_target[2]
    
    # 二维码与工件的旋转变换
    # p_target[3:] = [0.0 + p_change[3], 0.0 + p_change[4], np.pi/2 + p_change[5]]
    base_rot = Rotation.from_euler('xyz', [0, 0.0, -np.pi/2])
    delta_rot = Rotation.from_euler('xyz', p_change[3:])
    target_rot = delta_rot * base_rot
    p_target[3:] = target_rot.as_euler('xyz')

    return p_target

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

def Jacobian(q):
    T_list = compute_all_transforms(q)
    J = np.zeros((6, 6))

    # 末端位置
    Te = T_list[-1]
    pe = Te[:3, 3]

    for i in range(6):
        Ti = T_list[i]
        pi = Ti[:3, 3]  # 当前关节的位置
        Ri = Ti[:3, :3]
        zi = Ri @ np.array([0, 0, 1])   # 当前关节的 z 轴

        # 对应列的线速度部分和角速度部分
        Jp = np.cross(zi, pe - pi)
        Jo = zi

        J[:3, i] = Jp
        J[3:, i] = Jo

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


# 导纳控制函数
def admittance_controller_factory():
    F_err_I = np.zeros(6)
    F_last = np.zeros(6)
    F_err_D_prev = np.zeros(6)
    eef_vel_last = np.zeros(6)
    force_predict = []

    def admittance_controller(eef_vel_now, eef_pos_err, F_target, F_ext, dt, d_f, P_f):
        nonlocal F_err_I, F_last, F_err_D_prev, eef_vel_last, force_predict

        # 将力数据存入列表，如果力历史记录已满，删除最早的力数据
        force_predict.append(F_ext)
        if len(force_predict) > force_predict_SIZE:
            force_predict.pop(0)

        # 计算平均力
        avg_force = np.mean(force_predict, axis=0)

        # 使用了与目标位置的位置误差以及目标速度为静止的速度误差
        F_control = P_f @ avg_force[0]  # 计算力控制方向上目前的力（将总外力中力控制方向上的力通过投影矩阵取出来）
        # F_control = P_f @ F_ext[0]  # 计算力控制方向上目前的力（将总外力中力控制方向上的力通过投影矩阵取出来）
        F_target_vector = F_target * d_f # 计算目标力向量
        F_err = F_control - F_target_vector  # 计算力误差
        F_err_I += F_err * dt  # 计算误差的积分项
        F_err_D = beta * (F_err - F_last) / dt + (1 - beta) * F_err_D_prev
        F_err_D_prev = F_err_D
        # F_err_D = (F_err - F_last) / dt  # 计算误差的微分项
        F_last = F_err

        # 限制积分项的范围，防止积分风暴
        F_err_I = np.clip(F_err_I, -I_max, I_max)
        # 当误差小于阈值时，归零积分项
        # if np.linalg.norm(F_err) < error_threshold:
        #     F_err_I = np.zeros_like(F_err_I)  # 保持原来形状的零向量
        # 当误差大于扰动阈值时，归零积分项（例如大扰动或系统异常时）
        # if np.linalg.norm(F_err) > disturbance_threshold:
        #     F_err_I = np.zeros_like(F_err_I)
        
        # 当切换到位置控制时误差归零
        if np.linalg.norm(d_f) == 0:
            F_err_I = np.zeros_like(F_err_I)

        # 计算加速度
        # dot_v = (eef_vel_now - eef_vel_last) / dt
        dot_v = np.linalg.inv(M) @ ((kp * F_err + ki * F_err_I + kd * F_err_D) - D @ eef_vel_now - K @ eef_pos_err)
        # v = np.linalg.inv(D) @ ((kp * F_err + ki * F_err_I + kd * F_err_D) - M @ dot_v - K @ eef_pos_err)
        # 更新末端速度
        v = dot_v * dt + eef_vel_now

        return v, F_err_I

    return admittance_controller

adm_controller = admittance_controller_factory()

# 关节逆运动学计算函数
def compute_inverse_kinematics(dt, eef_H, p_goal, F_target = 0.0, F_ext = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], force_control_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
    global des_eef_vel
    # 计算力位混合选择矩阵
    # 将力控制向量在基坐标系
    d_f = force_control_vector.copy()

    # 归一化力控制向量
    if np.linalg.norm(d_f) != 0:
        d_f = d_f / np.linalg.norm(d_f)
    else:
        d_f = np.array([0, 0, 0, 0, 0, 0])  # 默认没有力控制

    P_f = np.outer(d_f, d_f)  # 力控制投影
    P_p = np.eye(6) - P_f     # 位置控制投影

    # 初始化关节角度目标
    q_updated = np.array(qpos) # 保证不修改原始输入的值    
    
    # 计算位置误差
    err = np.zeros(6)
    err[:3] = eef_H[:3, 3] - p_goal[:3]  

    # 计算旋转误差（矩阵形式）
    rot_curr = eef_H[:3, :3]  
    rot_goal = Rotation.from_euler('xyz', p_goal[3:]).as_matrix()
    rot_err = np.dot(rot_curr, rot_goal.T)    # 计算旋转矩阵的相对旋转

    # 转到旋转向量形式
    rotvec_err = Rotation.from_matrix(rot_err).as_rotvec()
    err[3:] = rotvec_err

    # 计算雅可比矩阵
    jacob = Jacobian(qpos)  
    # Mjacob = Manipulability_Jacobian(q_current, jacob)  # 计算可操纵性雅各比矩阵

    # 计算末端速度
    eef_vel_now = np.dot(jacob, qvel[:6])  

    # # 计算末端力矩
    # J_T_inv = np.linalg.inv(jacob.T)
    # eef_force = J_T_inv @ qtor[:6]

    # 计算力控制方向上的速度使用导纳控制器
    F_target = np.array(F_target)
    F_ext = np.array(F_ext).reshape(1, -1)
    force_vel,_ = adm_controller(eef_vel_now[:6], err[:6], F_target, F_ext, dt, d_f, P_f)

    # Quadratic Programmming
    # 初始猜测值
    q0 = np.zeros(6)
    slack0 = np.zeros(6)
    x0 = np.concatenate([q0, slack0])

    # 末端的期望速度
    err_vel = np.zeros(6)
    err_vel[:3] = -k_pos * err[:3]
    err_vel[3:] = -k_rot * err[3:]
    
    # # 判断并合并力控制方向和位置控制方向的速度控制量
    # for i in range(3):
    #     if force_control_vector[i] == 1:  # 如果使用力控制
    #         err_vel[i] = force_vel[i]
    U_vel = P_p @ err_vel + P_f @ force_vel

    Sjacob = np.concatenate([jacob, np.eye(len(slack0))], axis=1)
    SI = np.concatenate([np.concatenate([np.eye(len(q0)) * k_vel, np.zeros((len(q0), len(slack0)))], axis=1), np.concatenate([np.zeros((len(slack0), len(q0))), np.eye(len(slack0)) * k_slack], axis=1)], axis=0)

    # 最小化问题包含松弛量
    cons = ({'type': 'eq', 'fun': lambda x: np.dot(Sjacob, x.reshape(-1,1)).flatten() - U_vel}, )       # 运动学约束
            # {'type': 'ineq', 'fun': lambda x: ((np.pi - q_updated[1] * np.sign(q_updated[1])) - Ps)/(Pi - Ps) * k_positioncon - x[1] * np.sign(q_updated[1])})   # 关节2角度限制
            # {'type': 'ineq', 'fun': lambda x: ((0.6 - q_updated[3] * np.sign(q_updated[3])) - Ps)/(Pi - Ps) * k_positioncon - x[3] * np.sign(q_updated[3])})    # 关节3角度限制
    obj = lambda x: (np.dot(np.dot(x, SI), x.reshape(-1,1)) / 2)[0] #+ np.dot(Mjacob.T, x[:6].reshape(-1,1))[0]
    bounds = [(-1, 1), (-1, 1), (-1, 1), (-1, 1), (-1, 1), (-1, 1), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
    q_vel = minimize(obj, x0, constraints=cons, bounds=bounds)

    q_updated[:6] = q_vel.x[:6]  # 更新关节角速度（速度控制）
    
    des_eef_vel = np.dot(jacob, q_updated[:6])  # 计算期望末端速度

    return q_updated

class JointVelocityIK(Node):
    def __init__(self):
        super().__init__("joint_velocity_IK")

        # Declare all parameters
        self.running = True
        self.declare_parameter("FPS", FPS)
        self.eef_H = np.eye(4)
        self.force_network = 0.0
        self.force_data = np.zeros(6) # 用来存储当前力数据
        self.eef_vel = np.zeros(6) # 用来存储当前末端速度
        self.init_force = np.zeros(6) # 用来存储初始力数据
        self.run_sign = True  # 用来通知其他节点IK是否在运行
        self.received_first_message = np.zeros(2)  # 是否初始化了关节姿态
        self.last_time = self.get_clock().now()    # 用来记录上一循环的时间点
        self.iniT = self.get_clock().now()    # 用来记录开始运行的时间
        self.save_data = []  # 用于储存存储数据

        # 发布即机械臂速度控制量
        self.publisher_ = self.create_publisher(Float64MultiArray, "control_velocity_unswiched", 1)
        # 发布停止信号
        self.run_publisher = self.create_publisher(Bool, 'run_sign', 1)
        # 发布末端位置
        self.eef_vel_publisher = self.create_publisher(Float64MultiArray, 'eef_vel', 1)
        # 发布显示数据
        self.plot_data_publisher = self.create_publisher(Float64MultiArray, 'plot_data', 1)

        # 启动主循环
        FPS_seconds = 1 / self.get_parameter("FPS").value
        self.get_logger().info(f"IK started. Timer interval is {FPS_seconds:.4f} seconds")
        self.timer = self.create_timer(FPS_seconds, self.timer_callback)

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.qpos_callback,
            10)
        self.subscription  # prevent unused variable warning
        # self.get_logger().info('joint state subscriber created')

        self.trolley_subscription = self.create_subscription(
            Float64MultiArray,
            '/ArUco_pos',
            self.trolley_position_callback,
            10)
        self.trolley_subscription
        # self.get_logger().info('trolley position subscriber created')  

        self.ft_sensor_subscription = self.create_subscription(
            WrenchStamped,
            '/ft_wrench',
            self.ft_sensor_callback,
            10)
        self.ft_sensor_subscription
        # self.get_logger().info('F/T sensor subscriber created')

        self.force_network_subscription = self.create_subscription(
            Float64MultiArray,
            '/force_predict',
            self.force_network_callback,
            10)
        self.force_network_subscription
        # self.get_logger().info('force predict subscriber created')    

        self.get_logger().info('使用的末端公具重力参数为:{}'.format(eef_mass[0][0]))
        self.get_logger().info('末端零点位置为:{}'.format(T_obj[:3, 3]))

    def save_all_data(self):
        data_file_path = '/home/zzy/temporary_data/force_pos_data.pkl'
        if len(self.save_data) == 0:
            self.get_logger().error("No data to save.")
            return
        with open(data_file_path, "wb") as file:
            pickle.dump(self.save_data, file)
        self.get_logger().info(f"Saved date to: {data_file_path}")

    def calculate_eef_pos(self):

        q_current = np.array(qpos) # 更新末端状态
        self.eef_H = FK(q_current[:6])
        eef_pos = self.eef_H[:3, 3]

        return eef_pos

    def trolley_position_callback(self, msg):
        global trolley_position, trolley_position_display
        # trolley_position = msg.data
        trolley_position_display = msg.data

    def ft_sensor_callback(self, msg):
        # 从 WrenchStamped 消息中提取力
        force = msg.wrench.force

        # 提取 x, y, z 方向的力值
        force_x = force.x - force_init[0]
        force_y = force.y - force_init[1]
        force_z = force.z - force_init[2]
        data_eef = np.array([force_x, force_y, force_z]).reshape(3, 1)
    
        # 定义重力加速度
        # g = 9.81  # m/s^2, eef_mass[0]是工具重力，若输入质量则需要乘g

        # 计算工具重力在基座标系下的力
        tool_gravity_base = np.array([0.0, 0.0, eef_mass[0][0]]).reshape(3, 1)

        # 将工具重力转换到末端坐标系
        R_eef = self.eef_H[:3, :3]  # 从齐次变换矩阵中提取旋转矩阵
        # tool_gravity_eef = np.zeros(3)
        tool_gravity_eef = np.dot(R_eef.T, tool_gravity_base)# np.dot(R_eef, np.dot(Rz(-np.pi/2)[:3, :3], Ry(np.pi)[:3, :3])))

        # 计算工具重心产生的力矩
        # tool_gravity_eef[3:] = np.cross(tool_com, tool_gravity_eef[:3])

        # 减去工具重力的影响
        corrected_data = data_eef - tool_gravity_eef.reshape(3, 1)

        #转回基座标系
        force_base = np.dot(R_eef, corrected_data)
        self.force_data = np.array([force_base[0][0], force_base[1][0], force_base[2][0], msg.wrench.torque.x, msg.wrench.torque.y, msg.wrench.torque.z])

    def force_network_callback(self, msg):
        self.force_network = -msg.data[0]

    def qpos_callback(self, msg):
        global qpos, qvel, qtor, p_control_target

        if self.received_first_message[0] == 0 and not np.all(qpos == 0):
            # 第一次接收到关节角度（非零）后的一个循环
            self.received_first_message[0] = 1
            if self.received_first_message[1] == 0:
                self.received_first_message[1] = 1
                p_control_target = self.calculate_eef_pos()
                self.get_logger().info("Received first joint state message")

        # 更新末端坐标
        _ = self.calculate_eef_pos()

        # 计算末端速度
        jacob = Jacobian(qpos)  
        self.eef_vel = np.dot(jacob, qvel)

        publish_msg = Float64MultiArray()
        publish_msg.data = self.eef_vel.tolist()
        self.eef_vel_publisher.publish(publish_msg)
        
        qpos[1:] = msg.position[:5]
        qpos[0] = msg.position[5]

        qvel[1:] = msg.velocity[:5]
        qvel[0] = msg.velocity[5]

        qtor[1:] = msg.effort[:5]
        qtor[0] = msg.effort[5]

    def timer_callback(self):

        msg = Float64MultiArray()
        msg.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # 更新时间
        time_now = self.get_clock().now()
        time_from_start = (time_now - self.iniT).nanoseconds / 1e9
        dt = (time_now - self.last_time).nanoseconds / 1e9
        self.last_time = time_now
        dt = 1/FPS

        # if time_from_start <= start_time:
            # eef_pose = self.calculate_eef_pos()
            # p_control_target = eef_pose
            # _ = get_target_position(self.last_time, self.eef_vel, [eef_pose[0], eef_pose[1], eef_pose[2], 0.0-1.57, 0.0, 0.0])

        # if time_from_start > 1 and time_from_start <= 1.1:
        if time_from_start < start_time + 3.1:
            # 重置力传感器(仅在竖直状态可用)
            self.init_force = self.force_data

        #  收集训练数据
        # if time_from_start > start_time and time_from_start <= 5:
        #     offset = [0.0, 0.0, 0.005]
        #     force_vector = np.zeros(6)
        #     F_target = 0

        #     # 获取目标位置
        #     pos_target = [trolley_position[0] - offset[0],
        #                 -trolley_position[1] - offset[1],
        #                 trolley_position[2] + offset[2]]

        #     # IK 求解
        #     p_target = get_target_position(dt, self.eef_vel, [pos_target[0], pos_target[1], pos_target[2], -trolley_position[4], trolley_position[3], trolley_position[5]])
        #     IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, self.force_data - self.init_force, force_vector)
        #     # IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, [0.0, 0.0, self.force_network, 0.0, 0.0, 0.0], force_vector)

        #     msg.data = [round(v, 6) for v in IK]
        # if time_from_start > 5 and time_from_start <= end_time:
        #     offset = [0.0, 0.0, 0.00]
        #     force_vector = Force_vector
        #     F_target = np.array(-2.5*(np.sin(time_from_start/3)+0.8))
        #     # F_target = F_target_preset

        #     # 获取目标位置
        #     pos_target = [trolley_position[0] - offset[0],
        #                 -trolley_position[1] - offset[1],
        #                 trolley_position[2] + offset[2]]

        #     # IK 求解
        #     p_target = get_target_position(dt, self.eef_vel, [pos_target[0], pos_target[1], pos_target[2], -trolley_position[4], trolley_position[3], trolley_position[5]])
        #     IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, self.force_data - self.init_force, force_vector)
        #     # IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, [0.0, 0.0, self.force_network, 0.0, 0.0, 0.0], force_vector)

        #     msg.data = [round(v, 6) for v in IK]

        # 找到当前时间段
        current_task = None
        for row in time_plan:
            t_min, t_max, offset, force_mode, fz = row
            if t_min < time_from_start <= t_max:
                current_task = row
                break

        if current_task:
            t_min, t_max, offset, force_mode, fz = current_task
            force_vector = Force_vector if force_mode else [0.0] * 6 # 力位混合控制中力控制的方向向量
            F_target = np.array(fz)

            # 获取目标位置
            pos_target = [trolley_position[0] - offset[0],
                        -trolley_position[1] - offset[1],
                        trolley_position[2] + offset[2]]

            # IK 求解
            p_target = get_target_position(dt, self.eef_vel, [pos_target[0], pos_target[1], pos_target[2], -trolley_position[4], trolley_position[3], trolley_position[5]])
            IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, self.force_data - self.init_force, force_vector)
            # IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, [0.0, 0.0, self.force_network, 0.0, 0.0, 0.0], force_vector)

            msg.data = [round(v, 6) for v in IK]

        # 停止运动并复位
        if time_from_start > end_time:
            offset = [0.0, 0.0, 0.03]
            force_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]   # 力位混合控制中力控制的方向向量
            F_target = np.zeros(6)

            # 获取目标位置
            pos_target = [trolley_position[0] - offset[0],
                        -trolley_position[1] - offset[1],
                        trolley_position[2] + offset[2]]

            # IK 求解
            p_target = get_target_position(dt, self.eef_vel, [pos_target[0], pos_target[1], pos_target[2], -trolley_position[4], trolley_position[3], trolley_position[5]])
            IK = compute_inverse_kinematics(dt, self.eef_H, p_target, F_target, self.force_data, force_vector)

            msg.data = [round(v, 6) for v in IK]

        # 发布关节数据
        self.publisher_.publish(msg)
        self.run_publisher.publish(Bool(data=self.run_sign))

        # 发布需要显示的数据
        time_now_sec = time_now.nanoseconds / 1e9
        plot_msg = Float64MultiArray()
        plot_msg.data = [
            time_now_sec,
            self.force_data[plot_axis] - self.init_force[plot_axis],
            self.eef_H[2, 3].copy(),
            # display[0],
            self.force_network
        ]
        self.plot_data_publisher.publish(plot_msg) 

        # 保存数据
        self.save_data.append((time_from_start, self.force_data[plot_axis], trolley_position_display[0], trolley_position_display[1], trolley_position_display[2], self.eef_H[:3, 3].copy(), self.force_network, self.eef_vel))

def main(args=None):

    init_params()
    rclpy.init(args=args)

    joint_velocity_IK = JointVelocityIK()
        
    def shutdown_handler(signum, frame):
        # 保存数据
        joint_velocity_IK.save_all_data()
        joint_velocity_IK.running = False

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        while rclpy.ok() and joint_velocity_IK.running:
            rclpy.spin_once(joint_velocity_IK)

    finally:
        joint_velocity_IK.destroy_node()
        rclpy.shutdown()



if __name__ == "__main__":
    main()
