import os
from wx.lib import sheet
import wx

wildcard = "Python source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
num_lines = 0;
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


class parser():
    global num_lines
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


class DataInput(sheet.CSheet):
    def __init__(self, parent):
        sheet.CSheet.__init__(self, parent)
        self.row = self.col = 0
        self.SetNumberRows(num_lines)
        self.SetNumberCols(6)

class Dragon(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs)
        self.currentDirectory = os.getcwd()
        self.InitUI()
                
    def InitUI(self):
        self.SetSize((600, 400))
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
        #image = 'Icons/article32.png'
        #img = wx.Image(image, wx.BITMAP_TYPE_ANY)
    	#self.sBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img))

        #---FRAME---#
        box1 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box1)
        notebook1 = wx.Notebook(self, -1, style=wx.BOTTOM)

        #parser()

        sheet1 = DataInput(notebook1)
        sheet1.SetFocus()
        notebook1.AddPage(sheet1, 'Original')
        box1.Add(notebook1, 1, wx.EXPAND)


        box2 = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box2)
        notebook2 = wx.Notebook(self, -1, style=wx.BOTTOM)
        sheet2 = DataInput(notebook2)
        #sheet2.SetFocus()
        notebook2.AddPage(sheet2, 'Modified')
        box2.Add(notebook2, 1, wx.EXPAND)

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
                parser()

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