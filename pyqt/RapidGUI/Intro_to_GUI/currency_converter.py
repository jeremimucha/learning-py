#! python3
import sys
from urllib.request import urlopen
from PyQt5.QtWidgets import QDialog, QLabel, QComboBox, QDoubleSpinBox, QApplication, QGridLayout


class Form(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        date = self.getData()
        rates = sorted(self.rates.keys())

        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 100000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)

        self.fromComboBox.currentIndexChanged.connect(self.updateUI)
        self.toComboBox.currentIndexChanged.connect(self.updateUI)
        self.fromSpinBox.valueChanged.connect(self.updateUI)
        
        self.setWindowTitle("Currency")

    def updateUI(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        amount = (self.rates[from_] / self.rates[to]) * self.fromSpinBox.value()
        self.toLabel.setText("{:.2f}".format(amount))

    def getData(self):
        self.rates = {}
        try:
            date = "Unknown"
            fh = urlopen("http://www.bankofcanada.ca/stats/assets/csv/fx-seven-day.csv")
            for line in fh:
                if not line or line.startswith(b"#") or line.startswith(b"Closing "):
                    continue
                fields = line.split(b", ")
                if line.startswith(b"Date "):
                    date = fields[-1].decode('utf8')
                else:
                    try:
                        value = float(fields[-1])
                        self.rates[fields[0].decode('utf8')] = value
                    except ValueError:
                        pass
            return "Exchange Rates Date: {}".format(date)
        except Exception as e:
            return "Failed to download:\n{}".format(e)

app = QApplication(sys.argv)
form =  Form()
form.show()
app.exec_()
