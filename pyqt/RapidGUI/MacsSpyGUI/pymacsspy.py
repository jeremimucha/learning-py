#! python3

import os
import sys
from PyQt5.QtCore import (QThread, QMutex, QMutexLocker, QReadLocker,
     QWriteLocker, pyqtSignal)


class MacsThread(QThread):

    tick = pyqtSignal('QString')

    def __init__(self, lock, parent=None):
        super().__init__(parent)

        self.args = None
        self.command = None


    def initialize(self, command, args):
        self.command = command
        self.args = args


    def run(self):
        process = QProcess()
        process.start(self.command, self.args)
        process.waitForFinished(-1)
