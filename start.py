# coding:utf-8
"""
入口函数
"""
import sys
import os
import urllib
import requests
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt, QPoint, QThread, QTimer

import main
from dataManager import data_define
from dataManager import data_manager
from utils import log

log = log.LogHandler('main')


class WebEngine(QWebEngineView):
    def __init__(self):
        super(WebEngine, self).__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)  # 设置右键菜单规则为自定义右键菜单


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.data_obj = data_define.DataDefine()
        self.data_manager_obj = data_manager.DataManager(self.data_obj)
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self)
        # 显示地图对象
        self.view = None
        # 初始化信号
        self.init_signal_slot()
        self.timer = QTimer()

    # 绑定信号连接
    def init_signal_slot(self):
        self.ui.forward_button.clicked.connect(self.update_move)
        self.ui.backword_button.clicked.connect(self.update_move)
        self.ui.left_button.clicked.connect(self.update_move)
        self.ui.right_button.clicked.connect(self.update_move)
        self.ui.stop_button.clicked.connect(self.update_move)

    # 初始化定时器
    def init_timer(self):
        self.timer.timeout.connect(self.map_center)
        self.timer.start(500)

    def update_move(self):
        sender = self.sender()
        if self.data_obj.move_mode == 1:
            if sender == self.ui.forward_button:
                self.data_obj.update_direction(data_define.MoveDirection.forward)
            if sender == self.ui.left_button:
                self.data_obj.update_direction(data_define.MoveDirection.left)
            if sender == self.ui.backword_button:
                self.data_obj.update_direction(data_define.MoveDirection.backward)
            if sender == self.ui.right_button:
                self.data_obj.update_direction(data_define.MoveDirection.right)
        else:
            if sender == self.ui.forward_button:
                self.data_obj.update_direction(data_define.MoveDirection.north)
            if sender == self.ui.left_button:
                self.data_obj.update_direction(data_define.MoveDirection.west)
            if sender == self.ui.backword_button:
                self.data_obj.update_direction(data_define.MoveDirection.south)
            if sender == self.ui.right_button:
                self.data_obj.update_direction(data_define.MoveDirection.east)
        if sender == self.ui.stop_button:
            self.data_obj.update_direction(data_define.MoveDirection.stop)
        print('move_direction', self.data_obj.move_direction)

    # 设置地图居中
    def map_center(self):
        if self.data_obj.lng_lat is not None and self.data_obj.zoom is not None:
            if self.data_obj.is_center:
                str_command = "window.set_zoom_and_center('%d','%f','%f')" % \
                              (self.data_obj.zoom, self.data_obj.lng_lat[0], self.data_obj.lng_lat[1])
                log.info(str_command)
                view.page().runJavaScript(str_command)

    # 在地图上添加标记物
    def map_add_marker(self):
        pass

    # 在地图上连线
    def map_add_line(self):
        pass

    # 点击地图上的经纬度
    @pyqtSlot(str, result=str)  # 第一个参数即为回调时携带的参数类型
    def send_lng_lat(self, str_args):
        log.info({'gps data': str_args})
        lng_lat_zoom = str_args.split(',')
        if len(lng_lat_zoom) == 3:
            self.data_obj.lng_lat = [float(lng_lat_zoom[0]), float(lng_lat_zoom[1])]
            self.data_obj.zoom = lng_lat_zoom[2]
            # print(self.data_obj.lng_lat, self.data_obj.zoom)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    view = WebEngine()
    channel = QWebChannel()
    channel.registerObject('PyHandler', myDlg)  # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
    view.page().setWebChannel(channel)  # 挂载前端处理对象
    url_string = urllib.request.pathname2url(os.path.join(os.getcwd(), "gaode.html"))  # 加载本地html文件
    view.load(QUrl(url_string))
    myDlg.ui.horizontalLayout_6.addWidget(view)
    myDlg.view = view
    myDlg.show()
    sys.exit(myapp.exec_())
