from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare the launch arguments
    netft_host_arg = DeclareLaunchArgument(
        'netft_host', default_value='192.168.3.123', description='IP address of the Net F/T sensor'
    )
    publish_frequency_arg = DeclareLaunchArgument(
        'publish_frequency', default_value='50', description='Publishing frequency of the sensor data'
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

    # Create the launch description and add the launch arguments and node
    return LaunchDescription([
        netft_host_arg,
        publish_frequency_arg,
        ati_net_ft_driver_node
    ])

