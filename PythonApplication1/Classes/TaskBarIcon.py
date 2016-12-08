import wx
import sys
import os
import socket

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(os.path.join(os.getcwd(),"icon.png"))
    
    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Get Web Address', self.on_show_IP)
        menu.AppendSeparator()
        create_menu_item(menu, 'Settings', self.on_configure_server)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, "VEXDisplay Web Server")

    def on_configure_server(self, event):
        self.frame.Show(True)
        self.frame.Restore()
        
    def on_show_IP(self,event):
        ip = socket.gethostbyname(socket.gethostname())

        ipText = "The VEXDisplay Server Address is: http://" + ip + ":" + self.frame.settings.getPort()

        dlg = wx.MessageDialog(self.frame, ipText, "VEXDisplay Server Address", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()        
               
    def on_exit(self, event):
        self.frame.Hide()
        self.frame.Destroy()
        wx.CallAfter(self.Destroy)
        sys.exit(0)