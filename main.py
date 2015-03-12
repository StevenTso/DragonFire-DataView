import os
import wx
import wx.lib.agw.hyperlink as hl

from pylab import *
from scipy import signal
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from numpy import sin, arange, pi

import parser
import DFfilt

path = None
#---File imported---#
isFileImported = False

parseFile = parser.parse()
fil = DFfilters.filters()

num_lines = 10;
original_data = []
modified_data = []

#Graph
#---CheckBox---#
CBX_val = False
CBY_val = False
CBZ_val = False
cb_show_original_val = False

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def formatFloat(listIn):
    f_data = []
    for x in range(0, len(listIn)):
        f_data.append("%0.2f" % float(listIn.pop(0)))
    return f_data

class FilterFrame(wx.Frame):
    LPFText1 = None
    LPFText2 = None
    LPF_default_button = None
    SMA_Text1 = None
    SMA_default_button = None
    EMA_Text1 = None
    EMA_default_button = None
    MAText1 = None
    MAText2 = None
    MA_default_button = None

    filter_button = None
    def __init__(self, priority, value):
        global filter_button

        if isFileImported == True and value!=0:
            wx.Frame.__init__(self, wx.GetApp().TopWindow, title="DF Filters")
            self.SetTitle('DF Smart Data')
            self.Centre()

            if value==1:
                global LPFText1, LPFText2, LPF_default_button
                self.SetSize((400, 160))
                wx.StaticText(self, label="Cut-Off Frequency", pos=(40, 20))
                LPFText1 = wx.TextCtrl(self, pos=(180, 20))
                LPFText1.AppendText(str(fil.LPF_Get_Cut_Off()))
                LPFText1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
                
                wx.StaticText(self, label="Numtaps", pos=(40, 50))
                LPFText2 = wx.TextCtrl(self, pos=(180, 50))
                LPFText2.AppendText(str(fil.LPF_Get_NumTaps()))
                LPFText2.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

                LPF_default_button = wx.Button(self, label="Default Settings", pos=(40, 80))
                self.Bind(wx.EVT_BUTTON, self.OnLPFDefault, LPF_default_button)

                filter_button = wx.Button(self, label=">>", pos=(290, 35))
                self.Bind(wx.EVT_BUTTON, self.OnLPFFilterGo, filter_button)

                self.Show(True)
                
            elif value==2:
                global SMA_Text1, SMA_default_button
                self.SetSize((350, 120))
                wx.StaticText(self, label="N (previous points)", pos=(20,20))
                SMA_Text1 = wx.TextCtrl(self, pos=(145, 20))
                SMA_Text1.AppendText(str(fil.SMA_Get_N()))
                SMA_Text1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

                SMA_default_button = wx.Button(self, label="Default Settings", pos=(20, 60))
                self.Bind(wx.EVT_BUTTON, self.OnSMADefault, SMA_default_button)

                filter_button = wx.Button(self, label=">>", pos=(260, 20))
                self.Bind(wx.EVT_BUTTON, self.OnSMAFilterGo, filter_button)

                self.Show(True)

            elif value==3:
                global EMA_Text1, EMA_default_button
                self.SetSize((350, 120))
                wx.StaticText(self, label="Alpha", pos=(20,20))
                EMA_Text1 = wx.TextCtrl(self, pos=(145, 20))
                EMA_Text1.AppendText(str(fil.EMA_Get_A()))
                EMA_Text1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

                EMA_default_button = wx.Button(self, label="Default Settings", pos=(20, 60))
                self.Bind(wx.EVT_BUTTON, self.OnEMADefault, EMA_default_button)

                filter_button = wx.Button(self, label=">>", pos=(260, 20))
                self.Bind(wx.EVT_BUTTON, self.OnEMAFilterGo, filter_button)

                self.Show(True)
            elif value==4:
                global MAText1, MAText2, MA_default_button
                self.SetSize((400, 160))
                wx.StaticText(self, label="Weight (previous)", pos=(40, 20))
                MAText1 = wx.TextCtrl(self, pos=(180, 20))
                MAText1.AppendText(str(fil.MA_Get_Prev()))
                MAText1.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
                
                wx.StaticText(self, label="Weight (current)", pos=(40, 50))
                MAText2 = wx.TextCtrl(self, pos=(180, 50))
                MAText2.AppendText(str(fil.MA_Get_Cur()))
                MAText2.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)

                MA_default_button = wx.Button(self, label="Default Settings", pos=(40, 80))
                self.Bind(wx.EVT_BUTTON, self.OnMADefault, MA_default_button)

                filter_button = wx.Button(self, label=">>", pos=(290, 35))
                self.Bind(wx.EVT_BUTTON, self.OnMAFilterGo, filter_button)

                self.Show(True)
            else:
                pass

        elif isFileImported == False:
            wx.MessageBox("Import File First")

        else:
            wx.MessageBox("No settings found")

    def OnLPFDefault(self, e):
        global LPFText1, LPFText2
        LPFText1.Clear()
        LPFText1.AppendText(str(fil.LPF_Default_Cut_Off()))
        LPFText2.Clear()
        LPFText2.AppendText(str(fil.LPF_Default_NumTaps()))

    def OnLPFFilterGo(self, e):
        global LPFText1, LPFText2
        cut_off_val = LPFText1.GetValue()
        numtaps_val = LPFText2.GetValue()
        if(cut_off_val.isdigit() and numtaps_val.isdigit()):
            if(int(cut_off_val)<fil.LPF_Get_Freq_Limit()):
                fil.LPF_Set_Cut_Off(int(cut_off_val))
                fil.LPF_Set_NumTaps(int(numtaps_val))
                wx.MessageBox("Settings Applied!")
            else:
                wx.MessageBox("Lower the value of the cut-off")
        else:
            wx.MessageBox("Please enter whole digits!")

    def OnLPFDefault(self, e):
        global LPFText1, LPFText2
        LPFText1.Clear()
        LPFText1.AppendText(str(fil.LPF_Default_Cut_Off()))
        LPFText2.Clear()
        LPFText2.AppendText(str(fil.LPF_Default_NumTaps()))

    def OnLPFFilterGo(self, e):
        global LPFText1, LPFText2
        cut_off_val = LPFText1.GetValue()
        numtaps_val = LPFText2.GetValue()
        if(cut_off_val.isdigit() and numtaps_val.isdigit()):
            if(int(cut_off_val)<fil.LPF_Get_Freq_Limit()):
                fil.LPF_Set_Cut_Off(int(cut_off_val))
                fil.LPF_Set_NumTaps(int(numtaps_val))
                wx.MessageBox("Settings Applied!")
            else:
                wx.MessageBox("Lower the value of the cut-off")
        else:
            wx.MessageBox("Please enter whole digits!")

    def OnSMADefault(self, e):
        global SMA_Text1
        SMA_Text1.Clear()
        SMA_Text1.AppendText(str(fil.SMA_Get_N()))

    def OnSMAFilterGo(self, e):
        global SMA_Text1
        value = SMA_Text1.GetValue()
        if(value.isdigit()):
            fil.SMA_Set_N(int(value))
            wx.MessageBox("Settings Applied!")
        else:
            wx.MessageBox("Please enter a whole number!")

    def OnEMADefault(self, e):
        global EMA_Text1
        EMA_Text1.Clear()
        EMA_Text1.AppendText(str(fil.EMA_Get_A()))

    def OnEMAFilterGo(self, e):
        global EMA_Text1
        value = EMA_Text1.GetValue()
        if(isFloat(value)):
            if(float(value)<=1):
                fil.EMA_Set_A(float(value))
                wx.MessageBox("Settings Applied!")
            else:
                wx.MessageBox("Please enter a number less than or equal to 1!")
        else:
            wx.MessageBox("Please enter an number!")


    def OnMADefault(self, e):
        global MAText1, MAText2
        MAText1.Clear()
        MAText1.AppendText(str(fil.MA_Default_Prev()))
        MAText2.Clear()
        MAText2.AppendText(str(fil.MA_Default_Cur()))

    def OnMAFilterGo(self, e):
        global MAText1, MAText2
        pre_val = MAText1.GetValue()
        cur_val = MAText2.GetValue()
        if(isFloat(pre_val) and isFloat(cur_val)):
            if((float(pre_val)+float(cur_val))==1):
                fil.MA_Set_Prev(float(pre_val))
                fil.MA_Set_Cur(float(cur_val))
                wx.MessageBox("Settings Applied!")
            else:
                wx.MessageBox("Make sure values add up to 1")
        else:
            wx.MessageBox("Please enter whole digits!")

    def OnUndoKeyPress(self, e):
        focus = wx.Window.FindFocus()
        if focus == self.LPFText1:
            self.LPFText1.Undo()
        elif focus == self.LPFText2:
            self.LPFText2.Undo()
        else:
            self.SMA_Text1.Undo()

    def OnRedoKeyPress(self, e):
        focus = wx.Window.FindFocus()
        if focus == self.LPFText1:
            self.LPFText1.Redo()
        elif focus == self.LPFText2:
            self.LPFText2.Redo()
        else:
            self.SMA_Text1.Redo()
            

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


