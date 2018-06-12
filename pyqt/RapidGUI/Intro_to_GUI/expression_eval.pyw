#! python3
import sys
from math import *
# from PyQt5.QtCore import 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QApplication, QTextBrowser


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self._browser = QTextBrowser()
        self._lineedit = QLineEdit("Type an expression and press Enter")
        self._lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self._browser)
        layout.addWidget(self._lineedit)
        self.setLayout(layout)
        self._lineedit.setFocus()
        # self.connect(self._lineedit, SIGNAL("returnPressed()"), self._updateUI)
        self._lineedit.returnPressed.connect(self._updateUI)
        self.setWindowTitle("Calculate")

    def _updateUI(self):
        try:
            text = self._lineedit.text()
            self._browser.append("{0} = <b>{1}</b>".format(text, eval(text)))
        except:
            self._browser.append(
                "<font color=red>{0} is invalid!</font>".format(text)
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
