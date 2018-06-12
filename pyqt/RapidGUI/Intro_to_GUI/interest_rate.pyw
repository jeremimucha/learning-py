#! python3
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QDoubleSpinBox, QComboBox, QGridLayout


class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        lbl_principal = QLabel("Principal:")
        lbl_rate      = QLabel("Rate:")
        lbl_years     = QLabel("Years:")
        lbl_amount    = QLabel("Amount")
        self.lbl_result    = QLabel("$ 1.01")

        self.sbox_principal = QDoubleSpinBox()
        self.sbox_principal.setRange(0.01, 1000000.00)
        self.sbox_principal.setValue(1.00)
        self.sbox_principal.setPrefix('$ ')

        self.sbox_rate = QDoubleSpinBox()
        self.sbox_rate.setRange(0.01, 100.00)
        self.sbox_rate.setValue(1.00)
        self.sbox_rate.setSuffix(' %')

        self.cbox_years = QComboBox()
        self.cbox_years.addItems(('{} years'.format(i) for i in range(1, 11)))

        grid = QGridLayout()
        grid.addWidget(lbl_principal, 0, 0)
        grid.addWidget(self.sbox_principal, 0, 1)
        grid.addWidget(lbl_rate, 1, 0)
        grid.addWidget(self.sbox_rate, 1, 1)
        grid.addWidget(lbl_years, 2, 0)
        grid.addWidget(self.cbox_years, 2, 1)
        grid.addWidget(lbl_amount, 3, 0)
        grid.addWidget(self.lbl_result, 3, 1)

        self.sbox_principal.valueChanged.connect(self.updateUI)
        self.sbox_rate.valueChanged.connect(self.updateUI)
        self.cbox_years.currentIndexChanged.connect(self.updateUI)

        self.setLayout(grid)
        self.setWindowTitle('Interest')

    def updateUI(self):
        principal = self.sbox_principal.value()
        rate = self.sbox_rate.value()
        years = self.cbox_years.currentIndex() + 1
        amount = principal * ((1 + (rate / 100.0)) ** years)
        self.lbl_result.setText('$ {:.2f}'.format(amount))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
