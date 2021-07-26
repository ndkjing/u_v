# -*- coding: utf-8 -*-

"""
这是一个关于Web页面交互初探1（QWebEngineView）的小例子
文章链接：http://www.xdbcb8.com/archives/1036.html
"""

import sys
import os
import codecs
import random
from Ui_main import Ui_Form
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFileInfo, QTimer, Qt

class PiChart(QWidget, Ui_Form):
    """
    饼图演示
    """
    def __init__(self, parent=None):
        """
        一些初始设置
        """
        super(PiChart, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        """
        一些界面配置
        """
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # 窗口上只有关闭按钮

        self.splitter.setOpaqueResize(False)
        # QSplitter调整大小不透明，默认是True

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 9)
        # 按照窗口索引(0，1)分别增加1、9个伸缩因子

        self.view = QWebEngineView(self.widget)
        vv = QVBoxLayout()
        vv.addWidget(self.view)
        self.widget.setLayout(vv)

        with codecs.open("pie-simple.html", "r", "utf-8") as f:
            html = f.read()
        # 读取html文件

        self.view.setHtml(html)
        # Web视图的内容设置为指定的html内容；无法显示大于2 MB的内容，切记！！！

        self.time = QTimer()
    
    def showPi(self):
        """
        显示饼形图
        """
        food = self.spinBox_food.value()
        rent = self.spinBox_rent.value()
        electricity = self.spinBox_electricity.value()
        traffic = self.spinBox_traffic.value()
        relationship = self.spinBox_relationship.value()
        taobao = self.spinBox_taobao.value()
        # 将微调框的数值赋值给变量

        jscode = "showPiChart({}, {}, {}, {}, {}, {});".format(food, traffic, relationship, rent, electricity, taobao)
        self.view.page().runJavaScript(jscode)
        # 加载运行JavaScript

    def autoShow(self):
        """
        自动演示
        """
        self.spinBox_food.setValue(random.randint(100, 10000))
        self.spinBox_rent.setValue(random.randint(100, 10000))
        self.spinBox_electricity.setValue(random.randint(100, 1000))
        self.spinBox_traffic.setValue(random.randint(100, 2000))
        self.spinBox_relationship.setValue(random.randint(100, 3000))
        self.spinBox_taobao.setValue(random.randint(100, 10000))
        # 数值随机生成

    @pyqtSlot(bool)
    def on_checkBox_toggled(self, flag):
        """
        复选框选中时触发
        """
        if flag:
            self.time.start(1000)
            self.time.timeout.connect(self.autoShow)
            # 选中开始计时
        else:
            self.time.stop()
            # 未选中停止计时

    @pyqtSlot(int)
    def on_spinBox_food_valueChanged(self, n):
        """
        伙食消费微调框数值改变时触发
        """
        self.showPi()
    
    @pyqtSlot(int)
    def on_spinBox_rent_valueChanged(self):
        """
        房租微调框数值改变时触发
        """
        self.showPi()
    
    @pyqtSlot(int)
    def on_spinBox_electricity_valueChanged(self):
        """
        水电气微调框数值改变时触发
        """
        self.showPi()
    
    @pyqtSlot(int)
    def on_spinBox_traffic_valueChanged(self):
        """
        交通微调框数值改变时触发
        """
        self.showPi()
    
    @pyqtSlot(int)
    def on_spinBox_relationship_valueChanged(self):
        """
        人情往来微调框数值改变时触发
        """
        self.showPi()
    
    @pyqtSlot(int)
    def on_spinBox_taobao_valueChanged(self):
        """
        淘宝网购微调框数值改变时触发
        """
        self.showPi()

    def __del__(self):
        '''
        删除相关对象
        '''
        self.view.deleteLater()
        # 让系统加快释放这部分内存，避免QWebEngineView崩溃

if __name__ == "__main__":
    app = QApplication(sys.argv)
    piChart = PiChart()
    piChart.show()
    sys.exit(app.exec_())