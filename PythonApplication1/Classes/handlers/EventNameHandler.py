import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
import json
from Classes.EventData import *
class EventNameHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
        
    @asynchronous
    def get(self,**params):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')
        output = "{ \"name\" : \"" + EVENT_DATA.eventName + "\"}"
        self.finish(output)
        