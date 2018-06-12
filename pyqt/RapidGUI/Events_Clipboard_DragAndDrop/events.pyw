#! python3
import sys
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QMenu


class Widget(QWidget):

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.justDoubleClicked = False
        self.key = ""
        self.text = ""
        self.message = ""
        self.resize(400, 300)
        self.move(100, 100)
        self.setWindowTitle("Events")
        QTimer.singleShot(0, self.giveHelp) # Avoids first resize msg


    def giveHelp(self):
        self.text = "Click to toggle mouse tracking"
        self.update()


    def closeEvent(self, event):
        print("Closed")


    def contextMenuEvent(self, event):
        menu = QMenu(self)
        oneAction = menu.addAction("&One")
        twoAction = menu.addAction("&Two")
        # self.connect(oneAction, SIGNAL("triggered()"), self.one)
        # self.connect(twoAction, SIGNAL("triggered()"), self.two)
        oneAction.triggered.connect(self.one)
        twoAction.triggered.connect(self.one)
        if not self.message:
            menu.addSeparator()
            threeAction = menu.addAction("Thre&e")
            threeAction.triggered.connect(self.three)
            # self.connect(threeAction, SIGNAL("triggered()"),
            #              self.three)
        menu.exec_(event.globalPos())


    def one(self):
        self.message = "Menu option One"
        self.update()


    def two(self):
        self.message = "Menu option Two"
        self.update()


    def three(self):
        self.message = "Menu option Three"
        self.update()


    def paintEvent(self, event):
        text = self.text
        i = text.find("\n\n")
        if i >= 0:
            text = text[:i]
        if self.key:
            text += "\n\nYou pressed: {}".format(self.key)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.drawText(self.rect(), Qt.AlignCenter, text)
        if self.message:
            painter.drawText(self.rect(), Qt.AlignBottom|Qt.AlignHCenter,
                             self.message)
            # QTimer.singleShot(5000, self.message.)
            QTimer.singleShot(5000, self.update)


    def resizeEvent(self, event):
        self.text = "Resized to QSize({}, {})".format(
                            event.size().width(), event.size().height())
        self.update()

        
    def mouseReleaseEvent(self, event):
        if self.justDoubleClicked:
            self.justDoubleClicked = False
        else:
            self.setMouseTracking(not self.hasMouseTracking())
            if self.hasMouseTracking():
                self.text = ("Mouse tracking is on.\n"
                        "Try moving the mouse!\n"
                        "Single click to switch it off")
            else:
                self.text = ("Mouse tracking is off.\n"
                             "Single click to switch it on")
            self.update()


    def mouseMoveEvent(self, event):
        if not self.justDoubleClicked:
            globalPos = self.mapToGlobal(event.pos())
            self.text = ("The mouse is at\nQPoint({0}, {1}) "
                    "in widget coords, and\n"
                    "QPoint({2}, {3}) in screen coords".format(
                    event.pos().x(), event.pos().y(), globalPos.x(),
                    globalPos.y()))
            self.update()


    def mouseDoubleClickEvent(self, event):
        self.justDoubleClicked = True
        self.text = "Double-clicked."
        self.update()


    def keyPressEvent(self, event):
        self.key = ""
        if event.key() == Qt.Key_Home:
            self.key = "Home"
        elif event.key() == Qt.Key_End:
            self.key = "End"
        elif event.key() == Qt.Key_PageUp:
            if event.modifiers() & Qt.ControlModifier:
                self.key = "Ctrl+PageUp"
            else:
                self.key = "PageUp"
        elif event.key() == Qt.Key_PageDown:
            if event.modifiers() & Qt.ControlModifier:
                self.key = "Ctrl+PageDown"
            else:
                self.key = "PageDown"
        elif Qt.Key_A <= event.key() <= Qt.Key_Z:
            if event.modifiers() & Qt.ShiftModifier:
                self.key = "Shift+"
            self.key += event.text()
        if self.key:
            self.update()
        else:
            QWidget.keyPressEvent(self, event)


    def event(self, event):
        if (event.type() == QEvent.KeyPress and
            event.key() == Qt.Key_Tab):
            self.key = "Tab captured in event()"
            self.update()
            return True
        return QWidget.event(self, event)


app = QApplication(sys.argv)
form = Widget()
form.show()
app.exec_()

