import os
from wx.lib import sheet
import wx
import wx.grid as gridlib
import wx.lib.agw.hyperlink as hl
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

class graphParser:
    def __init__(self, path):
        #for filePath in path:
        #   stringPath.append(filePath)
        stringPath = ''.join(path)

        global num_lines
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

            global ACCEL_X, ACCEL_Y, ACCEL_Z, GYRO_X, GYRO_Y, GYRO_Z    
            ACCEL_X.append(parsed_line[0]);
            ACCEL_Y.append(parsed_line[1]);
            ACCEL_Z.append(parsed_line[2]);
            GYRO_X.append(parsed_line[3]);
            GYRO_Y.append(parsed_line[4]);
            GYRO_Z.append(parsed_line[5]);

class viewParser:
    def __init__(self, path):
        global FORMATTED_DATA
        FORMATTED_DATA = []
        graphParser(path)
        for var in range(0, num_lines):
            ax = str(ACCEL_X[var]).zfill(5) + "    |    "
            ay = str(ACCEL_X[var]).zfill(5) + "    |    "
            az = str(ACCEL_X[var]).zfill(5) + "    |    "
            gx = str(ACCEL_X[var]).zfill(5) + "    |    "
            gy = str(ACCEL_X[var]).zfill(5) + "    |    "
            gz = str(ACCEL_X[var]).zfill(5) + "   |"
            newLine = ax + ay + az + gx + gy + gz
            FORMATTED_DATA.append(newLine)
            
