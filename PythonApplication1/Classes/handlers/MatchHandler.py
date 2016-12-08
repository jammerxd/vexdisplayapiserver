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
        self.application.getTeams(self.division)
        self.application.getMatches(self.division)
        output = "{ \"count\" : " + str(len(EVENT_DATA.divisions[self.divisionStr]["matches"])) + ", \"matches\" : ["
        
        for match in EVENT_DATA.divisions["division"+str(self.division)]["matches"]:
            output += json.dumps(EVENT_DATA.divisions["division"+str(self.division)]["matches"][match].__dict__) + ","

        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "]}"
        self.finish(output)