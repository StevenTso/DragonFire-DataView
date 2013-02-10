import os
from wx.lib import sheet
import wx
import wx.grid as gridlib

wildcard = "Python source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
num_lines = 10;
ACCEL_X = []
ACCEL_Y = []
ACCEL_Z = []
GYRO_X = []
GYRO_Y = []
GYRO_Z = []
# some constants
samp_rate = 20
sim_time = 60
nsamps = samp_rate*sim_time
cuttoff_freq = 0.1

ID_BUTTON=100

class LeftPanel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        grid = gridlib.Grid(self)
        grid.CreateGrid(num_lines,6)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)

class RightPanel(wx.Panel):      
    def __init__(self, parent):
        
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)

        grid = gridlib.Grid(self)
        grid.CreateGrid(num_lines,6)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)


class Dragon(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs)
        self.currentDirectory = os.getcwd()
        self.InitUI()
                
    def InitUI(self):
        self.SetSize((800, 600))
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

        #---TOP PANEL---#
        box = wx.BoxSizer(wx.VERTICAL)
        toolbar2 = wx.ToolBar(self, wx.TB_HORIZONTAL | wx.TB_TEXT)
        
        self.position = wx.TextCtrl(toolbar2)
        fonts = ['Times New Roman', 'Times', 'Courier', 'Courier New', 'Helvetica',
                'Sans', 'verdana', 'utkal', 'aakar', 'Arial']
        font_sizes = ['10', '11', '12', '14', '16']

        font = wx.ComboBox(toolbar2, -1, value = 'Times', choices=fonts, size=(100, -1),
                style=wx.CB_DROPDOWN)
        
        font_height = wx.ComboBox(toolbar2, -1, value = '10',  choices=font_sizes,
                size=(50, -1), style=wx.CB_DROPDOWN)

        toolbar2.AddControl(self.position)
        
        toolbar2.AddControl(font)
        toolbar2.AddControl(font_height)
        toolbar2.AddSeparator()
        bold = wx.Bitmap('Icons/folder32.png')
        
        toolbar2.AddCheckTool(-1, bold)
        italic = wx.Bitmap('Icons/folder32.png')
        toolbar2.AddCheckTool(-1, italic)
        under = wx.Bitmap('Icons/folder32.png')
        
        toolbar2.AddCheckTool(-1, under)
        toolbar2.AddSeparator()
        toolbar2.AddLabelTool(-1, '', wx.Bitmap('Icons/folder32.png'))
        toolbar2.AddLabelTool(-1, '', wx.Bitmap('Icons/folder32.png'))
        toolbar2.AddLabelTool(-1, '', wx.Bitmap('Icons/folder32.png'))

        box.Add(toolbar2)
        box.Add((5,10) , 0)
        
        """
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        button1 = wx.Button(self, ID_BUTTON+1, "F3 View")
        self.sizer2.Add(button1, 1, wx.EXPAND)
        """
        #---IMAGE---#
        """
        image = 'Icons/article32.png'
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
    	self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))
        """
        #---SPREADSHEET---#        
        
        splitter = wx.SplitterWindow(self)
        leftP = LeftPanel(splitter)
        rightP = RightPanel(splitter)

        # split the window
        splitter.SplitVertically(leftP, rightP)
        splitter.SetMinimumPaneSize(25)

        sizer = wx.BoxSizer(wx.BOTTOM)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
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
                print "Test"
                #parser()

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

    def parser():
        global num_lines
        print "ENTERED"
        num_lines= sum(1 for line in open('DATA.TXT', 'r'))
        f = open('data.txt', 'r')
        for var0 in range(0, num_lines):
            line = f.readline();
            #removes last comma and new line
            parsed_line = line[:-2];
            
            parsed_line = parsed_line.split(',');
            
            for var1 in range(0, 6):
                #removes white spaces
                if parsed_line[var1][-1:] == ' ':
                    parsed_line[var1] = parsed_line[var1].rstrip();
                #remove escape character
                if parsed_line[var1][-1:] == '\x00':
                    parsed_line[var1] = parsed_line[var1].rstrip('\x00');
                #parsed_line from string ---> int format
                parsed_line[var1] = int(parsed_line[var1])

            ACCEL_X.append(parsed_line[0]);
            ACCEL_Y.append(parsed_line[1]);
            ACCEL_Z.append(parsed_line[2]);
            GYRO_X.append(parsed_line[3]);
            GYRO_Y.append(parsed_line[4]);
            GYRO_Z.append(parsed_line[5]);

def main():
    df = wx.App()
    Dragon(None)
    df.MainLoop()    


if __name__ == '__main__':
    main()