import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class RankHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
    def initialize(self,division):
        self.division = division
        self.divisionStr = "division"+str(division)
        
    @asynchronous
    def get(self,**params):
        self.application.getTeams(self.division)
        self.application.getRanks(self.division)
        output = "{ \"count\" : " + str(len(EVENT_DATA.divisions[self.divisionStr]["ranks"])) + ", \"ranks\" : ["
        
        for i in range(len(EVENT_DATA.divisions[self.divisionStr]["ranks"])):
            output += "{ \"" + str(i+1) + "\" : \"" + EVENT_DATA.divisions[self.divisionStr]["ranks"][str(i+1)] + "\"},"

        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "]}"
        self.finish(output)