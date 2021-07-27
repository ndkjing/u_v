"""
数据定义类
"""
import enum
import config


class DataDefine:
    def __init__(self):
        # 运动方向
        self.move_direction = config.MoveDirection.stop
        self.move_mode = 1  # 运动模式上下左右与东南西北
        self.lng_lat = None  # 经纬度
        self.zoom = None  # 缩放等级
        self.home_lng_lat = None  # 返航点经纬度
        self.gaode_lng_lat = None  # 高德经纬度
        self.home_gaode_lng_lat = None  # 返航点高德经纬度
        self.last_lng_lat = None  # 上次有效经纬度
        self.head_direction = None  # 船头方向
        self.dump_energy = None  # 剩余电量
        self.is_center = False  # 是否使用船居中模式
        self.control_mode = config.ShipControlStatus.hand_control

    def update_direction(self, target_direction):
        self.move_direction = target_direction
