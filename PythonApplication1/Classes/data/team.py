class Team(object):
    def __init__(self):
        self.number = ""
        self.name = ""
        self.town = ""
        self.state = ""
        self.country = ""
        self.school = ""
        self.location = ""
        self.division = ""
        self.divisionName = ""
    
        self.rank = ""
        self.wins = "0"
        self.losses = "0"
        self.ties = "0"
        self.aps = "0"
        self.wps = "0"
        self.sps = "0"   

        self.checkedIn = False
        self.inspectionStatus = "Not Started"

        
    def getCheckedIn(self):
        return self.checkedIn
    def setCheckedIn(self,val):
        self.checkedIn = val
    def getInspectionStatus(self):
        return self.inspectionStatus
    def setInspectionStatus(self,val):
        self.inspectionStatus = val
    def getNumber(self):
        return self.number
    def setNumber(self,val):
        self.number = val
    def getName(self):
        return self.name
    def setName(self,val):
        self.name = val  
    def getTown(self):
        return self.town
    def setTown(self,val):
        self.town = val
    def getState(self):
        return self.state
    def setState(self,val):
        self.state = val
    def getCountry(self):
        return self.country
    def setCountry(self,val):
        self.country = val
    def getSchool(self):
        return self.school
    def setSchool(self,val):
        self.school = val
    def getRank(self):
        return self.rank
    def setRank(self,val):
        self.rank = val
    def getWins(self):
        return self.wins
    def setWins(self,val):
        self.wins = val
    def getLosses(self):
        return self.losses
    def setLosses(self,val):
        self.losses = val
    def getTies(self):
        return self.ties
    def setTies(self,val):
        self.ties = val
    def getAPS(self):
        return self.aps
    def setAPS(self,val):
        self.aps = val
    def getSPS(self):
        return self.sps
    def setSPS(self,val):
        self.sps = val
    def getWPS(self):
        return self.wps
    def setWPS(self,val):
        self.wps = val  
    def getLocation(self):
        return self.location
    def setLocation(self,val):
        self.location = val
    def getDivision(self):
        return self.division
    def setDivision(self,val):
        self.division = val
    def getDivisionName(self):
        return self.divisionName
    def setDivisionName(self,val):
        self.divisionName = val
    def __str__(self):
        return self.number
    def getString(self):
        rtrStr = self.number + ", " + self.name + ", " + self.town + ", " + self.state + ", " + self.country + ", " + self.school
        return rtrStr