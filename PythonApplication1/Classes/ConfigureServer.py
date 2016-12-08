import wx
import sys
import time
import threading
from Settings import *
from WebServer import *
from EventData import *
class ConfigureServer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self.Bind(wx.EVT_ICONIZE, self.on_iconify)
        self.Bind(wx.EVT_CLOSE,self.on_exit)  
        icon = wx.IconFromBitmap(wx.Bitmap(os.path.join(os.getcwd(),"icon.png")))
        self.SetIcon(icon)
        self.settings = Settings()
        self.ws = None
        self.wsThread = None
        self.wsRunning = False
        
        self.SetToolTip(wx.ToolTip('VEXDisplay Web Server'))
        self.SetTitle('VEXDisplay Web Server Settings')
        self.SetSize(wx.Size(460,500))
        self.SetBackgroundColour((255,255,255))
        self.Bind(wx.EVT_ICONIZE, self.on_iconify)
        self.Bind(wx.EVT_CLOSE,self.on_exit)    
        self.segoeUIBold = wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.BOLD,faceName="Segoe UI")
        self.segoeUIRegular = wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.NORMAL,faceName="Segoe UI")

        self.settings_lbl_header = wx.StaticText(self,-1)
        self.settings_lbl_header.SetFont(self.segoeUIBold)
        self.settings_lbl_header.SetLabel("Configure Settings")
        self.settings_lbl_header.SetPosition(((self.GetSize()[0]-self.settings_lbl_header.GetSize()[0])/2,10))


        self.settings_lbl_TMWebServer = wx.StaticText(self,-1)
        self.settings_lbl_TMWebServer.SetFont(self.segoeUIRegular)
        self.settings_lbl_TMWebServer.SetLabel("TM Web Server Address: ")
        self.settings_lbl_TMWebServer.SetPosition((20,62))   
        
        self.TxtbxTMWebServer = wx.TextCtrl(self, value=self.settings.getWebServer(), pos=(self.settings_lbl_TMWebServer.GetSize()[0]+25,60), size=(self.GetSize()[0]-self.settings_lbl_TMWebServer.GetSize()[0]-25-25,self.settings_lbl_TMWebServer.GetSize()[1]+4))
        self.TxtbxTMWebServer.SetFont(self.segoeUIRegular)


        self.settings_lbl_Port = wx.StaticText(self,-1)
        self.settings_lbl_Port.SetFont(self.segoeUIRegular)
        self.settings_lbl_Port.SetLabel("Server Port: ")
        self.settings_lbl_Port.SetPosition((20,102))
        
        self.TxtbxPort = wx.TextCtrl(self, value=self.settings.getPort(), pos=(self.settings_lbl_Port.GetSize()[0]+25,100), size=(self.GetSize()[0]-self.settings_lbl_Port.GetSize()[0]-25-25,self.settings_lbl_Port.GetSize()[1]+4))
        self.TxtbxPort.SetFont(self.segoeUIRegular)  


        self.settings_lbl_UploadDir = wx.StaticText(self,-1)
        self.settings_lbl_UploadDir.SetFont(self.segoeUIRegular)
        self.settings_lbl_UploadDir.SetLabel("Upload Folder: ")
        self.settings_lbl_UploadDir.SetPosition((20,142))   
        
        self.TxtbxUploadDir = wx.TextCtrl(self, value=self.settings.getUploadDir(), pos=(self.settings_lbl_UploadDir.GetSize()[0]+25,140), size=(self.GetSize()[0]-self.settings_lbl_UploadDir.GetSize()[0]-25-25,self.settings_lbl_UploadDir.GetSize()[1]+4))
        self.TxtbxUploadDir.SetFont(self.segoeUIRegular) 

        
        self.settings_lbl_TMPassword = wx.StaticText(self,-1)
        self.settings_lbl_TMPassword.SetFont(self.segoeUIRegular)
        self.settings_lbl_TMPassword.SetLabel("TM Password: ")
        self.settings_lbl_TMPassword.SetPosition((20,182))   
        
        self.TxtbxTMPassword = wx.TextCtrl(self, style=wx.TE_PASSWORD,value=self.settings.getTMPassword(), pos=(self.settings_lbl_TMPassword.GetSize()[0]+25,180), size=(self.GetSize()[0]-self.settings_lbl_TMPassword.GetSize()[0]-25-25,self.settings_lbl_TMPassword.GetSize()[1]+4))
        self.TxtbxTMPassword.SetFont(self.segoeUIRegular) 


        self.BtnApply = wx.Button(self,label="Start",pos=(25,230))
        self.BtnApply.SetFont(self.segoeUIRegular)
        self.BtnApply.SetSize((self.BtnApply.GetSize()[0]+10,self.BtnApply.GetSize()[1]+10))
        self.BtnApply.SetPosition(((self.GetSize()[0]-self.BtnApply.GetSize()[0])/2,self.BtnApply.GetPosition()[1]+5))
        
        self.BtnApply.Bind(wx.EVT_BUTTON, self.on_apply_settings)


        self.BtnRefetch = wx.Button(self,label="Re-Sync Data",pos=(25,278))
        self.BtnRefetch.SetFont(self.segoeUIRegular)
        self.BtnRefetch.SetSize((self.BtnRefetch.GetSize()[0]+50,self.BtnRefetch.GetSize()[1]+10))
        self.BtnRefetch.SetPosition(((self.GetSize()[0]-self.BtnRefetch.GetSize()[0])/2,self.BtnRefetch.GetPosition()[1]+5))
        self.BtnRefetch.Disable()
          
        self.BtnRefetch.Bind(wx.EVT_BUTTON,self.on_refetch_data)
        #self.Refresh()
        
    def refectchComplete(self):
        self.BtnRefetch.Enable()
        self.BtnApply.Enable()
    def refetchData(self):
        self.ws.app.getEventName()
        for i in range(12):
            self.ws.app.updateData(i+1)
        EVENT_DATA.doLogin(self.settings)
        self.ws.app.getInspections()
        self.ws.app.getCheckIns()
        self.ws.app.getSkills()
        self.refectchComplete()
    
    def on_refetch_data(self,e=None):
        self.BtnApply.Disable()
        self.BtnRefetch.Disable()
        threading.Thread(target=self.refetchData).start()

        
    
    def on_apply_settings(self,evt):
        self.BtnApply.Disable()
        self.Update()
        if(self.wsRunning == False):
            
            self.settings.setWebServer(self.TxtbxTMWebServer.GetValue())
            self.settings.setPort(self.TxtbxPort.GetValue())
            self.settings.setUploadDir(self.TxtbxUploadDir.GetValue())
            self.settings.setTMPassword(self.TxtbxTMPassword.GetValue())
            try:
                self.ws = WebServer(self.settings)
                self.wsThread = threading.Thread(target=self.ws.start)
                self.wsThread.start()
                
                self.BtnRefetch.Enable()

                self.BtnApply.SetLabel("Stop")
                self.TxtbxTMWebServer.Disable()
                self.TxtbxPort.Disable()
                self.TxtbxUploadDir.Disable()
                self.TxtbxTMPassword.Disable()
                self.wsRunning = True
            except Exception, e:
                self.wsRunning = False
                self.BtnApply.SetLabel("Start")
                self.TxtbxTMWebServer.Enable()
                self.TxtbxPort.Enable()
                self.TxtbxUploadDir.Enable()
                self.TxtbxTMPassword.Enable()
            
        else:
            try:
                self.ws.stop()
                self.wsThread.join()
                self.BtnApply.SetLabel("Start")
                self.TxtbxTMWebServer.Enable()
                self.TxtbxPort.Enable()
                self.TxtbxUploadDir.Enable()
                self.TxtbxTMPassword.Enable()
                self.BtnRefetch.Disable()
                self.wsRunning = False
            except:
                self.wsRunning = True
                self.BtnApply.SetLabel("Stop")
                self.TxtbxTMWebServer.Enable()
                self.TxtbxPort.Enable()
                self.TxtbxUploadDir.Enable()
                self.TxtbxTMPassword.Enable()
        self.BtnApply.Enable()









    def getSettings(self):
        return self.settings
    def on_iconify(self, e):
        self.Hide() 
    def on_exit(self, event):
        dlg = wx.MessageDialog(self, "Are you sure you want to exit?", "Exit Confirmation", wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()      
        if (result):
            if(self.wsRunning and self.ws != None and self.wsThread != None):
                self.ws.stop()
                self.wsThread.join()
            sys.exit(0)
        else:
            self.on_iconify(event)