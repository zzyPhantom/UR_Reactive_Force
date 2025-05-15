# UR_Reactive_Force
A Reactive Force Control System for UR Robots

# 启动虚拟机械臂和moveit
ros2 run ur_client_library start_ursim.sh -m ur5

ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur5 robot_ip:=192.168.56.1 launch_rviz:=true 

ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5 launch_rviz:=true

#启动真实机械臂和moveit
ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur5 robot_ip:=192.168.3.121 launch_rviz:=true

ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur5 launch_rviz:=true

#标定末端工具重力
ros2 run ati_sensor ati_net_ft_driver_ros 
ros2 run gravity_compensation ft_calib

# 启动虚拟机械臂和实时力控
ros2 launch ur_bringup fake_ur_driver.launch.py 

ros2 launch ur_bringup joint_velocity_controller.launch.py 

# 启动真实机械臂和实时力控

打开ati供电和urscript
source install/setup.bash 
ros2 launch ur_bringup ur5_driver.launch.py
ros2 launch ur_bringup joint_velocity_controller.launch.py 

