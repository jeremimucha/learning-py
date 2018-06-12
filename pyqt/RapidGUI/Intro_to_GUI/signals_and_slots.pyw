#! python3
import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDial, QDialog, QSpinBox, QHBoxLayout, QVBoxLayout, QApplication, QLabel

class ZeroSpinBox(QSpinBox):
    zeros = 0
    atzero = pyqtSignal(str, name='atzero')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.valueChanged[int].connect(self.checkzero)

    def checkzero(self):
        if self.value() == 0:
            self.zeros += 1
            self.atzero.emit(str(self.zeros))

class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        dial = QDial()
        dial.setNotchesVisible(True)
        
        spinbox = ZeroSpinBox()

        label = QLabel()

        layout = QHBoxLayout()
        layout.addWidget(dial)
        layout.addWidget(spinbox)

        vlayout = QVBoxLayout()
        vlayout.addWidget(label)
        vlayout.addLayout(layout)
        self.setLayout(vlayout)

        dial.valueChanged[int].connect(spinbox.setValue)
        spinbox.valueChanged[int].connect(dial.setValue)
        spinbox.atzero[str].connect(label.setText)

        self.setWindowTitle('Signals and Slots')

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
