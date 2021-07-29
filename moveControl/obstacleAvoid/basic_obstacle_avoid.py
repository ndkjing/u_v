"""
简单距离避障算法
"""
import time

def move(l_distance,r_distance):
    """
    :param l_distance: 左侧超声波距离 单位厘米
    :param r_distance: 右侧超声波距离 单位厘米
    :return: 移动方向
    """
    # 后退
    if l_distance < 200 and r_distance < 200:
        return 180
    # 右转
    elif l_distance < 200 and r_distance >= 200:
        return 270
    # 左转
    elif l_distance >= 200 and r_distance < 200:
        return 90
    # 前进
    elif l_distance >= 200 and r_distance >= 200:
        return 0
    # 停止
    else:
        return 360

if __name__ == "__main__":
    print(move(3300,1500))