class GraphFrame(wx.Frame):

    title = "DF Stats"

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title)
        global original_data, modified_data

        self.SetSize((400, 400))
        self.SetTitle('DF Smart Graph')
        self.Centre()
    
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)

        ACCEL_X = modified_data[0]
        ACCEL_Y = modified_data[1]
        ACCEL_Z = modified_data[2]
        GYRO_X = modified_data[3]
        GYRO_Y = modified_data[4]
        GYRO_Z = modified_data[5]

        #GRAPHS
        if(cb_show_original_val==True):
            t1 = arange(0, len(original_data[0]), 1)
            O_ACCEL_X = original_data[0]
            O_ACCEL_Y = original_data[1]
            O_ACCEL_Z = original_data[2]
            O_GYRO_X = original_data[3]
            O_GYRO_Y = original_data[4]
            O_GYRO_Z = original_data[5]          
            #ACCEL_X
            subplot(231)
            plot(t1, O_ACCEL_X,'k--', markerfacecolor='black')
            title('ACCEL_X')
            ylabel('Value')

            #ACCEL_Y
            subplot(232)
            plot(t1, O_ACCEL_Y,'k--', markerfacecolor='black')
            title('ACCEL_Y')
            ylabel('Value')


            #ACCEL_Z
            subplot(233)
            plot(t1, O_ACCEL_Z,'k--', markerfacecolor='black')
            title('ACCEL_Z')
            ylabel('Value')

            #GYRO_X
            subplot(234)
            plot(t1, O_GYRO_X,'k--', markerfacecolor='black')
            title('GYRO_X')
            ylabel('Value')

            #GRYO_Y
            subplot(235)
            plot(t1, O_GYRO_Y,'k--', markerfacecolor='black')
            title('GYRO_Y')
            ylabel('Value')
            
            #GRYO_Z
            subplot(236)
            plot(t1, O_GYRO_Z,'k--', markerfacecolor='black')
            title('GYRO_Z')
            ylabel('Value')


        t2 = arange(0, len(modified_data[0]), 1)
        #ACCEL_X
        subplot(231)
        plot(t2, ACCEL_X,'b--', markerfacecolor='green')
        title('ACCEL_X')
        ylabel('Value')

        #ACCEL_Y
        subplot(232)
        plot(t2, ACCEL_Y,'b--', markerfacecolor='green')
        title('ACCEL_Y')
        ylabel('Value')


        #ACCEL_Z
        subplot(233)
        plot(t2, ACCEL_Z,'b--', markerfacecolor='green')
        title('ACCEL_Z')
        ylabel('Value')

        #GYRO_X
        subplot(234)
        plot(t2, GYRO_X,'b--', markerfacecolor='green')
        title('GYRO_X')
        ylabel('Value')

        #GRYO_Y
        subplot(235)
        plot(t2, GYRO_Y,'b--', markerfacecolor='green')
        title('GYRO_Y')
        ylabel('Value')
        
        #GRYO_Z
        subplot(236)
        plot(t2, GYRO_Z,'b--', markerfacecolor='green')
        title('GYRO_Z')
        ylabel('Value')
        
        show()

