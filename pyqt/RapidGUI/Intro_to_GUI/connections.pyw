#! python3
import sys
from functools import partial
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QApplication, QHBoxLayout, QDialog

# or use this instead of partial
def descr(func, *args):
    def wrapper():
        return func(*args)
    return wrapper

class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()

        btn1 = QPushButton("One")
        btn2 = QPushButton("Two")
        btn3 = QPushButton("Three")
        btn4 = QPushButton("Four")
        btn5 = QPushButton("Five")

        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        layout.addWidget(btn4)
        layout.addWidget(btn5)

        self.btn1_cb = partial(self.anyButton, "One")
        self.btn2_cb = partial(self.anyButton, "Two")
        self.btn3_cb = partial(self.anyButton, "Three")
        self.btn4_cb = partial(self.anyButton, "Four")
        self.btn5_cb = partial(self.anyButton, "Five")

        btn1.clicked.connect(self.btn1_cb)
        btn2.clicked.connect(self.btn2_cb)
        btn3.clicked.connect(self.btn3_cb)
        btn4.clicked.connect(self.btn4_cb)
        btn5.clicked.connect(self.btn5_cb)

        # Or use a lambda instead of partial:
        '''
        btn1.clicked.connect(lambda who="One": self.anyButton(who))
        btn2.clicked.connect(lambda who="Two": self.anyButton(who))
        btn3.clicked.connect(lambda who="Three": self.anyButton(who))
        btn4.clicked.connect(lambda who="Four": self.anyButton(who))
        btn5.clicked.connect(lambda who="Five": self.anyButton(who))
        '''

        # Or we could create buttons and callbacks more pythonicly:
        '''
        self.cb = {}
        for name in ("One", "Two", "Three", "Four", "Five"):
            btn = QPushButton(name)
            layout.addWidget(btn)
            self.cb[name] = partial(self.anyButton, name)
            btn.clicked.connect(self.cb[name])
        '''
        self.lbl = QLabel("Click a button")
        layout.addWidget(self.lbl)
        
        self.setLayout(layout)
        self.setWindowTitle("Connections - functools.partial and lambda approach")

    def anyButton(self, who):
        self.lbl.setText("You clicked button '%s'" % who)


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()        
