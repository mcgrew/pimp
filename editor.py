"""
pimpgui.py
Copyright 2007 Thomas McGrew

This file is part of The Python Image Manipulation Project.

The Python Image Manipulation Project is free software: you can
redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either
version 2 of the License, or (at your option) any later version.

The Python Image Manipulation Project is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with The Python Image Manipulation Project.  If not, see
<http://www.gnu.org/licenses/>.
"""

# library imports
import types
import wx
from glob import glob
from sys import path, argv, platform
import os

# constants
VERSION = "0.1"
TITLE = "The PIMP"
DEBUG = False
MAXIMUM_UNDO_LIMIT = 10

#make sure we are in the right directory
os.chdir( os.path.abspath( os.path.dirname( argv[ 0 ] ) ) )

# local imports
from error import *
# C extensions
if ( platform == "win32" ):
    C_EXTENSIONS = ".pyd"
else:
    C_EXTENSIONS = os.extsep + "so"

from image import Image

# import the core module
import extensions.lib.core


# create dictionaries for storing file reader extensions.
fileReader = { 'ext' : dict( ), 'marker' : dict( ) }


def reloadExtensions( ):
    """
    Reloads file reader extensions. Currently does not re-parse already loaded
    extensions but will load new ones.
    """
    fileReader = { 'ext' : dict( ), 'marker' : dict( ) }
    loadExtensions( )

def loadExtensions( ):
    """
    Scans extension directories for available extensions and attempts to load them.
    """
    # file reader extension path
    formatExtensionPkg = ( "extensions", "format" )
    formatExtensionDir = os.path.join( os.getcwd( ), *formatExtensionPkg )

    debug( "Loading file format extensions" )
    fileFormatExtensions = glob( os.path.join( formatExtensionDir, '*%spy' % os.extsep ) ) + glob( os.path.join( formatExtensionDir, '*'+ C_EXTENSIONS ) )
    for f in fileFormatExtensions:
        module = os.path.basename( f )
        # import the module into a temporary variable for checking
        moduleName = '.'.join( formatExtensionPkg + ( module[ : module.rindex( "." ) ], ) )
        exec ( "import %s" % moduleName )
        tmp = eval( moduleName )
        if ( "FILE_EXTENSION" in dir( tmp ) ):
            if ( type( tmp.FILE_EXTENSION ) in ( list, tuple ) ):
                for ext in tmp.FILE_EXTENSION:
                    fileReader[ 'ext' ][ ext.lower( ) ] = tmp
            else:
                fileReader[ 'ext' ][ tmp.FILE_EXTENSION.lower( ) ] = tmp
        if ( "FILE_MARKER" in dir( tmp ) ):
            fileReader[ 'marker' ][ tmp.FILE_MARKER ] = tmp
    for ext in fileReader[ 'ext' ].keys( ):
        debug( "Loaded fileHandler for %s files" % ext )
    debug( )

