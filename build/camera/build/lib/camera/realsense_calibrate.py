import cv2
import numpy as np
import time
import pyrealsense2 as rs
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float64MultiArray
from tf2_ros import TransformBroadcaster, TransformStamped
from geometry_msgs.msg import Transform


# 相机的参数
cam_interval = 1/60.0  # 相机显示间隔时间，30FPS
image_width = 640  # 图像的宽度ii
image_height = 480  # 图像的高度
# 棋盘格尺寸
pattern_size = (4, 4)
square_size = 0.05  # 每个格子的边长，例如25毫米

# The different ArUco dictionaries built into the OpenCV library. 
ARUCO_DICT = {
  "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
  "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
  "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
  "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
  "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
  "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
  "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
  "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
  "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
  "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
  "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
  "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
  "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
  "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
  "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
  "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
  "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}
desired_aruco_dictionary = "DICT_7X7_1000"
this_aruco_dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[desired_aruco_dictionary])
this_aruco_parameters = cv2.aruco.DetectorParameters_create()
tag_size = 0.05  # tag的边长

class Aruco_reader(Node):
    def __init__(self):
        super().__init__("ArUco_reader")
        self.mark_index = 0
        
        self.tf_broadcaster = TransformBroadcaster(self)
        # 初始化图像
        self.base_img = np.zeros((image_height, image_width, 3), dtype=np.uint8)
        self.base_img_tag = np.zeros((image_height, image_width, 3), dtype=np.uint8)   

        try:
            self.pipe = rs.pipeline()
            self.cfg  = rs.config()
            self.cfg.enable_stream(rs.stream.color, image_width, image_height, rs.format.bgr8, 30)
            self.pipe.start(self.cfg)
            self.init_camera_parameters()
            self.timer = self.create_timer(cam_interval, self.timer_callback)
        except Exception as err:
            print(err)
            self.get_logger().error("INTEL REALSENSE IS NOT CONNECTED")

    def init_camera_parameters(self):
        # Get frames from the camera to get the intrinsic parameters
        profile = self.pipe.get_active_profile()
        color_stream = profile.get_stream(rs.stream.color)
        color_intrinsics = color_stream.as_video_stream_profile().get_intrinsics()

        # 从彩色相机内参中获取焦距和主点坐标
        focal_length_x = color_intrinsics.fx
        focal_length_y = color_intrinsics.fy
        cx = color_intrinsics.ppx
        cy = color_intrinsics.ppy
        self.dist_coeffs = np.array(color_intrinsics.coeffs)

        # 构造相机内参矩阵
        self.camera_matrix = np.array([[focal_length_x, 0, cx],
                                [0, focal_length_y, cy],
                                [0, 0, 1]], dtype=np.float32)

    def timer_callback(self):
        frames = self.pipe.wait_for_frames()
        color_frame = frames.get_color_frame()
        self.base_img = np.asanyarray(color_frame.get_data())
        self.vision_position()

    def vision_position(self):

        if time.time() >=2:
            # Detect ArUco markers in the video frame

            tag = cv2.cvtColor(self.base_img, cv2.COLOR_BGR2GRAY)
            (self.corners, self.ids, rejected) = cv2.aruco.detectMarkers(
            tag, this_aruco_dictionary, parameters=this_aruco_parameters)
            
            # Check that at least one ArUco marker was detected
            if self.ids is not None:
                self.rvecs, self.tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(self.corners[self.mark_index], tag_size, self.camera_matrix, self.dist_coeffs)
                self.rvec = self.rvecs[self.mark_index]
                self.tvec = self.tvecs[self.mark_index]
                
                # # 计算旋转矩阵
                # R, _ = cv2.Rodrigues(self.rvec)
                # # 创建一个 4x4 的齐次变换矩阵
                # T_camera_to_aruco = np.eye(4)
                # T_camera_to_aruco[:3, :3] = R   # 设置旋转矩阵
                # T_camera_to_aruco[:3, 3] = [self.tvec[0][2], -self.tvec[0][0], -self.tvec[0][1]]  # 设置平移向量

                # Broadcast TF
                transform = TransformStamped()
                transform.header.stamp = self.node.get_clock().now().to_msg()
                transform.header.frame_id = 'camera_link'
                transform.child_frame_id = f'aruco_marker_{ids[i][0]}'
                transform.transform.translation.x = float(tvec[0][0][0])
                transform.transform.translation.y = float(tvec[0][0][1])
                transform.transform.translation.z = float(tvec[0][0][2])
                transform.transform.rotation.x = float(rvec[0][0][0])
                transform.transform.rotation.y = float(rvec[0][0][1])
                transform.transform.rotation.z = float(rvec[0][0][2])
                transform.transform.rotation.w = float(rvec[0][0][3])
                
                self.tf_broadcaster.sendTransform(transform)

            
            else:
                # self.get_logger().error("未找到ArUco标记")
                # self.trolley_position = [0.0, 0.0, 1.2]

                cv2.imshow('Image from base camera', self.base_img)
                cv2.waitKey(1)  # 确保图像显示


    def data_display(self):
        
        self.base_img_tag = self.base_img.copy()
        # 绘制标记
        # 将 self.ids 转换为 NumPy 数组
        self.ids_array = np.array([self.ids[self.mark_index]], dtype=np.int32)
        cv2.aruco.drawDetectedMarkers(self.base_img_tag, [self.corners[self.mark_index]], self.ids_array)
        
        # 生成坐标轴的三维点
        length = 0.1
        axis = np.float32([[0, 0, 0], [length, 0, 0], [0, length, 0], [0, 0, length]]).reshape(-1, 3)
        
        # 投影坐标轴点到图像平面
        imgpts, _ = cv2.projectPoints(axis, self.rvec, self.tvec, self.camera_matrix, self.dist_coeffs)
        imgpts = np.int32(imgpts).reshape(-1, 2)
        
        # 绘制坐标轴
        self.base_img_tag = cv2.line(self.base_img_tag, tuple(imgpts[0]), tuple(imgpts[1]), (0, 0, 255), 3)  # X轴 - 红色
        self.base_img_tag = cv2.line(self.base_img_tag, tuple(imgpts[0]), tuple(imgpts[2]), (0, 255, 0), 3)  # Y轴 - 绿色
        self.base_img_tag = cv2.line(self.base_img_tag, tuple(imgpts[0]), tuple(imgpts[3]), (255, 0, 0), 3)  # Z轴 - 蓝色

        cv2.imshow('Image from base camera', self.base_img_tag)
        cv2.waitKey(1)  # 确保图像显示


def main(args = None):
    rclpy.init(args = None)
    ArUco_reader = Aruco_reader()
    rclpy.spin(ArUco_reader)

    ArUco_reader.pipe.stop()
    ArUco_reader.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()