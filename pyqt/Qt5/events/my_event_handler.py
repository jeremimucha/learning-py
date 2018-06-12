#! python3
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        self._lbl = QLabel('blabl                 ', self)
        self._lbl.move(100, 100)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event Handler')

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        else:
            s = 'Key id: {}'.format(str(e.key()))
            self._lbl.setText(s)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
