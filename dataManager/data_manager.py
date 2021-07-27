"""
数据收发
"""
import time
import threading
import config
from utils import log
from dataManager import lora_communication
from dataManager import mqtt_communication


class DataManager:
    def __init__(self, data_obj=None):
        if config.communication == config.CommunicationMethod.lora:
            self.receive_data_obj = lora_communication.LoraCommunication()
        elif config.communication == config.CommunicationMethod.mqtt:
            self.receive_data_obj = mqtt_communication.MqttCommunication(log.LogHandler('MqttCommunication'),
                                                                         config.topics)
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
