#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import urllib.request
import socket, platform
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt, QPoint
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json

class CallHandler(QObject):
    def __init__(self):
        super(CallHandler, self).__init__()

    @pyqtSlot(str, result=str)  # 第一个参数即为回调时携带的参数类型
    def init_home(self, str_args):
        print('resolving......init home..')
        print(str_args)  # 查看参数
        # #####
        # # 这里写对应的处理逻辑比如：
        # # msg = '收到来自python的消息'
        # msg = self.getInfo()
        # # view.page().runJavaScript("alert('%s')" % msg)
        # view.page().runJavaScript("window.say_hello('%s')" % msg)
        # return 'hello, Python'

    def getInfo(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        list_info = platform.uname()
        sys_name = list_info[0] + list_info[2]
        cpu_name = list_info[5]
        dic_info = {"hostname": hostname, "ip": ip, "sys_name": sys_name, \
                    "cpu_name": cpu_name}
        print(dic_info)
        # # 调用js函数，实现回调
        # self.mainFrame.evaluateJavaScript('%s(%s)' % ('onGetInfo', json.dumps(dic_info)))
        return json.dumps(dic_info)



class WebEngine(QWebEngineView):
    def __init__(self):
        super(WebEngine, self).__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)  # 设置右键菜单规则为自定义右键菜单
        # self.customContextMenuRequested.connect(self.showRightMenu)  # 这里加载并显示自定义右键菜单，我们重点不在这里略去了详细带吗

        self.setWindowTitle('QWebChannel与前端交互')
        self.resize(1100, 650)
        cp = QDesktopWidget().availableGeometry().center()
        self.move(QPoint(cp.x() - self.width() / 2, cp.y() - self.height() / 2))

if __name__ == '__main__':
    # 加载程序主窗口
    app = QApplication(sys.argv)
    view = WebEngine()
    channel = QWebChannel()
    handler = CallHandler()  # 实例化QWebChannel的前端处理对象
    channel.registerObject('PyHandler', handler)  # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
    view.page().setWebChannel(channel)  # 挂载前端处理对象
    url_string = urllib.request.pathname2url(os.path.join(os.getcwd(), "gaode.html"))  # 加载本地html文件
    view.load(QUrl(url_string))
    view.show()
    sys.exit(app.exec_())