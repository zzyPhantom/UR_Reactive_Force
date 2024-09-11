#!/usr/bin/env python3

from .rpi_ati_net_ft import *
import sys
import time

def main():
    try:
        # if len(sys.argv) < 2:
        #     raise Exception('需要提供ATI Net F/T传感器的IP地址')
        
        # host = sys.argv[1]
        host = "192.168.3.123"
        netft = NET_FT(host)
        netft.set_tare_from_ft()
        
        print(netft.read_ft_http())
        print(netft.try_read_ft_http())
        
        netft.start_streaming()
        
        while True:
            print(netft.read_ft_streaming(0.1))
            print(netft.try_read_ft_streaming(0.1))
            time.sleep(0.1)  # 添加休眠以避免紧循环

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()