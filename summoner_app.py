import collections
from riot import RiotError
from overview_widget import OverviewWidget
from champions_widget import ChampionsWidget
from rune_widget import RuneWidget
from mastery_widget import MasteryWidget
from summoner_data import SummonerData

from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QTabWidget
from PyQt4.QtGui import QWidget

class Panel(QWidget):

    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)

        self.clean_up_queue = []
        self.summoner = SummonerData()
        self.summoner.getStaticData()

        ### Search Bar ###
        ##################

        #label
        self.search_label = QLabel(self)
        self.search_label.move(20, 15)
        self.search_label.resize(220, 25)
        self.search_label.setText('Enter summoner name(s):')
        self.search_label.setStyleSheet("QLabel {font:14pt}")

        #text field
        self.search_field = QLineEdit(self)
        self.search_field.move(260, 15)
        self.search_field.resize(250, 25)
        self.search_field.setPlaceholderText("ex: mcnuggets, teltor, ...")
        self.search_field.setFocusPolicy(Qt.ClickFocus)

        #search button
        self.search_button = QPushButton(self)
        self.search_button.move(520, 15)
        self.search_button.resize(150, 25)
        self.search_button.setText('Search Summoner')

        #region combobox
        self.region_list = QComboBox(self)
        self.region_list.move(680, 15)
        self.region_list.resize(75, 25)
        regions = ['NA', 'LAN', 'BR', 'LAS', 'EUW', 'EUNE', 'TR', 'RU', 'OCE']
        self.region_list.addItems(regions)

        #error label
        self.error_label = QLabel(self)
        self.error_label.move(775, 15)
        self.error_label.resize(160, 25)
        self.error_label.setStyleSheet("QLabel {font:14pt}")

        ### Summoner Information ###
        ############################

        #summoner Icon label
        self.icon_label = QLabel(self)
        self.icon_label.setScaledContents(True)
        self.icon_label.move(260, 50)
        self.icon_label.resize(110, 110)

        #name label
        self.name_label = QLabel(self)
        self.name_label.move(380, 50)
        self.name_label.resize(620, 50)
        self.name_label.setText('SUMMONER NAME')
        self.name_label.setStyleSheet("QLabel {font:32pt}")

        #rank label
        self.rank_label = QLabel(self)
        self.rank_label.move(380, 100)
        self.rank_label.resize(200, 60)
        self.rank_label.setText('summoner rank')
        self.rank_label.setStyleSheet("QLabel {font:18pt}")

        #miniseries labels
        self.series_labels = {}
        self.pixmap_win = QPixmap()
        self.pixmap_loss = QPixmap()
        self.pixmap_n = QPixmap()
        self.pixmap_win.load("./images/win.png")
        self.pixmap_loss.load("./images/loss.png")
        self.pixmap_n.load("./images/n.png")
        xPos = 600
        for x in range(5):
            match_label = QLabel(self)
            match_label.move(xPos, 120)
            match_label.resize(35, 35)
            match_label.setScaledContents(True)
            match_label.hide()
            self.series_labels[x] = match_label
            xPos += 40

        #mastery image labels
        print 'loading mastery images ...'
        self.ferocity_tree_images = self.getMasteryImages(self.summoner.ferocityMasteryTree())
        self.cunning_tree_images = self.getMasteryImages(self.summoner.cunningMasteryTree())
        self.resolve_tree_images = self.getMasteryImages(self.summoner.resolveMasteryTree())
        print 'Done'

        #champion icon image labels
        print 'loading champion icon images ...'
        self.championIcons = self.getChampionIconImages(self.summoner.championList())
        print 'Done'

        #overview widget
        self.overview_widget = QWidget()
        self.overview_menu = QTabWidget(self.overview_widget)
        self.overview_menu.resize(720, 270)

        #runes widget
        self.runes_widget = QWidget()
        self.runes_menu = QTabWidget(self.runes_widget)
        self.runes_menu.resize(720, 270)

        #masteries widget
        self.masteries_widget = QWidget()
        self.masteries_menu = QTabWidget(self.masteries_widget)
        self.masteries_menu.resize(720, 270)

        #summoner menu
        self.menu = QTabWidget(self)
        self.menu.move(260, 180)
        self.menu.resize(720, 300)
        self.menu.addTab(self.overview_widget, "Overview")
        self.menu.addTab(self.runes_widget, "Runes")
        self.menu.addTab(self.masteries_widget, "Masteries")
        self.menu.hide()

        #summoners buttons
        self.button_list = {}
        yPos = 150
        for x in range(10):
            sum_button = QPushButton(self)
            sum_button.move(50, yPos)
            sum_button.resize(150, 25)
            sum_button.hide()
            self.button_list[x] = sum_button
            yPos += 25

        ### Connecting Widgets ###
        ##########################

        self.connect(self.search_button, QtCore.SIGNAL("clicked()"), self.getData)
        self.connect(self.search_button, QtCore.SIGNAL("clicked()"), self.getRankedData)
        self.connect(self.button_list[0], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[0].text())))
        self.connect(self.button_list[1], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[1].text())))
        self.connect(self.button_list[2], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[2].text())))
        self.connect(self.button_list[3], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[3].text())))
        self.connect(self.button_list[4], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[4].text())))
        self.connect(self.button_list[5], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[5].text())))
        self.connect(self.button_list[6], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[6].text())))
        self.connect(self.button_list[7], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[7].text())))
        self.connect(self.button_list[8], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[8].text())))
        self.connect(self.button_list[9], QtCore.SIGNAL("clicked()"), lambda: self.displayData(str(self.button_list[9].text())))

        ### Window Configuration ###
        ############################

        #window settings
        self.setGeometry(200, 150, 1000, 500)
        self.setMaximumSize(1000, 500)
        self.setWindowTitle('summoner App') 

        self.show()

    ### GUI methods ###
    ###################

    ############### GUI get methods ###############

    #get data related to given summoner names
    def getData(self):
        self.cleanUp()
        name_list = str(self.search_field.text()).replace(' ', '').lower().split(',')
        region = str(self.region_list.currentText()).lower()
        if name_list != ['']:
            try:
                self.summoner.getSummonerData(name_list, region)
                for x in range(len(name_list)):
                    sum_name = self.summoner.getName(name_list[x])
                    if sum_name != None:
                        self.button_list[x].setText(sum_name)
                        self.clean_up_queue.append(self.button_list[x])
                    else:
                        self.button_list[x].setText(name_list[x])
                        self.clean_up_queue.append(self.button_list[x])
                        self.button_list[x].setEnabled(False)
                    self.button_list[x].show()
            except RiotError as e:
                response = e.message
                print response
                if response == 'ServiceUnavailable':
                    self.error_label.setText(response)
                elif response == '429':
                    self.error_label.setText('Rate limit reached')
                elif response == 'InternalServerError':
                    self.error_label.setText(response)
                elif response == 'Unauthorized':
                    self.error_label.setText('Invalid Input')
                elif response == 'ServerError':
                    self.error_label.setText(response)
                else:
                    self.error_label.setText('Not Found')
            except KeyError as k:
                self.error_label.setText('Invalid Input')

    #get summoner ranked data
    def getRankedData(self):
        if str(self.search_field.text()) != '':
            region = str(self.region_list.currentText()).lower()
            try:
                self.summoner.getRankedData(region)
            except RiotError:
                print 'Rank info not found'

    #get mastery images
    def getMasteryImages(self, masteryList):
        pixmap_list = collections.OrderedDict()
        empty_spaces = 0
        for row in masteryList:
            if len(row['masteryTreeItems']) == 2:
            #if len(row) == 3:
                row['masteryTreeItems'].append(None)
                #row.append(None)
            for element in row['masteryTreeItems']:
            #for element in row:
                if element != None:
                    pixmap = QPixmap()
                    pixmap.loadFromData(self.summoner.getImage('mastery', str(element['masteryId']) + '.png'))
                    pixmap_list[element['masteryId']] = pixmap
                else:
                    pixmap_list['null' + str(empty_spaces)] = None
                    empty_spaces += 1
        return pixmap_list

    #get champion icon images
    def getChampionIconImages(self, clist):
        pixmap_list = {}
        for champ in clist.values():
            pixmap = QPixmap()
            pixmap.loadFromData(self.summoner.getImage('champion', champ['key'] + '.png'))
            pixmap_list[champ['name']] = pixmap
        return pixmap_list

    ############### GUI update methods ###############

    #removes previous data from GUI
    def cleanUp(self):
        self.error_label.setText("")
        #clears summoner info
        self.icon_label.setPixmap(QPixmap())
        self.icon_label.setStyleSheet("QLabel {}")
        self.name_label.setText("")
        self.rank_label.setText("")
        #hides elements in clean up queue
        for x in self.clean_up_queue:
            x.hide()
            x.setEnabled(True)

    #display data
    def displayData(self, buttonName):
        sum_ID = self.summoner.getID(buttonName)
        self.displayIcon(buttonName.replace(' ', '').lower())
        self.name_label.setText(buttonName)
        self.displayRank(sum_ID)
        self.displayMenu(sum_ID)

    #display summoner icon
    def displayIcon(self, summoner_name):
        iconName = self.summoner.getIcon(summoner_name)
        iconPixmap = QPixmap()
        self.icon_label.setStyleSheet("QLabel {border-style: outset; border-width: 3px; border-color: gold}")
        try:
            iconPixmap.loadFromData(self.summoner.getImage('profileicon', iconName))
            self.icon_label.setPixmap(iconPixmap)
        except RiotError:
            iconPixmap.load("./images/no_image.png")
            self.icon_label.setPixmap(iconPixmap)

    #display summoner rank
    def displayRank(self, sumID):
        for x in range(len(self.series_labels)):
            self.series_labels[x].setPixmap(QPixmap())
        try:
            tier = self.summoner.getTier(sumID)
            division = self.summoner.getDivision(sumID)
            points = self.summoner.getLeaguePoints(sumID)
            self.rank_label.setText(tier + ': ' + division + '\n' + str(points) + ' league points')
            if points == 100:
                self.displayMiniseries(sumID)
        except KeyError:
            self.rank_label.setText('UNRANKED')

    #display promotion series
    def displayMiniseries(self, sumID):
        progress = self.summoner.getRankSeries(sumID)
        i = 0
        for x in progress:
            if x == 'W':
                self.series_labels[i].setPixmap(self.pixmap_win)
            elif x == 'L':
                self.series_labels[i].setPixmap(self.pixmap_loss)
            else:
                self.series_labels[i].setPixmap(self.pixmap_n)
            self.clean_up_queue.append(self.series_labels[i])
            self.series_labels[i].show()
            i += 1

    #display summoner menu
    def displayMenu(self, sumID):
        self.displayOverviewMenu(sumID)
        self.displayRuneMenu(sumID)
        self.displayMasteryMenu(sumID)
        self.clean_up_queue.append(self.menu)
        self.menu.show()

    #display overview menu
    def displayOverviewMenu(self, sumID):
        self.overview_menu.clear()

        overview_normal = OverviewWidget()
        overview_ranked_solo = OverviewWidget()
        overview_ranked_team = OverviewWidget()
        overview_champions = ChampionsWidget()

        overview_normal.showStats(self.summoner.getStats(sumID, 'Normal'))
        overview_ranked_solo.showStats(self.summoner.getStats(sumID, 'Ranked Solo'))
        overview_ranked_team.showStats(self.summoner.getStats(sumID, 'Ranked Team'))
        overview_champions.showStats(self.summoner.getChampionStats(sumID), self.championIcons)

        self.overview_menu.addTab(overview_normal, 'Normal')
        self.overview_menu.addTab(overview_ranked_solo, 'Ranked Solo')
        self.overview_menu.addTab(overview_ranked_team, 'Ranked Team')
        self.overview_menu.addTab(overview_champions, 'Champions')

    #display rune menu
    def displayRuneMenu(self, sumID):
        self.runes_menu.clear()
        for x in range(self.summoner.getNumOfRunePages(sumID)):
            rune_page = RuneWidget()
            rune_page.setSize(700, 225)
            rune_page.setName(self.summoner.getRunePageName(sumID, x))
            rune_data = self.summoner.getRunes(sumID, x)
            if rune_data != None:
                for y in rune_data:
                    rid = self.summoner.getRuneID(y)
                    desc = self.summoner.runeDescription(rid)
                    rname = self.summoner.runeName(rid)
                    rune_page.addRune(rid, desc, rname)
                rune_page.showRunes()
            self.runes_menu.addTab(rune_page, str(x + 1))

    #display mastery menu
    def displayMasteryMenu(self, sumID):
        self.masteries_menu.clear()
        for x in range(self.summoner.getNumOfMasteryPages(sumID)):
            mastery_page = MasteryWidget()
            mastery_page.setMasteryLabels(self.ferocity_tree_images, self.cunning_tree_images, self.resolve_tree_images)
            mastery_page.setName(self.summoner.getMasteryPageName(sumID, x))
            mastery_data = self.summoner.getMasteries(sumID, x)
            if mastery_data != None:
                for y in mastery_data:
                    mid = self.summoner.getMasteryID(y)
                    rank = self.summoner.getMasteryRank(y)
                    mastery_page.setMasteryRank(mid, rank)
            mastery_page.setTotalPoints()
            self.masteries_menu.addTab(mastery_page, str(x + 1))


if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv)
    main = Panel()
    sys.exit(app.exec_())
