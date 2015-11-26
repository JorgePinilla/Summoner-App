from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel

class OverviewWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.neutral_monsters_title = QLabel(self)
        self.neutral_monsters_total = QLabel(self)
        self.neutral_monsters_title.resize(230, 30)
        self.neutral_monsters_total.resize(230, 70)
        self.neutral_monsters_title.move(240, 115)
        self.neutral_monsters_total.move(240, 155)
        self.neutral_monsters_title.setAlignment(Qt.AlignCenter)
        self.neutral_monsters_total.setAlignment(Qt.AlignCenter)
        self.neutral_monsters_title.setStyleSheet("QLabel {font: 14pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")
        self.neutral_monsters_total.setStyleSheet("QLabel {font: 24pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")

        self.minions_title = QLabel(self)
        self.minions_total = QLabel(self)
        self.minions_title.resize(230, 30)
        self.minions_total.resize(230, 70)
        self.minions_title.move(0, 115)
        self.minions_total.move(0, 155)
        self.minions_title.setAlignment(Qt.AlignCenter)
        self.minions_total.setAlignment(Qt.AlignCenter)
        self.minions_title.setStyleSheet("QLabel {font: 14pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")
        self.minions_total.setStyleSheet("QLabel {font: 24pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")

        self.champions_title = QLabel(self)
        self.champions_total = QLabel(self)
        self.champions_title.resize(230, 30)
        self.champions_total.resize(230, 70)
        self.champions_title.move(240, 0)
        self.champions_total.move(240, 40)
        self.champions_title.setAlignment(Qt.AlignCenter)
        self.champions_total.setAlignment(Qt.AlignCenter)
        self.champions_title.setStyleSheet("QLabel {font: 14pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")
        self.champions_total.setStyleSheet("QLabel {font: 24pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")

        self.assists_title = QLabel(self)
        self.assists_total = QLabel(self)
        self.assists_title.resize(230, 30)
        self.assists_total.resize(230, 70)
        self.assists_title.move(480, 0)
        self.assists_total.move(480, 40)
        self.assists_title.setAlignment(Qt.AlignCenter)
        self.assists_total.setAlignment(Qt.AlignCenter)
        self.assists_title.setStyleSheet("QLabel {font: 14pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")
        self.assists_total.setStyleSheet("QLabel {font: 24pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")

        self.turrets_title = QLabel(self)
        self.turrets_total = QLabel(self)
        self.turrets_title.resize(230, 30)
        self.turrets_total.resize(230, 70)
        self.turrets_title.move(480, 115)
        self.turrets_total.move(480, 155)
        self.turrets_title.setAlignment(Qt.AlignCenter)
        self.turrets_total.setAlignment(Qt.AlignCenter)
        self.turrets_title.setStyleSheet("QLabel {font: 14pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")
        self.turrets_total.setStyleSheet("QLabel {font: 24pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")

        self.win_loss_title = QLabel(self)
        self.win_loss_total = QLabel(self)
        self.win_loss_title.resize(230, 30)
        self.win_loss_total.resize(230, 70)
        self.win_loss_title.move(0, 0)
        self.win_loss_total.move(0, 40)
        self.win_loss_title.setAlignment(Qt.AlignCenter)
        self.win_loss_total.setAlignment(Qt.AlignCenter)
        self.win_loss_title.setStyleSheet("QLabel {font: 14pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")
        self.win_loss_total.setStyleSheet("QLabel {font: 24pt ;color:black; background-color:tan; border-style: outset; border-width: 2px; border-color: black}")

    def showStats(self, values):
        if len(values) == 7:
            self.win_loss_title.setText('Wins/Losses')
            self.win_loss_total.setText(str(values[0]) + '/' + str(values[6]))
        else:
            self.win_loss_title.setText('Wins')
            self.win_loss_total.setText(str(values[0]))

        if len(values) > 2:
            self.neutral_monsters_title.setText('Neutral Monsters Killed')
            self.neutral_monsters_total.setText(str(values[4]))
            self.champions_title.setText('Champions Killed')
            self.champions_total.setText(str(values[1]))
            self.minions_title.setText('Minions Killed')
            self.minions_total.setText(str(values[3]))
            self.assists_title.setText('Assists')
            self.assists_total.setText(str(values[2]))
            self.turrets_title.setText('Turrets Killed')
            self.turrets_total.setText(str(values[5]))
