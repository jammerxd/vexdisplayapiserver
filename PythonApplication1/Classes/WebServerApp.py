import tornado, xlrd, csv, os, glob, urllib2, time
from datetime import datetime
from collections import OrderedDict
from EventData import *
from data import *
TIME_FORMAT = ""
if os.name == 'nt':
    TIME_FORMAT = "%#I:%M %p"
else:
    TIME_FORMAT = "%-I:%M %p"
class WebServerApp(tornado.web.Application):
    global EVENT_DATA
    def __init__(self,handlers,config):
        handlers = handlers
        settings = dict(debug=True,static_path=os.path.join(os.getcwd()))
        self.config = config
        
        tornado.web.Application.__init__(self, handlers, **settings)
    
    def updateData(self,division):
        self.getName(division)
        self.getTeams(division)
        self.getRanks(division)
        self.getMatches(division)
        

    def urlRequest(self,url):
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            data = opener.open(url).read().decode('utf-8')
            self.dataUpdateSuccess = True
        except Exception,ex:
            data = ""
            self.dataUpdateSuccess = False
        return data
    def getEventName(self):
        raw_html = self.urlRequest(self.config.getWebServer() + "/division1/teams")
        if raw_html != "" and raw_html != None:
            name = raw_html.split("<title>")[1]
            name = raw_html.split("</title>")[0].split(":: ")[1]
            EVENT_DATA.eventName = name.strip()
    def getName(self,division):
        raw_html = self.urlRequest(self.config.getWebServer() + "/division" + str(division) + "/teams")
        if raw_html != "" and raw_html != None:
            name = raw_html.split("</small>")[0]
            name = name.split("<small>")[1]
            EVENT_DATA.divisions["division"+str(division)]["name"] = name

    def getTeams(self,division):
        raw_html = self.urlRequest(self.config.getWebServer() + "/division" + str(division) + "/teams")
        if raw_html != "" and raw_html != None:
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            teamList = {}
            index = 0
            for row in tableBody.split("<tr>"):  
                raw_data = row.replace("</tr>","").replace("<td>","").replace("</td>","").split('\n')
                if(len(raw_data) == 8):                    
                    tempTeam = Team()
                    tempTeam.setNumber(str(raw_data[1]))
                    tempTeam.setName(raw_data[2])
                    tempTeam.setLocation(raw_data[3])
                    if tempTeam.getLocation() != "":
                        tempTeam.setTown(raw_data[3].split(",")[0])
                        tempTeam.setState(raw_data[3].split(",")[1])
                        tempTeam.setCountry(raw_data[3].split(",")[2])
                    tempTeam.setSchool(raw_data[4])
                    tempTeam.setDivision(str(division))
                    tempTeam.setDivisionName(EVENT_DATA.divisions["division"+str(division)]["name"])
                    teamList[str(tempTeam.number)] = tempTeam
                index+=1 
            EVENT_DATA.divisions["division"+str(division)]["teams"] = teamList
            EVENT_DATA.teams.update(teamList)
                    
                    
    def getRanks(self,division):
        raw_html = self.urlRequest(self.config.getWebServer() + "/division"+str(division)+"/rankings")
        if(raw_html != "" and raw_html != None):
            ranksList = {}
            tableBody = raw_html.split("<tbody>")[1]
            tableBody = tableBody.split("</tbody>")[0]
            
            tI = 0
            for row in tableBody.split("<tr>"):
                raw_data = row.replace("</tr>","").replace("<td>","").replace("<td class=\"td-centered\">","").replace("<td class=\"td-centered\" nowrap=\"nowrap\">","").replace("</td>","").split('\n')
                if len(raw_data) == 13:
                    teamNumber = str(raw_data[2])
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setRank(str(raw_data[1]))
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setWins(str(raw_data[4].split("-")[0]))
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setLosses(str(raw_data[4].split("-")[1]))
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setTies(str(raw_data[4].split("-")[2]))
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setWPS(str(raw_data[5]))
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setAPS(str(raw_data[7]))
                    EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].setSPS(str(raw_data[9]))
                    #EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].ranksStr = str(EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].getRank()).rjust(len(str(len(EVENT_DATA.divisions["division"+str(division)]["teams"])))) + "  "
                    #EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].ranksStr += '{:^6}'.format(str(self.teams[teamNumber].number)) + "  "
                    #EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].ranksStr += str('{:^'+str(self.maxTeamNameChars)+'}').format(str(self.teams[teamNumber].name)) + "  "
                    #EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].ranksStr += '{:^8}'.format(str(self.teams[teamNumber].wins) + "-" + self.teams[teamNumber].losses + "-" + self.teams[teamNumber].ties) + "  "
                    #EVENT_DATA.divisions["division"+str(division)]["teams"][teamNumber].ranksStr += '{:^11}'.format(str(self.teams[teamNumber].wps) + "-" + self.teams[teamNumber].aps + "-" + self.teams[teamNumber].sps) + "  "
                    #if len(self.teams[teamNumber].ranksStr) > self.maxRankChars:
                    #    self.maxRankChars = len(self.teams[teamNumber].ranksStr)
                    


                    EVENT_DATA.teams[teamNumber].setRank(str(raw_data[1]))
                    EVENT_DATA.teams[teamNumber].setWins(str(raw_data[4].split("-")[0]))
                    EVENT_DATA.teams[teamNumber].setLosses(str(raw_data[4].split("-")[1]))
                    EVENT_DATA.teams[teamNumber].setTies(str(raw_data[4].split("-")[2]))
                    EVENT_DATA.teams[teamNumber].setWPS(str(raw_data[5]))
                    EVENT_DATA.teams[teamNumber].setAPS(str(raw_data[7]))
                    EVENT_DATA.teams[teamNumber].setSPS(str(raw_data[9]))

                    EVENT_DATA.divisions["division"+str(division)]["ranks"][str(tI+1)] = teamNumber
                    tI+=1
            
            if len(EVENT_DATA.divisions["division"+str(division)]["ranks"]) == 0:
                i = 0
                for team in EVENT_DATA.divisions["division"+str(division)]["teams"]:
                    EVENT_DATA.divisions["division"+str(division)]["teams"][team].setRank(str(i+1))
                    EVENT_DATA.teams[team].setRank(str(i+1))            
                    EVENT_DATA.divisions["division"+str(division)]["ranks"][str(i+1)] = EVENT_DATA.divisions["division"+str(division)]["teams"][team].getNumber()
                    i += 1
            #elif len(EVENT_DATA.divisions["division"+str(division)]["ranks"]) != (tI-1):
            #    EVENT_DATA.divisions["division"+str(division)]["ranks"] = OrderedDict()
            #    self.getRanks(division)
            else:
                for rank in EVENT_DATA.divisions["division"+str(division)]["ranks"]:
                    team = EVENT_DATA.divisions["division"+str(division)]["ranks"][rank]
                    EVENT_DATA.divisions["division"+str(division)]["teams"][team].setRank(rank)
                    EVENT_DATA.teams[team].setRank(rank)
        try:
            if len(EVENT_DATA.divisions["division"+str(division)]["ranks"]) != tI and len(EVENT_DATA.divisions["division"+str(division)]["ranks"]) > 0 and tI > 0:
                EVENT_DATA.divisions["division"+str(division)]["ranks"] = OrderedDict()
                self.getRanks(division)
        except Exception, ex:
            t = false           
    def getMatches(self,division):
        matchData = {}
        matchDataFileStr = None
        
        for f in glob.glob(os.path.join(self.config.getUploadDir(),"division"+str(division),"*.csv")):
            if f.find("match") > -1 or f.find("Match") > -1:
                matchDataFileStr = f
                break   
        if matchDataFileStr != None:
            matchData = self.getMatchInfoContent(f)
     
            matchTimesFileStr = None
            matchTimes = {}
        
            #for f in glob.glob(os.path.join(self.config.getUploadDir(),"division"+str(division),"*.xlsx")):
            #    if f.find("Times") > -1:
            #        matchTimesFileStr = f
            #        break
        
            #if matchTimesFileStr != None:
            #    matchTimes = self.getMatchTimesContent(f)
            #
            #for matchName in matchTimes:
            #    if matchName in matchData.keys():
            #        matchData[matchName].setScheduledTime(matchTimes[matchName].getScheduledTime())


            EVENT_DATA.divisions["division"+str(division)]["matches"] = matchData

        
    def getMatchInfoContent(self,fileName):
        matches = OrderedDict()
        matchOrder = OrderedDict()
        currentMatchIndex = 1
        
        matchFile = open(fileName, 'rb')
        raw_data = matchFile.readlines()[1:]
        matchFile.close()
        os.remove(fileName)
        for line in raw_data:
            line = line.replace("\r","").replace("\n","").replace("\t","").replace("\"","").strip()
            if line != "":
                splitData = line.split(",")
                if len(splitData) >= 17:#31 - Added Match Times...
                    division = splitData[0]
                    round = splitData[1]
                    instance = splitData[2]
                    matchNum = splitData[3]
                    #if str(division) == str(division) and (str(round) == "2" and str(instance) == "1") or (str(round) == "1" and str(instance) == "1"):
                    #if str(division) == str(division) and (str(round) == "2" and str(instance) == "1"):
                    tempMatch = Match()
                    matchPrefix = "Q" if str(round) == "2" and str(instance) == "1" else "P"
                    if str(round) == "2" and str(instance) == "1":
                        matchPrefix = "Q"
                    elif str(round) == "1" and str(instance) == "1":
                        matchPrefix = "P"
                    elif str(round) == "3":
                        matchPrefix = "QF" + str(instance) + "-"
                    elif str(round) == "4":
                        matchPrefix = "SF" + str(instance) + "-"
                    elif str(round) == "5":
                        matchPrefix = "F"  
                    #matchPrefix = "Q"
                    tempMatch.setDivision(str(division))
                    tempMatch.setRound(str(round))
                    tempMatch.setInstance(str(instance))
                    tempMatch.setMatchNum(str(matchNum))
                    tempMatch.setMatch(matchPrefix + str(matchNum))
                    tempMatch.setField(splitData[4])
                    tempMatch.setRed1(splitData[5])
                    tempMatch.setRed2(splitData[6])
                    tempMatch.setRed3(splitData[7])
                    tempMatch.setBlue1(splitData[8])
                    tempMatch.setBlue2(splitData[9])
                    tempMatch.setBlue3(splitData[10])
                    tempMatch.setRedScore(splitData[11])
                    tempMatch.setBlueScore(splitData[12])
                    tempMatch.setRedSit(splitData[13])
                    tempMatch.setBlueSit(splitData[14])
                    tempMatch.setScored(True if splitData[15] == "True" else False)
                    tempMatch.setWinner(splitData[16])
                    #d = datetime.strptime(splitData[17],'%Y-%m-%d %H-%M-%S')
                    if(tempMatch.getRound() == "1" or tempMatch.getRound() == "2"):
                        tempMatch.setScheduledTime(datetime.strptime(splitData[17],'%Y-%m-%d %H:%M:%S').strftime(TIME_FORMAT))
                    if len(splitData) == 32:
                        tempMatch.setRedFarCubes(splitData[18])
                        tempMatch.setRedAuto(True if splitData[19] == "1" else False)
                        
                        tempMatch.setRedFarStars(splitData[20])
                        tempMatch.setRedHighRobots(splitData[24])
                        tempMatch.setRedLowRobots(splitData[23])
                        tempMatch.setRedNearCubes(splitData[22])
                        tempMatch.setRedNearStars(splitData[21])
                        tempMatch.setBlueAuto(True if splitData[26] == "1" else False)
                        tempMatch.setBlueFarCubes(splitData[25])
                        tempMatch.setBlueFarStars(splitData[27])
                        tempMatch.setBlueHighRobots(splitData[31])
                        tempMatch.setBlueLowRobots(splitData[30])
                        tempMatch.setBlueNearCubes(splitData[29])
                        tempMatch.setBlueNearStars(splitData[28])
                    matches[tempMatch.getMatch()] = tempMatch
                    currentMatchIndex+=1
        return matches
    #def getMatchTimesContent(self,fileName):
    #    matchTimes = {}
    #    wb = xlrd.open_workbook(fileName)
    #    sh = wb.sheet_by_index(0)
    
    #    for rownum in range(1,sh.nrows):
    #        tempMatch = Match()
    #        tempMatch.setMatch(sh.cell_value(rownum,0))
    #        if ((tempMatch.getMatch().startswith("Q") or tempMatch.getMatch().startswith("P")) and tempMatch.getMatch().find("-") < 0):
    #            tempMatch.setScheduledTime(str(sh.cell_value(rownum,1)))
    #            matchTimes[tempMatch.getMatch()] = tempMatch
    #    os.remove(fileName)
    #    return matchTimes

    def getSkills(self):
        raw_html = self.urlRequest(self.config.getWebServer() + "/skills/rankings")
        if raw_html != None and raw_html != "":
            tableLst = raw_html.split("<tbody>")
            if len(tableLst) > 1:
                table = tableLst[1].split("</tbody>")[0]
                table = table[table.find("<tr>"):]
                rowList = table.split("<tr>")
                for row in rowList:
                    row = row.strip().replace("</td>","").replace("\n","").replace("\r","").replace("</tr>","")
                    if row != "" and row.replace("\"","") != "":
                        raw_data = row.split("<td>")[1:]
                        EVENT_DATA.skillsRanks[raw_data[0]] = Skills()
                        EVENT_DATA.skillsRanks[raw_data[0]].setSkillsRank(raw_data[0])
                        EVENT_DATA.skillsRanks[raw_data[0]].setTeam(raw_data[1])
                        EVENT_DATA.skillsRanks[raw_data[0]].setName(raw_data[2])
                        EVENT_DATA.skillsRanks[raw_data[0]].setTotalSkillsScore(raw_data[3])
                        EVENT_DATA.skillsRanks[raw_data[0]].setSkillsProgScore(raw_data[4])
                        EVENT_DATA.skillsRanks[raw_data[0]].setSkillsProgAttempts(raw_data[5])
                        EVENT_DATA.skillsRanks[raw_data[0]].setSkillsDriverScore(raw_data[6])
                        EVENT_DATA.skillsRanks[raw_data[0]].setSkillsDriverAttempts(raw_data[7])

    def getInspections(self):
        raw_html = EVENT_DATA.getRequest(self.config.getWebServer() + "/inspection/summary")
        if raw_html != None and raw_html != "" and raw_html.find("<html><title>500: Internal Server Error</title><body>500: Internal Server Error</body></html>") < 0:
            tableLst = raw_html.split("<tbody>")
            if len(tableLst) > 1:
                table = tableLst[1].split("</tbody>")[0]
                table = table[table.find("<tr>"):]
                rowList = table.split("<tr>")
                
                EVENT_DATA.inspections_c = 0
                EVENT_DATA.inspections_ns = 0
                EVENT_DATA.inspections_p = 0
                EVENT_DATA.inspections_t = 0

                for row in rowList:
                    row = row.strip().replace("</td>","").replace("\n","").replace("\r","").replace("</tr>","")
                    if row != "" and row.replace("\"","") != "":
                        raw_data = row.split("<td>")[1:]
                        if raw_data[0] in EVENT_DATA.teams:
                            EVENT_DATA.teams[raw_data[0]].setInspectionStatus(raw_data[1])
                            if raw_data[0] in EVENT_DATA.divisions["division"+str(EVENT_DATA.teams[raw_data[0]].getDivision())]["teams"]:
                                EVENT_DATA.divisions["division"+str(EVENT_DATA.teams[raw_data[0]].getDivision())]["teams"][raw_data[0]].setInspectionStatus(raw_data[1])
                                
                            
                        EVENT_DATA.inspections[raw_data[0]] = raw_data[1]
                        EVENT_DATA.inspections_t += 1
                        if raw_data[1] == "Not Started":
                            EVENT_DATA.inspections_ns += 1
                        elif raw_data[1] == "Partial":
                            EVENT_DATA.inspections_p  += 1
                        elif raw_data[1] == "Completed":
                            EVENT_DATA.inspections_c += 1
    def getCheckIns(self):
        raw_html = EVENT_DATA.getRequest(self.config.getWebServer() + "/admin/checkin/summary")
        if raw_html != None and raw_html != "" and raw_html.find("<html><title>500: Internal Server Error</title><body>500: Internal Server Error</body></html>") < 0:
            tableLst = raw_html.split("<tbody>")
            if len(tableLst) > 1:
                table = tableLst[1].split("</tbody>")[0]
                table = table[table.find("<tr>"):]
                rowList = table.split("<tr>")
                for row in rowList:
                    row = row.strip().replace("</td>","").replace("\n","").replace("\r","").replace("</tr>","")
                    if row != "" and row.replace("\"","") != "":
                        raw_data = row.split("<td>")[1:]
                        if raw_data[0] in EVENT_DATA.teams:
                            EVENT_DATA.teams[raw_data[0]].setCheckedIn(True if raw_data[1] == "Yes" else False)
                            if raw_data[0] in EVENT_DATA.divisions["division"+str(EVENT_DATA.teams[raw_data[0]].getDivision())]["teams"]:
                                EVENT_DATA.divisions["division"+str(EVENT_DATA.teams[raw_data[0]].getDivision())]["teams"][raw_data[0]].setCheckedIn(True if raw_data[1] == "Yes" else False)
                                
                            
                        EVENT_DATA.checkIns[raw_data[0]] = True if raw_data[1] == "Yes" else False