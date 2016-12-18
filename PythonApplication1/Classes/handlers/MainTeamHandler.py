import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class MainTeamHandler(tornado.web.RequestHandler):
    global EVENT_DATA 

    @asynchronous
    def get(self,**params):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        for i in range(12): 
            self.application.getName(i+1)
            self.application.getTeams(i+1)
            self.application.getRanks(i+1)
        self.application.getInspections()
        self.application.getCheckIns()
        output = "{ \"teams\" : ["
        for team in EVENT_DATA.teams:
            output += json.dumps(EVENT_DATA.teams[team].__dict__) + ","
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "]}"
        self.finish(output)