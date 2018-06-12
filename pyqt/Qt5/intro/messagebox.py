#! python3
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
'''
On closing a QWidget a QCloseEvent is generated. To modify the widget behavior closeEvent() method needs
to be modified
'''

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Message Box demo")
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
