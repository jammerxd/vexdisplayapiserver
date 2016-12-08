import wx
import socket
import threading
import os
from Classes import *


app = wx.App(False)
mainFrame = ConfigureServer()
app.SetTopWindow(mainFrame)
mainFrame.Show()
TaskBarIcon(mainFrame)
app.MainLoop()