class Dragon(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Dragon, self).__init__(*args, **kwargs)
        self.currentDirectory = os.getcwd()
        self.InitUI()   

    def InitUI(self):
        #wx.Frame(parent, style=wx.MINIMIZE_BOX)
        #self.Maximize(not self.IsMaximized())
        self.SetSize((1200, 800))
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

        #Edit
        editMenu = wx.Menu()
        undo = editMenu.Append(wx.ID_ANY, 'Undo')
        redo = editMenu.Append(wx.ID_ANY, 'Redo')
        self.Bind(wx.EVT_MENU, self.OnUndoKeyPress, undo)
        self.Bind(wx.EVT_MENU, self.OnRedoKeyPress, redo)
        
        #View
        viewMenu = wx.Menu()
        stats = viewMenu.Append(wx.ID_ANY, '&Stats')
        graphs = viewMenu.Append(wx.ID_ANY, 'Graphs')
        self.Bind(wx.EVT_MENU, self.OnStats, stats)
        self.Bind(wx.EVT_MENU, self.OnGraphs, graphs)

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

        #---2nd DOWN---#
        
        #_____________________PANELS______________________________#
        self.split1 = wx.SplitterWindow(self)
        self.split2 = wx.SplitterWindow(self.split1)

        #---TEXT FRAMES---#
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
        xOffset = 20
        yOffset = 3
 
        self.bottompanel = wx.Panel(self.split1)
        #---STATS----#
        statsSeperator = 200
        xConstantStat = 200
        yConstantStat = 30

        font = wx.Font(pointSize=14, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        header = wx.StaticText(self.bottompanel, label="Stats", pos=(xOffset, yOffset))
        header.SetFont(font)

        text = wx.StaticText(self.bottompanel, label="Avg.X", pos=(xOffset, yOffset+2*yConstantStat))
        text = wx.StaticText(self.bottompanel, label="Avg.Y", pos=(xOffset, yOffset+3*yConstantStat))
        text = wx.StaticText(self.bottompanel, label="Avg.Z", pos=(xOffset, yOffset+4*yConstantStat))


        font = wx.Font(pointSize=12, family=wx.FONTFAMILY_MODERN, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_BOLD)
        text = wx.StaticText(self.bottompanel, label="Accelerometer", pos=(xOffset+xConstantStat, yOffset+yConstantStat))
        text.SetFont(font)

        #text.SetFont(font)

        wx.StaticText(self.bottompanel, label = "Avg.X", pos=(xOffset + xConstantStat, yOffset+yConstantStat))
        wx.StaticText(self.bottompanel, label = "Avg.Y", pos=(xOffset + xConstantStat, yOffset+2*yConstantStat))
        wx.StaticText(self.bottompanel, label = "Avg.Z", pos=(xOffset + xConstantStat, yOffset+3*yConstantStat))

        #---Graph---#

        '''
        graph = wx.StaticText(self.bottompanel, label="Stats", pos=(xOffset, yOffset))
        
        self.cb_accel_x = wx.CheckBox(self.bottompanel, -1, 'Accelerometer X', (xOffset, yOffset+yConstant))
        self.cb_accel_y = wx.CheckBox(self.bottompanel, -1, 'Accelerometer Y', (xOffset, yOffset+2*yConstant))
        self.cb_accel_z = wx.CheckBox(self.bottompanel, -1, 'Accelerometer Z', (xOffset, yOffset+3*yConstant))

        self.cb_gyro_x = wx.CheckBox(self.bottompanel, -1, 'Gyroscope X', (xOffset + xConstant, yOffset+yConstant))
        self.cb_gyro_y = wx.CheckBox(self.bottompanel, -1, 'Gyroscope Y', (xOffset + xConstant, yOffset+2*yConstant))
        self.cb_gyro_z = wx.CheckBox(self.bottompanel, -1, 'Gyroscope Z', (xOffset + xConstant, yOffset+3*yConstant))
        '''
        #---SEPERATOR---#
        self.ln = wx.StaticLine(self.bottompanel, -1, pos= (xOffset + xConstantStat + statsSeperator, 0), size=(10,200), style=wx.LI_VERTICAL)
        #self.ln.SetSize()


        #self.bottompanel.AddSeparator()
        #self.cb_accel_z = 
        """   
        fonts = ['Times New Roman', 'Times', 'Courier', 'Courier New', 'Helvetica', 'Sans', 'verdana', 'utkal', 'aakar', 'Arial']
        self.bottompanel = wx.Panel(self.split1)
        toolbar2 = wx.ToolBar(self.bottompanel, wx.TB_HORIZONTAL | wx.TB_TEXT)
        self.position = wx.TextCtrl(toolbar2)
        font = wx.ComboBox(toolbar2, -1, value = 'Times', choices=fonts, size=(100, -1), style=wx.CB_DROPDOWN)
        font_height = wx.ComboBox(toolbar2, -1, value = '10',  choices=['10', '11', '12', '14', '16'], size=(50, -1), style=wx.CB_DROPDOWN)
        toolbar2.AddControl(self.position)
        toolbar2.AddControl(wx.StaticText(toolbar2, -1, '  '))
        toolbar2.AddControl(font)
        toolbar2.AddControl(wx.StaticText(toolbar2, -1, '  '))
        toolbar2.AddControl(font_height)
        toolbar2.AddSeparator()
        bold = wx.Image('Icons/folder32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        toolbar2.AddCheckTool(-1, bold , shortHelp = 'Bold')
        italic = wx.Image('Icons/folder32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        toolbar2.AddCheckTool(-1, italic,  shortHelp = 'Italic')
        under = wx.Image('Icons/folder32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        toolbar2.AddCheckTool(-1, under, shortHelp = 'Underline')
        toolbar2.AddSeparator()
        toolbar2.AddSimpleTool(-1, wx.Image('Icons/folder32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Align Left', '')
        toolbar2.AddSimpleTool(-1, wx.Image('Icons/folder32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Center', '')
        toolbar2.AddSimpleTool(-1, wx.Image('Icons/folder32.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Align Right', '')
        """
        #---IMAGE---#
        
        image = 'Icons/article32.png'
        img = wx.Image(image, wx.BITMAP_TYPE_ANY)
    	self.sBmp = wx.StaticBitmap(self.bottompanel, wx.ID_ANY, wx.BitmapFromImage(img), (1100,10))


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
            self.textL.Clear()
            self.textL.SetEditable(True)
            paths = dlg.GetPaths()
            #for path in paths:
            graphParser(paths)
            viewParser(paths)
            self.textL.AppendText("ACCEL_X |  ACCEL_Y  |  ACCEL_Z   |   GYRO_X  |   GYRO_Y   |   GYRO_Z  |\n")
            for i in range(0, num_lines):
                self.textL.AppendText(FORMATTED_DATA[i])
                self.textL.AppendText('\n')
            self.textL.SetEditable(False)
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