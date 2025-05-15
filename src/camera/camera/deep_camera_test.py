import pyrealsense2 as rs
import numpy as np
import cv2
import cv2.aruco as aruco

def detect_aruco_and_get_depth():
    # 配置 RealSense 管道
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # 启动管道
    pipeline.start(config)

    try:
        while True:
            # 获取一帧深度和颜色数据
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue

            # 转换为 Numpy 数组
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # 检测 ArUco 标记
            gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
            aruco_dict = aruco.Dictionary_get(aruco.DICT_7X7_1000)
            aruco_params = aruco.DetectorParameters_create()

            corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
            
            if ids is not None:
                # 在图像上绘制标记
                aruco.drawDetectedMarkers(color_image, corners, ids)

                for corner in corners:
                    # 计算标记中心点
                    corner_points = corner[0]
                    center_x = int(np.mean(corner_points[:, 0]))
                    center_y = int(np.mean(corner_points[:, 1]))

                    # 获取深度图中的深度值
                    depth = depth_frame.get_distance(center_x, center_y)
                    print(f"Marker ID: {ids[0]}, Depth: {depth:.2f} meters")

                    # 在图像上显示中心点和深度信息
                    cv2.circle(color_image, (center_x, center_y), 5, (0, 0, 255), -1)
                    cv2.putText(color_image, f"Depth: {depth:.2f}m", (center_x, center_y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 显示结果
            cv2.imshow('RealSense RGB', color_image)
            cv2.imshow('RealSense Depth', cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

def main():
    detect_aruco_and_get_depth()

if __name__ == "__main__":
    main()