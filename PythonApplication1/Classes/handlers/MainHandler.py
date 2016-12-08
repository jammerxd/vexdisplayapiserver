import sys
sys.path.append("..")
import tornado
from tornado.web import asynchronous
from tornado.web import RedirectHandler
from Classes.EventData import *
import os, json, xlrd,csv,sys

class MainHandler(tornado.web.RequestHandler):
    global EVENT_DATA 
    @asynchronous
    def post(self,**params):
        division = int(self.get_argument('div', True))
        updateType = self.get_argument('type',True)
        actual_file = None
        if(updateType == "all" and division > 0 and division < 13):
            for f in self.request.files:
                fileName = self.request.files[f][0]['filename']


                if fileName == "matchdata.csv":
                    actual_file = self.request.files[f][0]['body']
                    break
            
        if actual_file != None and actual_file != "":
            matchFile = open(os.path.join(self.application.config.getUploadDir(),"division"+str(division),"Matches.csv"),"wb")
            matchFile.write(actual_file)
            matchFile.close()
            
            self.application.updateData(division)
        self.finish("Success")

    





    @asynchronous
    def get(self,**params):
        self.application.getEventName()
        for i in range(12):
            self.application.updateData(i+1)
        EVENT_DATA.doLogin(self.application.config)
        self.application.getInspections()
        self.application.getCheckIns()
        self.write("Welcome to the Tournament Manager API Server! Valid URL's are division#/[teams,ranks,matches]\n")
        self.finish("")