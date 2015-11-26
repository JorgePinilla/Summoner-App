from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QScrollArea
from PyQt4.QtGui import QVBoxLayout

class ChampionsWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.widgetLayout = QVBoxLayout()
        self.setLayout(self.widgetLayout)

        self.container = QLabel()
        self.container.setStyleSheet("QLabel {background-color: black}")

        self.championPanel = QScrollArea()
        self.championPanel.resize(620, 240)
        self.championPanel.setWidget(self.container)

        self.widgetLayout.addWidget(self.championPanel)

    def showStats(self, values, championIconList):
        yPos = 5
        self.container.resize(680, (len(values) * 55) + yPos)
        for x in values:
            temp = ChampionTab(self.container)
            temp.setIcon(championIconList[x['name']])
            temp.setName(x['name'])
            temp.setNumOfSessions(x['sessions'])
            temp.setWinRatio(x['winRate'])
            temp.setKDA(x['kills'], x['deaths'], x['assists'])
            temp.setCS(x['cs'])
            temp.move(5, yPos)
            yPos += 55


class ChampionTab(QLabel):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.resize(670, 50)
        self.setStyleSheet("QLabel {color: black; background-color: gold; border-radius:10px}")

        self.champPic = QLabel(self)
        self.champPic.setScaledContents(True)
        self.champPic.resize(40, 40)
        self.champPic.move(5, 5)

        self.champName = QLabel(self)
        self.champName.setStyleSheet("QLabel {font: 14px}")
        self.champName.resize(100, 40)
        self.champName.move(46, 5)

        self.numOfSessions = QLabel(self)
        self.numOfSessions.setAlignment(Qt.AlignCenter)
        self.numOfSessions.resize(40, 40)
        self.numOfSessions.move(147, 5)

        self.winRatio = QLabel(self)
        self.winRatio.setAlignment(Qt.AlignCenter)
        self.winRatio.resize(60, 40)
        self.winRatio.move(188, 5)

        self.kda = QLabel(self)
        self.kda.setAlignment(Qt.AlignCenter)
        self.kda.resize(200, 40)
        self.kda.move(249, 5)

        self.cs = QLabel(self)
        self.cs.setAlignment(Qt.AlignCenter)
        self.cs.resize(60, 40)
        self.cs.move(450, 5)

    def setIcon(self, champIcon):
        self.champPic.setPixmap(champIcon)

    def setName(self, name):
        self.champName.setText(name)

    def setNumOfSessions(self, num):
        self.numOfSessions.setText(str(num))

    def setWinRatio(self, winRate):
        self.winRatio.setText(str(winRate) + '%')

    def setKDA(self, kills, deaths, assists):
        self.kda.setText(str(kills) + " / " + str(deaths) + " / " + str(assists))

    def setCS(self, cs):
        self.cs.setText(str(cs))
