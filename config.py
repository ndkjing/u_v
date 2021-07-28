import enum
import platform
import os


class ShipControlStatus(enum.Enum):
    """
    船状态
    手动
    单点
    多点
    返航
    定点
    """
    hand_control = 1
    single_point = 2
    multi_points = 3
    backhome = 4
    fix_point=5

class MoveDirection(enum.Enum):
    forward = 0
    backward = 1
    left = 2
    right = 3
    stop = 4
    north = 5
    south = 6
    east = 7
    west = 8

class CommunicationMethod(enum.Enum):
    lora = 0
    mqtt = 1


communication = CommunicationMethod.mqtt


class CurrentPlatform(enum.Enum):
    windows = 1
    linux = 2
    pi = 3
    others = 4


sysstr = platform.system()
if sysstr == "Windows":
    print("Call Windows tasks")
    current_platform = CurrentPlatform.windows
elif sysstr == "Linux":  # 树莓派上也是Linux
    print("Call Linux tasks")
    # 公司Linux电脑名称
    if platform.node() == 'raspberrypi':
        current_platform = CurrentPlatform.pi
    else:
        current_platform = CurrentPlatform.linux
else:
    print("other System tasks")
    current_platform = CurrentPlatform.others

# 百度地图key
baidu_key = 'wIt2mDCMGWRIi2pioR8GZnfrhSKQHzLY'
# 高德秘钥
gaode_key = '8177df6428097c5e23d3280ffdc5a13a'
# 腾讯地图key
tencent_key = 'PSABZ-URMWP-3ATDK-VBRCR-FBBMF-YHFCE'

# 罗盘等待时间间隔
compass_timeout = 0.1
# 单片机发送给树莓派等待时间
stc2pi_timeout = 1
# 给单片机发送等待时间
pi2com_timeout = 0.05
# 给服务器发送时间间隔
pi2mqtt_interval = 1
# 上传给单片机心跳时间间隔 单位秒
# com_heart_time = 1 * 60
# 线程等待时间
thread_sleep_time = 0.5
# 船编号
ship_code = '3c50f4c3-a9c1-4872-9f18-883af014380c'
# 串口位置和波特率
# 单片机
# stc_port = '/dev/ttyAMA0'
stc_port = '/dev/ttyUSB0'
stc_baud = 115200
b_com_stc = os.path.exists(stc_port)
# http 接口
# 查询船是否注册  wuhanligong.xxlun.com/union
http_binding = 'http://wuhanligong.xxlun.com/union/admin/xxl/device/binding/%s' % (ship_code)
# 注册新的湖泊ID
http_save = 'http://wuhanligong.xxlun.com/union/admin/xxl/map/save'
# http_save = 'http://192.168.8.13:8009/union/admin/xxl/map/save'
# 发送检测数据
http_data_save = 'http://wuhanligong.xxlun.com/union/admin/xxl/data/save'
# http_data_save = 'http://192.168.199.186:8009/union/admin/xxl/data/save'
# mqtt服务器ip地址和端口号
mqtt_host = '47.97.183.24'
mqtt_port = 1884
# 调试的时候使用初始经纬度
ship_gaode_lng_lat = [114.524096, 30.506853]
# 电机前进分量
motor_forward = 200
# 电机转弯分量
motor_steer = 200
# pid三参数
kp = 2.0
ki = 0.3
kd = 1.0
# 大于多少米全速
full_speed_meter = 6.0
# 发送状态数据时间间隔
check_status_interval = 1.0
# 最大pwm值
max_pwm = 1800
# 最小pwm值
min_pwm = 1200
# 停止中位pwm
stop_pwm = 1500
# 左侧电机正反桨  0 正桨叶   1 反桨叶
left_motor_cw = 1
# 右侧电机正反桨  0 正桨叶   1 反桨叶
right_motor_cw = 0
# 抽水时间单位秒
draw_time = 30
# pid间隔
pid_interval = 0.2
# 开机前等待时间
start_sleep_time = 6
# 电机初始化时间
motor_init_time = 1
# 检查网络连接状态间隔
check_network_interval = 10
# 断网返航 0关闭  1开启 大于1的数值表示断网超过该值就返航，默认600秒
network_backhome = 1
# 剩余电量返航 0关闭  1开启 大于1的数值表示剩余电量低于该值就返航，默认30
energy_backhome = 1
# 最多查找连接点数量
find_points_num = 5
# TSP优化路径 0 不使用  1使用
b_tsp = 0
# 断网检查
b_check_network = 1
# 是否播放声音
b_play_audio = 0
# 不是在树莓派上都是用调试模式
if current_platform == CurrentPlatform.pi:
    home_debug = 0
else:
    home_debug = 1
# 添加避障方式设置0 不避障 1 避障停止  2 自动避障绕行 3 自动避障绕行和手动模式下避障停止
obstacle_avoid_type = 0
control_obstacle_distance = 2.5  # 手动模式避障距离 单位m
# 路径规划方式  0 不平滑路径 1 平滑路径
path_plan_type = 1
# 路径跟踪方式  1 pid
path_track_type = 1
# 校准罗盘  0 不校准 1 开始校准 2 结束校准
calibration_compass = 0
# 地图规划最小单位，米
cell_size = 2
# 是否使用平滑路径  1 平滑路径 0 不平滑
b_smooth_path = path_plan_type
# 平滑路径最小单位 m
smooth_path_ceil_size = 5
# 前视觉距离
forward_see_distance = 9
# 舵机最大扫描角度单侧 左边为正右边为负
steer_max_angle = 30
# 最小转向距离
min_steer_distance = 10  # 自动模式下避障距离 单位m
# 测试在家调试也发送数据
debug_send_detect_data = 0
# 转向速度
angular_velocity = 90

topics = [('pool_click_%s' % ship_code, 0),
          ('notice_info_%s' % ship_code, 0),
          ('detect_data_%s' % ship_code, 0),
          ('control_data_%s' % ship_code, 0),
          ('path_confirm_%s' % ship_code, 0),
          ('user_lng_lat_%s' % ship_code, 0),
          ('start_%s' % ship_code, 0),
          ('switch_%s' % ship_code, 0),
          ('pool_info_%s' % ship_code, 0),
          ('auto_lng_lat_%s' % ship_code, 0),
          ('path_planning_%s' % ship_code, 0),
          ('status_data_%s' % ship_code, 0),
          ('base_setting_%s' % ship_code, 0),
          ('height_setting_%s' % ship_code, 0),
          ('refresh_%s' % ship_code, 0),
          ('reset_pool_%s' % ship_code, 0),
          ('heart_%s' % ship_code, 0),
          ('set_home_%s' % ship_code, 0),
          ('poweroff_restart_%s' % ship_code, 0),
          ('path_planning_confirm_%s' % ship_code, 0)
          ]

video_src = 'rtmp://rtmp01open.ys7.com:1935/v3/openlive/D50551834_1_2?expire=1657329096&id' \
                          '=335347591388602368&t=e1dd42835fd9bece1478d0d19d68b727dafbb8630d96a1272d65c3f389dd9bca&ev' \
                          '=100 '