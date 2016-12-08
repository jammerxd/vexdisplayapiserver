import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class TeamHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
    def initialize(self,division):
        self.division = division
        self.divisionStr = "division"+str(division)
        
    @asynchronous
    def get(self,**params):
        self.application.getTeams(self.division)
        self.application.getRanks(self.division)
        self.application.getInspections()
        self.application.getCheckIns()
        output = "{ \"teams\" : ["
        for team in EVENT_DATA.divisions[self.divisionStr]["teams"]:
            output += json.dumps(EVENT_DATA.divisions[self.divisionStr]["teams"][team].__dict__) + ","
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "]}"
        self.finish(output)