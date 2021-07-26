"""
数据收发
"""
import enum
import config
from utils import log
from dataManager import lora_communication
from dataManager import mqtt_communication


class DataManager:
    def __init__(self, receiver_data_type):
        if config.communication == config.CommunicationMethod.lora:
            self.receive_data_obj = lora_communication.LoraCommunication()
        elif config.communication == config.CommunicationMethod.mqtt:
            self.receive_data_obj = mqtt_communication.MqttCommunication(log.LogHandler('MqttCommunication'),
                                                                         config.topics)

    # 发送数据
    def send_data(self):
        pass

    # 接受数据
    def get_data(self):
        pass
