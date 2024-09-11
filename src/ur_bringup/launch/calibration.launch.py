from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

def generate_launch_description():
    # 使用 FindPackageShare 查找 easy_handeye2 包的路径
    easy_handeye2_launch_path = PathJoinSubstitution(
        [FindPackageShare('easy_handeye2'), 'launch', 'calibrate.launch.py']
    )

    return LaunchDescription([
        # 包含另一个 launch 文件
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(easy_handeye2_launch_path),
            launch_arguments={
                'calibration_type': 'eye_on_base',
                'name': 'my_eob_calib',
                'robot_base_frame': 'base',
                'robot_effector_frame': 'ft_frame',
                'tracking_base_frame': 'camera_frame',
                'tracking_marker_frame': 'aruco_frame',
            }.items()
        ),
        Node(
            package="camera",
            executable="realsense_calibrate",
            name="realsense_calibrate",
            output="screen",
        )
    ])

