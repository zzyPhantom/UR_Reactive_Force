import pickle
import matplotlib.pyplot as plt

# 加载数据
def load_data(filename):
    with open(filename, "rb") as file:
        data = pickle.load(file)
    return data

# 绘制前10秒的数据
def plot_first_10_seconds(data, data_1):
    # # 提取前10秒的数据
    # times = [entry[0] for entry in data_1 if entry[0] <= 15 and entry[0] >= 0.2]
    # position = [entry[1] for entry in data_1 if entry[0] <= 15 and entry[0] >= 0.2]
    # pre_position = [entry[2] for entry in data_1 if entry[0] <= 15 and entry[0] >= 0.2]
    
    # # 绘制图表
    # plt.figure(figsize=(10, 5))
    # plt.plot(times, pre_position, label="User inputs target position", color="b", marker="o", markersize=2, linestyle="-")
    # plt.plot(times, position, label="Real target position", color="r", marker="o", markersize=2, linestyle="-")
    # plt.xlabel("Time (s)")
    # plt.ylabel("X-Axis Position (m)")
    # plt.title("Time-Position Plot (First 15 Seconds)")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # 提取前10秒的数据
    times = [entry[0] for entry in data if entry[0] <= 15 and entry[0] >= 0.2]
    position = [entry[1] for entry in data if entry[0] <= 15 and entry[0] >= 0.2]
    times_1 = [entry[0] for entry in data_1 if entry[0] <= 15 and entry[0] >= 0.2]
    position_1 = [entry[1] for entry in data_1 if entry[0] <= 15 and entry[0] >= 0.2]
    
    # 绘制图表
    plt.figure(figsize=(10, 5))
    plt.plot(times_1, position_1, label="Tool velocity using user inputs target pose", color="b", marker="o", markersize=2, linestyle="-")
    plt.plot(times, position, label="Tool velocity using modified target pose", color="r", marker="o", markersize=2, linestyle="-")
    plt.xlabel("Time (s)")
    plt.ylabel("X-Axis Velocity (m)")
    plt.title("Time-Velocity Plot (First 15 Seconds)")
    plt.legend()
    plt.grid(True)
    plt.show()


# 主函数
if __name__ == "__main__":
    filename = '/home/zzy/ur_real/save_data.pkl'
    data = load_data(filename)
    filename = '/home/zzy/ur_real/save_data_1.pkl'
    data_1 = load_data(filename)
    plot_first_10_seconds(data, data_1)
