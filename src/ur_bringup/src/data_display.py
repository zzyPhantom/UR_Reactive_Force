import pickle
import matplotlib.pyplot as plt

startTime = 5 # 开始时间
startTime2 = 8
endTime = 70 # 结束时间
target_force = -20

# 加载数据
def load_data(filename):
    with open(filename, "rb") as file:
        data = pickle.load(file)
    return data

# 绘制前10秒的数据
def plot_first_10_seconds(data):

    # 提取前n秒的数据
    times = [entry[0] for entry in data if entry[0] <= endTime and entry[0] >= startTime]
    force = [entry[1] for entry in data if entry[0] <= endTime and entry[0] >= startTime]
    pos_x = [entry[2] for entry in data if entry[0] <= endTime and entry[0] >= startTime2]
    pos_y = [entry[3] for entry in data if entry[0] <= endTime and entry[0] >= startTime2]
    pos_z = [entry[4] for entry in data if entry[0] <= endTime and entry[0] >= startTime2]
    # 创建 force_target 列表，所有值都为 -20
    force_target = [target_force] * len(times)    

    # 获取1秒时的初始位置
    closest_entry = min(data, key=lambda entry: abs(entry[0] - startTime2))
    initial_pos_x = closest_entry[2]
    initial_pos_y = closest_entry[3]
    initial_pos_z = closest_entry[4]

    # 减去初始位置
    pos_x = [x - initial_pos_x for x in pos_x]
    pos_y = [-y + initial_pos_y for y in pos_y]
    pos_z = [z - initial_pos_z for z in pos_z]

    # 绘制图表
    # plt.figure(figsize=(10, 5))
    # plt.plot(times, force_target, label="Force target", color="r", marker="o", markersize=2, linestyle="-")
    # plt.plot(times, force, label="Force on Z-Axis", color="b", marker="o", markersize=2, linestyle="-")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Z-Axis Force (n)")
    # plt.title("Time-Force Plot")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # 创建图表和子图
    fig, axes = plt.subplots(1, 2, figsize=(12, 10))
    fig.suptitle("Time-Force and Time-Position Plots")

    # 子图1: 时间-力
    axes[0].plot(times, force_target, label="Force Target", color="r", linestyle="--")
    axes[0].plot(times, force, label="Force on Z-Axis", color="b")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Z-Axis Force (N)")
    axes[0].set_title("Time vs Force")
    axes[0].legend()
    axes[0].grid(True)

    # 子图2: X-Y平面上的曲线
    axes[1].plot(pos_y, pos_z, label="Trajectory in XY Plane", color="g")
    axes[1].set_xlabel("Position X")
    axes[1].set_ylabel("Position Y")
    axes[1].set_title("Trajectory in XY Plane")
    axes[1].grid(True)
    axes[1].set_aspect('equal')  # 确保坐标轴比例相同
    axes[1].set_box_aspect(1.5)  # 设置宽高比为 1.5

    # # 子图2: 时间-位置X
    # axes[0, 1].plot(times, pos_x, label="Position X", color="g")
    # axes[0, 1].set_xlabel("Time (s)")
    # axes[0, 1].set_ylabel("Position X")
    # axes[0, 1].set_title("Time vs Position X")
    # axes[0, 1].grid(True)

    # # 子图3: 时间-位置Y
    # axes[1, 0].plot(times, pos_y, label="Position Y", color="m")
    # axes[1, 0].set_xlabel("Time (s)")
    # axes[1, 0].set_ylabel("Position Y")
    # axes[1, 0].set_title("Time vs Position Y")
    # axes[1, 0].grid(True)

    # # 子图4: 时间-位置Z
    # axes[1, 1].plot(times, pos_z, label="Position Z", color="c")
    # axes[1, 1].set_xlabel("Time (s)")
    # axes[1, 1].set_ylabel("Position Z")
    # axes[1, 1].set_title("Time vs Position Z")
    # axes[1, 1].grid(True)

    # 调整子图间距
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# 主函数
if __name__ == "__main__":
    filename = '/home/zzy/temporary_data/force_pos_data.pkl'
    data = load_data(filename)
    plot_first_10_seconds(data)