# ============================================================ FRAME CLASS ========================================
class Frame( wx.Frame ):
    """
    The Frame object is used as the main application window.
    """
    def __init__( self ):
        """
        Creates a new Frame object.
        """
        wx.Frame.__init__( self, None, -1, TITLE, wx.DefaultPosition, wx.DefaultSize )
        self.image = None
        self.setImageFileName( None )
        self.scroller = wx.ScrolledWindow( self )
        self.panel = wx.Panel( self.scroller )
        self.scroller.EnableScrolling( True, True )
        #self.panel = wx.Panel( self )
        self.extensions = dict( )
        self.CreateStatusBar( )
        self.buildMenu( )
        self.loadMenuExtensions( )
        self.undoStack = list( )
        self.redoStack = list( )
        self.windowIsDirty = False

        #self.Bind( wx.EVT_SIZE, self.onSize )
        self.panel.Bind( wx.EVT_SIZE, self.onPanelSize )
        self.Bind( wx.EVT_PAINT, self.onPaint )
        self.Bind( wx.EVT_MOVE, self.onMove )
        self.Bind( wx.EVT_IDLE, self.onIdle )

    def setImage( self, image ):
        """
        Sets the image for the application.

        :Parameters:
            image : Image
                The image to be displayed.
        """
        width = image.getWidth( )
        height = image.getHeight( )
        # set the sizes of our main frame and inner panel
        self.scroller.SetScrollbars( 1, 1, width, height )
        self.SetSize( ( width + 5, height + 52 ) )
        self.panel.SetSize( ( width, height ) )
        # set the image and repaint the frame to display it.
        self.image = image
        self.Refresh( )

    # ================================= EVENT HANDLERS ================================
    def Refresh( self ):
        """
        This method overrides the Refresh method of the wx.Frame class. The Refresh( )
        method doesn't seem to work correctly on all versions of wxPython, so I'm replacing
        it with one that should work anywhere.
        """
        self.windowIsDirty = True

    def onMove( self, event=None ):
        """
        Internal Function. Called when the window is moved.
        """
        self.Refresh( )

    def onPanelSize( self, event=None ):
        """
        Internal Function. Called when the window is resized.
        """
        self.Refresh( )

    def onIdle( self, event=None ):
        """
        Internal Function. Called when the application becomes idle.
        """
        # Is the window marked dirty?
        if ( self.windowIsDirty ):
            windowIsDirty = False
            # check to see if scroll bars are needed.
            self.checkScrollBars( )
            # repaint the window
            self.paint( )

    def onPaint(self, event=None ):
        """
        Internal Function. Called when repainting the window.
        """
        self.paint( )
        
    def paint( self ):
        """
        Internal Function. Called when the window needs to be repainted.
        """
        # There is still a problem on fluxbox where the portion of the image under the
        # window position display doesn't get repainted when moving a window. I'm not
        # sure how to deal with this problem yet. Sleeping after a move doesn't help.
        if self.image:
            dc = wx.WindowDC( self.panel )
            dc.DrawBitmap( self.getBitmap( ), 0, 0 )
    
    def checkScrollBars( self, event=None ):
        if self.image:
            # turn off the scrollbars by default
            xScroll = 0
            yScroll = 0
            if ( self.GetSize( )[ 0 ] < self.panel.GetSize( )[ 0 ] + 5 ):
                xScroll = 5 # enable the horizontal scrollbar
            if ( self.GetSize( )[ 1 ] < self.panel.GetSize( )[ 1 ]  + 52 ):
                yScroll = 5 # enable the vertical scrollbar
            self.scroller.SetScrollRate( xScroll, yScroll )

    # ================================ END EVENT HANDLERS ==================================

    def getBitmap( self ):
        """
        Returns a copy of the application's image for display. This allows a different
        image to be displayed on the screen than is stored internally, i.e. for zooming.
        """
        returnvalue = extensions.lib.core.dataToBitmap( self.image.getWidth( ),
                                                        self.image.getHeight( ),
                                                        self.image.getData( ) )
        return returnvalue

    def zoom( self, event=None ):
        """
        As of yet, this does nothing.
        """
        pass

    def buildMenu( self ):
        """
        Internal Function. Builds the menu bar for the application.
        """
        self.menuBar = wx.MenuBar( )
        self.SetMenuBar( self.menuBar )
        menus = list( )
        fileMenu = wx.Menu( )
        self.menuBar.Append( fileMenu, "&File" )
        editMenu = wx.Menu( )
        self.menuBar.Append( editMenu, "&Edit" )
        helpMenu = wx.Menu( )
        self.menuBar.Append( helpMenu, "&Help" )
        # ============ ADD ITEMS TO THE MENU =============
        self.Bind( wx.EVT_MENU, self.openFile, fileMenu.Append( -1, "&Open", "Open a file" ) )
        self.Bind( wx.EVT_MENU, self.saveFile, fileMenu.Append( -1, "&Save", "Save the file" ) )
        self.Bind( wx.EVT_MENU, self.saveFileAs, fileMenu.Append( -1, "&Save As", "Save the file under a different name" ) )
        self.Bind( wx.EVT_MENU, self.reloadMenuExtensions, fileMenu.Append( -1, "Reload Extensions", "Reload all PIMP extensions" ) )
        self.Bind( wx.EVT_MENU, self.onExit, fileMenu.Append( -1, "E&xit", "Close the program" ) )
        self.Bind( wx.EVT_MENU, self.undo, editMenu.Append( -1, "&Undo", "Undo the last change" ) )
        self.Bind( wx.EVT_MENU, self.redo, editMenu.Append( -1, "&Redo", "Redo the last undone change" ) )

    def setImageFileName( self, filename ):
        """
        Internal Function. Updates the name of the current file being edited and
        displays it in the titlebar.
        """
        self.imageFileName = filename
        if self.imageFileName:
            self.SetTitle( os.path.basename( filename ) + " - " + TITLE )
        else:
            self.SetTitle( TITLE )


    # ==================================== STATIC MENU METHODS ======================
    def openFile( self, event=None ):
        """
        Opens an image file
        """
        dialog = wx.FileDialog( self, style = wx.FD_OPEN )
        if dialog.ShowModal( ) == wx.ID_OK:
            self.setImageFileName( dialog.GetPath( ) )
            self.setImage( read( self.imageFileName ) )
            # clear the undo and redo stacks
            self.undoStack = list( )
            self.redoStack = list( )
        dialog.Destroy( )

    def saveFile( self, event=None ):
        """
        Saves the file out to the previously defined image.
        """
        if self.imageFileName:
            write( self.imageFileName, self.image )
        else:
            self.saveFileAs( )

    def saveFileAs( self, event=None ):
        """
        Saves the file under a different filename
        """
        dialog = wx.FileDialog( self, style = wx.FD_SAVE )
        if dialog.ShowModal( ) == wx.ID_OK:
            self.setImageFileName( dialog.GetPath( ) )
            self.saveFile( )
        dialog.Destroy( )

    def undo( self, event=None ):
        """
        Rolls back the last change made to an image.
        """
        if ( len( self.undoStack ) ):
            self.redoStack.append( self.image )
            self.setImage( self.undoStack.pop( ) )

    def redo( self, event=None ):
        """
        Reapplies the last undone change to an image.
        """
        if ( len( self.redoStack ) ):
            self.undoStack.append( self.image )
            self.setImage( self.redoStack.pop( ) )


    # ================================== EXTENSION LOADING METHODS ==========================
    def reloadMenuExtensions( self, event=None ):
        """
        Internal function. Reloads the menu extensions.
        """
        # This function doens't work quite right. Python caches the modules it loads
        # somehow and a call to reload( ) is needed to completely reload them.
        debug( "RELOADING EXTENSIONS" )
        #reload the fileformat extensions
        reloadExtensions( )
        #reload the default menu items
        self.buildMenu( )
        # reload the menu extensions
        self.loadMenuExtensions( )


    def loadMenuExtensions( self ):
        """
        Internal Function. Loads Extensions that create menu items.
        """
        # menu item extension path
        menuExtensionPkg = ( "extensions", "menu" )
        menuExtensionDir = os.path.join( os.getcwd( ), *menuExtensionPkg )

        debug( "Loading menu items" )
        menuExtensions = glob( os.path.join( menuExtensionDir, '*%spy'%os.extsep ) ) + glob( os.path.join( menuExtensionDir, '*'+ C_EXTENSIONS ) )
        for f in menuExtensions:
            moduleFile = os.path.basename( f )
            moduleName = '.'.join( menuExtensionPkg + ( moduleFile[ : moduleFile.index( "." ) ], ) )
            module = getattr(__import__(moduleName).menu, moduleName[moduleName.rfind('.')+1:])

            if ( "MENU" in dir(module) and "LABEL" in dir( module ) ):
                self.extensions[ '.'.join( ( module.MENU, module.LABEL ) ) ] = module

                #insert this into the proper menu (and possibly submenu)

                # split up the menu path to see if it contains submenus
                menuPath = module.MENU.split( '.' )

                menuPos = self.menuBar.FindMenu( menuPath[ 0 ])
                if ( menuPos == -1 ):
                    self.menuBar.Insert( self.menuBar.GetMenuCount( )-1, wx.Menu( ), menuPath[ 0 ] )
                    menuPos = self.menuBar.FindMenu( menuPath[ 0 ] )

                menu = self.menuBar.GetMenu( menuPos )
                menu_list = self.findMenu(menu, menuPath[1:])
                self.addItem(module, menu_list[-1] if len(menu_list) else menu)

            else:
                # the module does not have the correct 'constants' defined.
                debug( moduleFile + " is not a valid module." )
        debug( )

    def findMenu(self, menu, menuPath):
        if not len(menuPath):
            return []
        items = menu.GetMenuItems()
        for m in items:
            if hasattr(m, 'GetName'):
                if m.GetName().replace('&', '') == menuPath[0].replace('&',''):
                    return m, *self.findMenu(m, menuPath[1:])
        m = menu.Append(-1, menuPath[0], wx.Menu())
        return m, *self.findMenu(m, menuPath[1:])

    def addItem(self, module, menu):
        if not hasattr(menu, 'Append'):
            menu = menu.GetSubMenu()
        if ( "DESCRIPTION" in dir( module ) ):
            description = module.DESCRIPTION
        else:
            description = str()
        # create and bind a handler to a menuItem.
        self.Bind(wx.EVT_MENU, self.filterHandler(module.execute), menu.Append(-1, module.LABEL, description))

    def filterHandler( self, handler ):
        """
        Internal Function. Creates a custom dynamic handler for menu items.
        """
        # define a new function and return it.
        def f( evt ):
            if ( self.image ):
                newImageData = handler( self.image.getWidth( ), self.image.getHeight( ), extensions.lib.core.stringCopy( bytes(self.image.getData( )) ) )
            else:
                handler( 1, 1, "\x00" )
                newImageData = False
            # set this frame's image to the one returned by the filter.
            if ( newImageData and len( newImageData ) == 3 ):
                self.redoStack = list( )
                self.undoStack.append( self.image )
                while ( len( self.undoStack ) > MAXIMUM_UNDO_LIMIT ):
                    del self.undoStack[ 0 ]
                self.setImage( Image( *newImageData ) )
        return f
    # ================================== END EXTENSION LOADING METHODS =================================


    def onExit( self, event ):
        """
        Internal function. Closes the program.
        """
        self.Close( True )

