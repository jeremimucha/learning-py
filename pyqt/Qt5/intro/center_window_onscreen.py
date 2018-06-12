#! python3
import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self.resize(250, 150)
        self.setWindowTitle('Center a window demo')

        btn = QPushButton('Center Me!', self)
        btn.setToolTip('Center this window on screen.')
        btn.resize(btn.sizeHint())
        btn.move(100, 65)
        btn.clicked.connect(self.center)

        self.show()

    # Method to move a window to the center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
