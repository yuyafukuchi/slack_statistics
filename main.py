from PyQt5.QtWidgets import *
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from util import *
import datetime 

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
        self.createHorizontalResultTitlebox()
        self.createHorizontalResultbox()

        windowLayout.addWidget(titlelabel,stretch = 1)
        windowLayout.addWidget(self.horizontalGroupBox1,stretch = 1)
        windowLayout.addWidget(runbutton,alignment=Qt.AlignCenter,stretch = 1)
        windowLayout.addWidget(self.horizontalGroupBox2,stretch = 1)
        windowLayout.addWidget(self.horizontalGroupBox3,stretch = 5)
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

    def createHorizontalResultTitlebox(self):
        self.horizontalGroupBox2 = QGroupBox()
        layout = QHBoxLayout()

        self.message_result_label = QLabel('メッセージ数ランキング',self)
        self.reaction_result_label = QLabel('スタンプ数ランキング',self)

        layout.addWidget(self.message_result_label)
        layout.addWidget(self.reaction_result_label)

        self.horizontalGroupBox2.setLayout(layout)     

    def createHorizontalResultbox(self):
        self.horizontalGroupBox3 = QGroupBox()
        layout = QHBoxLayout()

        self.message_result_label = QLabel('\n'.join(map(str,range(1,10))),self)
        self.message_result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.reaction_result_label = QLabel('\n'.join(map(str,range(1,10))),self)
        self.reaction_result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(self.message_result_label)
        layout.addWidget(self.reaction_result_label)

        self.horizontalGroupBox3.setLayout(layout)

    @pyqtSlot()
    def didTapRunButton(self):
        dt_latest = datetime.datetime.strptime(self.endtime_textbox.text(),TIMEFORMAT)
        dt_oldest = datetime.datetime.strptime(self.starttime_textbox.text(),TIMEFORMAT)
        if dt_latest < dt_oldest:
            raise Exception('oldest day should be older than latest day')
        
        message_counts,reaction_counts = fetch_historys(dt_latest=dt_latest,dt_oldest=dt_oldest)
        message_counts = sorted(message_counts.items(),key=lambda x: -x[1])
        reaction_counts = sorted(reaction_counts.items(),key=lambda x: -x[1])

        m_ranking_texts = []
        r_ranking_texts = []

        for userid, value in message_counts[:MAX_RANKING]:
            user = convert_userid_to_username(userid)
            m_ranking_texts.append(f"{user} : {value} 回")

        for userid, value in message_counts[:MAX_RANKING]:
            user = convert_userid_to_username(userid)
            r_ranking_texts.append(f"{user} : {value} 回")
        
        self.message_result_label.setText('\n'.join(m_ranking_texts))
        self.reaction_result_label.setText('\n'.join(r_ranking_texts))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ew = App()    
    sys.exit(app.exec_())

