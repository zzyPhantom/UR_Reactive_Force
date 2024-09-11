from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription


def generate_launch_description():

    netft_host_arg = DeclareLaunchArgument(
        'netft_host', default_value='192.168.3.123', description='IP address of the Net F/T sensor'
    )
    publish_frequency_arg = DeclareLaunchArgument(
        'publish_frequency', default_value='50', description='Publishing frequency of the sensor data'
    )

    # 使用 FindPackageShare 查找 easy_handeye2 包的路径
    easy_handeye2_launch_path = PathJoinSubstitution(
        [FindPackageShare('easy_handeye2'), 'launch', 'publish.launch.py']
    )

    # Define the node
    ati_net_ft_driver_node = Node(
        package='ati_sensor',
        executable='ati_net_ft_driver_ros',
        name='ati_net_ft_driver',
        output='screen',
        parameters=[{
            'netft_host': LaunchConfiguration('netft_host'),
            'publish_frequency': LaunchConfiguration('publish_frequency')
        }]
    )

    return LaunchDescription(
        [
            # Node(
            #     package="ur10_vel",
            #     executable="publisher_forward_velocity_controller",
            #     name="publisher_forward_velocity_controller",
            #     output="screen",
            # ),
                    # 包含另一个 launch 文件
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(easy_handeye2_launch_path),
                launch_arguments={
                    'name': 'my_eob_calib',
                }.items()
            ),
            Node(
                package="camera",
                executable="realsense_ArUco_reader",
                name="realsense_ArUco_reader",
                output="screen",
            ),
            # netft_host_arg,
            # publish_frequency_arg,
            # ati_net_ft_driver_node,
            Node(
                package="ur10_vel",
                executable="joint_velocity_IK",
                name="joint_velocity_IK",
                output="screen",
            )
        ]
    )
