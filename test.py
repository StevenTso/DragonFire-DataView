# Get the GUI stuff
import wx

# We're going to be handling files and directories
import os

# Set up some button numbers for the menu

ID_ABOUT=101
ID_OPEN=102
ID_SAVE=103
ID_BUTTON1=300
ID_EXIT=200

class MainWindow(wx.Frame):
    def __init__(self,parent,title):
        # based on a frame, so set up the frame
        wx.Frame.__init__(self,parent,wx.ID_ANY, title)

        # Add a text editor and a status bar
        # Each of these is within the current instance
        # so that we can refer to them later.
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)

        # Setting up the menu. filemenu is a local variable at this stage.


        # Set up the overall frame verically - text edit window above buttons
        # We want to arrange the buttons vertically below the text edit window
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control,1,wx.EXPAND)

        # Tell it which sizer is to be used for main frame
        # It may lay out automatically and be altered to fit window
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        # Show it !!!
        self.Show(1)



# Set up a window based app, and create a main window in it
app = wx.PySimpleApp()
view = MainWindow(None, "Sample editor")
# Enter event loop
app.MainLoop()