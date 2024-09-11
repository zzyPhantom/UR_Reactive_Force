#!/usr/bin/env python3
from geometry_msgs.msg import WrenchStamped
from .rpi_ati_net_ft import *
import rclpy
from rclpy.node import Node

class ATINetFTDriver(Node):
    def __init__(self):
        super().__init__('ati_net_ft_driver')
        
        self.declare_parameter("netft_host", "192.168.3.123")
        self.declare_parameter("publish_frequency", 50)
        
        netft_host = self.get_parameter("netft_host").get_parameter_value().string_value
        publish_frequency = self.get_parameter("publish_frequency").get_parameter_value().integer_value
        
        self.ft_sensor = NET_FT(netft_host)
        self.ft_sensor.set_tare_from_ft()
        self.ft_sensor.start_streaming()
        
        self.ft_wrench_pub = self.create_publisher(WrenchStamped, "ft_wrench", 10)
        self.timer = self.create_timer(1.0 / publish_frequency, self.timer_callback)
    
    def timer_callback(self):
        res, ft, status = self.ft_sensor.try_read_ft_streaming(0)
        
        if res and status == 0:
            w = WrenchStamped()
            w.header.stamp = self.get_clock().now().to_msg()
            w.wrench.torque.x = ft[0]
            w.wrench.torque.y = ft[1]
            w.wrench.torque.z = ft[2]
            w.wrench.force.x = ft[3]
            w.wrench.force.y = ft[4]
            w.wrench.force.z = ft[5]
            
            self.ft_wrench_pub.publish(w)

def main(args=None):
    rclpy.init(args=args)
    node = ATINetFTDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

        
    
    
    



