import os
from wx.lib import sheet
import wx
import wx.grid as gridlib
import wx.lib.agw.hyperlink as hl

from pylab import *
from scipy import signal
from scipy.signal import lfilter, firwin
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from numpy import sin, arange, pi

import binascii
wildcard = "Python source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"

num_lines = 10;
ACCEL_X = []
ACCEL_Y = []
ACCEL_Z = []
GYRO_X = []
GYRO_Y = []
GYRO_Z = []
FORMATTED_DATA = []


# some constants
samp_rate = 20
sim_time = 60
nsamps = samp_rate*sim_time
cuttoff_freq = 0.1

ID_BUTTON=100


#Graph
#---CheckBox---#
CBX_val = False
CBY_val = False
CBZ_val = False
#---File imported---#
isFileImported = False


class viewParser:
    def __init__(self, path):
        #for filePath in path:
        #   stringPath.append(filePath)
        stringPath = ''.join(path)

        global num_lines, ACCEL_X, ACCEL_Y, ACCEL_Z, GYRO_X, GYRO_Y, GYRO_Z, FORMATTED_DATA
        FORMATTED_DATA = []
        ACCEL_X = []
        ACCEL_Y = []
        ACCEL_Z = []
        GYRO_X = []
        GYRO_Y = []
        GYRO_Z = []
        num_lines = sum(1 for line in open(stringPath, 'r'))

        f = open(stringPath, 'r')
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

        for var in range(0, num_lines):
            ax = str(ACCEL_X[var]).zfill(5) + "    |    "
            ay = str(ACCEL_Y[var]).zfill(5) + "    |    "
            az = str(ACCEL_Z[var]).zfill(5) + "    |    "
            gx = str(GYRO_X[var]).zfill(5) + "    |    "
            gy = str(GYRO_Y[var]).zfill(5) + "    |    "
            gz = str(GYRO_Z[var]).zfill(5) + "   |"
            newLine = ax + ay + az + gx + gy + gz
            FORMATTED_DATA.append(newLine)


class FilterFrame(wx.Frame):

    title = "DF Stats"

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title)
        self.SetSize((400, 400))
        self.SetTitle('DF Smart Data')
        self.Centre()
        self.Show(True)

class GraphFrame(wx.Frame):

    title = "DF Stats"

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title)
 
        self.SetSize((400, 400))
        self.SetTitle('DF Smart Data')
        self.Centre()
    

        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)

        #GRAPHS
        t1 = arange(0, num_lines, 1)
        #ACCEL_X       
        self.axes = self.figure.add_subplot(231)
        self.axes.plot(t1, ACCEL_X,'k--', markerfacecolor='green')
        title('ACCEL_X')
        ylabel('Value')
        self.Show(True)
        #self.Fit()
        #self.Show(True)

class StatsFrame(wx.Frame):

    title = "DF Stats"

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title)
        self.SetSize((400, 400))
        self.SetTitle('DF Smart Stats')
        self.Centre()
        self.Show(True)

