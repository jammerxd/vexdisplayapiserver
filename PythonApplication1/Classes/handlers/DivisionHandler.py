import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class DivisionHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
    def initialize(self,division):
        self.divisionStr = "division"+str(division)
        
    @asynchronous
    def get(self,**params):
        #output = "{ \"teams\" : ["
        #for team in EVENT_DATA.divisions[self.divisionStr]["teams"]:
        #    output += json.dumps(EVENT_DATA.divisions[self.divisionStr]["teams"][team]) + ","
        #if(output.endswith(",")):
        #    output = output[:len(output)-1]
        #output += "]}"
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        output = "{ \"name\" : \"" + EVENT_DATA.divisions[self.divisionStr]["name"] + "\"}"
        self.finish(output)
        