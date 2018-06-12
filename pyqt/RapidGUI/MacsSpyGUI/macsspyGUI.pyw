#! python3
import os
import sys
from serial.tools import list_ports
from PyQt5.QtCore import (Qt, QSettings, QDir, pyqtSignal, QProcess, QThread)
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QLabel,
     QComboBox, QDialogButtonBox, QGridLayout, QVBoxLayout, QLineEdit,
     QTextBrowser, QTextEdit, QPushButton, QFileDialog, QDialog, QGroupBox,
     QFrame)
#import pymacsspy


class OptionsForm(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        settings = QSettings()

        macsspyLabel = QLabel('MacsSpy')
        self.macsspyLabel = QLabel(settings.value('macsspy', MACSSPY))
        # self.macsspyLabel = QLabel(MACSSPY)
        macsspyButton = QPushButton('Macs&Spy')

        macssplitLabel = QLabel('MacSplit')
        self.macssplitLabel = QLabel(settings.value('macssplit', MACSSPLIT))
        # self.macssplitLabel = QLabel(MACSSPLIT)
        macssplitButton = QPushButton('MacsSpli&t')

        macsreadLabel = QLabel('MacsRead')
        self.macsreadLabel = QLabel(settings.value('macsread', MACSREAD))
        # self.macsreadLabel = QLabel(MACSREAD)
        macsreadButton = QPushButton('Macs&Read')

        timeconvertLabel = QLabel('TimeConvert')
        self.timeconvertLabel = QLabel(settings.value('timeconvert', TIMECONVERT))
        # self.timeconvertLabel = QLabel(TIMECONVERT)
        timeconvertButton = QPushButton('Time&Convert')

        for label in (self.macsspyLabel, self.macsreadLabel,
                        self.macssplitLabel, self.timeconvertLabel):
            label.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)

        toolPathGroupBox = QGroupBox('Tool Paths')
        pathLayout = QGridLayout()
        pathLayout.addWidget(macsspyLabel, 0, 0)
        pathLayout.addWidget(self.macsspyLabel, 0, 1)
        pathLayout.addWidget(macsspyButton, 0, 2)
        pathLayout.addWidget(macssplitLabel, 1, 0)
        pathLayout.addWidget(self.macssplitLabel, 1, 1)
        pathLayout.addWidget(macssplitButton, 1, 2)
        pathLayout.addWidget(macsreadLabel, 2, 0)
        pathLayout.addWidget(self.macsreadLabel, 2, 1)
        pathLayout.addWidget(macsreadButton, 2, 2)
        pathLayout.addWidget(timeconvertLabel, 3, 0)
        pathLayout.addWidget(self.timeconvertLabel, 3, 1)
        pathLayout.addWidget(timeconvertButton, 3, 2)
        toolPathGroupBox.setLayout(pathLayout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(toolPathGroupBox)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.tools = {'macsspy': self.macsspyLabel,
                      'macssplit': self.macssplitLabel,
                      'macsread': self.macsreadLabel,
                      'timeconvert': self.timeconvertLabel
                     }

        macsspyButton.clicked.connect(lambda: self.setPath('macsspy'))
        macsreadButton.clicked.connect(lambda: self.setPath('macsread'))
        macssplitButton.clicked.connect(lambda: self.setPath('macssplit'))
        timeconvertButton.clicked.connect(lambda: self.setPath('timeconvert'))
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.setWindowTitle('macsspyGUI - Settings')

    def accept(self):
        settings = QSettings()
        settings.setValue('macsspy', self.macsspyLabel.text())
        settings.setValue('macsread', self.macsreadLabel.text())
        settings.setValue('macssplit', self.macssplitLabel.text())
        settings.setValue('timeconvert', self.timeconvertLabel.text())
        QDialog.accept(self)

    
    def setPath(self, tool):
        label = self.tools.get(tool)
        path, _ = QFileDialog.getOpenFileName(self, 'MacsSpyGUI - Set Tool Path',
                label.text())
        if path:
            label.setText(QDir.toNativeSeparators(path))


class ComComboBox(QComboBox):
    popupAboutToBeShown = pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super().showPopup()


class MacsThread(QThread):
    
    started = pyqtSignal(bool)
    finished = pyqtSignal(bool)
    readyRead = pyqtSignal(str)

    def __init__(self, lock, parent=None):
        super().__init__(parent)

        self.process = QProcess()
        self.process.readyRead.connect(self.emitReadyRead)
        self.process.started.connect(self.emitStarted)
        self.process.finished.connect(self.emitFinished)

        self.args = None
        self.command = None

    def initialize(self, command, args):
        self.command = command
        self.args = args

    def run(self):
        self.process.start(self.command, self.args)
        self.process.waitForFinished(-1)


    def stop(self):
        if self.process:
            self.process.kill()
            self.finished.emit(True)

    def emitReadyRead(self):
        self.readyRead.emit(str(self.process.readAll(), encoding='UTF8'))

    def emitStarted(self):
        self.started.emit(True)

    def emitFinished(self):
        self.finished.emit(True)


class Form(QMainWindow):

    def __init__(self):
        super().__init__(None)

        settings = QSettings()
        self.macsspy = settings.value('macsspy', MACSSPY)
        self.macssplit = settings.value('macssplit', MACSSPLIT)
        self.macsread = settings.value('macsread', MACSREAD)
        self.timeconvert = settings.value('timeconvert', TIMECONVERT)
        print('Tools:')
        for tool in (self.macsspy, self.macssplit, self.macsread, self.timeconvert):
            print(tool)

        self.process = MacsThread(self)
        self.process.readyRead[str].connect(self.readSpy)
        self.process.started.connect(lambda: self.updateUi(False))
        self.process.finished.connect(lambda: self.updateUi(True))


        # pathLabel = QLabel("Path:");
        path = settings.value("path") or os.getcwd()
        self.pathEdit = QLineEdit(path)
        self.pathEdit.setToolTip("Log files will be saved in this directory.")
        self.pathButton = QPushButton("&Path...")

        self.comBox = ComComboBox()
        self.updatePorts()
        # possibly useful?
        # self.comBox.currentIndexChanged.connect(self. ???)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Vertical)
        self.runButton = self.buttonBox.addButton("&Run",
                QDialogButtonBox.ActionRole)
        self.stopButton = self.buttonBox.addButton("&Stop",
                QDialogButtonBox.ActionRole)
        self.stopButton.setEnabled(False)
        self.settingsButton = self.buttonBox.addButton("&Settings",
                QDialogButtonBox.ActionRole)
        
        self.spyLog = QTextEdit()
        self.spyLog.setReadOnly(True)
        self.spyLog.setLineWrapMode(QTextEdit.NoWrap)

        layout = QGridLayout()
        layout.addWidget(self.pathButton, 0, 0)
        layout.addWidget(self.pathEdit, 0, 1)
        layout.addWidget(self.comBox, 1, 0)
        layout.addWidget(self.buttonBox, 2, 0)
        layout.addWidget(self.spyLog, 1, 1, 2, 1)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.settingsButton.clicked.connect(self.setSettings)
        self.pathButton.clicked.connect(self.setPath)
        self.runButton.clicked.connect(self.runSpy)
        self.stopButton.clicked.connect(self.stopSpy)
        self.comBox.popupAboutToBeShown.connect(self.updatePorts)

        self.setWindowTitle("MacsSpyGUI")


    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("path", self.pathEdit.text())
        event.accept()


    def setPath(self):
        fname = self.pathEdit.text() or '.'
        fname, _ = QFileDialog.getSaveFileName(self,
                "MacsSpyGUI - Save Log", fname,
                "Log files *.log")
        if fname:
            if '.' not in fname:
                fname += '.log'
            self.pathEdit.setText(QDir.toNativeSeparators(fname))
            return True
        return False


    def runSpy(self):
        comport = str(self.comBox.currentText())
        print('Starting process: {} {}'.format(self.macsspy, comport))
        self.process.initialize(self.macsspy, (comport,))
        self.process.start()


    def stopSpy(self):
        self.process.stop()

    
    def readSpy(self, str):
        cursor = self.spyLog.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str)
        # self.output.ensureCursorV


    def setSettings(self):
        dlg = OptionsForm(self)
        if dlg.exec_(): pass
            # self.macsspy = 


    def updatePorts(self):
        print('In updatePorts()')
        ports = list_ports.comports()
        self.comBox.clear()
        self.comBox.addItems([str(p).split('-')[0] for p in ports])

    
    def updateUi(self, enable):
        print('In updateUI(self, {})'.format(enable))
        for widget in (self.comBox, self.pathEdit,
                    self.runButton, self.pathButton):
            widget.setEnabled(enable)
        self.stopButton.setEnabled(not enable)
        self.spyLog.setFocus()


app = QApplication(sys.argv)
# PATH = app.applicationDirPath()
PATH = os.path.abspath('.')
PATH = os.path.join(PATH, 'MacsLib')
MACSSPY = os.path.join(PATH, 'MacsSpy.exe')
MACSREAD = os.path.join(PATH, 'MacsReadGMB.exe')
MACSSPLIT = os.path.join(PATH, 'MacsSplit.exe')
TIMECONVERT = os.path.join(PATH, 'TimeConvert.exe')
form = Form()
form.show()
app.exec_()