class Dragon(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs)
        self.currentDirectory = os.getcwd()
        self.InitUI()   

    def InitUI(self):
        self.SetTitle('DF Smart Data')
        self.Centre()
        displaySize = wx.GetDisplaySize()
        #______________________MENU OPTIONS______________________________#
        menubar = wx.MenuBar()
        #File
        fileMenu = wx.Menu()
        open = fileMenu.Append(wx.ID_OPEN, '&Open')
        generate = fileMenu.Append(wx.ID_ANY, '&Generate File')
        self.Bind(wx.EVT_MENU, self.OnOpen, open)
        self.Bind(wx.EVT_MENU, self.OnGenerateFile, generate)

        #Edit
        editMenu = wx.Menu()
        undo = editMenu.Append(wx.ID_ANY, 'Undo')
        redo = editMenu.Append(wx.ID_ANY, 'Redo')
        self.Bind(wx.EVT_MENU, self.OnUndoKeyPress, undo)
        self.Bind(wx.EVT_MENU, self.OnRedoKeyPress, redo)
        
        #View
        viewMenu = wx.Menu()
        stats = viewMenu.Append(wx.ID_ANY, '&Stats')
        graph = viewMenu.Append(wx.ID_ANY, 'Graphs')
        self.Bind(wx.EVT_MENU, self.OnStats, stats)
        self.Bind(wx.EVT_MENU, self.OnGraph, graph)

        #Help
        helpMenu = wx.Menu()
        help = helpMenu.Append(wx.ID_ANY, '&Help')
        about = helpMenu.Append(wx.ID_ANY, '&About')
        self.Bind(wx.EVT_MENU, self.OnHelp, help)
        self.Bind(wx.EVT_MENU, self.OnAbout, about)

        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(viewMenu, '&View')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        #---1st TOOLBAR---#
        toolbar1 = self.CreateToolBar()
        open = toolbar1.AddLabelTool(wx.ID_ANY, 'Open', wx.Bitmap('Icons/folder32.png')) #open
        self.Bind(wx.EVT_TOOL, self.OnOpen, open)
        generate = toolbar1.AddLabelTool(wx.ID_ANY, 'Generate', wx.Bitmap('Icons/arrowright32.png')) #generate
        self.Bind(wx.EVT_TOOL, self.OnOpen, generate)
        toolbar1.Realize()

        
        #_____________________PANELS______________________________#
        self.split1 = wx.SplitterWindow(self)
        self.split2 = wx.SplitterWindow(self.split1)

        #---TEXT PANELS---#
        self.topleftpanel = wx.Panel(self.split2)
        self.toprightpanel = wx.Panel(self.split2)

        self.textL = wx.TextCtrl(self.topleftpanel, 1, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.textL, wx.ID_ANY, wx.EXPAND, 3)
        self.topleftpanel.SetSizer(sizer)
        self.textL.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        self.textR = wx.TextCtrl(self.toprightpanel, 1, style=wx.TE_MULTILINE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.textR, 1, wx.EXPAND, 4)
        self.toprightpanel.SetSizer(sizer)
        self.textR.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

        #---BOTTOM PANEL---#
        self.bottompanel = wx.Panel(self.split1)
        xConstant = 20
        seperatorConstant = 50

        #Filters
        xOffsetFilters = xConstant
        yOffsetFilters = 3
        xConstantFilters = 100
        yConstantFilters = 30
        xBoxSize = 150

        settingsImagePlace = 'Icons/folder32.png'
        settingsImage = wx.Image(settingsImagePlace, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        filters = wx.StaticText(self.bottompanel, label="Filters", pos=(xOffsetFilters, yOffsetFilters))
        filters.SetFont(font)

        filter_list = ['---', 'Low Pass Filter', 'Averager']

        Filter0 = wx.ComboBox(self.bottompanel, pos=(xOffsetFilters, yOffsetFilters+1*yConstantFilters), size=(xBoxSize,-1), choices=filter_list, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        Filter0Setting = wx.BitmapButton(self.bottompanel, id=-1, bitmap=settingsImage, pos=(xBoxSize + 2*xOffsetFilters, yOffsetFilters+yConstantFilters), size = (3*settingsImage.GetWidth()/4, 3*settingsImage.GetHeight()/4))
        self.Bind(wx.EVT_BUTTON, self.OnFilter0Settings, Filter0Setting)

        Filter1 = wx.ComboBox(self.bottompanel, pos=(xOffsetFilters, yOffsetFilters+2*yConstantFilters), size=(xBoxSize,-1), choices=filter_list, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        Filter1Setting = wx.BitmapButton(self.bottompanel, id=-1, bitmap=settingsImage, pos=(xBoxSize + 2*xOffsetFilters, yOffsetFilters+2*yConstantFilters), size = (3*settingsImage.GetWidth()/4, 3*settingsImage.GetHeight()/4))
        self.Bind(wx.EVT_BUTTON, self.OnFilter1Settings, Filter1Setting)

        filter_button = wx.Button(self.bottompanel, label=">>>", pos=((1*displaySize[0]/3)-3*seperatorConstant, yOffsetFilters+7*yConstantFilters/3))
        self.Bind(wx.EVT_BUTTON, self.OnFilter, filter_button)
        #Seperator
        self.ln = wx.StaticLine(self.bottompanel, -1, pos= ((1*displaySize[0]/3)-seperatorConstant, 0), size=(10,200), style=wx.LI_VERTICAL)
        

        #Graph
        xOffsetGraph = xConstant+1*displaySize[0]/3-seperatorConstant
        yOffsetGraph = 3
        xConstantGraph = 150
        yConstantGraph = 30
        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        graph = wx.StaticText(self.bottompanel, label="Graph", pos=(xOffsetGraph, yOffsetGraph))
        graph.SetFont(font)
        
        wx.StaticText(self.bottompanel, label="Accelerometer/Gyroscope", pos=(xOffsetGraph+xConstantGraph, yOffsetGraph+yConstantGraph))
        wx.StaticText(self.bottompanel, label="X-Axis --->", pos=(xOffsetGraph+xConstantGraph/2, yOffsetGraph+2*yConstantGraph))
        wx.StaticText(self.bottompanel, label="Y-Axis --->", pos=(xOffsetGraph+xConstantGraph/2, yOffsetGraph+3*yConstantGraph))
        wx.StaticText(self.bottompanel, label="Z-Axis --->", pos=(xOffsetGraph+xConstantGraph/2, yOffsetGraph+4*yConstantGraph))

        cb_x = wx.CheckBox(self.bottompanel, -1, '', (xOffsetGraph+3*xConstantGraph/2, yOffsetGraph+2*yConstantGraph))
        self.Bind(wx.EVT_CHECKBOX, self.OnCBX, cb_x)
        cb_y = wx.CheckBox(self.bottompanel, -1, '', (xOffsetGraph+3*xConstantGraph/2, yOffsetGraph+3*yConstantGraph))
        self.Bind(wx.EVT_CHECKBOX, self.OnCBY, cb_y)
        cb_z = wx.CheckBox(self.bottompanel, -1, '', (xOffsetGraph+3*xConstantGraph/2, yOffsetGraph+4*yConstantGraph))
        self.Bind(wx.EVT_CHECKBOX, self.OnCBZ, cb_z)

        graph_button = wx.Button(self.bottompanel, label=">>>", pos=((2*displaySize[0]/3)-3*seperatorConstant, yOffsetGraph+7*yConstantGraph/3))
        self.Bind(wx.EVT_BUTTON, self.OnGraph, graph_button)
        #Separator
        self.ln = wx.StaticLine(self.bottompanel, -1, pos= (2*displaySize[0]/3-seperatorConstant, 0), size=(10,200), style=wx.LI_VERTICAL)


        #Stats
        xOffsetStats = xConstant+2*displaySize[0]/3+xConstant-seperatorConstant
        yOffsetStats = 3
        xConstantStat = 150
        yConstantStat = 30

        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        stats = wx.StaticText(self.bottompanel, label="Stats", pos=(xOffsetStats, yOffsetStats))
        stats.SetFont(font)

        stats = wx.Button(self.bottompanel, label="View Stats", pos=(xOffsetStats, yOffsetStats+yConstantStat))
        self.Bind(wx.EVT_BUTTON, self.OnStats, stats)
        #Separator
        self.ln = wx.StaticLine(self.bottompanel, -1, pos= (3*displaySize[0]/3-6*seperatorConstant, 0), size=(10,200), style=wx.LI_VERTICAL)


        #Image        
        image = 'Icons/article32.png'
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
    	self.sBmp = wx.StaticBitmap(self.bottompanel, wx.ID_ANY, wx.BitmapFromImage(img), (1100,10))

        #Generate

        generate = wx.Button(self.bottompanel, label="Generate Output File", pos=(displaySize[0]-11*xConstant, (displaySize[1]/3)-7*xConstant))
        self.Bind(wx.EVT_BUTTON, self.OnGenerateFile, generate)

        #---SPLITTER FRAMES---#
        displaySize = wx.DisplaySize()
        self.split1.SplitHorizontally(self.split2, self.bottompanel)
        self.split1.SetMinimumPaneSize(11*displaySize[1]/16) #top panels take 3/4 of screen estate vertically
        self.split2.SplitVertically(self.topleftpanel, self.toprightpanel)

        self.Show(True)
        self.Maximize()

    def OnOpen(self, e):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            global isFileImported 
            isFileImported = True
            self.textL.Clear()
            self.textL.SetEditable(True)
            paths = dlg.GetPaths()
            viewParser(paths)
            self.textL.AppendText("ACCEL_X |  ACCEL_Y  |  ACCEL_Z   |   GYRO_X  |   GYRO_Y   |   GYRO_Z  |\n")
            for i in range(0, num_lines):
                self.textL.AppendText(FORMATTED_DATA[i])
                self.textL.AppendText('\n')
            self.textL.SetEditable(False)
        dlg.Destroy()

    #Filter
    def OnFilter0Settings(self, e):
        FilterFrame()

    def OnFilter1Settings(self, e):
        FilterFrame()

    def OnFilter(self, e):
        global isFileImported
        if isFileImported == True:
            self.textR.Clear()
            self.textR.AppendText("CHECK")
        else:
            wx.MessageBox("Import File First")
    #Graph
    def OnCBX(self, e):
        global CBX_val
        CBX_val =e.IsChecked()

    def OnCBY(self, e):
        global CBY_val
        CBY_val =e.IsChecked()

    def OnCBZ(self, e):
        global CBZ_val
        CBZ_val =e.IsChecked()

    def OnGraph(self, e):
        global isFileImported
        if isFileImported == True:
            GraphFrame()
        else:
            wx.MessageBox("Import File First")

    #Stats
    def OnStats(self, e):
        global isFileImported
        if isFileImported == True:
            StatsFrame()
        else:
            wx.MessageBox("Import File First")

    #Generate
    def OnGenerateFile(self, e):
        global isFileImported
        if isFileImported == True:
            self.Close()
        else:
            wx.MessageBox("Import File First")

    def OnHelp(self, e):
        self.Close()

    def OnAbout(self, e):
        hyper1 = hl.HyperLinkCtrl(self.bottompanel, -1, "Basic Electronixs", pos=(100, 250), URL="http://www.BasicElectronixs.com/")
        self.Close()

    #def OnTextChange(self, e):
        #self.textL.Undo()
    def OnUndoKeyPress(self, e):
        if wx.Window.FindFocus() == self.textL:
            self.textL.Undo()
        else:
            self.textR.Undo()

    def OnRedoKeyPress(self, e):
        if wx.Window.FindFocus() == self.textL:
            self.textL.Redo()
        else:
            self.textR.Redo()
            

    def OnKeyPress(self, e):
        keycode = e.GetKeyCode()
        #Undo Event
        if keycode == 90 and e.CmdDown():
            self.OnUndoKeyPress(self)
        #Redo Event
        elif keycode == 89 and e.CmdDown():
            self.OnRedoKeyPress(self)
        else:
            e.Skip()



def main():
    df = wx.App()
    Dragon(None)
    df.MainLoop()    


if __name__ == '__main__':
    main()