from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():


    return LaunchDescription(
        [
            Node(
                package="ferrobotics_acf",
                executable="acf",
                name="acf",
                output="screen",
            ),
            Node(
                package="ferrobotics_acf",
                executable="force_publisher",
                name="force_publisher",
                output="screen",
            )
        ]
    )
