# coding:utf-8

import sys
from PyQt5.QtWidgets import QApplication, QDialog
import requests


def query_weather(city_name):
    city_code = get_code(city_name)
    url = "https://restapi.amap.com/v3/weather/weatherInfo?city={}&key=8177df6428097c5e23d3280ffdc5a13a".format(
        city_code)
    print(url)
    r = requests.get(url)
    print(r.json())
    if int(r.json().get('status')) == 1:
        weatherMsg = '城市：{}\n日期：{}\n天气：{}\n 温度：{}\n风力：{}\n'.format(
            r.json()['lives'][0]['province'] + '  ' + r.json()['lives'][0]['city'],
            r.json()['lives'][0]['reporttime'],
            r.json()['lives'][0]['weather'],
            r.json()['lives'][0]['temperature'],
            r.json()['lives'][0]['windpower'],
        )
    else:
        weatherMsg = '天气查询失败，请稍后再试！'
    return weatherMsg


def get_code(cityName):
    cityDict = {"武汉": "420100",
                "天门": "429006",
                "北京": "110101"}
    return cityDict.get(cityName, '110101')


def clear_text(self):
    self.ui.textEdit.clear()


if __name__ == '__main__':
    pass
