"""
mqtt数据
"""
import config
from utils import poweroff_restart
import copy
import paho.mqtt.client as mqtt
import time
import json
import requests


class MqttCommunication:
    def __init__(self, logger,
                 topics,
                 data_obj):
        self.logger = logger
        self.topics = topics
        self.mqtt_send_get_obj = MqttSendGet(self.logger, topics=topics, data_obj=data_obj)

    # 发送数据到服务器http
    def send_server_http_data(self, request_type, data, url):
        # 请求头设置
        payload_header = {
            'Content-Type': 'application/json',
        }
        assert request_type in ['POST', 'GET']
        self.logger.info(url)
        if request_type == 'POST':
            dump_json_data = json.dumps(data)
            return_data = requests.post(
                url=url, data=dump_json_data, headers=payload_header)
        else:
            return_data = requests.get(url=url)
        return return_data

    # 发送数据到服务器mqtt
    def send_server_mqtt_data(self, topic='test', data="", qos=0):
        self.mqtt_send_get_obj.publish_topic(topic=topic, data=data, qos=qos)


class MqttSendGet:
    """
    处理mqtt数据收发
    """

    def __init__(
            self,
            logger,
            topics,
            data_obj,
            mqtt_host=config.mqtt_host,
            mqtt_port=config.mqtt_port,
            client_id=config.ship_code

    ):
        self.data_obj = data_obj
        self.topics = topics
        self.logger = logger
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        if config.current_platform == config.CurrentPlatform.pi:
            client_id = client_id + '_pi'
            self.mqtt_user = 'linux_pi'
        elif config.current_platform == config.CurrentPlatform.linux:
            client_id = client_id + 'linux'
            self.mqtt_user = 'linux'
        else:
            client_id = client_id + 'windows_client'
            self.mqtt_user = 'windows'
        self.mqtt_passwd = 'public'
        self.mqtt_client = mqtt.Client(client_id=client_id)
        self.mqtt_client.username_pw_set(self.mqtt_user, password=self.mqtt_passwd)
        self.mqtt_client.on_connect = self.on_connect_callback
        self.mqtt_client.on_publish = self.on_publish_callback
        # self.mqtt_client.on_subscribe = self.on_message_come
        self.mqtt_client.on_message = self.on_message_callback
        self.last_command_time = time.time()
        self.is_connected = 0

    # 连接MQTT服务器
    def mqtt_connect(self):
        while True:
            if not self.is_connected:
                try:
                    self.mqtt_client.connect(self.mqtt_host, self.mqtt_port, 30)
                    # 开启接收循环，直到程序终止
                    self.mqtt_client.loop_start()
                    self.is_connected = 1
                    # 启动后自动订阅话题
                    for topic_, qos_ in self.topics:
                        self.subscribe_topic(topic=topic_, qos=qos_)
                except TimeoutError:
                    pass
            else:
                time.sleep(5)

    # 建立连接时候回调
    def on_connect_callback(self, client, userdata, flags, rc):
        self.logger.info('Connected with result code:  ' + str(rc))

    # 发布消息回调
    def on_publish_callback(self, client, userdata, mid):
        pass

    # 消息处理函数回调
    def on_message_callback(self, client, userdata, msg):
        topic = msg.topic
        # 处理初始点击确定湖数据
        if topic == 'pool_click_%s' % config.ship_code:
            pool_click_data = json.loads(msg.payload)
            if pool_click_data.get('lng_lat') is None:
                self.logger.error('pool_click  用户点击经纬度数据没有经纬度字段')
                return
            if pool_click_data.get('zoom') is None:
                self.logger.error('pool_click 用户点击经纬度数据没有zoom字段')
                return
            lng_lat = pool_click_data.get('lng_lat')
            self.data_obj.pool_click_lng_lat = lng_lat
            zoom = int(round(float(pool_click_data.get('zoom')), 0))
            self.data_obj.pool_click_zoom = zoom
            self.data_obj.b_pool_click = 1
            self.logger.info({'topic': topic,
                              'lng_lat': pool_click_data.get('lng_lat'),
                              'zoom': pool_click_data.get('zoom')
                              })

        # 用户点击经纬度和图层 保存到指定路径
        elif topic == 'detect_data_%s' % config.ship_code:
            detect_data = json.loads(msg.payload)
            if detect_data.get('water') is None:
                self.logger.error('detect_data_没有water字段')
                return
            self.data_obj.detect_lng_lat = detect_data.get("jwd")
            self.data_obj.detect_gaode_lng_lat = detect_data.get("gjwd")
            self.data_obj.wt = detect_data.get('water').get('wt')
            self.data_obj.ph = detect_data.get('water').get('ph')
            self.data_obj.doDo = detect_data.get('water').get('doDo')
            self.data_obj.cod = detect_data.get('water').get('cod')
            self.data_obj.ec = detect_data.get('water').get('ec')
            self.logger.info({'topic': topic,
                              'wt': self.data_obj.wt,
                              'ph': self.data_obj.ph,
                              'doDo': self.data_obj.doDo,
                              'cod': self.data_obj.cod,
                              'ec': self.data_obj.ec,
                              })

        # 用户点击经纬度和图层 保存到指定路径
        elif topic == 'user_lng_lat_%s' % config.ship_code:
            user_lng_lat_data = json.loads(msg.payload)
            if user_lng_lat_data.get('lng_lat') is None:
                self.logger.error('user_lng_lat_用户点击经纬度数据没有经纬度字段')
                return
            if user_lng_lat_data.get('zoom') is None:
                self.logger.error('user_lng_lat_用户点击经纬度数据没有zoom字段')
                return
            if user_lng_lat_data.get('meter_pix') is None:
                self.logger.error('user_lng_lat_用户点击经纬度数据没有meter_pix字段')
            if user_lng_lat_data.get('config') is None:
                self.logger.error('user_lng_lat_用户点击经纬度数据没有config字段')

            # 添加新的点
            lng_lat = user_lng_lat_data.get('lng_lat')
            self.data_obj.target_lng_lat = lng_lat
            self.data_obj.target_lng_lat_status = [0] * len(lng_lat)
            zoom = int(round(float(user_lng_lat_data.get('zoom')), 0))
            self.data_obj.zoom.append(zoom)
            self.data_obj.meter_pix.update({zoom: float(user_lng_lat_data.get('meter_pix'))})
            if user_lng_lat_data.get('config').get('back_home') is not None:
                self.data_obj.back_home = user_lng_lat_data.get('config').get('back_home')
            self.logger.info({'topic': topic,
                              'target_lng_lat': self.data_obj.target_lng_lat,
                              'zoom': zoom,
                              'meter_pix': user_lng_lat_data.get('meter_pix'),
                              'back_home': self.data_obj.back_home,
                              })

        # 用户设置自动求取检测点经纬度
        elif topic == 'auto_lng_lat_%s' % config.ship_code:
            auto_lng_lat_data = json.loads(msg.payload)
            if auto_lng_lat_data.get('config') is None:
                self.logger.error('auto_lng_lat_用户设置自动求取检测点经纬度没有config字段')
                return
            if auto_lng_lat_data.get('config').get('row_gap') is None:
                self.logger.error('auto_lng_lat_用户设置自动求取检测点经纬度config字段没有row_gap')
                return
            self.data_obj.row_gap = auto_lng_lat_data.get('config').get('row_gap')
            self.data_obj.col_gap = auto_lng_lat_data.get('config').get('col_gap')
            if auto_lng_lat_data.get('config').get('safe_gap') is not None:
                self.data_obj.safe_gap = auto_lng_lat_data.get('config').get('safe_gap')
            self.data_obj.round_pool_gap = auto_lng_lat_data.get('config').get('round_pool_gap')
            self.logger.info({'topic': topic,
                              'row_gap': self.data_obj.row_gap,
                              'col_gap': self.data_obj.col_gap,
                              'safe_gap': self.data_obj.safe_gap,
                              'round_pool_gap': self.data_obj.round_pool_gap})

        # 返回路径规划点
        elif topic == 'path_planning_%s' % config.ship_code:
            path_planning_data = json.loads(msg.payload)
            if path_planning_data.get('path_points') is None:
                self.logger.error('path_planning_用户确认轨迹 没有path_points字段')
                return
            self.path_planning_points = path_planning_data.get('path_points')
            self.path_planning_points_status = [0] * len(self.path_planning_points)
            self.logger.info({'topic': topic,
                              'path_points': path_planning_data.get('path_points'),
                              })

        # 启动设备
        elif topic == 'start_%s' % config.ship_code:
            start_data = json.loads(msg.payload)
            if not start_data.get('search_pattern'):
                self.logger.error('start_设置启动消息没有search_pattern字段')
                return
            self.data_obj.b_start = int(start_data.get('search_pattern'))
            self.logger.info({'topic': topic, 'b_start': start_data.get('search_pattern')})

        # 湖泊id
        elif topic == 'pool_info_%s' % config.ship_code:
            pool_info_data = json.loads(msg.payload)
            if not pool_info_data.get('mapId'):
                self.logger.error('pool_info_data设置启动消息没有mapId字段')
                return
            self.data_obj.pool_id = str(pool_info_data.get('mapId'))
            self.logger.info({'topic': topic, 'mapId': pool_info_data.get('mapId')})

        # 服务器从状态数据中获取 当前经纬度
        elif topic == 'status_data_%s' % config.ship_code:
            status_data = json.loads(msg.payload)
            if status_data.get("current_lng_lat") is None:
                self.logger.error('"status_data"设置启动消息没有"current_lng_lat"字段')
            else:
                self.data_obj.current_lng_lat = status_data.get('current_lng_lat')
            if status_data.get("home_lng_lat") is not None:
                self.data_obj.home_lng_lat = status_data.get('home_lng_lat')
            self.data_obj.charge_energy = status_data.get('charge_energy')
            self.data_obj.head_direction = status_data.get('direction')
            self.data_obj.speed = status_data.get('speed')
            self.data_obj.run_distance = status_data.get('run_distance')

        elif topic == 'notice_info_%s' % config.ship_code:
            notice_info_data = json.loads(msg.payload)
            if notice_info_data.get("progress") is None:
                self.logger.error('notice_info_设置启动消息没有progress字段')
                self.data_obj.progress = 1
            else:
                self.data_obj.progress = max(int(notice_info_data.get("progress"))+1,100)
            self.data_obj.pool_code = notice_info_data['mapId']

        # 基本设置
        elif topic == 'base_setting_%s' % config.ship_code:
            base_setting_data = json.loads(msg.payload)
            info_type = base_setting_data.get("info_type")
            if info_type == 3:
                self.data_obj.base_setting_data = base_setting_data
            elif info_type == 1:
                pass
            elif info_type == 1:
                pass
            elif info_type == 4:
                pass
            self.logger.info(base_setting_data)

        # 高级设置
        elif topic == 'height_setting_%s' % config.ship_code:
            height_setting_data = json.loads(msg.payload)
            info_type = height_setting_data.get("info_type")
            if info_type == 3:
                self.data_obj.height_setting_data = height_setting_data
            elif info_type == 1:
                pass
            elif info_type == 1:
                pass
            elif info_type == 4:
                pass
            print(self.data_obj.height_setting_data)
            self.logger.info(height_setting_data)

    # 发布消息
    def publish_topic(self, topic, data, qos=0):
        """
        向指定话题发布消息
        :param topic 发布话题名称
        :param data 　发布消息
        :param qos　　发布质量
        """
        if isinstance(data, list):
            data = str(data)
            self.mqtt_client.publish(topic, payload=data, qos=qos)
        elif isinstance(data, dict):
            data = json.dumps(data)
            self.mqtt_client.publish(topic, payload=data, qos=qos)
        elif isinstance(data, int) or isinstance(data, float):
            data = str(data)
            self.mqtt_client.publish(topic, payload=data, qos=qos)
        else:
            self.mqtt_client.publish(topic, payload=data, qos=qos)

    # 订阅消息
    def subscribe_topic(self, topic='qqq', qos=0):
        """
        :param topic 订阅的话题
        :param qos　　发布质量
        """
        self.logger.info({'topic': topic, 'qos': qos})
        self.mqtt_client.subscribe(topic, qos)
