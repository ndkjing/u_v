"""
数据定义类
"""
import enum
import time

import config


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


@singleton
class DataDefine:
    def __init__(self):
        # 客户端点击信息
        self.move_direction = config.MoveDirection.stop  # 运动方向
        self.move_mode = 1  # 运动模式上下左右与东南西北
        self.lng_lat = None  # 设备上传经纬度
        self.zoom = None  # 设备上传缩放等级
        self.click_lng_lat = None  # 点击经纬度
        self.click_zoom = None  # 点击缩放等级
        self.home_lng_lat = None  # 返航点经纬度
        self.gaode_lng_lat = None  # 高德经纬度
        self.home_gaode_lng_lat = None  # 返航点高德经纬度
        self.last_lng_lat = None  # 上次有效经纬度

        self.dump_energy = None  # 剩余电量
        self.is_center = False  # 是否使用船居中模式
        self.control_mode = config.ShipControlStatus.hand_control

        # 服务器上传
        self.head_direction = None  # 船头方向
        self.speed = None  # 速度
        self.pool_click_lng_lat = None  # 点击湖泊经纬度
        self.pool_click_zoom = None  # 点击湖泊经纬度对应地图缩放等级
        self.b_pool_click = None  # 是否已经点击湖泊
        # 接收到点击的经纬度目标地点和点击是地图层次，二维矩阵
        self.target_lng_lat = []
        self.zoom = []
        self.meter_pix = {}
        self.mode = []
        self.pool_code = None
        # 记录经纬度是不是已经到达或者放弃到达（在去的过程中手动操作） 0准备过去(自动) -1放弃（手动）  1 已经到达的点  2:该点是陆地
        self.target_lng_lat_status = []
        # 当前航线  -1是还没选择
        self.current_lng_lat_index = -1
        self.confirm_index = -1
        # 路径规划话题中的消息
        self.sampling_points = []
        self.path_planning_points = []
        self.sampling_points_status = []
        self.sampling_points_gps = []
        self.path_planning_points_gps = []
        self.keep_point = 0
        # 船当前经纬度 给服务器路径规划使用
        self.current_lng_lat = None
        # 船返航点经纬度 给服务器路径规划使用
        self.home_lng_lat = []
        # 自动求取经纬度设置 使用行间距和记录当前路径点是使用行间距
        self.row_gap = None
        self.use_col_gap = False
        self.safe_gap = 10
        # 环绕湖运行距离岸边间距
        self.round_pool_gap = None
        # 行驶轨迹确认ID 与是否确认
        self.path_id = None
        self.path_id_confirm = None
        # 前后左右移动控制键　0 为前进　90 度向左　　180 向后　　270向右　　-1为停止  -2 为不为平台控制
        self.control_move_direction = -2
        self.last_control_move_direction = -2
        # 状态灯
        self.status_light = 1  # 默认为红色
        # 启动还是停止
        self.b_start = 0
        # 基础设置数据
        self.is_update_base = False
        self.base_setting_data = None
        # 基础数据设置类型
        self.base_setting_data_info = None
        self.base_setting_default_data = None
        # 高级设置
        self.is_update_advance = False
        self.height_setting_data = None
        # 类型
        self.height_setting_data_info = None
        self.height_setting_default_data = None
        # 刷新后请求数据
        self.refresh_info_type = 0
        # 重置湖泊
        self.reset_pool_click = 0
        # 检查超过指定时间没有收到服务器数据就开启  断网返航
        self.last_command_time = time.time()
        self.b_network_backhome = 0
        # 设置的返航点
        self.set_home_gaode_lng_lat = None
        # 定点和返航
        self.back_home = 0
        self.fix_point = 0
        self.is_connected = 0
        self.charge_energy = 0
        self.run_distance = 0
        # 水质数据
        self.detect_lng_lat = None   # 检测数据点经纬度
        self.detect_gaode_lng_lat = None  # 检测数据点高德经纬度
        self.wt = None
        self.ph = None
        self.doDo = None
        self.cod = None
        self.ec = None
        # 进度
        self.progress = 0

        self.switch_data_dict = {
            # 检测 1 检测 没有该键表示不检测
            "b_sampling": 0,
            "b_drain": 0,
            # 抽水 1 抽水 没有该键或者0表示不抽水
            "b_draw": 0,
            # 前大灯 1 打开前大灯 没有该键或者0表示不打开
            "headlight": 0,
            # 声光报警器 1 打开声光报警器 没有该键或者0表示不打开
            "audio_light": 0,
            # 舷灯 1 允许打开舷灯 没有该键或者0表示不打开
            "side_light": 0,
        }
        # 地图对象
        self.baidu_map_obj = None

    def update_direction(self, target_direction):
        self.move_direction = target_direction
