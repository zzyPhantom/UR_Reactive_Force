# UR_Reactive_Force
A Reactive Force Control System for UR Robots

ros2 run ur_client_library start_ursim.sh -m ur10

ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur10 robot_ip:=192.168.56.1 launch_rviz:=true initial_joint_controller:=forward_velocity_controller


[build_scripts] 
executable=/usr/bin/env python3
放在setup.cfg前面可以让程序在虚拟环境中运行