# ====================================================== END FRAME CLASS =====================================================================

def buildImage( width, height, data ):
    """
    Creates an image type (from image.py) for use in the program.

    :Parameters:
        width : int
            The width of the image in pixels
        height : int
            The height of the image in pixels
        data : string
            The image data as a string.
    """
    # this used to do something more complicated...
    return Image( width, height, data )

def write( filename, image ):
    """
    Writes an image out to file. The image format must be supported by a file format extension.

    :Parameters:
        filename : string
            The path to the file to be written.
        image : Image
            The Image containing the data to be written.
    """
    width, height = image.getSize( )
    imageExt = filename[ filename.index( '.' ) + 1 : ].lower( ) # get the file extension
    
    if imageExt not in fileReader[ 'ext' ]:
        raise UnsupportedImageTypeError( "File extension %s has no extension associated with it" % imageExt )
    if not ( "write" in dir( fileReader[ 'ext' ][ imageExt ] ) ):
        raise UnsupportedImageTypeError( "The extension for handling files of type '%s' contains no method for writing." % imageExt )
    try:
        return fileReader[ 'ext' ][ imageExt ].write(filename, image.getWidth(), image.getHeight(), extensions.lib.core.stringCopy(bytes(image.getData())))
    except:
        raise # TODO: show an error dialog


