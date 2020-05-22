from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Active Rankings"
        self.left = 100
        self.top = 10
        self.width = 640
        self.height = 640
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self._center()

        windowLayout = QVBoxLayout()

        titlelabel = QLabel('日付を入力して実行ボタンを押してください\n例) 2020-01-01',self)
        titlelabel.setAlignment(Qt.AlignCenter)

        runbutton = QPushButton('実行', self)
        runbutton.clicked.connect(self.didTapRunButton)
        runbutton.setFixedWidth(100)

        self.createHorizontalTextbox()
        self.createHorizontalResultbox()

        windowLayout.addWidget(titlelabel)
        windowLayout.addWidget(self.horizontalGroupBox1)
        windowLayout.addWidget(runbutton,alignment=Qt.AlignCenter)
        windowLayout.addWidget(self.horizontalGroupBox2)
        self.setLayout(windowLayout)
        self.show()
    
    def _center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def createHorizontalTextbox(self):
        self.horizontalGroupBox1 = QGroupBox()
        layout = QHBoxLayout()

        starttime_label = QLabel('oldest day',self)
        endtime_label = QLabel('latest day',self)
        self.starttime_textbox = QLineEdit(self)
        self.endtime_textbox = QLineEdit(self)

        layout.addWidget(starttime_label)
        layout.addWidget(self.starttime_textbox)
        layout.addWidget(endtime_label)
        layout.addWidget(self.endtime_textbox)

        self.horizontalGroupBox1.setLayout(layout)

    def createHorizontalResultbox(self):
        self.horizontalGroupBox2 = QGroupBox()
        layout = QHBoxLayout()
        
        self.message_result_label = QLabel('\n'.join(map(str,range(1,10))),self)
        self.message_result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.reaction_result_label = QLabel('\n'.join(map(str,range(1,10))),self)
        self.message_result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(self.message_result_label)
        layout.addWidget(self.reaction_result_label)

        self.horizontalGroupBox2.setLayout(layout)


    @pyqtSlot()
    def on_click(self):
        print("PyQt5 button click")

    @pyqtSlot()
    def didTapRunButton(self):
        print('didtap')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ew = App()    
    sys.exit(app.exec_())

