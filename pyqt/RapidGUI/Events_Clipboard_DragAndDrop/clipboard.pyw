#! python3
import os
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QDialog, QPushButton, QLabel, QGridLayout,
    QApplication)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        textCopyButton = QPushButton("&Copy Text")
        textPasteButton = QPushButton("Paste &Text")
        htmlCopyButton = QPushButton("C&opy HTML")
        htmlPasteButton = QPushButton("Paste &HTML")
        imageCopyButton = QPushButton("Co&py Image")
        imagePasteButton = QPushButton("Paste &Image")
        self.textLabel = QLabel("Original text")
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap(os.path.join(
                os.path.dirname(__file__), "images/clock.png")))

        layout = QGridLayout()
        layout.addWidget(textCopyButton, 0, 0)
        layout.addWidget(imageCopyButton, 0, 1)
        layout.addWidget(htmlCopyButton, 0, 2)
        layout.addWidget(textPasteButton, 1, 0)
        layout.addWidget(imagePasteButton, 1, 1)
        layout.addWidget(htmlPasteButton, 1, 2)
        layout.addWidget(self.textLabel, 2, 0, 1, 2)
        layout.addWidget(self.imageLabel, 2, 2)
        self.setLayout(layout)

        # self.connect(textCopyButton, SIGNAL("clicked()"), self.copyText)
        # self.connect(textPasteButton, SIGNAL("clicked()"), self.pasteText)
        # self.connect(htmlCopyButton, SIGNAL("clicked()"), self.copyHtml)
        # self.connect(htmlPasteButton, SIGNAL("clicked()"), self.pasteHtml)
        # self.connect(imageCopyButton, SIGNAL("clicked()"), self.copyImage)
        # self.connect(imagePasteButton, SIGNAL("clicked()"),
        #              self.pasteImage)

        textCopyButton.clicked.connect(self.copyText)
        textPasteButton.clicked.connect(self.pasteText)
        htmlCopyButton.clicked.connect(self.copyHtml)
        htmlPasteButton.clicked.connect(self.pasteHtml)
        imageCopyButton.clicked.connect(self.copyImage)
        imagePasteButton.clicked.connect(self.pasteImage)

        self.setWindowTitle("Clipboard")


    def copyText(self):
        clipboard = QApplication.clipboard()
        clipboard.setText("I've been clipped!")


    def pasteText(self):
        clipboard = QApplication.clipboard()
        self.textLabel.setText(clipboard.text())


    def copyImage(self):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(QPixmap(os.path.join(
                os.path.dirname(__file__), "images/gvim.png")))

    def pasteImage(self):
        clipboard = QApplication.clipboard()
        self.imageLabel.setPixmap(clipboard.pixmap())


    def copyHtml(self):
        mimeData = QMimeData()
        mimeData.setHtml("<b>Bold and <font color=red>Red</font></b>")
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mimeData)


    def pasteHtml(self):
        clipboard = QApplication.clipboard()
        mimeData = clipboard.mimeData()
        if mimeData.hasHtml():
            self.textLabel.setText(mimeData.html())


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()