def read( filename ):
    """
    Calls the appropriate extension to read the image file, if one exists.

    :Paramters:
        filename : string
            The name of the file to be read.
    """
    imageExt = filename[ filename.index( '.' ) + 1 : ].lower( ) # get the file extension
    try:
        if not imageExt in fileReader[ 'ext' ]:
            raise UnsupportedImageTypeError( "File extension %s has no extension associated with it" % imageExt )
        if not ( "read" in dir( fileReader[ 'ext' ][ imageExt ] ) ):
            raise UnsupportedImageTypeError( "The extension for handling files of type '%s' contains no method for reading." % imageExt )
        imageData =  fileReader[ 'ext' ][ imageExt ].read( filename )

    except ImageFormatError as message:
        debug( message )
        imageFile = open( filename, 'rb' )
        fileMarker = imageFile.read( 2 )
        imageFile.close(  )
        if not fileMarker not in fileReader[ 'marker' ]:
            imageFile.close( )
            raise UnsupportedImageTypeError( "This image type has no extension associated with it" )
        try: # in case the extension doesn't define a description field (it should)
            debug( "File %s was found to be an incorrectly named %s file" % ( filename, fileReader[ 'marker' ][ fileMarker ].DESCRIPTION ) )
        except:
            debug( "File %s was found to be an incorrectly named file" % ( filename ) )
        imageData = fileReader[ 'marker' ][ fileMarker ].read( filename )

    if ( len( imageData ) != 3 ):
       raise ExtensionError( "File format extension for %s returned an invalid number of arguments" % imageExt )
    width, height, data = imageData
    returnvalue = Image( width, height, data )

    return returnvalue


def log( string ):
    """
    Internal Function to appropriately handle important messages.

    :Parameters:
        string : string
            The message to output to the log.
    """
    print(string)

def debug( string="" ):
    """
    Internal Function that handles debug output for the program.
    """
    if DEBUG:
        print(string)


loadExtensions( ) # call the function to load all available extensions.
