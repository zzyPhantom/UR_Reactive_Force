from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # 使用 FindPackageShare 查找 easy_handeye2 包的路径
    easy_handeye2_launch_path = PathJoinSubstitution(
        [FindPackageShare('easy_handeye2'), 'launch', 'publish.launch.py']
    )

    return LaunchDescription([
        # 包含另一个 launch 文件
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(easy_handeye2_launch_path),
            launch_arguments={
                'name': 'my_eob_calib',
            }.items()
        ),
    ])

