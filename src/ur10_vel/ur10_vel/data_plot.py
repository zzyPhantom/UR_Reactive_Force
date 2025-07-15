import rclpy
from rclpy.node import Node

import threading
import signal

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from std_msgs.msg import Float64MultiArray

class dataPlot(Node):
    def __init__(self):
        super().__init__("data_plot")

        self.running = True
        # 画图部分
        self.data_list = []  # 用于储存显示数据
        self.data_list_2 = []
        self.save_data = []  # 用于储存存储数据
        self.plot_duration = 30  # 用于确定显示范围
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], 'b-')  # 初始化折线
        self.line_2, = self.ax.plot([], [], 'g-')  # 初始化折线2
        self.ax.set_xlim(0, self.plot_duration)  # x轴范围
        # 启动动画
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=500)  # 每秒更新一次

        self.data_subscription = self.create_subscription(
            Float64MultiArray,
            '/plot_data',
            self.data_callback,
            10)
        self.data_subscription
        # self.get_logger().info('force predict subscriber created')    

    def data_callback(self, msg):
        time_now_sec = self.get_clock().now().to_msg().sec
        data = msg.data
        self.data_list.append((data[0], data[1]))    
        # self.data_list_2.append((data[0], data[3])) 
        self.data_list_2.append((data[0], data[3]))
        # 清除超过5秒的数据
        self.data_list = [(t, data) for t, data in self.data_list if time_now_sec - t <= self.plot_duration]
        self.data_list_2 = [(t, data) for t, data in self.data_list_2 if time_now_sec - t <= self.plot_duration]

    def update_plot(self, frame):
        # 更新折线图
        if not self.running:
            plt.close() 
        if self.data_list:
            times, values = zip(*self.data_list)
            times = [t - times[0] for t in times]  # 调整时间以显示最近5秒
            self.line.set_data(times, values)
            self.ax.set_xlim(0, self.plot_duration)
            # 自动调整y轴范围
            self.ax.relim()  # 重新计算数据范围
            self.ax.autoscale_view()  # 自动缩放视图
        if self.data_list_2:
            times, values = zip(*self.data_list_2)
            times = [t - times[0] for t in times]  # 调整时间以显示最近5秒
            self.line_2.set_data(times, values)
            self.ax.set_xlim(0, self.plot_duration)
            # 自动调整y轴范围
            self.ax.relim()  # 重新计算数据范围
            self.ax.autoscale_view()  # 自动缩放视图
        return self.line, self.line_2

def ros_spin_thread(node):
    rclpy.spin(node)

def main(args=None):

    rclpy.init(args=args)

    data_plot = dataPlot()

    def shutdown_handler(signum, frame):
        data_plot.running = False  # 通知动画退出
        rclpy.shutdown()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        # 启动 ROS 线程
        ros_thread = threading.Thread(target=ros_spin_thread, args=(data_plot,), daemon=True)
        ros_thread.start()

        # 启动 matplotlib 主线程
        plt.show()

    finally:
        data_plot.destroy_node()

if __name__ == "__main__":
    main()