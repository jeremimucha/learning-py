#! python3
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog, QLabel, QDoubleSpinBox, QDialogButtonBox, QGridLayout)


class ResizeDlg(QDialog):


    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        lbl_width = QLabel("&Width")
        self.sbox_width = QDoubleSpinBox()
        lbl_width.setBuddy(self.sbox_width)
        self.sbox_width.setRange(4, 4*width)
        self.sbox_width.setValue(width)
        self.sbox_width.setDecimals(0)
        self.sbox_width.setAlignment(Qt.AlignRight)

        lbl_height = QLabel("&Height")
        self.sbox_height = QDoubleSpinBox()
        lbl_height.setBuddy(self.sbox_height)
        self.sbox_height.setRange(4, 4*height)
        self.sbox_height.setValue(height)
        self.sbox_height.setDecimals(0)
        self.sbox_height.setAlignment(Qt.AlignRight)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        grid = QGridLayout()
        grid.addWidget(lbl_width, 0, 0)
        grid.addWidget(self.sbox_width, 0, 1)
        grid.addWidget(lbl_height, 1, 0)
        grid.addWidget(self.sbox_height, 1, 1)
        grid.addWidget(buttonBox, 2, 0, 1, 2)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject) 

        self.setLayout(grid)
        self.setWindowTitle("Image Changer - Resize")

    def result(self):
        return (self.sbox_width.value(), self.sbox_height.value())

if __name__ == '__main__':
    import sys
    import qrc_resources
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon.png"))
    form = ResizeDlg(300, 400)
    form.show()
    app.exec_()
