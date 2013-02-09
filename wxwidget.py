import os
import wx

wildcard = "Python source (*.py)|*.py|" \
            "All files (*.*)|*.*"

class Dragon(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs) 
        self.currentDirectory = os.getcwd()
        self.InitUI()
                
    def InitUI(self):
        self.SetSize((300, 200))
        self.SetTitle('DF Smart Data')
        self.Centre()

        #---MENU OPTIONS---#
        menubar = wx.MenuBar()
        #File
        fileMenu = wx.Menu()
        open = fileMenu.Append(wx.ID_OPEN, '&Open')
        save = fileMenu.Append(wx.ID_SAVE, '&Save')
        generate = fileMenu.Append(wx.ID_ANY, '&Generate')
        self.Bind(wx.EVT_MENU, self.OnOpen, open)
        self.Bind(wx.EVT_MENU, self.OnSave, save)
        self.Bind(wx.EVT_MENU, self.OnGenerate, generate)

        #View
        viewMenu = wx.Menu()
        stats = viewMenu.Append(wx.ID_ANY, '&Stats')
        graphs = viewMenu.Append(wx.ID_ANY, '&Graphs')
        self.Bind(wx.EVT_MENU, self.OnStats, stats)
        self.Bind(wx.EVT_MENU, self.OnGraphs, graphs)

        #Help
        helpMenu = wx.Menu()
        help = helpMenu.Append(wx.ID_ANY, '&Help')
        about = helpMenu.Append(wx.ID_ANY, '&About')
        self.Bind(wx.EVT_MENU, self.OnHelp, help)
        self.Bind(wx.EVT_MENU, self.OnAbout, about)

        menubar.Append(fileMenu, '&File')
        menubar.Append(viewMenu, '&View')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        #---TOOLBARS---#
        toolbar = self.CreateToolBar()
        tool = toolbar.AddLabelTool(wx.ID_ANY, 'TEST', wx.Bitmap('Icons/folder32.png')) #open
        toolbar.Realize()
        tool = toolbar.AddLabelTool(wx.ID_ANY, 'TEST2', wx.Bitmap('Icons/arrowright32.png')) #generate
        toolbar.Realize()
        #self.Bind(wx.EVT_TOOL, self.OnQuit, tool)


        #---IMAGE---#
        image = 'Icons/article32.png'
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
    	self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))


        self.Show(True)
    
    def OnOpen(self, e):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()

    def OnSave(self, e):
        self.Close()

    def OnGenerate(self, e):
        self.Close()

    def OnQuit(self, e):
        self.Close()

    def OnStats(self, e):
        self.Close()

    def OnGraphs(self, e):
        self.Close()

    def OnHelp(self, e):
        self.Close()

    def OnAbout(self, e):
        self.Close()

def main():
    
    df = wx.App()
    Dragon(None)
    df.MainLoop()    


if __name__ == '__main__':
    main()