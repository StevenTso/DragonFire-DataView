import wx 

class MyFrame(wx.Frame): 
    """ Test of vertical wx.StaticLine """
    def __init__(self, parent=None, id=-1, title=None): 
        wx.Frame.__init__(self, parent, id, title) 
        self.panel = wx.Panel(self, size=(350, 200))

        self.ln = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL)
        self.ln.SetSize((30,30))

        print self.ln.IsVertical()

        self.Fit() 

app = wx.PySimpleApp() 
frame1 = MyFrame(title='wx.StaticLine') 
frame1.Center() 
frame1.Show() 
app.MainLoop()