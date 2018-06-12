#! python3
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self._initUI()

    def _initUI(self):
        lbl = QLabel('bla', self)
        # lbl.move(150, 150)

        okButton = QPushButton("OK")
        okButton.clicked.connect(lambda : lbl.setText('OK Clicked'))
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(lambda : lbl.setText('Cancel Clicked'))

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("Buttons")
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
