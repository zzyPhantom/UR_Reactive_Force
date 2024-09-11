from launch import LaunchDescription
import os
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    ur_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join('/opt/ros/humble/share/ur_robot_driver/launch', 'ur_control.launch.py')
        ),
        launch_arguments={
            'ur_type': LaunchConfiguration('ur_type'),
            'robot_ip': LaunchConfiguration('robot_ip'),
            'launch_rviz': LaunchConfiguration('launch_rviz'),
            'initial_joint_controller': LaunchConfiguration('initial_joint_controller'),
        }.items()
    )

    ur_moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join('/home/zzy/ur_real/src/ur10_moveit_config/launch', 'ur_moveit.launch.py')
        )
        # launch_arguments={'arg_name': 'arg_value'}.items(),  # 如果有需要传递的参数，可以在这里设置
    )


    return LaunchDescription(
        [
            DeclareLaunchArgument('ur_type', default_value='ur10'),
            DeclareLaunchArgument('robot_ip', default_value='192.168.125.100'),
            DeclareLaunchArgument('launch_rviz', default_value='true'),
            DeclareLaunchArgument('initial_joint_controller', default_value='forward_velocity_controller'),
            
            ur_control_launch,

            DeclareLaunchArgument('launch_rviz', default_value='true'),
            ur_moveit_launch,

            Node(
                package="ur10_vel",
                executable="publisher_forward_velocity_controller",
                name="publisher_forward_velocity_controller",
                output="screen",
            ),
            Node(
                package="ur10_vel",
                executable="Joint_Velocity_Transfer",
                name="Joint_Velocity_Transfer",
                output="screen",
            )
        ]
    )
