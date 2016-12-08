import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
from Classes.EventData import *
class TestHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
    
    @asynchronous
    def get(self,**params):
        #for i in range(12):
        #    self.application.updateData(i+1)
        #for t in EVENT_DATA.teams:
        #    self.write(EVENT_DATA.teams[t].getName() + " : " + EVENT_DATA.teams[t].getDivisionName() + " : " + EVENT_DATA.teams[t].getRank() + "<br/>")
        #self.finish("")
        self.finish("No data here. But this is a test page.")