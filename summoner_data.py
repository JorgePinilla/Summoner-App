import json
from riot import Riot

class SummonerData:

    def __init__(self):
        self.riot = Riot()
        self.summoner_data = {}
        self.summoner_ID = {}
        self.summary = {}
        self.ranked_summary = {}
        self.rank_data = {}
        self.rune_pages = {}
        self.mastery_pages = {}
        self.runes = {}
        self.masteries = {}
        self.champions = {}

    ### methods that request static data ###
    ########################################

    def getStaticData(self):
        print 'loading rune data ...'
        #with open('rune.json') as rune_file:
            #self.runes = json.load(rune_file)
        self.runes = self.riot.getRunes('na')
        print 'Done'
        print 'loading mastery data ...'
        #with open('masteryID.json') as mastery_file:
            #self.masteries = json.load(mastery_file)
        self.masteries = self.riot.getMasteries('na', 'all')
        print 'Done'
        print 'loading champions ...'
        self.champions = self.riot.getChampions('na')
        print 'Done'

    def getImage(self, imageType, imageName):
        return self.riot.getImage(imageType, imageName)

    #methods related to static-rune information
    def runeDescription(self, runeID):
        return self.runes['data'][str(runeID)]['description']

    def runeName(self, runeID):
        return self.runes['data'][str(runeID)]['name']

    #methods related to static-mastery information
    def ferocityMasteryTree(self):
        return self.masteries['tree']['Ferocity']

    def cunningMasteryTree(self):
        return self.masteries['tree']['Cunning']

    def resolveMasteryTree(self):
        return self.masteries['tree']['Resolve']

    #methods related to static-champion information
    def championList(self):
        return self.champions['data']

    ### methods that request summoner related data ###
    ##################################################

    def getSummonerData(self, summonerNames, region):
        self.summoner_data = self.riot.getSummoner(summonerNames, region)
        self.setID(self.summoner_data)
        self.getSummary(self.summoner_ID.values(), region)
        self.getRankedSummary(self.summoner_ID.values(), region)
        self.rune_pages = self.riot.getSummonerRunes(self.summoner_ID.values(), region)
        self.mastery_pages = self.riot.getSummonerMasteries(self.summoner_ID.values(), region)

    def setID(self, summonerDto):
        for x in summonerDto.keys():
            self.summoner_ID[summonerDto[x]['name']] = str(summonerDto[x]['id'])

    def getSummary(self, summonerID, region):
        for x in summonerID:
            self.summary[x] = self.riot.getSummary(x, region)

    def getRankedSummary(self, summonerID, region):
        for x in summonerID:
            self.ranked_summary[x] = self.riot.getRankedSummary(x, region)

    def getRankedData(self, region):
        self.rank_data = self.riot.getPlayerRank(self.summoner_ID.values(), region)

    ### methods used by GUI to retrieve specific information ###
    ############################################################

    #misc methods
    def getName(self, summonerName):
        if self.summoner_data.get(summonerName) != None:
            return self.summoner_data.get(summonerName)['name']
        else:
            return None

    def getID(self, summonerName):
        return self.summoner_ID[summonerName]

    def getIcon(self, summonerName):
        return str(self.summoner_data[summonerName]['profileIconId']) + '.png'

    # rank related methods
    def getTier(self, summonerID):
        return self.rank_data[summonerID][0]['tier']

    def getDivision(self, summonerID):
        return self.rank_data[summonerID][0]['entries'][0]['division']

    def getLeaguePoints(self, summonerID):
        return self.rank_data[summonerID][0]['entries'][0]['leaguePoints']

    def getRankSeries(self, summonerID):
        return self.rank_data[summonerID][0]['entries'][0]['miniSeries']['progress']

    #stats related methods
    def getStats(self, summonerID, matchType):
        stats = []
        temp_list = self.summary[summonerID]['playerStatSummaries']
        for item in temp_list:
            if matchType == 'Ranked Team' and item['playerStatSummaryType'] == 'RankedTeam5x5':
                stats.append(item['wins'])
                if item['aggregatedStats']:
                    stats.append(item['aggregatedStats']['totalChampionKills'])
                    stats.append(item['aggregatedStats']['totalAssists'])
                    stats.append(item['aggregatedStats']['totalMinionKills'])
                    stats.append(item['aggregatedStats']['totalNeutralMinionsKilled'])
                    stats.append(item['aggregatedStats']['totalTurretsKilled'])
                stats.append(item['losses'])
                break
            elif matchType == 'Ranked Solo' and item['playerStatSummaryType'] == 'RankedSolo5x5':
                stats.append(item['wins'])
                if item['aggregatedStats']:
                    stats.append(item['aggregatedStats']['totalChampionKills'])
                    stats.append(item['aggregatedStats']['totalAssists'])
                    stats.append(item['aggregatedStats']['totalMinionKills'])
                    stats.append(item['aggregatedStats']['totalNeutralMinionsKilled'])
                    stats.append(item['aggregatedStats']['totalTurretsKilled'])
                stats.append(item['losses'])
                break
            elif matchType == 'Normal' and item['playerStatSummaryType'] == 'Unranked':
                stats.append(item['wins'])
                if item['aggregatedStats']:
                    stats.append(item['aggregatedStats']['totalChampionKills'])
                    stats.append(item['aggregatedStats']['totalAssists'])
                    stats.append(item['aggregatedStats']['totalMinionKills'])
                    stats.append(item['aggregatedStats']['totalNeutralMinionsKilled'])
                    stats.append(item['aggregatedStats']['totalTurretsKilled'])
                break
        return stats

    def getChampionStats(self, summonerID):
        stats_list = []
        champion_stats = self.ranked_summary[summonerID]
        for x in champion_stats['champions']:
            if x['id'] != 0:
                sessions_played = float(x['stats']['totalSessionsPlayed'])
                kills = x['stats']['totalChampionKills'] / sessions_played
                deaths = x['stats']['totalDeathsPerSession'] / sessions_played
                assists = x['stats']['totalAssists'] / sessions_played
                minions_killed = x['stats']['totalMinionKills'] / sessions_played
                win_rate = (x['stats']['totalSessionsWon'] / sessions_played) * 100
                champion = self.riot.getChampion('na', str(x['id']))
                stats_list.append({'name': champion['name'], 'id': x['id'], 'sessions': int(sessions_played),
                                   'winRate': "{:.1f}".format(win_rate), 'kills': "{:.1f}".format(kills), 'deaths': "{:.1f}".format(deaths),
                                   'assists': "{:.1f}".format(assists), 'cs': "{:.1f}".format(minions_killed)})
        return stats_list

    #rune page related methods
    def getNumOfRunePages(self, summonerID):
        return len(self.rune_pages[summonerID]['pages'])

    def getRunePageName(self, summonerID, pageNum):
        return self.rune_pages[summonerID]['pages'][pageNum]['name']

    def getRunes(self, summonerID, pageNum):
        return self.rune_pages[summonerID]['pages'][pageNum].get('slots')

    def getRuneID(self, rune):
        return rune['runeId']

    #mastery page related methods
    def getNumOfMasteryPages(self, summonerID):
        return len(self.mastery_pages[summonerID]['pages'])

    def getMasteryPageName(self, summonerID, pageNum):
        return self.mastery_pages[summonerID]['pages'][pageNum]['name']

    def getMasteries(self, summonerID, pageNum):
        return self.mastery_pages[summonerID]['pages'][pageNum].get('masteries')

    def getMasteryID(self, mastery):
        return mastery['id']

    def getMasteryRank(self, mastery):
        return str(mastery['rank'])
