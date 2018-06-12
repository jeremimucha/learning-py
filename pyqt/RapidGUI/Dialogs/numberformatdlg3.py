#! python3
#! python3
from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, QSpinBox, QCheckBox, QDialogButtonBox,
    QMessageBox, QGridLayout)


'''
modeless "live" dialog - uses exclusively preventative validation, changes are applied automatically
on every edit action.

To avoid creating the dialog everytime, we can hide it and show it once it is created for the first time

def setNumberFormat3(self):
    if self.numberFormatDlg is None:
        self.numberFormatDlg = numberformatdlg3.NumberFormatDlg(self.format, self.refreshTable, self)
    
    self.numberFormatDlg.show()
    self.numberFormatDlg.raise_()
    self.numberFormatDlg.activateWindow()

'''

class NumberFormatDlg(QDialog):

    changed = pyqtSignal(name='changed')

    def __init__(self, format, callback, parent=None):
        super().__init__(parent)

        # keep a reference to the callback
        self.callback = callback
        # take a reference to the format dict
        self.format = format

        puctuationRe = QRegExp(r'[ ,;:.]')

        thousandsLabel = QLabel("&Thousands separator")
        self.thousandsEdit = QLineEdit(format['thousandsseparator'])
        thousandsLabel.setBuddy(self.thousandsEdit)
        self.thousandsEdit.setMaxLength(1)
        self.thousandsEdit.setValidator(QRegExpValidator(puctuationRe, self))

        decimalMarkerLabel = QLabel('Decimal &marker')
        self.decimalMarkerEdit = QLineEdit(format['decimalmarker'])
        decimalMarkerLabel.setBuddy(self.decimalMarkerEdit)
        self.decimalMarkerEdit.setMaxLength(1)
        self.decimalMarkerEdit.setValidator(QRegExpValidator(puctuationRe, self))
        self.decimalMarkerEdit.setInputMask("X")

        decimalPlacesLabel = QLabel ("&Decimal places")
        self.decimalPlacesSpinBox = QSpinBox()
        decimalPlacesLabel.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format['decimalplaces'])

        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format['rednegatives'])

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Close)

        grid = QGridLayout()
        grid.addWidget(thousandsLabel, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimalMarkerLabel, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimalPlacesLabel, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0 , 1, 2)
        grid.addWidget(buttonBox, 4, 0, 1, 2)

        self.setLayout(grid)

        self.thousandsEdit.textEdited['QString'].connect(self.checkAndFix)
        self.decimalMarkerEdit.textEdited['QString'].connect(self.checkAndFix)
        self.decimalPlacesSpinBox.valueChanged[int].connect(self.apply)
        self.redNegativesCheckBox.toggled[bool].connect(self.apply)

        self.setWindowTitle("Set Number Format (Modeless)")

    def numberFormat(self):
        return self.format

    def checkAndFix(self):
        thousands = str(self.thousandsEdit.text())
        decimal = str(self.decimalMarkerEdit.text())
        if thousands == decimal:
            self.thousandsEdit.clear()
            self.thousandsEdit.setFocus()
        if len(decimal) == 0:
            self.decimalMarkerEdit.setText('.')
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
        self.apply()

    def apply(self):

        self.format['thousandsseparator'] = str(self.thousandsEdit.text())
        self.format['decimalmarker'] = str(self.decimalMarkerEdit.text())
        self.format['decimalplaaces'] = self.decimalPlacesSpinBox.value()
        self.format['rednegatives'] = self.redNegativesCheckBox.isChecked()
        
        self.callback()


if __name__ == '__main__':
    import sys
    
    def someCallback():
        print("someCallback called")
    
    app = QApplication(sys.argv)
    format = dict(thousandsseparator=',', decimalmarker='.', decimalplaces=7, rednegatives=False)
    form = NumberFormatDlg(format, someCallback)
    form.show()
    app.exec_()
