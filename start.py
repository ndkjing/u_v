# coding:utf-8
"""
入口函数
"""
import sys
import os
import time
import cv2
import urllib
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QGridLayout
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, Qt, QPoint, QThread, QTimer, QDateTime

import main
from dataManager import data_define
from dataManager import data_manager
from utils import log
from utils import opencv_radar_scan

import config
logger = log.LogHandler('main')


class WebEngine(QWebEngineView):
    def __init__(self):
        super(WebEngine, self).__init__()
        # self.setContextMenuPolicy(Qt.NoContextMenu)  # 设置右键菜单规则为自定义右键菜单


class CameraThread(QThread):
    """
    摄像头对象
    """

    def __init__(self, url, out_label, parent=None, run_func=None):
        """初始化方法"""
        super().__init__(parent)
        self.url = url
        self.outLabel = out_label
        self.run_func = run_func

    def run(self):
        self.run_func(self.url, self.outLabel)


class DistanceShowThread(QThread):
    """
    摄像头对象
    """
    def __init__(self, radar_obj, parent=None, run_func=None):
        """初始化方法"""
        super().__init__(parent)
        self.radar_obj = radar_obj
        self.run_func = run_func

    def run(self):
        self.run_func(self.radar_obj)


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle('uuv')
        self.setWindowIcon(QIcon('statics/logo.ico'))
        self.data_obj = data_define.DataDefine()
        self.data_manager_obj = data_manager.DataManager(self.data_obj)
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self)
        # 显示地图对象
        self.view = None
        # 显示视频
        self.frame = None
        self.open_flag = False
        self.video_work = CameraThread(url=config.video_src, out_label=self.ui.video_label,
                                       parent=None,
                                       run_func=self.display_video)
        self.video_work.start()
        # 显示障碍物
        self.radar_obj = opencv_radar_scan.RadarScan()
        self.radar_work = DistanceShowThread(radar_obj=self.radar_obj,
                                       parent=None,
                                       run_func=self.display_distance)
        self.radar_work.start()
        # 初始化信号
        self.init_signal_slot()
        self.timer = QTimer()
        self.init_timer()

    # 绑定信号连接
    def init_signal_slot(self):
        # 测试使用
        # self.ui.forward_button.clicked.connect(self.map_add_line)
        # 刷新页面
        self.ui.reload_button.clicked.connect(self.reload_view)
        # 重选湖泊
        self.ui.reselect_button.clicked.connect(self.reselect_pool)
        # 手动控制按键信号
        self.ui.forward_button.clicked.connect(self.update_move)
        self.ui.backword_button.clicked.connect(self.update_move)
        self.ui.left_button.clicked.connect(self.update_move)
        self.ui.right_button.clicked.connect(self.update_move)
        self.ui.stop_button.clicked.connect(self.update_move)
        # 绑定用于手动按键时切换
        self.ui.forward_button.clicked.connect(self.update_control_status)
        self.ui.backword_button.clicked.connect(self.update_control_status)
        self.ui.left_button.clicked.connect(self.update_control_status)
        self.ui.right_button.clicked.connect(self.update_control_status)
        self.ui.stop_button.clicked.connect(self.update_control_status)
        # 自动控制模式设置
        self.ui.single_point_button.clicked.connect(self.update_control_status)
        self.ui.multi_points_button.clicked.connect(self.update_control_status)
        self.ui.backhome_button.clicked.connect(self.update_control_status)
        self.ui.fix_point_button.clicked.connect(self.update_control_status)

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            os._exit(0)
        else:
            event.ignore()

    def display_video(self, url, label):
        """显示"""
        cap = cv2.VideoCapture(url)
        start_time = time.time()
        print(cap, cap.isOpened())
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                if (time.time() - start_time) > 0.1:
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    self.frame = frame
                    # print(self.ui.video_label.width(), self.ui.video_label.height())
                    frame = cv2.resize(frame, (self.ui.video_label.width(), self.ui.video_label.height()),
                                       interpolation=cv2.INTER_AREA)
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    label.setPixmap(QPixmap.fromImage(img))
                    cv2.waitKey(1)
                    start_time = time.time()

    def display_distance(self, radar_scan_obj):
        """显示"""
        start_time = time.time()
        while 1:
            if (time.time() - start_time) > 0.1:
                frame = radar_scan_obj.get_img()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                # frame = cv2.resize(frame, (self.ui.distance_show_label.width(), self.ui.distance_show_label.height()),
                #                    interpolation=cv2.INTER_AREA)
                resize = min(self.ui.distance_show_label.width(), self.ui.distance_show_label.height())
                resize = int(resize*0.75)
                # print('distance label',resize,self.ui.distance_show_label.width(), self.ui.distance_show_label.height())
                frame = cv2.resize(frame, (resize, resize),
                                   interpolation=cv2.INTER_AREA)
                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.ui.distance_show_label.setPixmap(QPixmap.fromImage(img))
                cv2.waitKey(1)
                start_time = time.time()

    def reselect_pool(self):
        """
        重新选择湖泊
        :return:
        """
        # TODO

    def reload_view(self):
        """
        刷新地图页面
        :return:
        """
        view.reload()

    # 初始化定时器
    def init_timer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.timeout.connect(self.map_center)
        timer.start(1000)

    def update_control_status(self):
        """
        更新运动模式：单点 多点 返航
        :return:
        """
        sender = self.sender()
        if sender == self.ui.single_point_button:
            self.set_auto_button_check(True)
            self.ui.single_point_button.setChecked(True)
            self.data_obj.control_mode = config.ShipControlStatus.single_point

        elif sender == self.ui.multi_points_button:
            self.set_auto_button_check(True)
            self.ui.multi_points_button.setChecked(True)
            self.data_obj.control_mode = config.ShipControlStatus.multi_points

        elif sender == self.ui.backhome_button:
            self.set_auto_button_check(True)
            self.ui.backhome_button.setChecked(True)
            self.data_obj.control_mode = config.ShipControlStatus.backhome
        elif sender == self.ui.fix_point_button:
            self.set_auto_button_check(True)
            self.ui.fix_point_button.setChecked(True)
            self.data_obj.control_mode = config.ShipControlStatus.fix_point
        else:
            self.data_obj.control_mode = config.ShipControlStatus.hand_control
            self.set_auto_button_check(False)
        logger.info({'self.data_obj.control_mode': self.data_obj.control_mode})
        self.update()

    def set_auto_button_check(self, checkable: bool):
        """
        设置自动按钮是否是可选模式
        :return:
        """
        self.ui.single_point_button.setCheckable(checkable)
        self.ui.multi_points_button.setCheckable(checkable)
        self.ui.backword_button.setCheckable(checkable)
        self.ui.fix_point_button.setCheckable(checkable)
        self.update()

    def showtime(self):
        """
        显示时间标签
        :return:
        """
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        self.ui.time_label.setText("  " + text)

    def update_move(self):
        sender = self.sender()
        data_dict = {"deviceId": config.ship_code, "mode": self.data_obj.move_mode}
        if self.data_obj.move_mode == 1:
            if sender == self.ui.forward_button:
                self.data_obj.update_direction(config.MoveDirection.forward)
                data_dict.update({"move_direction": 0})
            if sender == self.ui.left_button:
                self.data_obj.update_direction(config.MoveDirection.left)
                data_dict.update({"move_direction": 90})
            if sender == self.ui.backword_button:
                self.data_obj.update_direction(config.MoveDirection.backward)
                data_dict.update({"move_direction": 180})
            if sender == self.ui.right_button:
                self.data_obj.update_direction(config.MoveDirection.right)
                data_dict.update({"move_direction": 270})
        else:
            if sender == self.ui.forward_button:
                self.data_obj.update_direction(config.MoveDirection.north)
                data_dict.update({"move_direction": 0})
            if sender == self.ui.left_button:
                self.data_obj.update_direction(config.MoveDirection.west)
                data_dict.update({"move_direction": 90})
            if sender == self.ui.backword_button:
                self.data_obj.update_direction(config.MoveDirection.south)
                data_dict.update({"move_direction": 180})
            if sender == self.ui.right_button:
                self.data_obj.update_direction(config.MoveDirection.east)
                data_dict.update({"move_direction": 270})
        if sender == self.ui.stop_button:
            self.data_obj.update_direction(config.MoveDirection.stop)
            data_dict.update({"move_direction": -1})
        msg = (
            "control_data_%s" % config.ship_code,
            data_dict
        )
        self.data_manager_obj.send_data(msg=msg)

    # 设置地图居中
    def map_center(self):
        if self.data_obj.lng_lat is not None and self.data_obj.zoom is not None:
            if self.data_obj.is_center:
                str_command = "window.set_zoom_and_center('%d','%f','%f')" % \
                              (self.data_obj.zoom, self.data_obj.lng_lat[0], self.data_obj.lng_lat[1])
                logger.info(str_command)
                view.page().runJavaScript(str_command)

    # 在地图上添加标记物
    def map_add_marker(self):
        str_command = "window.add_marker('%f','%f')" % \
                      (self.data_obj.lng_lat[0], self.data_obj.lng_lat[1])
        logger.info(str_command)
        view.page().runJavaScript(str_command)

    # 在地图上连线
    def map_add_line(self):
        line_list = [
            [114.144539, 30.492879],
            [114.153809, 30.490808],
            [114.153809, 30.500808]
        ]
        str_command = "window.add_line(line_list)"
        logger.info(str_command)
        view.page().runJavaScript(str_command)

    # 点击地图上的经纬度
    @pyqtSlot(str, result=str)  # 第一个参数即为回调时携带的参数类型
    def send_lng_lat(self, str_args):
        logger.info({'gps data': str_args})
        lng_lat_zoom = str_args.split(',')
        print('lng_lat_zoom', lng_lat_zoom)
        if len(lng_lat_zoom) == 3:
            self.data_obj.lng_lat = [float(lng_lat_zoom[0]), float(lng_lat_zoom[1])]
            self.data_obj.zoom = int(lng_lat_zoom[2])
            self.map_add_marker()
            if self.data_obj.control_mode == config.ShipControlStatus.single_point:
                send_dict = {
                    # 设备号
                    "deviceId": config.ship_code,
                    # 点击经纬度一维数组 先经度 后纬度
                    "lng_lat": self.data_obj.lng_lat,
                    # 点击地图的图层
                    "zoom": self.data_obj.zoom,
                }
                msg = (
                    'pool_click_%s' % config.ship_code,
                    send_dict
                )
                print('send data', msg)

                self.data_manager_obj.send_data(msg=msg)


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
