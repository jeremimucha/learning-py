#! python3
import sys
from PyQt5.QtWidgets import (QDialog, QApplication, QLabel, QSpinBox, QPushButton,
        QCheckBox, QComboBox, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt


class PenPropertiesDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # the '&' here means that 'W' will be underlined and will be a keyboard accelerator
        # this only happens if a widget has a 'buddy' -> .setBuddy method
        # if that's the case on pressing the keyboard accel. focus will be switched to the buddy
        # in this case: Alt+W will switch focus to self.widthSpinBox because widthLabel has
        # a 'W' accelerator and a self.widthSpinBox buddy
        widthLabel = QLabel("&Width:")
        self.widthSpinBox = QSpinBox()
        widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight)
        self.widthSpinBox.setRange(0, 24)

        self.bevelledCheckBox = QCheckBox("&Bevelled edges")
        
        styleLabel = QLabel("&Style:")
        self.styleComboBox = QComboBox()
        styleLabel.setBuddy(self.styleComboBox)
        self.styleComboBox.addItems(['Solid', 'Dashed', 'Dotted', 'DashedDotted', "DashDotDotted"])
        
        okButton = QPushButton("&OK")
        cancelButton = QPushButton("Cancel")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout = QGridLayout()
        layout.addWidget(widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.bevelledCheckBox, 0, 2)
        layout.addWidget(styleLabel, 1, 0)
        layout.addWidget(self.styleComboBox, 1, 1, 1, 2)
        layout.addLayout(buttonLayout, 2, 0, 1, 3)

        self.setLayout(layout)

        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)

        self.setWindowTitle("Pen Properties")

    def accept(self):
        print("OK clicked")
        QDialog.accept(self)
    
    def reject(self):
        print("Cancel clicked")
        QDialog.accept(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = PenPropertiesDlg()
    form.show()
    app.exec_()
