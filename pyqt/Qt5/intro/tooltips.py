#! python3
import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QFont, QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.setWindowIcon(QIcon('py.png'))
        QToolTip.setFont(QFont('SansSerif', 8))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Tooltips")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
