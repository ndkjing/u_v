# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(806, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dump_energy_label = QtWidgets.QLabel(self.groupBox)
        self.dump_energy_label.setObjectName("dump_energy_label")
        self.horizontalLayout_3.addWidget(self.dump_energy_label)
        self.remote_control_label = QtWidgets.QLabel(self.groupBox)
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
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.angle_label = QtWidgets.QLabel(self.groupBox_4)
        self.angle_label.setObjectName("angle_label")
        self.verticalLayout_2.addWidget(self.angle_label)
        self.detect_label = QtWidgets.QLabel(self.groupBox_4)
        self.detect_label.setObjectName("detect_label")
        self.verticalLayout_2.addWidget(self.detect_label)
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_4)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
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
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.left_button = QtWidgets.QPushButton(self.groupBox_7)
        self.left_button.setObjectName("left_button")
        self.gridLayout.addWidget(self.left_button, 1, 0, 1, 1)
        self.forward_button = QtWidgets.QPushButton(self.groupBox_7)
        self.forward_button.setObjectName("forward_button")
        self.gridLayout.addWidget(self.forward_button, 0, 1, 1, 1)
        self.right_button = QtWidgets.QPushButton(self.groupBox_7)
        self.right_button.setObjectName("right_button")
        self.gridLayout.addWidget(self.right_button, 1, 2, 1, 1)
        self.stop_button = QtWidgets.QPushButton(self.groupBox_7)
        self.stop_button.setObjectName("stop_button")
        self.gridLayout.addWidget(self.stop_button, 1, 1, 1, 1)
        self.backword_button = QtWidgets.QPushButton(self.groupBox_7)
        self.backword_button.setObjectName("backword_button")
        self.gridLayout.addWidget(self.backword_button, 2, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.groupBox_7)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_9.setTitle("")
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.single_point_button = QtWidgets.QPushButton(self.groupBox_9)
        self.single_point_button.setObjectName("single_point_button")
        self.horizontalLayout_4.addWidget(self.single_point_button)
        self.multi_points_button = QtWidgets.QPushButton(self.groupBox_9)
        self.multi_points_button.setObjectName("multi_points_button")
        self.horizontalLayout_4.addWidget(self.multi_points_button)
        self.fix_point_button = QtWidgets.QPushButton(self.groupBox_9)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 806, 23))
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
        self.actiondas = QtWidgets.QAction(MainWindow)
        self.actiondas.setObjectName("actiondas")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.choice_type)
        self.menu.addSeparator()
        self.menu.addAction(self.actiondas)
        self.menu.addSeparator()
        self.menu.addAction(self.action_5)
        self.menu_2.addAction(self.action)
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "U_V"))
        self.dump_energy_label.setText(_translate("MainWindow", "TextLabel"))
        self.remote_control_label.setText(_translate("MainWindow", "TextLabel"))
        self.angle_label.setText(_translate("MainWindow", "TextLabel"))
        self.detect_label.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.video_label.setText(_translate("MainWindow", "TextLabel"))
        self.distance_show_label.setText(_translate("MainWindow", "TextLabel"))
        self.left_button.setText(_translate("MainWindow", "左"))
        self.forward_button.setText(_translate("MainWindow", "上"))
        self.right_button.setText(_translate("MainWindow", "右"))
        self.stop_button.setText(_translate("MainWindow", "停止"))
        self.backword_button.setText(_translate("MainWindow", "下"))
        self.single_point_button.setText(_translate("MainWindow", "单点"))
        self.multi_points_button.setText(_translate("MainWindow", "多点"))
        self.fix_point_button.setText(_translate("MainWindow", "定点"))
        self.menu.setStatusTip(_translate("MainWindow", "基础设置"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.menu_2.setTitle(_translate("MainWindow", "关于"))
        self.choice_type.setText(_translate("MainWindow", "选择类型"))
        self.actiondas.setText(_translate("MainWindow", "基础设置"))
        self.action.setText(_translate("MainWindow", "作者"))
        self.action_5.setText(_translate("MainWindow", "高级设置"))
