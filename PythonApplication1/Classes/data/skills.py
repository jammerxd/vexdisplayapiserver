class Skills(object):
    def __init__(self):
        self.team = ""
        self.name = ""
        self.skillsRank = ""
        self.totalSkillsScore = "0"
        self.skillsProgScore = "0"
        self.skillsDriverScore = "0"
        self.skillsDriverAttempts = "0"
        self.skillsProgAttempts = "0"  
    def getTeam(self):
        return self.team
    def setTeam(self,val):
        self.team = val 
    def getName(self):
        return self.name
    def setName(self,val):
        self.name = val
    def getSkillsRank(self):
        return self.skillsRank
    def setSkillsRank(self,val):
        self.skillsRank = val
    def getTotalSkillsScore(self):
        return totalSkillsScore
    def setTotalSkillsScore(self,val):
        self.totalSkillsScore = val
    def getSkillsProgScore(self):
        return self.skillsProgScore
    def setSkillsProgScore(self,val):
        self.skillsProgScore = val
    def getSkillsDriverScore(self):
        return self.skillsDriverScore
    def setSkillsDriverScore(self,val):
        self.skillsDriverScore = val
    def getSkillsDriverAttempts(self):
        return self.skillsDriverAttempts
    def setSkillsDriverAttempts(self,val):
        self.skillsDriverAttempts = val
    def getSkillsProgAttempts(self):
        return self.skillsProgAttempts
    def setSkillsProgAttempts(self,val):
        self.skillsProgAttempts = val   