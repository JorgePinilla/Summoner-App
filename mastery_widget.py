from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLabel

class MasteryWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.mastery_rank_labels = {}

        #mastery page name label
        self.page_name = QLabel(self)
        self.page_name.resize(500, 25)

        #ferocity tree label
        self.ferocity_tree = QLabel(self)
        self.ferocity_tree.move(7, 25)
        self.ferocity_tree.resize(230, 211)
        self.ferocity_tree.setStyleSheet("QLabel {color:black; background-color:maroon; border-style: outset; border-width: 2px; border-color: black}")
        self.total_ferocity_points = QLabel(self.ferocity_tree)
        self.total_ferocity_points.move(175, 178)
        self.total_ferocity_points.resize(30, 30)
        self.total_ferocity_points.setAlignment(Qt.AlignCenter)
        self.total_ferocity_points.setStyleSheet("QLabel {color:black; background-color:white; border-radius:10px; font: bold 14px}")

        #cunning tree label
        self.cunning_tree = QLabel(self)
        self.cunning_tree.move(242, 25)
        self.cunning_tree.resize(230, 211)
        self.cunning_tree.setStyleSheet("QLabel {color:black; background-color:navy; border-style: outset; border-width: 2px; border-color: black}")
        self.total_cunning_points = QLabel(self.cunning_tree)
        self.total_cunning_points.move(175, 178)
        self.total_cunning_points.resize(30, 30)
        self.total_cunning_points.setAlignment(Qt.AlignCenter)
        self.total_cunning_points.setStyleSheet("QLabel {color:black; background-color:white; border-radius:10px; font: bold 14px}")

        #resolve tree label
        self.resolve_tree = QLabel(self)
        self.resolve_tree.move(477, 25)
        self.resolve_tree.resize(230, 211)
        self.resolve_tree.setStyleSheet("QLabel {color:black; background-color:green; border-style: outset; border-width: 2px; border-color: black}")
        self.total_resolve_points = QLabel(self.resolve_tree)
        self.total_resolve_points.move(175, 178)
        self.total_resolve_points.resize(30, 30)
        self.total_resolve_points.setAlignment(Qt.AlignCenter)
        self.total_resolve_points.setStyleSheet("QLabel {color:black; background-color:white; border-radius:10px; font: bold 14px}")

    def setName(self, name):
        self.page_name.setText("  " + name)

    def setMasteryRank(self, mid, rank):
        self.mastery_rank_labels[mid].setText(rank)
        #self.mastery_rank_labels[str(mid)].setText(rank)

    def setTotalPoints(self):
        ferocity_points = 0
        cunning_points = 0
        resolve_points = 0
        for x in self.mastery_rank_labels.keys():
            if x > 6100 and x < 6200:
            #if int(x) > 4100 and int(x) < 4200:
                ferocity_points += int(self.mastery_rank_labels[x].text())
            elif x > 6200 and x < 6300:
            #elif int(x) > 4200 and int(x) < 4300:
                resolve_points += int(self.mastery_rank_labels[x].text())
            else:
                cunning_points += int(self.mastery_rank_labels[x].text())
        self.total_ferocity_points.setText(str(ferocity_points))
        self.total_cunning_points.setText(str(cunning_points))
        self.total_resolve_points.setText(str(resolve_points))

    def setMasteryLabels(self, ferocityList, cunningList, resolveList):
        self.setMasteryTree(self.ferocity_tree, ferocityList)
        self.setMasteryTree(self.cunning_tree, cunningList)
        self.setMasteryTree(self.resolve_tree, resolveList)

    def setMasteryTree(self, tree, imageList):
        yPos = 3
        xPos = 7
        column = 1
        for element in imageList.keys():
            if not isinstance(element, str):
                mastery = QLabel(tree)
                mastery.setScaledContents(True)
                mastery.move(xPos, yPos)
                mastery.resize(30, 30)
                mastery.setPixmap(imageList[element])

                mastery_rank = QLabel(tree)
                mastery_rank.move(xPos + 31, yPos + 15)
                mastery_rank.resize(15, 15)
                mastery_rank.setAlignment(Qt.AlignCenter)
                mastery_rank.setText('0')
                mastery_rank.setStyleSheet("QLabel {color:white; border-style: outset; border-width: 2px; border-color: black}")
                self.mastery_rank_labels[element] = mastery_rank
            if column < 3:
                xPos += 56
                column += 1
            else:
                column = 1
                xPos = 7
                yPos += 35
