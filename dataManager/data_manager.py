"""
数据收发
"""
import time
import os
import threading
import json
import numpy as np
import uuid

import config
from utils import log
from dataManager import lora_communication
from dataManager import mqtt_communication
from dataManager import data_define
from moveControl import build_map


class DataManager:
    def __init__(self, data_obj: data_define.DataDefine):
        self.logger = log.LogHandler('DataManager')
        self.data_obj = data_obj
        self.ip_lng_lat = None
        self.current_map_type = config.MapType.gaode
        if config.communication == config.CommunicationMethod.lora:
            self.receive_data_obj = lora_communication.LoraCommunication(data_obj)
        elif config.communication == config.CommunicationMethod.mqtt:
            self.receive_data_obj = mqtt_communication.MqttCommunication(log.LogHandler('MqttCommunication'),
                                                                         config.topics,
                                                                         data_obj)
            self.init_thread()



    def init_thread(self):
        """
        开启线程并监视线程
        :return:
        """
        func_list = [self.receive_data_obj.mqtt_send_get_obj.mqtt_connect,
                     ]
        thread_list = []
        for func in func_list:
            thread_list.append(threading.Thread(target=func))
        for thread in thread_list:
            thread.start()
        # while 1:
        #     for index,thread in enumerate(thread_list):
        #         if not thread.is_alive():
        #             thread_list[index] = threading.Thread(target=func_list[index])
        #             thread_list[index].start()
        #     time.sleep(1)

    def find_pool(self):
        """
        查找与更新湖泊id
        :return:
        """
        for i in range(len(config.MapType)):
            # 超过1000张图片时候删除图片
            save_img_name_list = os.listdir(config.save_img_dir)
            if len(save_img_name_list) > 1000:
                for i in save_img_name_list[0:950]:
                    print(os.path.join(config.save_img_dir, i))
                    os.remove(os.path.join(config.save_img_dir, i))
            if self.current_map_type == config.MapType.gaode:
                save_img_path = os.path.join(
                    config.save_img_dir, 'gaode_%f_%f_%i_%i.png' %
                                         (self.data_obj.click_lng_lat[0],
                                          self.data_obj.click_lng_lat[1],
                                          self.data_obj.click_zoom,
                                          1))
            elif self.current_map_type == config.MapType.tecent:
                save_img_path = os.path.join(
                    config.save_img_dir, 'tecent_%f_%f_%i_%i.png' %
                                         (self.data_obj.click_lng_lat[0],
                                          self.data_obj.click_lng_lat[1],
                                          self.data_obj.click_zoom,
                                          1))
            else:
                save_img_path = os.path.join(
                    config.save_img_dir, 'baidu_%f_%f_%i_%i.png' %
                                         (self.data_obj.click_lng_lat[0],
                                          self.data_obj.click_lng_lat[1],
                                          self.data_obj.click_zoom,
                                          1))
            # 创建于查找湖泊  不存在湖泊id未第一次查找和图片不存在为更新
            if self.data_obj.pool_code or not os.path.exists(save_img_path):
                # 创建地图对象
                if os.path.exists(save_img_path) and self.data_obj.baidu_map_obj is not None:
                    continue
                else:
                    self.data_obj.baidu_map_obj = build_map.BaiduMap(
                        lng_lat=self.data_obj.click_lng_lat,
                        zoom=self.data_obj.click_zoom,
                        map_type=self.current_map_type)
                pool_cnts, (pool_cx, pool_cy) = self.data_obj.baidu_map_obj.get_pool_pix()
                # 为None表示没有找到湖泊 继续换地图找
                if pool_cnts is None:
                    if self.current_map_type == config.MapType.gaode:
                        self.current_map_type = config.MapType.tecent
                        continue
                    if self.current_map_type == config.MapType.tecent:
                        self.current_map_type = config.MapType.baidu
                        continue
                    if self.current_map_type == config.MapType.baidu:
                        self.current_map_type = config.MapType.gaode
                        # 若返回为None表示没找到湖 定义错误代码
                        is_collision = 1
                        self.logger.error('无法在点击处找到湖泊')
                        return False
                # 获取湖泊轮廓与中心点经纬度位置 _位置为提供前端直接绘图使用
                _, self.data_obj.baidu_map_obj.pool_lng_lats = self.data_obj.baidu_map_obj.pix_to_gps(pool_cnts)
                _, self.data_obj.baidu_map_obj.pool_center_lng_lat = self.data_obj.baidu_map_obj.pix_to_gps(
                    [[pool_cx, pool_cy]])
                self.logger.info(
                    {'pool_center_lng_lat': self.data_obj.baidu_map_obj.pool_center_lng_lat})
                self.data_obj.baidu_map_obj.get_pool_name()
                if self.data_obj.baidu_map_obj.pool_name is not None:
                    config.pool_name = self.data_obj.baidu_map_obj.pool_name
                else:
                    config.pool_name = self.data_obj.baidu_map_obj.address

                self.logger.info({'config.pool_name': config.pool_name})
                # 判断当前湖泊是否曾经出现，出现过则获取的ID 没出现过发送请求获取新ID
                if isinstance(self.data_obj.baidu_map_obj.pool_cnts, np.ndarray):
                    save_pool_cnts = self.data_obj.baidu_map_obj.pool_cnts.tolist()
                else:
                    save_pool_cnts = self.data_obj.baidu_map_obj.pool_cnts
                send_data = {
                    "longitudeLatitude": json.dumps(
                        self.data_obj.baidu_map_obj.pool_center_lng_lat),
                    "mapData": json.dumps(
                        self.data_obj.baidu_map_obj.pool_lng_lats),
                    "deviceId": config.ship_code,
                    "name": config.pool_name,
                    "pixData": json.dumps(save_pool_cnts)}

                # 本地保存经纬度信息，放大1000000倍 用来只保存整数
                save_pool_lng_lats = [[int(i[0] * 1000000), int(i[1] * 1000000)]
                                      for i in self.data_obj.baidu_map_obj.pool_lng_lats]
                if not os.path.exists(config.local_map_data_path):
                    # 发送请求获取湖泊ID
                    pool_id = str(uuid.uuid4())
                    if isinstance(self.data_obj.baidu_map_obj.pool_cnts, np.ndarray):
                        save_pool_cnts = self.data_obj.baidu_map_obj.pool_cnts.tolist()
                    else:
                        save_pool_cnts = self.data_obj.baidu_map_obj.pool_cnts
                    save_data = {
                        "mapList": [
                            {
                                "id": pool_id,
                                "pool_center_lng_lat": self.data_obj.baidu_map_obj.pool_center_lng_lat,
                                "pool_lng_lats": save_pool_lng_lats,
                                "pool_cnts": save_pool_cnts}]}
                    self.logger.info({'pool_id': pool_id})
                    with open(config.local_map_data_path, 'w') as f:
                        json.dump(save_data, f)
                    self.data_obj.pool_code = pool_id
                else:
                    with open(config.local_map_data_path, 'r') as f:
                        local_map_data = json.load(f)
                        pool_id = build_map.is_in_contours(
                            (self.data_obj.baidu_map_obj.lng_lat[0] * 1000000,
                             self.data_obj.baidu_map_obj.lng_lat[1] * 1000000),
                            local_map_data)
                        print('pool_id', pool_id)
                    if pool_id is not None:
                        self.logger.info({'在本地找到湖泊 poolid': pool_id})
                    # 不存在获取新的id
                    else:
                        pool_id = str(uuid.uuid4())
                        self.logger.info({'新的湖泊 poolid': pool_id})
                        with open(config.local_map_data_path, 'w') as f:
                            # 以前存储键值
                            # local_map_data["mapList"].append({"id": pool_id,
                            #                                   "longitudeLatitude": self.baidu_map_obj.pool_center_lng_lat,
                            #                                   "mapData": self.baidu_map_obj.pool_lng_lat,
                            #                                   "pool_cnt": pool_cnts.tolist()})
                            if isinstance(self.data_obj.baidu_map_obj.pool_cnts, np.ndarray):
                                save_pool_cnts = self.data_obj.baidu_map_obj.pool_cnts.tolist()
                            local_map_data["mapList"].append(
                                {
                                    "id": pool_id,
                                    "pool_center_lng_lat": self.data_obj.baidu_map_obj.pool_center_lng_lat,
                                    "pool_lng_lats": save_pool_lng_lats,
                                    "pool_cnts": save_pool_cnts})
                            json.dump(local_map_data, f)
                self.data_obj.pool_code = pool_id

    # 发送数据
    def send_data(self, msg, send_type=config.CommunicationMethod.mqtt):
        if send_type == config.CommunicationMethod.mqtt:
            self.receive_data_obj.send_server_mqtt_data(msg[0], msg[1])
        else:
            # lora通讯暂时跳过
            pass

    # 接受数据
    def get_data(self):
        pass