class StatsFrame(wx.Frame):

    title = "DF Stats"

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title)
        self.SetSize((400, 400))
        self.SetTitle('DF Smart Stats')
        self.Centre()
        self.Show(True)

class Dragon(wx.Frame):
    filter_list = ['--------------', 'Low Pass Filter', 'Simple Moving Average', 'Exponential Moving Average', 'Weighted Mean']
    Filter0 = None
    Filter1 = None
    Filter2 = None
    Filter3 = None

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
        xConstantFilters = 120
        yConstantFilters = 25
        xBoxSize = 215

        settingsImagePlace = 'Icons/folder32.png'
        settingsImage = wx.Image(settingsImagePlace, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        filters = wx.StaticText(self.bottompanel, label="Filters", pos=(xOffsetFilters, yOffsetFilters))
        filters.SetFont(font)

        self.Filter0 = wx.ComboBox(self.bottompanel, pos=(xOffsetFilters, yOffsetFilters+1*yConstantFilters), size=(xBoxSize,-1), choices=self.filter_list, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Filter0.SetValue(self.filter_list[0])
        Filter0Setting = wx.BitmapButton(self.bottompanel, id=-1, bitmap=settingsImage, pos=(xBoxSize + 2*xOffsetFilters, yOffsetFilters+yConstantFilters), size = (3*settingsImage.GetWidth()/4, 3*settingsImage.GetHeight()/4))
        self.Bind(wx.EVT_BUTTON, self.OnFilter0Settings, Filter0Setting)

        self.Filter1 = wx.ComboBox(self.bottompanel, pos=(xOffsetFilters, yOffsetFilters+2*yConstantFilters), size=(xBoxSize,-1), choices=self.filter_list, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Filter1.SetValue(self.filter_list[0])
        Filter1Setting = wx.BitmapButton(self.bottompanel, id=-1, bitmap=settingsImage, pos=(xBoxSize + 2*xOffsetFilters, yOffsetFilters+2*yConstantFilters), size = (3*settingsImage.GetWidth()/4, 3*settingsImage.GetHeight()/4))
        self.Bind(wx.EVT_BUTTON, self.OnFilter1Settings, Filter1Setting)

        self.Filter2 = wx.ComboBox(self.bottompanel, pos=(xOffsetFilters, yOffsetFilters+3*yConstantFilters), size=(xBoxSize,-1), choices=self.filter_list, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Filter2.SetValue(self.filter_list[0])
        Filter2Setting = wx.BitmapButton(self.bottompanel, id=-1, bitmap=settingsImage, pos=(xBoxSize + 2*xOffsetFilters, yOffsetFilters+3*yConstantFilters), size = (3*settingsImage.GetWidth()/4, 3*settingsImage.GetHeight()/4))
        self.Bind(wx.EVT_BUTTON, self.OnFilter2Settings, Filter2Setting)

        self.Filter3 = wx.ComboBox(self.bottompanel, pos=(xOffsetFilters, yOffsetFilters+4*yConstantFilters), size=(xBoxSize,-1), choices=self.filter_list, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.Filter3.SetValue(self.filter_list[0])
        Filter3Setting = wx.BitmapButton(self.bottompanel, id=-1, bitmap=settingsImage, pos=(xBoxSize + 2*xOffsetFilters, yOffsetFilters+4*yConstantFilters), size = (3*settingsImage.GetWidth()/4, 3*settingsImage.GetHeight()/4))
        self.Bind(wx.EVT_BUTTON, self.OnFilter3Settings, Filter3Setting)

        filter_button = wx.Button(self.bottompanel, label=">>>", pos=((1*displaySize[0]/3)-2.5*seperatorConstant, yOffsetFilters+7*yConstantFilters/3))
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

        wx.StaticText(self.bottompanel, label="Graph Original", pos=((2*displaySize[0]/3)-4*seperatorConstant, yOffsetGraph+13*yConstantGraph/3))
        cb_show_original = wx.CheckBox(self.bottompanel, -1, '', pos=((2*displaySize[0]/3)-2*seperatorConstant, yOffsetGraph+13*yConstantGraph/3))
        self.Bind(wx.EVT_CHECKBOX, self.OnCB_show_original, cb_show_original)

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
        global path, num_lines, original_data, modified_data
        wildcard = "Python source (*.txt)|*.txt|" \
            "All files (*.*)|*.*"
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            global isFileImported
            original_data[:] = []
            isFileImported = True
            self.textL.Clear()
            self.textL.SetEditable(True)
            path = dlg.GetPaths()
            num_lines = parseFile.GetLineCount(path)
            original_data = parseFile.parser(path)
            modified_data = original_data
            formatted_data = parseFile.WindowView(original_data)
            for i in range(0, num_lines):
                self.textL.AppendText(formatted_data[i])
                self.textL.AppendText('\n')
            self.textL.SetEditable(False)
        dlg.Destroy()

    #Filter
    def OnFilter0Settings(self, e):
        FilterFrame(0, self.Filter0.GetCurrentSelection())

    def OnFilter1Settings(self, e):
        FilterFrame(1, self.Filter1.GetCurrentSelection())

    def OnFilter2Settings(self, e):
        FilterFrame(2, self.Filter2.GetCurrentSelection())

    def OnFilter3Settings(self, e):
    	FilterFrame(3, self.Filter3.GetCurrentSelection())

    def OnFilter(self, e):
        global isFileImported, path
        global original_data, modified_data
        if isFileImported == True:
            #LPF
            cut_off_freq = fil.LPF_Get_Cut_Off()
            numtaps = fil.LPF_Get_NumTaps()
            #SMA
            n = fil.SMA_Get_N()
            #EMA
            a = fil.EMA_Get_A()
            #MA
            x = fil.MA_Get_Cur()

            num_lines = parseFile.GetLineCount(path)
            original_data[:] = []
            buff = []
            modified_data[:] = []
            original_data = parseFile.parser(path)
            buff = original_data
            
            value0 = self.Filter0.GetCurrentSelection()
            if value0==1:
                modified_data = fil.LPF(buff, cut_off_freq, numtaps)
            elif value0==2:
                print original_data
                print modified_data
                modified_data = fil.Simple_Moving_Average(buff, n)
                print original_data
                print modified_data
            elif value0==3:
                modified_data = fil.Exponential_Moving_Average(buff, a)
            elif value0==4:
                modified_data = fil.Moving_Average(buff, x)
            else:
                pass
            
            value1 = self.Filter1.GetCurrentSelection()
            if value1==1:
                modified_data = fil.LPF(modified_data, cut_off_freq, numtaps)
            elif value1==2:
                modified_data = fil.Simple_Moving_Average(modified_data, n)
            elif value1==3:
                modified_data = fil.Exponential_Moving_Average(modified_data, a)
            elif value1==4:
                modified_data = fil.Moving_Average(modified_data, x)
            else:
                pass

            value2 = self.Filter2.GetCurrentSelection()
            if value2==1:
                modified_data = fil.LPF(modified_data, cut_off_freq, numtaps)
            elif value2==2:
                modified_data = fil.Simple_Moving_Average(modified_data, n)
            elif value2==3:
                modified_data = fil.Exponential_Moving_Average(modified_data, a)
            elif value2==4:
                modified_data = fil.Moving_Average(modified_data, x)
            else:
                pass

            value3 = self.Filter3.GetCurrentSelection()
            if value3==1:
                modified_data = fil.LPF(modified_data, cut_off_freq, numtaps)
            elif value3==2:
                modified_data = fil.Simple_Moving_Average(modified_data, n)
            elif value3==3:
                modified_data = fil.Exponential_Moving_Average(modified_data, a)
            elif value3==4:
                modified_data = fil.Moving_Average(modified_data, x)
            else:
                pass

            self.textR.Clear()
            #format data before displaying
            f_data = []

            if(type(modified_data[0])==list):
                ACCEL_X = modified_data[0]
                ACCEL_Y = modified_data[1]
                ACCEL_Z = modified_data[2]
                GYRO_X = modified_data[3]
                GYRO_Y = modified_data[4]
                GYRO_Z = modified_data[5]

            else:
                ACCEL_X = modified_data[0].tolist()
                ACCEL_Y = modified_data[1].tolist()
                ACCEL_Z = modified_data[2].tolist()
                GYRO_X = modified_data[3].tolist()
                GYRO_Y = modified_data[4].tolist()
                GYRO_Z = modified_data[5].tolist()

            ACCEL_X_filtered_signal = formatFloat(ACCEL_X)
            ACCEL_Y_filtered_signal = formatFloat(ACCEL_Y)
            ACCEL_Z_filtered_signal = formatFloat(ACCEL_Z)
            GYRO_X_filtered_signal = formatFloat(GYRO_X)
            GYRO_Y_filtered_signal = formatFloat(GYRO_Y)
            GYRO_Z_filtered_signal = formatFloat(GYRO_Z)

            f_data.append(ACCEL_X_filtered_signal)
            f_data.append(ACCEL_Y_filtered_signal)
            f_data.append(ACCEL_Z_filtered_signal)
            f_data.append(GYRO_X_filtered_signal)
            f_data.append(GYRO_Y_filtered_signal)
            f_data.append(GYRO_Z_filtered_signal)

            formatted_data = parseFile.WindowView(f_data)
            self.textR.SetEditable(True)
            self.textR.Clear()
            for i in range(0, len(formatted_data)):
                self.textR.AppendText(formatted_data[i])
                self.textR.AppendText('\n')
            self.textR.SetEditable(False)

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
    
    def OnCB_show_original(self, e):
        global cb_show_original_val
        cb_show_original_val = e.IsChecked()
    
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

    def OnUndoKeyPress(self, e):
        global textR
        if wx.Window.FindFocus() == self.textL:
            self.textL.Undo()
        else:
            textR.Undo()

    def OnRedoKeyPress(self, e):
        global textR
        if wx.Window.FindFocus() == self.textL:
            self.textL.Redo()
        else:
            textR.Redo()
            

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