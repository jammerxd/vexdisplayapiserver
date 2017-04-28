import wx
import socket
import threading
import os
from Classes import *
class VEXServer(wx.App):
    def OnInit(self):
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        return True
     
app = VEXServer(False)
mainFrame = ConfigureServer()
#app.SetTopWindow(mainFrame)
mainFrame.Show()
TaskBarIcon(mainFrame)
app.MainLoop()
#command to run C:\Python27\python setup.py py2exe