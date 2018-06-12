#! python3
#! python3
from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit, QSpinBox, QCheckBox, QDialogButtonBox,
    QMessageBox, QGridLayout)


'''
Smart dialog. -- Uses preventative validation.
It would be called like so:

def setNumberFormat2(self):
    dialog = numberformatdlg2.NumberFormatDlg(self.format, self)
    self.connect(dialog, SIGNAL('changed'), self.refreshTable)
    dialog.show()


'''

class NumberFormatDlg(QDialog):

    changed = pyqtSignal(name='changed')

    def __init__(self, format, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

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

        # connect directly to the button clicked method, so that the dialog isn't closed on apply
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.rejected.connect(self.reject)

        self.setWindowTitle("Set Number Format (Modeless)")

    def numberFormat(self):
        return self.format

    def apply(self):
        thousands = str(self.thousandsEdit.text())
        decimal = str(self.decimalMarkerEdit.text())
        if thousands == decimal:
            QMessageBox.warning(self, 'Format Error', 'The thousands separator and the decimal marker '
                'must be different.')
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        if len(decimal) == 0:
            QMessageBox.warning(self, 'Format Error', 'The decimal marker may not be empty.')
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format['thousandsseparator'] = thousands
        self.format['decimalmarker'] = decimal
        self.format['decimalplaaces'] = self.decimalPlacesSpinBox.value()
        self.format['rednegatives'] = self.redNegativesCheckBox.isChecked()
        # this signal is used by the caller
        self.changed.emit()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    format = dict(thousandsseparator=',', decimalmarker='.', decimalplaces=7, rednegatives=False)
    form = NumberFormatDlg(format)
    form.show()
    app.exec_()
