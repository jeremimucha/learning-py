#! python3
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
'''
Demonstrates the > sender() < method.
sender() returns the source of the callback (i.e. sender of the event)
'''

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):

        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')

        self.show()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage('{} was pressed'.format(sender.text()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
