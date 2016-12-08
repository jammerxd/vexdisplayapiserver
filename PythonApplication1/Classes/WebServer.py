import threading
import tornado.options
import tornado.ioloop
import tornado.httpserver
import tornado.httpclient
import tornado.web

from tornado.web import asynchronous
import glob, os, xlrd, csv,datetime,shutil
from handlers import *
from EventData import *
from WebServerApp import *
class WebServer(object):
    def __init__(self,settings):
        self.settings = settings
        self.app = None
        self.server = None
    
    def start(self):
        try:
            if os.path.isdir(self.settings.getUploadDir()):
                shutil.rmtree(self.settings.getUploadDir())
            if os.path.isdir(self.settings.getUploadDir()) == False:
                os.mkdir(self.settings.getUploadDir())
                for i in range(12):
                    os.mkdir(os.path.join(self.settings.getUploadDir(),"division"+str(i+1)))
        except Exception,ex:
            doNothing = True
        handlers = []
        handlers.append([r"/",MainHandler,{}])
        handlers.append([r"/teams",MainTeamHandler,{}])
        handlers.append([r"/teams/",MainTeamHandler,{}])
        handlers.append([r"/inspections",InspectionHandler,{}])
        handlers.append([r"/inspections/",InspectionHandler,{}])
        handlers.append([r"/checkins",CheckInHandler,{}])
        handlers.append([r"/checkins/",CheckInHandler,{}])
        handlers.append([r"/skills",SkillsHandler,{}])
        handlers.append([r"/skills/",SkillsHandler,{}])
        handlers.append([r"/eventName",EventNameHandler,{}])
        handlers.append([r"/eventName/",EventNameHandler,{}])
        handlers.append([r"/test",TestHandler,{}])
        for i in range(12):
            x = i+1
            handlers.append([r"/division"+str(x) + "/",DivisionHandler,{'division':x}])
            handlers.append([r"/division"+str(x),DivisionHandler,{'division':x}])

            handlers.append([r"/division"+str(x)+"/teams",TeamHandler,{'division':x}])
            handlers.append([r"/division"+str(x)+"/teams/",TeamHandler,{'division':x}])

            handlers.append([r"/division"+str(x)+"/ranks",RankHandler,{'division':x}])
            handlers.append([r"/division"+str(x)+"/ranks/",RankHandler,{'division':x}])

            handlers.append([r"/division"+str(x)+"/matches",MatchHandler,{'division':x}])
            handlers.append([r"/division"+str(x)+"/matches/",MatchHandler,{'division':x}])
    
        self.app = None
        self.app = WebServerApp(handlers,self.settings)
        self.app.getEventName()
        for i in range(12):
            self.app.updateData(i+1)
        EVENT_DATA.doLogin(self.app.config)
        self.app.getInspections()
        self.app.getCheckIns()
        self.app.getSkills()
        self.server = None
        self.server = tornado.httpserver.HTTPServer(self.app)
        self.server.listen(int(self.settings.getPort()))      
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        ioloop = tornado.ioloop.IOLoop.instance()
        ioloop.add_callback(ioloop.stop) 
        self.server.stop()