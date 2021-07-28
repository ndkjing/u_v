#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This is a simple drag and
drop example.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QApplication, QLabel
import sys


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


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        edit = QLineEdit('', self)
        edit.setDragEnabled(True)
        edit.setAcceptDrops(True)
        edit.move(30, 65)
        button = DropAreaLabel("Button", self)
        button.move(190, 65)

        self.setWindowTitle('Simple drag and drop')
        self.setGeometry(300, 300, 300, 150)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # ex = Example()
    # ex.show()
    # app.exec_()
    print(int(True),int(False))