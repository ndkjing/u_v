# coding:utf-8
"""
入口函数
"""
import sys
import json
import os
import time
import cv2
import urllib
from PyQt5.QtWidgets import QMainWindow, QLabel, QDialog
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtGui import QIcon, QPixmap, QImage, QMovie
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot, QUrl, Qt, QThread, QTimer, QDate
from qt_material import apply_stylesheet

from ui import main_ui, base_setting_ui, advance_setting_ui,author_ui
from dataManager import data_define
from dataManager import data_manager
from utils import log
from utils import opencv_radar_scan

import config

logger = log.LogHandler('main')


class BaseSettingWindow(QDialog):
    base_setting_signal = QtCore.pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)
        self.ui = base_setting_ui.Ui_Form()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出基础设置页面？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.base_setting_signal.emit()
            print('exit base setting')
        else:
            event.ignore()

class AuthorWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = author_ui.Ui_Form()
        self.ui.setupUi(self)

    # def closeEvent(self, event):
    #     """
    #     对MainWindow的函数closeEvent进行重构
    #     退出软件时结束所有进程
    #     :param event:
    #     :return:
    #     """
    #     reply = QtWidgets.QMessageBox.question(self,
    #                                            '本程序',
    #                                            "是否要退出基础设置页面？",
    #                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #                                            QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #         self.base_setting_signal.emit()
    #         print('exit base setting')
    #     else:
    #         event.ignore()

