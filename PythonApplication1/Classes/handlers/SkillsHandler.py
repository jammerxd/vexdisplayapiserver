import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class SkillsHandler(tornado.web.RequestHandler):
    global EVENT_DATA 

    @asynchronous
    def get(self,**params):
        self.application.getSkills()
        output = "{ \"count\" : " + str(len(EVENT_DATA.skillsRanks)) + ", \"skills\" : ["
        for team in EVENT_DATA.skillsRanks:
            output +=  json.dumps(EVENT_DATA.skillsRanks[team].__dict__)
            
            output += ","
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "]}"
        self.finish(output)