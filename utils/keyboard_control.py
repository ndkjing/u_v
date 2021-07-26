"""
备用键盘上上下左右方向键控制
"""
import sys
import os
# 不能被xshell转发
# from pynput.keyboard import Key,Listener
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)
from drivers import com_data
import config
# import enum
# class Direction(enum.Enum):
#     UP      = 1
#     DOWN    = 2
#     LEFT    = 3
#     RIGHT   = 4


# class Control():
#     def __init__(self):
#         self.dir_ = str(360) # dir一定要用成员变量，不然没办法在on_press中修改
#
#     def getdir(self):
#         self.dir_ = None    # 如果是不是上下左右则返回None
#         def on_press(key):
#             if key == Key.up:self.dir_ = str(0)
#             elif key == Key.down:self.dir_ = str(180)
#             elif key == Key.left:self.dir_ = str(90)
#             elif key == Key.right:self.dir_ = str(270)
#             return False
#         listener = Listener(on_press=on_press) # 创建监听器
#         listener.start()    # 开始监听，每次获取一个键
#         listener.join()     # 加入线程
#         listener.stop()     # 结束监听，没有这句也行，直接随函数终止
#         return self.dir_


if __name__ == '__main__':
    serial_obj = com_data.SerialData(config.port, config.baud, timeout=1 / config.com2pi_interval)
    # key_obj = Control()
    i = 0
    com_data_send = 'A5A5%d,0,0,0,0,0,0,0,0,0#\r\n' % 5
    try:
        while True:
            i+=1
            # key_input = key_obj.getdir()
            # w,a,s,d 为前后左右，q为后退 按键后需要按回车才能生效
            key_input = input('direction:')
            if key_input=='7':
                com_data_send= 'A5A50,0,114.00,30.00000,0,0,0,0,0,0#'
                serial_obj.send_data(com_data_send)
                logging.info({'com_data_send': com_data_send})
            if key_input=='w':
                temp_com_data = 1
            elif key_input=='a':
                temp_com_data = 3
            elif key_input=='s':
                temp_com_data = 2
            elif key_input=='d':
                temp_com_data = 4
            elif key_input=='q':
                temp_com_data = 5
            # else:
            #     temp_com_data = 5
            com_data_send = 'A5A5%d,0,0,0,0,0,0,0,0,0#\r\n' % temp_com_data
            logging.info({'com_data_send':com_data_send})
            serial_obj.send_data(com_data_send)
    except:
        serial_obj.send_data(com_data_send)

        # time.sleep(0.1)
        # if key_input:
        #     logging.info('A%sZ' % (key_input))
        #     serial_obj.send_data('A%sZ'%(key_input))

