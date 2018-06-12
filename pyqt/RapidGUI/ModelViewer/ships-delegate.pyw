#! python3
import sys
from PyQt5.QtCore import (Qt, QTimer, QFile,)
# from PyQt5.QtGui import ()
from PyQt5.QtWidgets import (QDialog, QApplication, QLabel, QTableView, QPushButton,
    QHBoxLayout, QVBoxLayout, QSplitter, QWidget, QMessageBox, QFileDialog)
import ships

MAC = "qt_mac_set_native_menubar" in dir()


class MainForm(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.model = ships.ShipTableModel("ships.dat")
        tableLabel1 = QLabel("Table &1")
        self.tableView1 = QTableView()
        tableLabel1.setBuddy(self.tableView1)
        self.tableView1.setModel(self.model)
        self.tableView1.setItemDelegate(ships.ShipDelegate(self))
        tableLabel2 = QLabel("Table &2")
        self.tableView2 = QTableView()
        tableLabel2.setBuddy(self.tableView2)
        self.tableView2.setModel(self.model)
        self.tableView2.setItemDelegate(ships.ShipDelegate(self))

        addShipButton = QPushButton("&Add Ship")
        removeShipButton = QPushButton("&Remove Ship")
        exportButton = QPushButton("&Export...")
        quitButton = QPushButton("&Quit")
        if not MAC:
            addShipButton.setFocusPolicy(Qt.NoFocus)
            removeShipButton.setFocusPolicy(Qt.NoFocus)
            exportButton.setFocusPolicy(Qt.NoFocus)
            quitButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addShipButton)
        buttonLayout.addWidget(removeShipButton)
        buttonLayout.addWidget(exportButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        splitter = QSplitter(Qt.Horizontal)
        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel1)
        vbox.addWidget(self.tableView1)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        vbox = QVBoxLayout()
        vbox.addWidget(tableLabel2)
        vbox.addWidget(self.tableView2)
        widget = QWidget()
        widget.setLayout(vbox)
        splitter.addWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        for tableView in (self.tableView1, self.tableView2):
            header = tableView.horizontalHeader()
            header.sectionClicked[int].connect(self.sortTable)
        addShipButton.clicked.connect(self.addShip)
        removeShipButton.clicked.connect(self.removeShip)
        exportButton.clicked.connect(self.exportData)
        quitButton.clicked.connect(self.accept)
        #     self.connect(header, SIGNAL("sectionClicked(int)"),
        #                  self.sortTable)
        # self.connect(addShipButton, SIGNAL("clicked()"), self.addShip)
        # self.connect(removeShipButton, SIGNAL("clicked()"),
        #              self.removeShip)
        # self.connect(quitButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle("Ships (delegate)")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        if not QFile.exists(self.model.filename):
            self.model.beginResetModel()
            for ship in ships.generateFakeShips():
                self.model.ships.append(ship)
                self.model.owners.add(ship.owner)
                self.model.countries.add(ship.country)
            self.model.endResetModel()
            # self.model.reset()
            self.model.dirty = False
        else:
            try:
                self.model.load()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to load: {}".format(e))
        self.model.sortByName()
        self.resizeColumns()


    def resizeColumns(self):
        self.tableView1.resizeColumnsToContents()
        self.tableView2.resizeColumnsToContents()


    def reject(self):
        self.accept()


    def accept(self):
        if (self.model.dirty and
            QMessageBox.question(self, "Ships - Save?",
                    "Save unsaved changes?",
                    QMessageBox.Yes|QMessageBox.No) ==
                    QMessageBox.Yes):
            try:
                self.model.save()
            except IOError as e:
                QMessageBox.warning(self, "Ships - Error",
                        "Failed to save: {}".format(e))
        QDialog.accept(self)

    
    def sortTable(self, section):
        if section in (ships.OWNER, ships.COUNTRY):
            self.model.sortByCountryOwner()
        elif section == ships.TEU:
            self.model.sortByTEU()
        else:
            self.model.sortByName()
        self.resizeColumns()


    def addShip(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, 0)
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        tableView.setFocus()
        tableView.setCurrentIndex(index)
        tableView.edit(index)


    def removeShip(self):
        tableView = self.tableView1
        if self.tableView2.hasFocus():
            tableView = self.tableView2
        index = tableView.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        name = self.model.data(
                    self.model.index(row, ships.NAME))
        owner = self.model.data(
                    self.model.index(row, ships.OWNER))
        country = self.model.data(
                    self.model.index(row, ships.COUNTRY))
        if (QMessageBox.question(self, "Ships - Remove", 
                "Remove {} of {}/{}?".format(name, owner, country),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRow(row)
        self.resizeColumns()

    def exportData(self, fname):
        fname = '.'
        fname, _ = QFileDialog.getSaveFileName(self, "Ships - Save to txt",
                                                fname, "Text files (*.txt)")
        if fname and fname[-4:] != '.txt':
            fname += '.txt'
        ok, msg = self.model.exportToTxt(fname)
        if ok:
            QMessageBox.information(self, "Ships - Save to txt", msg)
        else:
            QMessageBox.warning(self, "Ships - Error", msg)

app = QApplication(sys.argv)
form = MainForm()
form.show()
app.exec_()

