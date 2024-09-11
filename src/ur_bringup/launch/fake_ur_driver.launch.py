from launch import LaunchDescription
import os
from launch.actions import ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    script_path = '/opt/ros/humble/lib/ur_client_library/start_ursim.sh'

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
            ExecuteProcess(
                cmd=['bash', script_path, '-m', 'ur10'],
                output='screen'
            ),

            DeclareLaunchArgument('ur_type', default_value='ur10'),
            DeclareLaunchArgument('robot_ip', default_value='192.168.56.1'),
            DeclareLaunchArgument('launch_rviz', default_value='true'),
            DeclareLaunchArgument('initial_joint_controller', default_value='forward_velocity_controller'),
            
            # 延迟指定时间（10秒）
            TimerAction(
                period = 10.0,
                actions = [
                    ur_control_launch,
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
        ]
    )
