import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class MatchHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
    def initialize(self,division):
        self.division = division
        self.divisionStr = "division"+str(division)
        
    @asynchronous
    def get(self,**params):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.application.getTeams(self.division)
        self.application.getMatches(self.division)
        
        output = "{ \"count\" : " + str(len(EVENT_DATA.divisions[self.divisionStr]["matches"])) + ", \"matches\" : ["
        lastMatchScored = None
        allMatchesScored = False
        showMatchCount = 0
        for match in EVENT_DATA.divisions["division"+str(self.division)]["matches"]:
            output += json.dumps(EVENT_DATA.divisions["division"+str(self.division)]["matches"][match].__dict__) + ","
            if EVENT_DATA.divisions["division"+str(self.division)]["matches"][match].getScored() == True:
                lastMatchScored = EVENT_DATA.divisions["division"+str(self.division)]["matches"].keys().index(match)
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "], \"show\" : [ "

        if lastMatchScored == None and len(EVENT_DATA.divisions[self.divisionStr]["matches"]) > 0:
                lastMatchScored = 0

        if lastMatchScored != None:
            if lastMatchScored == (len(EVENT_DATA.divisions[self.divisionStr]["matches"])-1):
                allMatchesScored = True
            for i in range(3,-1,-1):
                indexChecked = lastMatchScored-i
                #print indexChecked
                if(indexChecked > -1 and indexChecked < len(EVENT_DATA.divisions["division"+str(self.division)]["matches"])):
                    output += "\"" +EVENT_DATA.divisions["division"+str(self.division)]["matches"].items()[indexChecked][0] + "\"" + ","
                    showMatchCount += 1
            for i in range(1,(9-showMatchCount)):#9 is 1 more than 8 for the (for)loop
                indexChecked = lastMatchScored + i
                if(indexChecked > -1 and indexChecked < len(EVENT_DATA.divisions["division"+str(self.division)]["matches"])):
                    output += "\"" + EVENT_DATA.divisions["division"+str(self.division)]["matches"].items()[indexChecked][0] + "\"" + ","
                    showMatchCount += 1
        #print lastMatchScored
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "], \"allMatchesScored\" : "
        if allMatchesScored == True:
            output += "true"
        else:
            output += "false"
        output += "}"  
        self.finish(output)