class AdvanceSettingWindow(QDialog):
    advance_setting_signal = QtCore.pyqtSignal()

    def __init__(self):
        QDialog.__init__(self)
        self.ui = advance_setting_ui.Ui_Form()
        self.ui.setupUi(self)

    def closeEvent(self, event):
        """
        对MainWindow的函数closeEvent进行重构
        退出软件时结束所有进程
        :param event:
        :return:
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出高级设置页面？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.advance_setting_signal.emit()
            print('exit base setting')
        else:
            event.ignore()


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


class DropAreaLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super(DropAreaLabel, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        print("drag event")
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("drop event")
        files = list()
        urls = [u for u in event.mimeData().urls()]
        for url in urls:
            print(url.path())
            files.append(url.toLocalFile())
        print(files)


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


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setWindowTitle('uuv')
        self.setWindowIcon(QIcon('statics/logo.ico'))
        self.data_obj = data_define.DataDefine()
        self.data_manager_obj = data_manager.DataManager(self.data_obj)
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.resize(1532, 1160)
        # 基础设置界面
        self.base_setting_obj = BaseSettingWindow()
        # 高级设置页面
        self.advance_setting_obj = AdvanceSettingWindow()
        self.author_obj = AuthorWindow()
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
        # 美化
        self.decorate_page()
        self.init_widget()
        # 显示状态消息
        self.show_status()

    def init_widget(self):
        """
        初始化控件设置和内容信息
        :return:
        """
        is_show_gif = False
        if is_show_gif:
            movie = QMovie("./statics/ship.gif")
            self.ui.logo_label.setMovie(movie)
            self.ui.logo_label.setMinimumSize(10, 10)
            self.ui.logo_label.setMaximumSize(self.ui.logo_label.height(), self.ui.logo_label.width())
            movie.start()
        else:
            # 设置logo 拖放失败
            pix = QPixmap('./statics/logo.ico')
            self.ui.logo_label.setPixmap(pix)
            self.ui.logo_label.setScaledContents(True)
        # 设置距离显示7位数 单位m 小数点前5位 小数点占一位 小数点后占一位
        self.ui.distance_lcd.setDigitCount(7)

    # def resizeEvent(self, event):
    #     rect = self.ui.logo_label.geometry()
    #     size = min(rect.width(), rect.height())
    #     movie = self.self.ui.logo_label.movie()
    #     movie.setScaledSize(QtCore.QSize(size, size))
    #     self.ui.logo_label.adjustSize()

    def update_switch(self):
        """
        更新外围继电器控制信息
        :return:
        """
        sender = self.sender()
        if sender == self.ui.draw_push_button:
            self.data_obj.switch_data_dict["b_draw"] = 1 if not self.data_obj.switch_data_dict["b_draw"] else 0
        elif sender == self.ui.drain_push_button:
            self.data_obj.switch_data_dict["b_drain"] = 1 if not self.data_obj.switch_data_dict["b_drain"] else 0
        elif sender == self.ui.head_light_push_button:
            self.data_obj.switch_data_dict["headlight"] = 1 if not self.data_obj.switch_data_dict["headlight"] else 0
        elif sender == self.ui.side_light_push_button:
            self.data_obj.switch_data_dict["side_light"] = 1 if not self.data_obj.switch_data_dict["side_light"] else 0
        msg = (
            "switch_%s" % config.ship_code,
            self.data_obj.switch_data_dict
        )
        logger.info(msg)
        self.data_manager_obj.send_data(msg=msg)

    def show_status(self, status_msg=None):
        """
        在状态栏显示消息
        :param status_msg:
        :return:
        """
        if status_msg is not None:
            self.statusBar().showMessage(status_msg)
        else:
            self.statusBar().showMessage('准备就绪')

    def decorate_page(self):
        pass

    # 绑定信号连接
    def init_signal_slot(self):
        # 测试使用
        self.ui.forward_button.clicked.connect(self.map_add_line)
        # 刷新页面
        self.ui.reload_button.clicked.connect(self.reload_view)
        # 重选湖泊
        self.ui.reselect_button.clicked.connect(self.reselect_pool)
        # 手动控制按键信号
        self.ui.mode_push_button.clicked.connect(self.update_mode)
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
        # 绑定动作
        self.ui.base_setting_action.triggered.connect(self.open_base_setting)
        self.ui.advance_setting_action.triggered.connect(self.open_advance_setting)
        # 绑定外设控制
        self.ui.draw_push_button.clicked.connect(self.update_switch)
        self.ui.drain_push_button.clicked.connect(self.update_switch)
        self.ui.head_light_push_button.clicked.connect(self.update_switch)
        self.ui.side_light_push_button.clicked.connect(self.update_switch)
        # 绑定基本设置和高级设置
        self.ui.base_setting_action.triggered.connect(self.get_base_setting_data)
        self.ui.advance_setting_action.triggered.connect(self.get_advance_setting_data)
        self.ui.about_author_action.triggered.connect(self.show_author)
        # 绑定设置页面退出信号
        self.base_setting_obj.base_setting_signal.connect(self.send_base_setting_data)
        self.advance_setting_obj.advance_setting_signal.connect(self.send_advance_setting_data)

    def show_author(self):
        self.author_obj.show()

    def get_base_setting_input_data(self):
        """
        获取基础设置页面当前输入信息
        :return:base setting data dict
        """
        base_input_dict = {}
        base_input_dict["arrive_range"] = float(self.base_setting_obj.ui.arriver_distance_line_edit.text())
        base_input_dict["speed_grade"] = self.base_setting_obj.ui.speed_grade_combo_box.currentIndex() + 1
        base_input_dict["secure_distance"] = int(self.base_setting_obj.ui.safe_distance_line_edit.text())
        base_input_dict["row"] = int(self.base_setting_obj.ui.sample_distance_line_edit.text())
        base_input_dict["keep_point"] = int(self.base_setting_obj.ui.search_points_line_edit.text())
        return base_input_dict

    def get_advance_setting_input_data(self):
        """
        获取高级设置页面当前输入信息
        :return:
        """
        advance_input_dict = {}
        advance_input_dict["stop_pwm"] = self.advance_setting_obj.ui.stop_pwm_spin_box.value()
        if self.advance_setting_obj.ui.left_positive_radio_button.isChecked():
            advance_input_dict["left_motor_cw"] = 0
        else:
            advance_input_dict["left_motor_cw"] = 1
        if self.advance_setting_obj.ui.right_positive_radio_button.isChecked():
            advance_input_dict["right_motor_cw"] = 0
        else:
            advance_input_dict["right_motor_cw"] = 1
        advance_input_dict["kp"] = self.advance_setting_obj.ui.kp_spin_box.value() / 10.0
        advance_input_dict["ki"] = self.advance_setting_obj.ui.ki_spin_box.value() / 10.0
        advance_input_dict["kd"] = self.advance_setting_obj.ui.kd_spin_box.value() / 10.0
        advance_input_dict["max_pwm"] = int(self.advance_setting_obj.ui.max_pwm_line_edit.text())
        advance_input_dict["min_pwm"] = int(self.advance_setting_obj.ui.min_pwm_line_edit.text())
        advance_input_dict["full_speed_meter"] = int(self.advance_setting_obj.ui.full_speed_line_edit.text())
        advance_input_dict["check_status_interval"] = self.advance_setting_obj.ui.check_status_spin_box.value()
        advance_input_dict["check_network_interval"] = self.advance_setting_obj.ui.check_connect_spin_box.value()
        advance_input_dict["draw_time"] = str(self.advance_setting_obj.ui.tasking_spin_box.value())
        advance_input_dict["home_debug"] = int(self.advance_setting_obj.ui.is_debug_radio_button.isChecked())
        advance_input_dict["b_play_audio"] = int(self.advance_setting_obj.ui.is_play_audio_radio_button.isChecked())
        advance_input_dict["path_track_type"] = self.advance_setting_obj.ui.path_track_combo_box.currentIndex() + 1
        advance_input_dict["path_plan_type"] = self.advance_setting_obj.ui.path_planning_combo_box.currentIndex() + 1
        advance_input_dict["obstacle_avoid_type"] = self.advance_setting_obj.ui.avoidance_combo_box.currentIndex() + 1
        advance_input_dict["b_tsp"] = int(self.advance_setting_obj.ui.is_use_tsp_radio_button.isChecked())
        advance_input_dict["network_backhome"] = int(
            self.advance_setting_obj.ui.network_backhome_radio_button.isChecked())
        advance_input_dict["energy_backhome"] = int(
            self.advance_setting_obj.ui.energy_backhome_radio_button.isChecked())
        advance_input_dict["calibration_compass"] = int(self.advance_setting_obj.ui.celebrate_push_button.isChecked())
        return advance_input_dict

    def send_base_setting_data(self):
        if self.data_obj.base_setting_data is None:
            pass
        else:
            base_input_dict = self.get_base_setting_input_data()
            print(base_input_dict)
            is_send_data = False
            for key, value in base_input_dict.items():
                if self.data_obj.base_setting_data.get(key) != value:
                    print('key', key, self.data_obj.base_setting_data.get(key), value)
                    is_send_data = True
            if is_send_data:
                base_input_dict["info_type"] = 2
                msg = (
                    "base_setting_%s" % config.ship_code,
                    base_input_dict
                )
                logger.info(msg)
                self.data_manager_obj.send_data(msg=msg)
            else:
                logger.info('没有改变基础设置数据')

    def send_advance_setting_data(self):
        if self.data_obj.height_setting_data is None:
            pass
        else:
            advance_input_data = self.get_advance_setting_input_data()
            is_send_data = False
            for key, value in advance_input_data.items():
                if self.data_obj.height_setting_data.get(key) != value:
                    print(type(self.data_obj.height_setting_data.get(key)), type(value))
                    print('key', key, self.data_obj.height_setting_data.get(key), value)
                    is_send_data = True
            if is_send_data:
                advance_input_data["info_type"] = 2
                msg = (
                    "height_setting_%s" % config.ship_code,
                    advance_input_data
                )
                logger.info(msg)
                self.data_manager_obj.send_data(msg=msg)
            else:
                logger.info('没有改变高级设置数据')

    def get_base_setting_data(self):
        """
        获取基本设置数据
        :return:
        """
        data_dict = {"info_type": 1}
        msg = (
            "base_setting_%s" % config.ship_code,
            data_dict
        )
        logger.info(msg)
        self.data_manager_obj.send_data(msg=msg)

    def get_advance_setting_data(self):
        """
        获取高级设置数据
        :return:
        """
        data_dict = {"info_type": 1}
        msg = (
            "height_setting_%s" % config.ship_code,
            data_dict
        )
        logger.info(msg)
        self.data_manager_obj.send_data(msg=msg)

    def update_base_setting_data(self):
        """
        更新基本设置数据
        :return:
        """
        if self.data_obj.base_setting_data is not None and not self.data_obj.is_update_base:
            self.base_setting_obj.ui.arriver_distance_line_edit.setText(
                str(self.data_obj.base_setting_data["arrive_range"]))
            self.base_setting_obj.ui.speed_grade_combo_box.setCurrentIndex(
                int(self.data_obj.base_setting_data["speed_grade"]) - 1)
            self.base_setting_obj.ui.safe_distance_line_edit.setText(
                str(self.data_obj.base_setting_data["secure_distance"]))
            self.base_setting_obj.ui.sample_distance_line_edit.setText(str(self.data_obj.base_setting_data["row"]))
            self.base_setting_obj.ui.search_points_line_edit.setText(str(self.data_obj.base_setting_data["keep_point"]))
            self.data_obj.is_update_base = True

    def update_advance_setting_data(self):
        """
        更新高级设置数据
        :return:
        """
        if self.data_obj.height_setting_data is not None and not self.data_obj.is_update_advance:
            ## 电机相关设置 电机停转pwm
            self.advance_setting_obj.ui.stop_pwm_spin_box.setValue(
                int(self.data_obj.height_setting_data["stop_pwm"]))
            # 左右正反桨设置
            if int(self.data_obj.height_setting_data["left_motor_cw"]):
                self.advance_setting_obj.ui.left_positive_radio_button.setChecked(False)
                self.advance_setting_obj.ui.left_opposite_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.left_positive_radio_button.setChecked(True)
                self.advance_setting_obj.ui.left_opposite_radio_button.setChecked(False)
            if int(self.data_obj.height_setting_data["right_motor_cw"]):
                self.advance_setting_obj.ui.right_positive_radio_button.setChecked(False)
                self.advance_setting_obj.ui.right_opposite_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.right_positive_radio_button.setChecked(True)
                self.advance_setting_obj.ui.right_opposite_radio_button.setChecked(False)
            # pid设置
            self.advance_setting_obj.ui.kp_spin_box.setValue(
                int(float(self.data_obj.height_setting_data["kp"]) * 10))
            self.advance_setting_obj.ui.ki_spin_box.setValue(
                int(float(self.data_obj.height_setting_data["ki"]) * 10))
            self.advance_setting_obj.ui.kd_spin_box.setValue(
                int(float(self.data_obj.height_setting_data["kd"]) * 10))
            # 最大最小pwm 安全距离
            self.advance_setting_obj.ui.max_pwm_line_edit.setText(str(self.data_obj.height_setting_data["max_pwm"]))
            self.advance_setting_obj.ui.min_pwm_line_edit.setText(str(self.data_obj.height_setting_data["min_pwm"]))
            self.advance_setting_obj.ui.full_speed_line_edit.setText(
                str(self.data_obj.height_setting_data["full_speed_meter"]))
            ##### 时间相关设置
            self.advance_setting_obj.ui.check_status_spin_box.setValue(
                int(self.data_obj.height_setting_data["check_status_interval"]))
            self.advance_setting_obj.ui.check_connect_spin_box.setValue(
                int(self.data_obj.height_setting_data["check_network_interval"]))
            self.advance_setting_obj.ui.tasking_spin_box.setValue(
                int(self.data_obj.height_setting_data["draw_time"]))
            #######  路径相关设置
            if int(self.data_obj.height_setting_data["home_debug"]):
                self.advance_setting_obj.ui.is_debug_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.is_debug_radio_button.setChecked(False)
            if int(self.data_obj.height_setting_data["b_play_audio"]):
                self.advance_setting_obj.ui.is_play_audio_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.is_play_audio_radio_button.setChecked(False)
            self.advance_setting_obj.ui.path_track_combo_box.setCurrentIndex(
                int(self.data_obj.height_setting_data["path_track_type"]) - 1)
            self.advance_setting_obj.ui.path_planning_combo_box.setCurrentIndex(
                int(self.data_obj.height_setting_data["path_plan_type"]) - 1)
            self.advance_setting_obj.ui.avoidance_combo_box.setCurrentIndex(
                int(self.data_obj.height_setting_data["obstacle_avoid_type"]) - 1)
            if int(self.data_obj.height_setting_data["b_tsp"]):
                self.advance_setting_obj.ui.is_use_tsp_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.is_use_tsp_radio_button.setChecked(False)
            #### 重要状态设置
            if int(self.data_obj.height_setting_data["network_backhome"]):
                self.advance_setting_obj.ui.network_backhome_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.network_backhome_radio_button.setChecked(False)
            if int(self.data_obj.height_setting_data["energy_backhome"]):
                self.advance_setting_obj.ui.energy_backhome_radio_button.setChecked(True)
            else:
                self.advance_setting_obj.ui.energy_backhome_radio_button.setChecked(False)
            if int(self.data_obj.height_setting_data["calibration_compass"]) == 1:
                self.advance_setting_obj.ui.celebrate_push_button.setChecked(True)
            elif int(self.data_obj.height_setting_data["calibration_compass"]) == 0:
                self.advance_setting_obj.ui.celebrate_push_button.setChecked(False)
            else:
                self.advance_setting_obj.ui.celebrate_push_button.setChecked(True)
            self.data_obj.is_update_advance = True

    def open_base_setting(self):
        self.base_setting_obj.show()

    def open_advance_setting(self):
        self.advance_setting_obj.show()

    def print_test(self):
        print('test action')

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
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
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
                frame = cv2.resize(frame, (resize, resize),
                                   interpolation=cv2.INTER_AREA)
                img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
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
        self.ui.time_lcd.setDigitCount(8)
        timer = QTimer(self)
        timer.timeout.connect(self.showtime)
        timer.timeout.connect(self.map_center)
        timer.timeout.connect(self.update_base_info)
        timer.timeout.connect(self.update_detect_info)
        timer.timeout.connect(self.update_base_setting_data)
        timer.timeout.connect(self.update_advance_setting_data)
        timer.start(1000)

    def update_detect_info(self):
        if self.data_obj.wt is not None:
            self.ui.detect_label.setText('水质数据:')
            show_detect_data = '水质数据: 水温 %.1f pH %.1f 溶解氧 %.2f 浊度 %.2f 电导率 %.2f' % (self.data_obj.wt,
                                                                                    self.data_obj.ph,
                                                                                    self.data_obj.cod,
                                                                                    self.data_obj.doDo,
                                                                                    self.data_obj.ec)
            self.ui.detect_label.setText(show_detect_data)
            self.update()

    def update_base_info(self):
        if self.data_obj.speed is not None:
            self.ui.speed_label.setText('速度:%.1f' % self.data_obj.speed)
        if self.data_obj.head_direction is not None:
            self.ui.direction_label.setText('航向:%.1f' % self.data_obj.head_direction)
        if self.data_obj.pool_code is not None:
            self.ui.pool_label.setText("湖泊ID: " + self.data_obj.pool_code)
        self.ui.distance_lcd.display(str(self.data_obj.run_distance))
        self.ui.progress_bar.setValue(self.data_obj.progress)

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
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm:ss')
        self.ui.time_lcd.display(text)
        now = QDate.currentDate()
        # print(now)  # PyQt5.QtCore.QDate(2018, 12, 3)
        # print(now.toString())  # 周一 12月 3 2018
        # print(now.toString(Qt.ISODate))  # 2018-12-03
        # print(now.toString(Qt.DefaultLocaleLongDate))  # 2018年12月3日, 星期一
        self.ui.time_label.setText(now.toString(Qt.DefaultLocaleLongDate))

    def update_mode(self):
        if self.data_obj.move_mode == 1:
            self.data_obj.move_mode = 2
            self.ui.mode_push_button.setText('方位')
        else:
            self.data_obj.move_mode = 1
            self.ui.mode_push_button.setText('方向')

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
        logger.info(msg)
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
                      (self.data_obj.click_lng_lat[0], self.data_obj.click_lng_lat[1])
        logger.info(str_command)
        view.page().runJavaScript(str_command)

    # 在地图上连线
    def map_add_line(self,lng_lat_data:list):
        """
        :param lng_lat_data:二位数组经纬度
        lng_lat_data = [
            [110.144539, 30.492879],
            [114.153809, 30.490808],
            [114.153809, 30.500808]
        ]
        :return: 无 在地图上绘制数据
        """
        json_lng_lat_data = json.dumps(lng_lat_data)
        str_command = "window.add_line(%s)"%json_lng_lat_data
        logger.info(str_command)
        view.page().runJavaScript(str_command)

    # 点击地图上的经纬度
    @pyqtSlot(str, result=str)  # 第一个参数即为回调时携带的参数类型
    def send_lng_lat(self, str_args):
        logger.info({'gps data': str_args})
        lng_lat_zoom = str_args.split(',')
        print('lng_lat_zoom', lng_lat_zoom)
        if len(lng_lat_zoom) == 3:
            self.data_obj.click_lng_lat = [float(lng_lat_zoom[0]), float(lng_lat_zoom[1])]
            self.data_obj.click_zoom = int(lng_lat_zoom[2])
            self.map_add_marker()
            # 如果还没有找到湖泊标记为找湖
            print('self.data_obj.pool_code',self.data_obj.pool_code)
            if self.data_obj.pool_code is None:
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
                logger.info(msg)
                # self.data_manager_obj.send_data(msg=msg)
                # 查找湖泊
                self.data_manager_obj.find_pool()
                if self.data_manager_obj.data_obj.pool_code is not None:
                    self.map_add_line(self.data_manager_obj.data_obj.baidu_map_obj.pool_lng_lats)
            # 已经找到后标记为添加目标点
            else:
                if self.data_obj.control_mode == config.ShipControlStatus.single_point:
                    self.data_obj.target_lng_lat = [float(lng_lat_zoom[0]), float(lng_lat_zoom[1])]
                    send_dict={
                        "deviceId": "asd2312",
                        "mapId": "12321",
                        # 准备执行采样或检测的点经纬度
                        "sampling_points": [self.data_obj.target_lng_lat],
                        # 准备行驶点经纬度
                        "path_points": [self.data_obj.target_lng_lat],
                        # 路径编号
                        "path_id": 1
                    }
                    msg = (
                        'path_planning_%s' % config.ship_code,
                        send_dict
                    )
                    logger.info(msg)
                    self.data_manager_obj.send_data(msg=msg)
                elif self.data_obj.control_mode == config.ShipControlStatus.multi_points:
                    self.data_obj.target_lng_lat.append([float(lng_lat_zoom[0]), float(lng_lat_zoom[1])])


if __name__ == '__main__':
    try:
        myapp = QApplication(sys.argv)
        desktop = QApplication.desktop()
        print(desktop.width() * 0.6, desktop.height() * 0.6)
        main_win = MainWindow()
        # myDlg.setFixedSize(desktop.width() * 0.6, desktop.height() * 0.6)
        view = WebEngine()
        channel = QWebChannel()
        channel.registerObject('PyHandler', main_win)  # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
        view.page().setWebChannel(channel)  # 挂载前端处理对象
        url_string = urllib.request.pathname2url(os.path.join(os.getcwd(), "gaode.html"))  # 加载本地html文件
        view.load(QUrl(url_string))
        main_win.ui.horizontalLayout_6.addWidget(view)
        main_win.view = view
        main_win.setWindowOpacity(0.9)  # 设置窗口透明度
        apply_stylesheet(myapp, theme='dark_teal.xml')
        # myDlg.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        # myDlg.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # myDlg.setStyleSheet("#MainWindow{border-image:url(./statics/background.jpg);}")
        main_win.show()
        sys.exit(myapp.exec_())
    except Exception as e:
        print(e)