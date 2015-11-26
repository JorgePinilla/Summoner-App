from riot import *
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QWidget

class RuneWidget(QWidget):

    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)

        self.page_name = QLabel(self)
        self.page_name.setMaximumHeight(30)

        self.field = QTextEdit(self)
        self.field.setReadOnly(True)
        self.field.setFontPointSize(14)
        self.field.move(0, 30)

        self.runesID = {}
        self.runesDescription = {}
        self.rune_name = {}

    def setSize(self, x, y):
        self.page_name.resize(x, 30)
        self.field.resize(x, y-30)

    def setName(self, name):
        self.page_name.setText(name)

    def addRune(self, rune, description, runeName):
        if not (rune in self.runesID):
            self.runesID[rune] = 1
            self.runesDescription[rune] = description
            self.rune_name[rune] = runeName.split(' ')[1]
        else:
            self.runesID[rune] += 1

    def showRunes(self):
        for x in self.runesID.keys():
            descript = self.runesDescription[x].replace('+', '').split(' ')
            stat = float(descript[0].replace('%', ''))
            del descript[0]
            info = ' '.join(descript).split('(')[0]
            self.field.insertPlainText("+" + str(self.runesID[x] * stat) + " " + info + " (" + self.rune_name[x] + ")" + "\n")
