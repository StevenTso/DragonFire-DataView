import wx
import wx.lib.sheet


stockUndo = []
stockRedo = []


class UndoText:
        def __init__( self, sheet, text1, text2, row, column ):
                self.RedoText = text2
                self.row = row
                self.col = column
                self.UndoText = text1
                self.sheet = sheet

        def undo( self ):
                self.RedoText = self.sheet.GetCellValue( self.row, self.col )
                if self.UndoText == None:
                        self.sheetSetCellValue( '' )
                else: self.sheet.SetCellValue( self.row, self.col, self.UndoText )

        def redo( self ):
                if self.RedoText == None:
                        self.sheet.SetCellValue( '' )
                else: self.sheet.SetCellValue( self.row, self.col, self.RedoText )


class UndoColSize:
        def __init__( self, sheet, position, size ):
                self.sheet = sheet
                self.pos = position
                self.RedoSize = size
                self.UndoSize = 80

        def undo( self ):
                self.RedoSize = self.sheet.GetColSize( self.pos )
                self.sheet.SetColSize( self.pos, self.UndoSize )
                self.sheet.ForceRefresh()

        def redo( self ):
                self.UndoSize = 80
                self.sheet.SetColSize( self.pos, self.RedoSize )
                self.sheet.ForceRefresh()


class UndoRowSize:
        def __init__( self, sheet, position, size ):
                self.sheet = sheet
                self.pos = position
                self.RedoSize = size
                self.UndoSize = 20

        def undo( self ):
                self.RedoSize = self.sheet.GetRowSize( self.pos )
                self.sheet.SetRowSize( self.pos, self.UndoSize )
                self.sheet.ForceRefresh()

        def redo( self ):
                self.UndoSize = 20
                self.sheet.SetRowSize( self.pos, self.RedoSize )
                self.sheet.ForceRefresh()


class MySheet( wx.lib.sheet.CSheet ):

    def __init__( self, parent ):
        wx.lib.sheet.CSheet.__init__( self, parent )
        self.SetLabelBackgroundColour( '#DBD4D4' )
        self.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.text = ''

    def OnCellChange( self, event ):
        toolbar = self.GetParent().toolbar1
        if ( toolbar.GetToolEnabled( 808 ) == False ):
                toolbar.EnableTool( 808, True )
        r = event.GetRow()
        c = event.GetCol()
        text = self.GetCellValue( r, c )
        # self.text - text before change
        # text - text after change
        undo = UndoText( self, self.text, text, r, c )
        stockUndo.append( undo )
        if stockRedo:
                del stockRedo[:] # this might be surprising, but it is a standard behaviour in all spreadsheets
                toolbar.EnableTool( 809, False )

    def OnColSize( self, event ):
        toolbar = self.GetParent().toolbar1
        if ( toolbar.GetToolEnabled( 808 ) == False ):
                toolbar.EnableTool( 808, True )
        pos = event.GetRowOrCol()
        size = self.GetColSize( pos )
        undo = UndoColSize( self, pos, size )
        stockUndo.append( undo )
        if stockRedo:
                del stockRedo[:]
                toolbar.EnableTool( 809, False )


    def OnRowSize( self, event ):
        toolbar = self.GetParent().toolbar1
        if ( toolbar.GetToolEnabled( 808 ) == False ):
                toolbar.EnableTool( 808, True )
        pos = event.GetRowOrCol()
        size = self.GetRowSize( pos )
        undo = UndoRowSize( self, pos, size )
        stockUndo.append( undo )
        if stockRedo:
                del stockRedo[:]
                toolbar.EnableTool( 809, False )


class Newt( wx.Frame ):
    def __init__( self, parent, id, title ):
        wx.Frame.__init__( self, parent, -4, title, size = ( 550, 500 ), style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE )

        box = wx.BoxSizer( wx.VERTICAL )

        menuBar = wx.MenuBar()


        menu1 = wx.Menu()
        quit = wx.MenuItem( menu1, 105, "&Quit\tCtrl+Q", "Quits Newt" )
        quit.SetBitmap( wx.ArtProvider_GetBitmap( wx.ART_QUIT, wx.ART_OTHER, wx.Size( 16, 16 ) ) )
        menu1.AppendItem( quit )
        menuBar.Append( menu1, "&File" )

        wx.EVT_MENU( self, 105, self.OnQuitNewt )

        self.SetMenuBar( menuBar )

        # Setting up Toolbar

        self.toolbar1 = wx.ToolBar( self, -1, style = wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT )

        self.toolbar1.AddSimpleTool( 808, wx.ArtProvider_GetBitmap( wx.ART_UNDO, wx.ART_OTHER, wx.Size( 16, 16 ) ), 'Undo', '' )
        self.toolbar1.AddSimpleTool( 809, wx.ArtProvider_GetBitmap( wx.ART_REDO, wx.ART_OTHER, wx.Size( 16, 16 ) ), 'Redo', '' )
        self.toolbar1.EnableTool( 808, False )
        self.toolbar1.EnableTool( 809, False )
        self.toolbar1.AddSeparator()
        self.toolbar1.AddSimpleTool( 813, wx.ArtProvider_GetBitmap( wx.ART_QUIT, wx.ART_OTHER, wx.Size( 16, 16 ) ), 'Quit', '' )
        self.toolbar1.Realize()

        wx.EVT_TOOL( self.toolbar1, 808, self.OnUndo )
        wx.EVT_TOOL( self.toolbar1, 809, self.OnRedo )
        wx.EVT_TOOL( self.toolbar1, 813, self.OnQuitNewt )

        box.Add( self.toolbar1, border = 5 )
        box.Add( ( 5, 10 ), 0 )


        self.SetSizer( box )

        self.sheet1 = MySheet( self )
        self.sheet1.SetNumberRows( 55 )
        self.sheet1.SetNumberCols( 25 )
        for i in range( self.sheet1.GetNumberRows() ):
                self.sheet1.SetRowSize( i, 20 )

        self.sheet1.SetFocus()


        box.Add( self.sheet1, 1, wx.EXPAND )
        self.CreateStatusBar()
        self.Centre()
        self.Show( True )


    def OnUndo( self, event ):
        if len( stockUndo ) == 0:
                return

        a = stockUndo.pop()
        if len( stockUndo ) == 0:
                self.toolbar1.EnableTool( 808, False )
        a.undo()
        stockRedo.append( a )
        self.toolbar1.EnableTool( 809, True )

    def OnRedo( self, event ):
        if len( stockRedo ) == 0:
                return
        a = stockRedo.pop()
        if len( stockRedo ) == 0:
                self.toolbar1.EnableTool( 809, False )
        a.redo()
        stockUndo.append( a )
        self.toolbar1.EnableTool( 808, True )


    def OnQuitNewt( self, event ):
        self.Close( True )



app = wx.App( redirect = None )
newt = Newt( None, -1, "Newt" )
app.MainLoop()