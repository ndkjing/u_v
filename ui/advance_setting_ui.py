# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'advance_setting_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(914, 721)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_15 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_15.setTitle("")
        self.groupBox_15.setObjectName("groupBox_15")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_15)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.label_5 = QtWidgets.QLabel(self.groupBox_15)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.celebrate_push_button = QtWidgets.QPushButton(self.groupBox_15)
        self.celebrate_push_button.setObjectName("celebrate_push_button")
        self.horizontalLayout_8.addWidget(self.celebrate_push_button)
        self.celebrate_progress_bar = QtWidgets.QProgressBar(self.groupBox_15)
        self.celebrate_progress_bar.setProperty("value", 24)
        self.celebrate_progress_bar.setObjectName("celebrate_progress_bar")
        self.horizontalLayout_8.addWidget(self.celebrate_progress_bar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.groupBox_15)
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.label_6 = QtWidgets.QLabel(self.groupBox_8)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        self.network_backhome_radio_button = QtWidgets.QRadioButton(self.groupBox_8)
        self.network_backhome_radio_button.setObjectName("network_backhome_radio_button")
        self.horizontalLayout_9.addWidget(self.network_backhome_radio_button)
        self.label_13 = QtWidgets.QLabel(self.groupBox_8)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_9.addWidget(self.label_13)
        self.network_backhome_spin_box = QtWidgets.QSpinBox(self.groupBox_8)
        self.network_backhome_spin_box.setObjectName("network_backhome_spin_box")
        self.horizontalLayout_9.addWidget(self.network_backhome_spin_box)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.groupBox_8)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.label_7 = QtWidgets.QLabel(self.groupBox_7)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_10.addWidget(self.label_7)
        self.energy_backhome_radio_button = QtWidgets.QRadioButton(self.groupBox_7)
        self.energy_backhome_radio_button.setObjectName("energy_backhome_radio_button")
        self.horizontalLayout_10.addWidget(self.energy_backhome_radio_button)
        self.label_14 = QtWidgets.QLabel(self.groupBox_7)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_10.addWidget(self.label_14)
        self.energy_backhome_spin_box = QtWidgets.QSpinBox(self.groupBox_7)
        self.energy_backhome_spin_box.setObjectName("energy_backhome_spin_box")
        self.horizontalLayout_10.addWidget(self.energy_backhome_spin_box)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem5)
        self.verticalLayout_2.addWidget(self.groupBox_7)
        self.groupBox_24 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_24.setObjectName("groupBox_24")
        self.verticalLayout_2.addWidget(self.groupBox_24)
        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_14 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_14.setTitle("")
        self.groupBox_14.setObjectName("groupBox_14")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_14)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.label = QtWidgets.QLabel(self.groupBox_14)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.stop_pwm_spin_box = QtWidgets.QSpinBox(self.groupBox_14)
        self.stop_pwm_spin_box.setMinimum(1400)
        self.stop_pwm_spin_box.setMaximum(1600)
        self.stop_pwm_spin_box.setProperty("value", 1500)
        self.stop_pwm_spin_box.setObjectName("stop_pwm_spin_box")
        self.horizontalLayout.addWidget(self.stop_pwm_spin_box)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout.addWidget(self.groupBox_14)
        self.groupBox_13 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_13.setTitle("")
        self.groupBox_13.setObjectName("groupBox_13")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_13)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.label_2 = QtWidgets.QLabel(self.groupBox_13)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.left_positive_radio_button = QtWidgets.QRadioButton(self.groupBox_13)
        self.left_positive_radio_button.setChecked(True)
        self.left_positive_radio_button.setObjectName("left_positive_radio_button")
        self.horizontalLayout_2.addWidget(self.left_positive_radio_button)
        self.left_opposite_radio_button = QtWidgets.QRadioButton(self.groupBox_13)
        self.left_opposite_radio_button.setObjectName("left_opposite_radio_button")
        self.horizontalLayout_2.addWidget(self.left_opposite_radio_button)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.verticalLayout.addWidget(self.groupBox_13)
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_12.setTitle("")
        self.groupBox_12.setObjectName("groupBox_12")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.label_3 = QtWidgets.QLabel(self.groupBox_12)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.right_positive_radio_button = QtWidgets.QRadioButton(self.groupBox_12)
        self.right_positive_radio_button.setChecked(False)
        self.right_positive_radio_button.setObjectName("right_positive_radio_button")
        self.horizontalLayout_3.addWidget(self.right_positive_radio_button)
        self.right_opposite_radio_button = QtWidgets.QRadioButton(self.groupBox_12)
        self.right_opposite_radio_button.setChecked(True)
        self.right_opposite_radio_button.setObjectName("right_opposite_radio_button")
        self.horizontalLayout_3.addWidget(self.right_opposite_radio_button)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem11)
        self.verticalLayout.addWidget(self.groupBox_12)
        self.groupBox_11 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_11.setTitle("")
        self.groupBox_11.setObjectName("groupBox_11")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_11)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem12)
        self.label_4 = QtWidgets.QLabel(self.groupBox_11)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.kp_spin_box = QtWidgets.QSpinBox(self.groupBox_11)
        self.kp_spin_box.setMaximum(100)
        self.kp_spin_box.setSingleStep(1)
        self.kp_spin_box.setObjectName("kp_spin_box")
        self.horizontalLayout_4.addWidget(self.kp_spin_box)
        self.label_11 = QtWidgets.QLabel(self.groupBox_11)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_4.addWidget(self.label_11)
        self.ki_spin_box = QtWidgets.QSpinBox(self.groupBox_11)
        self.ki_spin_box.setMaximum(100)
        self.ki_spin_box.setObjectName("ki_spin_box")
        self.horizontalLayout_4.addWidget(self.ki_spin_box)
        self.label_12 = QtWidgets.QLabel(self.groupBox_11)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.kd_spin_box = QtWidgets.QSpinBox(self.groupBox_11)
        self.kd_spin_box.setMaximum(100)
        self.kd_spin_box.setObjectName("kd_spin_box")
        self.horizontalLayout_4.addWidget(self.kd_spin_box)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem13)
        self.verticalLayout.addWidget(self.groupBox_11)
        self.groupBox_10 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_10.setTitle("")
        self.groupBox_10.setObjectName("groupBox_10")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem14)
        self.label_10 = QtWidgets.QLabel(self.groupBox_10)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_5.addWidget(self.label_10)
        self.max_pwm_line_edit = QtWidgets.QLineEdit(self.groupBox_10)
        self.max_pwm_line_edit.setObjectName("max_pwm_line_edit")
        self.horizontalLayout_5.addWidget(self.max_pwm_line_edit)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem15)
        self.verticalLayout.addWidget(self.groupBox_10)
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_9.setTitle("")
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem16)
        self.label_9 = QtWidgets.QLabel(self.groupBox_9)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        self.min_pwm_line_edit = QtWidgets.QLineEdit(self.groupBox_9)
        self.min_pwm_line_edit.setObjectName("min_pwm_line_edit")
        self.horizontalLayout_6.addWidget(self.min_pwm_line_edit)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem17)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem18)
        self.label_8 = QtWidgets.QLabel(self.groupBox_5)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_7.addWidget(self.label_8)
        self.full_speed_line_edit = QtWidgets.QLineEdit(self.groupBox_5)
        self.full_speed_line_edit.setObjectName("full_speed_line_edit")
        self.horizontalLayout_7.addWidget(self.full_speed_line_edit)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem19)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_23 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_23.setTitle("")
        self.groupBox_23.setObjectName("groupBox_23")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox_23)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem20)
        self.label_21 = QtWidgets.QLabel(self.groupBox_23)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_14.addWidget(self.label_21)
        self.is_debug_radio_button = QtWidgets.QRadioButton(self.groupBox_23)
        self.is_debug_radio_button.setObjectName("is_debug_radio_button")
        self.horizontalLayout_14.addWidget(self.is_debug_radio_button)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem21)
        self.verticalLayout_4.addWidget(self.groupBox_23)
        self.groupBox_22 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_22.setTitle("")
        self.groupBox_22.setObjectName("groupBox_22")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.groupBox_22)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem22)
        self.label_22 = QtWidgets.QLabel(self.groupBox_22)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_15.addWidget(self.label_22)
        self.is_play_audio_radio_button = QtWidgets.QRadioButton(self.groupBox_22)
        self.is_play_audio_radio_button.setObjectName("is_play_audio_radio_button")
        self.horizontalLayout_15.addWidget(self.is_play_audio_radio_button)
        spacerItem23 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem23)
        self.verticalLayout_4.addWidget(self.groupBox_22)
        self.groupBox_21 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_21.setTitle("")
        self.groupBox_21.setObjectName("groupBox_21")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.groupBox_21)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem24)
        self.label_23 = QtWidgets.QLabel(self.groupBox_21)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_16.addWidget(self.label_23)
        self.path_track_combo_box = QtWidgets.QComboBox(self.groupBox_21)
        self.path_track_combo_box.setObjectName("path_track_combo_box")
        self.path_track_combo_box.addItem("")
        self.path_track_combo_box.addItem("")
        self.path_track_combo_box.addItem("")
        self.horizontalLayout_16.addWidget(self.path_track_combo_box)
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem25)
        self.verticalLayout_4.addWidget(self.groupBox_21)
        self.groupBox_20 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_20.setTitle("")
        self.groupBox_20.setObjectName("groupBox_20")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.groupBox_20)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem26)
        self.label_18 = QtWidgets.QLabel(self.groupBox_20)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_17.addWidget(self.label_18)
        self.path_planning_combo_box = QtWidgets.QComboBox(self.groupBox_20)
        self.path_planning_combo_box.setObjectName("path_planning_combo_box")
        self.path_planning_combo_box.addItem("")
        self.path_planning_combo_box.addItem("")
        self.path_planning_combo_box.addItem("")
        self.horizontalLayout_17.addWidget(self.path_planning_combo_box)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem27)
        self.verticalLayout_4.addWidget(self.groupBox_20)
        self.groupBox_19 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_19.setTitle("")
        self.groupBox_19.setObjectName("groupBox_19")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.groupBox_19)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        spacerItem28 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem28)
        self.label_19 = QtWidgets.QLabel(self.groupBox_19)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_18.addWidget(self.label_19)
        self.avoidance_combo_box = QtWidgets.QComboBox(self.groupBox_19)
        self.avoidance_combo_box.setObjectName("avoidance_combo_box")
        self.avoidance_combo_box.addItem("")
        self.avoidance_combo_box.addItem("")
        self.avoidance_combo_box.addItem("")
        self.horizontalLayout_18.addWidget(self.avoidance_combo_box)
        self.label_24 = QtWidgets.QLabel(self.groupBox_19)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_18.addWidget(self.label_24)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_19)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_18.addWidget(self.spinBox)
        self.label_25 = QtWidgets.QLabel(self.groupBox_19)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_18.addWidget(self.label_25)
        self.spinBox_2 = QtWidgets.QSpinBox(self.groupBox_19)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_18.addWidget(self.spinBox_2)
        spacerItem29 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem29)
        self.verticalLayout_4.addWidget(self.groupBox_19)
        self.groupBox_18 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_18.setTitle("")
        self.groupBox_18.setObjectName("groupBox_18")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.groupBox_18)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        spacerItem30 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem30)
        self.label_20 = QtWidgets.QLabel(self.groupBox_18)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_19.addWidget(self.label_20)
        self.is_use_tsp_radio_button = QtWidgets.QRadioButton(self.groupBox_18)
        self.is_use_tsp_radio_button.setObjectName("is_use_tsp_radio_button")
        self.horizontalLayout_19.addWidget(self.is_use_tsp_radio_button)
        spacerItem31 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem31)
        self.verticalLayout_4.addWidget(self.groupBox_18)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem32 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem32)
        self.label_16 = QtWidgets.QLabel(self.groupBox_6)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_11.addWidget(self.label_16)
        self.check_status_spin_box = QtWidgets.QSpinBox(self.groupBox_6)
        self.check_status_spin_box.setObjectName("check_status_spin_box")
        self.horizontalLayout_11.addWidget(self.check_status_spin_box)
        spacerItem33 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem33)
        self.verticalLayout_3.addWidget(self.groupBox_6)
        self.groupBox_16 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_16.setTitle("")
        self.groupBox_16.setObjectName("groupBox_16")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.groupBox_16)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem34 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem34)
        self.label_15 = QtWidgets.QLabel(self.groupBox_16)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_12.addWidget(self.label_15)
        self.check_connect_spin_box = QtWidgets.QSpinBox(self.groupBox_16)
        self.check_connect_spin_box.setObjectName("check_connect_spin_box")
        self.horizontalLayout_12.addWidget(self.check_connect_spin_box)
        spacerItem35 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem35)
        self.verticalLayout_3.addWidget(self.groupBox_16)
        self.groupBox_17 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_17.setTitle("")
        self.groupBox_17.setObjectName("groupBox_17")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.groupBox_17)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem36 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem36)
        self.label_17 = QtWidgets.QLabel(self.groupBox_17)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_13.addWidget(self.label_17)
        self.tasking_spin_box = QtWidgets.QSpinBox(self.groupBox_17)
        self.tasking_spin_box.setObjectName("tasking_spin_box")
        self.horizontalLayout_13.addWidget(self.tasking_spin_box)
        spacerItem37 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem37)
        self.verticalLayout_3.addWidget(self.groupBox_17)
        self.groupBox_25 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_25.setObjectName("groupBox_25")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_25)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_27 = QtWidgets.QGroupBox(self.groupBox_25)
        self.groupBox_27.setTitle("")
        self.groupBox_27.setObjectName("groupBox_27")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.groupBox_27)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        spacerItem38 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem38)
        self.label_26 = QtWidgets.QLabel(self.groupBox_27)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_20.addWidget(self.label_26)
        self.is_mqtt_radio_button = QtWidgets.QRadioButton(self.groupBox_27)
        self.is_mqtt_radio_button.setObjectName("is_mqtt_radio_button")
        self.horizontalLayout_20.addWidget(self.is_mqtt_radio_button)
        self.label_28 = QtWidgets.QLabel(self.groupBox_27)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_20.addWidget(self.label_28)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_27)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_20.addWidget(self.lineEdit_4)
        self.label_29 = QtWidgets.QLabel(self.groupBox_27)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_20.addWidget(self.label_29)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_27)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_20.addWidget(self.lineEdit_5)
        spacerItem39 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem39)
        self.verticalLayout_5.addWidget(self.groupBox_27)
        self.groupBox_26 = QtWidgets.QGroupBox(self.groupBox_25)
        self.groupBox_26.setTitle("")
        self.groupBox_26.setObjectName("groupBox_26")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.groupBox_26)
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        spacerItem40 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem40)
        self.label_27 = QtWidgets.QLabel(self.groupBox_26)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_21.addWidget(self.label_27)
        self.is_lora_radio_button = QtWidgets.QRadioButton(self.groupBox_26)
        self.is_lora_radio_button.setObjectName("is_lora_radio_button")
        self.horizontalLayout_21.addWidget(self.is_lora_radio_button)
        self.label_30 = QtWidgets.QLabel(self.groupBox_26)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_21.addWidget(self.label_30)
        self.comboBox = QtWidgets.QComboBox(self.groupBox_26)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_21.addWidget(self.comboBox)
        self.label_31 = QtWidgets.QLabel(self.groupBox_26)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_21.addWidget(self.label_31)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_26)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_21.addWidget(self.lineEdit_7)
        spacerItem41 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem41)
        self.verticalLayout_5.addWidget(self.groupBox_26)
        self.verticalLayout_3.addWidget(self.groupBox_25)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_4.setTitle(_translate("Form", "????????????"))
        self.label_5.setText(_translate("Form", "????????????"))
        self.celebrate_push_button.setText(_translate("Form", "????????????"))
        self.label_6.setText(_translate("Form", "????????????"))
        self.network_backhome_radio_button.setText(_translate("Form", "RadioButton"))
        self.label_13.setText(_translate("Form", "??????????????????"))
        self.label_7.setText(_translate("Form", "????????????"))
        self.energy_backhome_radio_button.setText(_translate("Form", "RadioButton"))
        self.label_14.setText(_translate("Form", "?????????????????????"))
        self.groupBox_24.setTitle(_translate("Form", "????????????"))
        self.groupBox.setTitle(_translate("Form", "??????????????????"))
        self.label.setText(_translate("Form", "????????????PWM??????"))
        self.label_2.setText(_translate("Form", "????????????????????????"))
        self.left_positive_radio_button.setText(_translate("Form", "??????"))
        self.left_opposite_radio_button.setText(_translate("Form", "??????"))
        self.label_3.setText(_translate("Form", "????????????????????????"))
        self.right_positive_radio_button.setText(_translate("Form", "??????"))
        self.right_opposite_radio_button.setText(_translate("Form", "??????"))
        self.label_4.setText(_translate("Form", "Kp"))
        self.label_11.setText(_translate("Form", "Ki"))
        self.label_12.setText(_translate("Form", "Kd"))
        self.label_10.setText(_translate("Form", "????????????PWM??????"))
        self.label_9.setText(_translate("Form", "????????????PWM??????"))
        self.label_8.setText(_translate("Form", "??????????????????????????????(m)"))
        self.groupBox_3.setTitle(_translate("Form", "????????????"))
        self.label_21.setText(_translate("Form", "????????????"))
        self.is_debug_radio_button.setText(_translate("Form", "??????"))
        self.label_22.setText(_translate("Form", "??????????????????"))
        self.is_play_audio_radio_button.setText(_translate("Form", "????????????"))
        self.label_23.setText(_translate("Form", "??????????????????"))
        self.path_track_combo_box.setItemText(0, _translate("Form", "pid"))
        self.path_track_combo_box.setItemText(1, _translate("Form", "puresuit"))
        self.path_track_combo_box.setItemText(2, _translate("Form", "mpc"))
        self.label_18.setText(_translate("Form", "??????????????????"))
        self.path_planning_combo_box.setItemText(0, _translate("Form", "A star"))
        self.path_planning_combo_box.setItemText(1, _translate("Form", "direct go"))
        self.path_planning_combo_box.setItemText(2, _translate("Form", "RRT"))
        self.label_19.setText(_translate("Form", "????????????"))
        self.avoidance_combo_box.setItemText(0, _translate("Form", "?????????"))
        self.avoidance_combo_box.setItemText(1, _translate("Form", "??????????????????"))
        self.avoidance_combo_box.setItemText(2, _translate("Form", "??????????????????????????????"))
        self.label_24.setText(_translate("Form", "????????????????????????(m)"))
        self.label_25.setText(_translate("Form", "????????????????????????(m)"))
        self.label_20.setText(_translate("Form", "????????????TSP????????????"))
        self.is_use_tsp_radio_button.setText(_translate("Form", "TSP"))
        self.groupBox_2.setTitle(_translate("Form", "????????????"))
        self.label_16.setText(_translate("Form", "????????????????????????"))
        self.label_15.setText(_translate("Form", "????????????????????????"))
        self.label_17.setText(_translate("Form", "??????????????????"))
        self.groupBox_25.setTitle(_translate("Form", "????????????"))
        self.label_26.setText(_translate("Form", "mqtt"))
        self.is_mqtt_radio_button.setText(_translate("Form", "use mqtt"))
        self.label_28.setText(_translate("Form", "IP"))
        self.label_29.setText(_translate("Form", "port"))
        self.label_27.setText(_translate("Form", "lora"))
        self.is_lora_radio_button.setText(_translate("Form", "use lora"))
        self.label_30.setText(_translate("Form", "Com"))
        self.comboBox.setItemText(0, _translate("Form", "com1"))
        self.comboBox.setItemText(1, _translate("Form", "com2"))
        self.label_31.setText(_translate("Form", "baud"))
