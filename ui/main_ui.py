# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 760)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.logo_label = QtWidgets.QLabel(self.groupBox)
        self.logo_label.setObjectName("logo_label")
        self.horizontalLayout_3.addWidget(self.logo_label)
        self.time_label = QtWidgets.QLabel(self.groupBox)
        self.time_label.setObjectName("time_label")
        self.horizontalLayout_3.addWidget(self.time_label)
        self.direction_label = QtWidgets.QLabel(self.groupBox)
        self.direction_label.setObjectName("direction_label")
        self.horizontalLayout_3.addWidget(self.direction_label)
        self.speed_label = QtWidgets.QLabel(self.groupBox)
        self.speed_label.setObjectName("speed_label")
        self.horizontalLayout_3.addWidget(self.speed_label)
        self.dump_energy_label = QtWidgets.QLabel(self.groupBox)
        self.dump_energy_label.setObjectName("dump_energy_label")
        self.horizontalLayout_3.addWidget(self.dump_energy_label)
        self.remote_control_label = QtWidgets.QLabel(self.groupBox)
        self.remote_control_label.setWordWrap(True)
        self.remote_control_label.setObjectName("remote_control_label")
        self.horizontalLayout_3.addWidget(self.remote_control_label)
        self.time_lcd = QtWidgets.QLCDNumber(self.groupBox)
        self.time_lcd.setObjectName("time_lcd")
        self.horizontalLayout_3.addWidget(self.time_lcd)
        self.distance_lcd = QtWidgets.QLCDNumber(self.groupBox)
        self.distance_lcd.setObjectName("distance_lcd")
        self.horizontalLayout_3.addWidget(self.distance_lcd)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reload_button = QtWidgets.QPushButton(self.groupBox_4)
        self.reload_button.setObjectName("reload_button")
        self.verticalLayout_2.addWidget(self.reload_button)
        self.reselect_button = QtWidgets.QPushButton(self.groupBox_4)
        self.reselect_button.setObjectName("reselect_button")
        self.verticalLayout_2.addWidget(self.reselect_button)
        self.pool_label = QtWidgets.QLabel(self.groupBox_4)
        self.pool_label.setObjectName("pool_label")
        self.verticalLayout_2.addWidget(self.pool_label)
        self.detect_label = QtWidgets.QLabel(self.groupBox_4)
        self.detect_label.setWordWrap(True)
        self.detect_label.setObjectName("detect_label")
        self.verticalLayout_2.addWidget(self.detect_label)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.drain_push_button = QtWidgets.QPushButton(self.groupBox_5)
        self.drain_push_button.setCheckable(True)
        self.drain_push_button.setObjectName("drain_push_button")
        self.gridLayout_2.addWidget(self.drain_push_button, 0, 1, 1, 1)
        self.draw_push_button = QtWidgets.QPushButton(self.groupBox_5)
        self.draw_push_button.setCheckable(True)
        self.draw_push_button.setObjectName("draw_push_button")
        self.gridLayout_2.addWidget(self.draw_push_button, 0, 0, 1, 1)
        self.head_light_push_button = QtWidgets.QPushButton(self.groupBox_5)
        self.head_light_push_button.setCheckable(True)
        self.head_light_push_button.setObjectName("head_light_push_button")
        self.gridLayout_2.addWidget(self.head_light_push_button, 1, 0, 1, 1)
        self.side_light_push_button = QtWidgets.QPushButton(self.groupBox_5)
        self.side_light_push_button.setCheckable(True)
        self.side_light_push_button.setObjectName("side_light_push_button")
        self.gridLayout_2.addWidget(self.side_light_push_button, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.progress_bar = QtWidgets.QProgressBar(self.groupBox_4)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.horizontalLayout.addWidget(self.groupBox_4)
        self.view_group_box = QtWidgets.QGroupBox(self.groupBox_3)
        self.view_group_box.setTitle("")
        self.view_group_box.setObjectName("view_group_box")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.view_group_box)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout.addWidget(self.view_group_box)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_6)
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.video_horizontal_layout = QtWidgets.QHBoxLayout(self.groupBox_8)
        self.video_horizontal_layout.setObjectName("video_horizontal_layout")
        self.video_label = QtWidgets.QLabel(self.groupBox_8)
        self.video_label.setObjectName("video_label")
        self.video_horizontal_layout.addWidget(self.video_label)
        self.verticalLayout_3.addWidget(self.groupBox_8)
        self.distance_show_label = QtWidgets.QLabel(self.groupBox_6)
        self.distance_show_label.setObjectName("distance_show_label")
        self.verticalLayout_3.addWidget(self.distance_show_label)
        self.horizontalLayout.addWidget(self.groupBox_6)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout.setStretch(2, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.left_button = QtWidgets.QPushButton(self.groupBox_7)
        self.left_button.setCheckable(True)
        self.left_button.setAutoExclusive(True)
        self.left_button.setObjectName("left_button")
        self.gridLayout.addWidget(self.left_button, 1, 0, 1, 1)
        self.forward_button = QtWidgets.QPushButton(self.groupBox_7)
        self.forward_button.setCheckable(True)
        self.forward_button.setAutoExclusive(True)
        self.forward_button.setObjectName("forward_button")
        self.gridLayout.addWidget(self.forward_button, 0, 1, 1, 1)
        self.right_button = QtWidgets.QPushButton(self.groupBox_7)
        self.right_button.setCheckable(True)
        self.right_button.setAutoExclusive(True)
        self.right_button.setObjectName("right_button")
        self.gridLayout.addWidget(self.right_button, 1, 2, 1, 1)
        self.stop_button = QtWidgets.QPushButton(self.groupBox_7)
        self.stop_button.setCheckable(True)
        self.stop_button.setAutoExclusive(True)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 1, 1, 1, 1)
        self.backword_button = QtWidgets.QPushButton(self.groupBox_7)
        self.backword_button.setCheckable(True)
        self.backword_button.setAutoExclusive(True)
        self.backword_button.setObjectName("backword_button")
        self.gridLayout.addWidget(self.backword_button, 2, 1, 1, 1)
        self.mode_push_button = QtWidgets.QPushButton(self.groupBox_7)
        self.mode_push_button.setObjectName("mode_push_button")
        self.gridLayout.addWidget(self.mode_push_button, 0, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_7)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_9.setTitle("")
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.single_point_button = QtWidgets.QPushButton(self.groupBox_9)
        self.single_point_button.setCheckable(True)
        self.single_point_button.setChecked(False)
        self.single_point_button.setAutoRepeat(False)
        self.single_point_button.setAutoExclusive(True)
        self.single_point_button.setObjectName("single_point_button")
        self.horizontalLayout_4.addWidget(self.single_point_button)
        self.multi_points_button = QtWidgets.QPushButton(self.groupBox_9)
        self.multi_points_button.setCheckable(True)
        self.multi_points_button.setAutoExclusive(True)
        self.multi_points_button.setObjectName("multi_points_button")
        self.horizontalLayout_4.addWidget(self.multi_points_button)
        self.backhome_button = QtWidgets.QPushButton(self.groupBox_9)
        self.backhome_button.setCheckable(True)
        self.backhome_button.setAutoExclusive(True)
        self.backhome_button.setObjectName("backhome_button")
        self.horizontalLayout_4.addWidget(self.backhome_button)
        self.fix_point_button = QtWidgets.QPushButton(self.groupBox_9)
        self.fix_point_button.setCheckable(True)
        self.fix_point_button.setObjectName("fix_point_button")
        self.horizontalLayout_4.addWidget(self.fix_point_button)
        self.horizontalLayout_2.addWidget(self.groupBox_9)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 4)
        self.verticalLayout.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 932, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.choice_type = QtWidgets.QAction(MainWindow)
        self.choice_type.setObjectName("choice_type")
        self.base_setting_action = QtWidgets.QAction(MainWindow)
        self.base_setting_action.setObjectName("base_setting_action")
        self.about_author_action = QtWidgets.QAction(MainWindow)
        self.about_author_action.setObjectName("about_author_action")
        self.advance_setting_action = QtWidgets.QAction(MainWindow)
        self.advance_setting_action.setObjectName("advance_setting_action")
        self.menu.addAction(self.base_setting_action)
        self.menu.addSeparator()
        self.menu.addAction(self.advance_setting_action)
        self.menu_2.addAction(self.about_author_action)
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "U_V"))
        self.logo_label.setText(_translate("MainWindow", "ID"))
        self.time_label.setText(_translate("MainWindow", "日期"))
        self.direction_label.setText(_translate("MainWindow", "航向角：123"))
        self.speed_label.setText(_translate("MainWindow", "速度："))
        self.dump_energy_label.setText(_translate("MainWindow", "剩余电量：83%"))
        self.remote_control_label.setText(_translate("MainWindow", "启动遥控：0"))
        self.reload_button.setText(_translate("MainWindow", "刷新页面"))
        self.reselect_button.setText(_translate("MainWindow", "重选湖泊"))
        self.pool_label.setText(_translate("MainWindow", "湖泊信息："))
        self.detect_label.setText(_translate("MainWindow", "<html><head/><body><p>天气</p><p>水质</p></body></html>"))
        self.groupBox_5.setTitle(_translate("MainWindow", "控制外设"))
        self.drain_push_button.setText(_translate("MainWindow", "排水"))
        self.draw_push_button.setText(_translate("MainWindow", "抽水"))
        self.head_light_push_button.setText(_translate("MainWindow", "大灯"))
        self.side_light_push_button.setText(_translate("MainWindow", "舷灯"))
        self.video_label.setText(_translate("MainWindow", "图像"))
        self.distance_show_label.setText(_translate("MainWindow", "障碍物信息"))
        self.left_button.setText(_translate("MainWindow", "左"))
        self.forward_button.setText(_translate("MainWindow", "上"))
        self.right_button.setText(_translate("MainWindow", "右"))
        self.stop_button.setText(_translate("MainWindow", "停止"))
        self.backword_button.setText(_translate("MainWindow", "下"))
        self.mode_push_button.setText(_translate("MainWindow", "方向"))
        self.single_point_button.setText(_translate("MainWindow", "单点"))
        self.multi_points_button.setText(_translate("MainWindow", "多点"))
        self.backhome_button.setText(_translate("MainWindow", "返航"))
        self.fix_point_button.setText(_translate("MainWindow", "定点"))
        self.menu.setStatusTip(_translate("MainWindow", "基础设置"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.menu_2.setTitle(_translate("MainWindow", "关于"))
        self.choice_type.setText(_translate("MainWindow", "选择类型"))
        self.base_setting_action.setText(_translate("MainWindow", "基础设置"))
        self.about_author_action.setText(_translate("MainWindow", "作者"))
        self.advance_setting_action.setText(_translate("MainWindow", "高级设置"))
