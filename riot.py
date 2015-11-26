import json
import urllib2

class Riot:

    def __init__ (self):
        self.api_key = ''  #this is where the developer key goes

        # url used for http request
        self.url = 'https://na.api.pvp.net/api/lol'

        #######################
        ###types of requests###
        #######################

        self.regularRequest = '?api_key='

        #static requests
        self.masteryAllRequest = '?masteryListData=all&api_key='

        #url for requesting images
        self.ddragonUrl = 'https://ddragon.leagueoflegends.com/cdn/5.23.1/img'


    ### RIOT API methods ###
    ########################

    #Summoner api methods
    def getSummoner(self, summonerNames, region):
        names = ','.join(summonerNames)
        params = [self.url, region, 'v1.4', 'summoner', 'by-name', names]
        data = self.makeRequest(params, self.regularRequest)
        return data

    def getSummonerMasteries(self, summonerID, region):
        list_ID = ','.join(summonerID)
        params = [self.url, region, 'v1.4', 'summoner', list_ID, 'masteries']
        data = self.makeRequest(params, self.regularRequest)
        return data

    def getSummonerRunes(self, summonerID, region):
        list_ID = ','.join(summonerID)
        params = [self.url, region, 'v1.4', 'summoner', list_ID, 'runes']
        data = self.makeRequest(params, self.regularRequest)
        return data

    #static api methods

    def getChampions(self, region):
        params = [self.url, 'static-data', region, 'v1.2', 'champion']
        data = self.makeRequest(params, self.regularRequest)
        return data

    def getChampion(self, region, champID):
        params = [self.url, 'static-data', region, 'v1.2', 'champion', champID]
        data = self.makeRequest(params, self.regularRequest)
        return data

    def getRunes(self, region):
        params = [self.url, 'static-data', region, 'v1.2', 'rune']
        data = self.makeRequest(params, self.regularRequest)
        return data

    def getMasteries(self, region, requestType):
        params = [self.url, 'static-data', region, 'v1.2', 'mastery']
        if requestType == 'all':
            data = self.makeRequest(params, self.masteryAllRequest)
        else:
            data = self.makeRequest(params, self.regularRequest)
        return data

    #league api methods
    def getPlayerRank(self, summonerID, region):
        list_ID = ','.join(summonerID)
        params = [self.url, region, 'v2.5', 'league', 'by-summoner', list_ID, 'entry']
        data = self.makeRequest(params, self.regularRequest)
        return data

    #stats api methods
    def getSummary(self, summonerID, region):
        params = [self.url, region, 'v1.3', 'stats', 'by-summoner', str(summonerID), 'summary']
        data = self.makeRequest(params, self.regularRequest)
        return data

    def getRankedSummary(self, summonerID, region):
        params = [self.url, region, 'v1.3', 'stats', 'by-summoner', str(summonerID), 'ranked']
        data = self.makeRequest(params, self.regularRequest)
        return data

    ### Utility methods ###
    #######################

    #sends http requests
    def makeRequest(self, parameters, requestType):
        request = '/'.join(parameters) + requestType + self.api_key
        try:
            data = json.load(urllib2.urlopen(request))
            return data
        except urllib2.HTTPError as e:
            response = self.handleError(str(e))
            raise RiotError(response)

    #gets image from ddragon
    def getImage(self, imageType, imageName):
        request = '/'.join([self.ddragonUrl, imageType, imageName])
        try:
            data = urllib2.urlopen(request).read()
            return data
        except urllib2.HTTPError as e:
            response = self.handleError(str(e))
            raise RiotError(response)

    #handles HTTP errors
    def handleError(self, error):
        response = error.replace(' ', '').split(':')[1]
        return response


class RiotError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
