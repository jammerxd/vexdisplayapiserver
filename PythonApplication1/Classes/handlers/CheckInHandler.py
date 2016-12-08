import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class CheckInHandler(tornado.web.RequestHandler):
    global EVENT_DATA 

    @asynchronous
    def get(self,**params):
        self.application.getCheckIns()
        output = "{ \"count\" : " + str(len(EVENT_DATA.checkIns)) + ", \"checkins\" : ["
        for team in EVENT_DATA.checkIns:
            output += "{ \"" + team + "\" : "
            output += "true" if EVENT_DATA.checkIns[team] == True else "false"
            output += " },"
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "]}"
        self.finish(output)