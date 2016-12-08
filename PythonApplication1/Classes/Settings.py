import os
class Settings(object):
    def __init__(self):
        self.eventName = "Event Name"
        self.port = "8989"
        self.uploadDir = os.path.join(os.getcwd(),"divisions")
        self.webServer = "http://localhost"
        self.TMPassword = "TMPassword"

    def setEventName(self, val):
        self.eventName = val
    def getEventName(self):
        return self.eventName
    def setPort(self,val):
        self.port = val
    def getPort(self):
        return self.port
    def setUploadDir(self,val):
        self.uploadDir = val
    def getUploadDir(self):
        return self.uploadDir
    def setWebServer(self,val):
        self.webServer = val
    def getWebServer(self):
        return self.webServer
    def getTMPassword(self):
        return self.TMPassword
    def setTMPassword(self,val):
        self.TMPassword = val

