#! python3
import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QPushButton, QDialog


class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout()
        self._cb = {}

        btn = None
        for name in ("One", "Two", "Three", "Four", "Five"):
            btn = QPushButton(name)
            layout.addWidget(btn) 
            # by PyQt conventional programming style slots are given the same name as signals they connect to
            # reminder: signal is emited by an event -> button being clicked amits 'clicked' signal
            # slots are functions we connect the emited signal to
            # here ->
            # signal == btn.clicked
            # slot == self.clicked
            btn.clicked.connect(self.clicked)

        self.lbl = QLabel("Click a button")
        layout.addWidget(self.lbl)

        self.setLayout(layout)
        self.setWindowTitle("Connections - self.sender approach")

    def clicked(self):
        btn = self.sender()
        if btn is None or not isinstance(btn, QPushButton):
            return
        self.lbl.setText("You clicked button '%s'" % btn.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
