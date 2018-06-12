#! python3
import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QDialog, QApplication, QListWidget, QPushButton, QVBoxLayout, QInputDialog,
    QLineEdit, QMessageBox, QHBoxLayout)


class StringListDlg(QDialog):

    acceptedList = pyqtSignal('QStringList')

    def __init__(self, name, stringlist=None, parent=None):
        super().__init__(parent)

        self.name = name

        self.listWidget = QListWidget()
        if stringlist is not None:
            self.listWidget.addItems(stringlist)
            self.listWidget.setCurrentRow(0)
        
        buttonLayout = QVBoxLayout()
        button = None
        for text, slot in (('&Add...', self.add),
                           ('&Edit...', self.edit),
                           ('&Remove...', self.remove),
                           ('&Up', self.up),
                           ('&Down', self.down),
                           ('&Sort', self.listWidget.sortItems)):
            button = QPushButton(text)
            buttonLayout.addWidget(button)
            button.clicked.connect(slot)
        buttonLayout.addStretch()
        button = QPushButton("Close")
        buttonLayout.addWidget(button)
        button.clicked.connect(self.accept)

        layout = QHBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addLayout(buttonLayout)
        
        self.setLayout(layout)
        self.setWindowTitle("Edit {} List".format(self.name))

    def add(self):
        row = self.listWidget.currentRow()
        title = "Add {}".format(self.name)
        string, ok = QInputDialog.getText(self, title, title)
        if ok and string:
            self.listWidget.insertItem(row, string)

    def edit(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is not None:
            title = "Edit {}".format(self.name)
            string, ok = QInputDialog.getText(self, title, title, QLineEdit.Normal, item.text())
            if ok and string:
                item.setText(string)

    def remove(self):
        row = self.listWidget.currentRow()
        item = self.listWidget.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, "Remove {}".format(self.name),
                "Remove {} '{}'?".format(self.name, item.text()),
                QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.listWidget.takeItem(row)
            del item

    def up(self):
        row = self.listWidget.currentRow()
        if row >= 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row - 1, item)
            self.listWidget.setCurrentItem(item)

    def down(self):
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            item = self.listWidget.takeItem(row)
            self.listWidget.insertItem(row + 1, item)
            self.listWidget.setCurrentItem(item)

    def reject(self):
        self.accept()

    def accept(self):
        self.stringlist = []
        for row in range(self.listWidget.count()):
            self.stringlist.append(self.listWidget.item(row).text())
        self.acceptedList.emit(self.stringlist)
        QDialog.accept(self)


if __name__ == "__main__":
    fruit = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
        "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
        "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi", "Lemon",
        "Nectarine", "Plum", "Raspberry", "Strawberry", "Orange"]
    app = QApplication(sys.argv)
    form = StringListDlg("Fruit", fruit)
    form.exec_()
    print("\n".join(form.stringlist))
