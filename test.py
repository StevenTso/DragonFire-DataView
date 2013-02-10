import wx

class MainFrame(wx.Frame):

    def __init__(self,parent,id,title,position,size):
        wx.Frame.__init__(self, parent, id, title, position, size)
        toolbar = self.CreateToolBar()
        tool = toolbar.AddLabelTool(wx.ID_ANY, 'TEST', wx.Bitmap('Icons/folder32.png')) #open
        toolbar.Realize()
        tool = toolbar.AddLabelTool(wx.ID_ANY, 'TEST2', wx.Bitmap('Icons/arrowright32.png')) #generate
        toolbar.Realize()
        self.split1 = wx.SplitterWindow(self)
        self.split2 = wx.SplitterWindow(self.split1)

        self.bottompanel = wx.Panel(self.split1)
        self.topleftpanel = wx.Panel(self.split2)
        self.toprightpanel = wx.Panel(self.split2)
        self.topleftpanel.SetBackgroundColour('sky Blue')

        self.split1.SplitHorizontally(self.split2, self.bottompanel)
        self.split2.SplitVertically(self.topleftpanel, self.toprightpanel)


app = wx.App(0)
win = MainFrame(None, -1, "Hello!", (50, 50), (600, 400))
win.Show()
app.MainLoop()