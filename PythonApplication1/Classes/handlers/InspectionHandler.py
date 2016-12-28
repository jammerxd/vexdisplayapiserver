import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class InspectionHandler(tornado.web.RequestHandler):
    global EVENT_DATA 

    @asynchronous
    def get(self,**params):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        self.application.getInspections()
        output = "{ \"teams\" : {"
        for team in EVENT_DATA.inspections:
            output += " \"" + team + "\" : \"" + EVENT_DATA.inspections[team] + "\","
        if(output.endswith(",")):
            output = output[:len(output)-1]
        output += "}, \"NotStarted\" : " + str(EVENT_DATA.inspections_ns) + ", "
        output += "\"Partial\" : " + str(EVENT_DATA.inspections_p) + ", "
        output += "\"Completed\" : " + str(EVENT_DATA.inspections_c) + ", "
        output += "\"Total\" : " + str(EVENT_DATA.inspections_t) + " }"
        
        self.finish(output)