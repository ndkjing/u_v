# coding:utf-8

import sys
from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.initUI()

    def initUI(self):
        QMainWindow.setGeometry(self, 200, 200, 1000, 1000)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.view = QWebEngineView(self)
        # self.view.load(QUrl("http://www.baidu.com/"))
        self.view.setHtml('''
         <html>
         <head>
         <title>A Demo Page</title>

          <script language="javascript">
            // Completes the full-name control and
            // shows the submit button
            function completeAndReturnName() {
              var fname = document.getElementById('fname').value;
              var lname = document.getElementById('lname').value;
              var full = fname + ' ' + lname;

              document.getElementById('fullname').value = full;
              document.getElementById('submit-btn').style.display = 'block';

              return full;
            }
          </script>
        </head>

        <body>
          <form>
            <label for="fname">First name:</label>
            <input type="text" name="fname" id="fname"></input>
            <br />
            <label for="lname">Last name:</label>
            <input type="text" name="lname" id="lname"></input>
            <br />
            <label for="fullname">Full name:</label>
            <input disabled type="text" name="fullname" id="fullname"></input>
            <br />
            <input style="display: none;" type="submit" id="submit-btn"></input>
          </form>
        </body>
        </html>
         ''')
        self.button = QPushButton('设置全名')
        self.button.clicked.connect(self.complete_name)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def js_callback(self, result):
        print('result', result)

    def complete_name(self):
        print('complete_name')
        self.view.page().runJavaScript('completeAndReturnName();', self.js_callback)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
