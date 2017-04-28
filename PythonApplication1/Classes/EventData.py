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
        
        self.inspections_t = 0
        self.inspections_ns = 0
        self.inspections_p = 0
        self.inspections_c = 0

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
        try:
            r = self.RequestSession.get(url)
            return r.content
        except Exception, ex:
            return ""
global EVENT_DATA 
EVENT_DATA = None
if(EVENT_DATA == None):
    EVENT_DATA = EventData()
