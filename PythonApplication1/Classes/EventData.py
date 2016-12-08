from collections import OrderedDict
import requests
class EventData(object):
    def __init__(self):
        self.eventName = ""
        self.teams = {}
        self.inspections = {}
        self.checkIns = {}
        self.skillsRanks = OrderedDict()
        self.divisions = {}
        self.RequestSession = requests.Session()
        for i in range(12):
            self.divisions["division"+str(i+1)] = {}
            self.divisions["division"+str(i+1)]["teams"] = {}
            self.divisions["division"+str(i+1)]["ranks"] = {}
            self.divisions["division"+str(i+1)]["matches"] = OrderedDict()
            self.divisions["division"+str(i+1)]["name"] = "name here"

    def doLogin(self,config):
        data = dict(user='admin', password=config.getTMPassword())
        r = self.RequestSession.post(config.getWebServer()+"/admin/login",data=data,allow_redirects=True)
    def getRequest(self,url):
        r = self.RequestSession.get(url)
        return r.content
global EVENT_DATA 
EVENT_DATA = None
if(EVENT_DATA == None):
    EVENT_DATA = EventData()
