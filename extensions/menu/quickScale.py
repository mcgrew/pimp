"""
quickScale.py
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

import wx

from extensions.lib.core import quickScale

MENU = "&Image"
LABEL = "Image Size"
DESCRIPTION = "Scale The image using a fast, low quality algorithm"


def execute( width, height, data ):
    """
    Scales an image using a fast, low quality algorithm.
        
    :Parameters:
        width : int
            The width of the image being converted
        height : int
            The height of the image being converted
        data : string
            A string containing the data for the image
    
    :rtype: tuple
    :returns: a tuple containing a width, height, and data as a binary string.
    """
    dialog = scaleDialog( defaultWidth = width, defaultHeight = height )
    values = dialog.ShowModal( )
    
    if not values:
        return False
    
    newWidth, newHeight = values

    return quickScale( width, height, data, newWidth, newHeight )


class scaleDialog( wx.Dialog ):
    """
    A class for getting input values from the user for the scale filter
    """
    def __init__( self, parent=None, id=-1, okFunction = None, title="Scale Image", defaultWidth=1024, defaultHeight=768 ):
        """
        Initializes the dialog box.

        :Parameters:
            parent : wx.Frame
                The parent of this dialog. Defaults to None.
            id : int
                The id of this dialog. Defaults to -1
            okFunction : function
                An optional additional function to be called when the OK button is pressed. Defaults to None
            sliderUpdateFunction : function
                An an optional additional function to be called when one of the sliders is changed. Defaults to None.
            title : String
                The title of the dialog box to be displayed in the titlebar. Defaults to "Nintendize Options".
            maxResolution : int
                The maximim value to be available on the resolution slider. Defaults to 500.
        """
        wx.Dialog.__init__( self, None, -1, title, wx.DefaultPosition, ( 240, 110 ) )

        
        self.widthEntry  = wx.TextCtrl( self, -1, value = str( defaultWidth ),  pos = ( 70, 30 ), size = ( 100, 20 ) )
        self.heightEntry = wx.TextCtrl( self, -1, value = str( defaultHeight ), pos = ( 70, 50 ), size = ( 100, 20 ) )
        self.widthEntry.SetMaxLength(  5 )
        self.heightEntry.SetMaxLength( 5 )

        self.displayPanel   = wx.Panel( self, -1, pos = ( 180, 10 ), size = ( 50, 60 ) )
        self.headingDisplay = wx.StaticText( self.displayPanel, pos = ( 0,  0 ), label="Original Size" )
        self.widthDisplay   = wx.StaticText( self.displayPanel, pos = ( 0, 20 ), label=str( defaultWidth  ) )
        self.heightDisplay  = wx.StaticText( self.displayPanel, pos = ( 0, 40 ), label=str( defaultHeight ) )

        self.labelPanel = wx.Panel( self, -1, pos = ( 10, 30 ), size = ( 50, 40 ) )
        self.widthLabel = wx.StaticText( self.labelPanel, pos = ( 0,  0 ), label=" Width" )
        self.heightLabel   = wx.StaticText( self.labelPanel, pos = ( 0, 20 ), label="Height" )

        self.isOk = False
        okButton     = wx.Button( self, id = wx.ID_OK,     pos = (  30, 70 ), size = ( 80, 30 ) )
        cancelButton = wx.Button( self, id = wx.ID_CANCEL, pos = ( 130, 70 ), size = ( 80, 30 ) )

        if okFunction:
            self.okFunction = okFunction
        elif ( "onOk" in dir( self ) ):
            self.okFunction = self.onOk
        else:
            self.okFunction = lambda x,y: None

        self.widthEntry.Bind(  wx.EVT_CHAR, self.validate )
        self.heightEntry.Bind( wx.EVT_CHAR, self.validate )
        #self.Bind( wx.EVT_TEXT, self. )
        self.Bind( wx.EVT_CLOSE, self.cancel )
        okButton.Bind( wx.EVT_BUTTON, self.ok )
        cancelButton.Bind( wx.EVT_BUTTON, self.cancel )

    def validate( self, event ):
        """
        Internal Function. Validates input by making sure only the proper keypresses are allowed.

        :Parameters:
            event : wx.Event
                The event that triggered the calling of this function. Not optional
        """
        keyCode = event.GetKeyCode( )
        if keyCode == wx.WXK_RETURN:
            return self.ok( )
        if keyCode == wx.WXK_ESCAPE:
            return self.cancel( )
                                        # the numbers 0-9
        if not keyCode in ( 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_HOME, wx.WXK_END, wx.WXK_TAB ):
            return
        event.Skip( )
    
    def cancel( self, event=None ):
        """
        Internal function. Called when the "Cancel" button is pressed.

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self.Destroy( )

    def ok( self, event=None ):
        """
        Internal function. Called when the "OK" button is pressed

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self.okFunction( int( self.widthEntry.GetValue( ) ), int( self.heightEntry.GetValue( ) ) )
        self.isOk = True
        self.Destroy( )

    def ShowModal( self ):
        """
        Displays the dialog window and waits for the user to click OK or Cancel to return a value.

        :rtype: tuple or boolean
        :returns: The values for resolution and color level in a tuple if OK is clicked. Returns False otherwise.
        """
        wx.Dialog.ShowModal( self )
        if self.isOk:
            return ( int( self.widthEntry.GetValue( ) ), int( self.heightEntry.GetValue( ) ) )
        return False
