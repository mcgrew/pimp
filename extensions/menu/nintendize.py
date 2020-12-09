"""
nintendize.py
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

from extensions.lib import nintendize

MENU = "Fil&ter.&Comic"
LABEL = "Nintendi&ze"
DESCRIPTION = "Nintendize it!"

def execute( width, height, data, resolution=None, colorLevel=None ):
    """
    Pixellates the image and reduces bit quality in a way such that it
    looks like an image from an old video game console. Resolution and
    colorLevel are optional, either both or none should be provided. A
    dialog will appear requesting both values if one is not supplied,
    in which case the passed in values are ignored.
    
    :Parameters:
        filename : string
            The name of the file to write to.
        width : int
            The width of the image in pixels
        height : int
            The height of the image in pixels
        data : string
            The data as a string - chr(red) + chr(green) + chr(blue) for each pixel.
        resolution : int
            The resolution value to apply to the image.
        colorLevel : int
            The colorLevel value to apply to the image
    
    :rtype: tuple
    :returns: A tuple ( width, height, data ). Width and height are in pixels, data is a binary string.
    """
    if ( None in ( resolution, colorLevel ) ):
        dialog = nintendizeDialog( maxResolution = min( width, height ) )
        values = dialog.ShowModal( )
        
        if not values:
            return False
        
        resolution, colorlevel = values
    
    return nintendize.execute( width, height, data, resolution, colorlevel )


class nintendizeDialog( wx.Dialog ):
    """
    A class for getting input values from the user for the nintendize filter
    """
    def __init__( self, parent=None, id=-1, okFunction=None, sliderUpdateFunction=None, title="Nintendize Options", maxResolution=500 ):
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
        wx.Dialog.__init__( self, None, -1, title, wx.DefaultPosition, ( 320, 90 ) )

        self.resolutionValue = 200
        self.colorLevelValue = 2
        
        self.resolutionSlider = wx.Slider( self, -1, value = self.resolutionValue, minValue = 1, maxValue = maxResolution, pos = ( 70, 10 ), size = ( 200, 20 ) )
        self.colorLevelSlider   = wx.Slider( self, -1, value = self.colorLevelValue, minValue =  1, maxValue =  8, pos = ( 70, 30 ), size = ( 200, 20 ) )

        self.displayPanel = wx.Panel( self, -1, pos = ( 270, 10 ), size = ( 50, 100 ) )
        self.resolutionDisplay = wx.StaticText( self.displayPanel, pos = ( 0,  0 ) )
        self.colorLevelDisplay   = wx.StaticText( self.displayPanel, pos = ( 0, 20 ) )

        self.labelPanel = wx.Panel( self, -1, pos = ( 0, 10 ), size = ( 70, 40 ) )
        self.resolutionLabel = wx.StaticText( self.labelPanel, pos = ( 0,  0 ), label="Resolution" )
        self.colorLevelLabel   = wx.StaticText( self.labelPanel, pos = ( 0, 20 ), label="Color Level"   )

        self.isOk = False
        okButton     = wx.Button( self, id = wx.ID_OK,     pos = (  60, 50 ), size = ( 80, 30 ) )
        cancelButton = wx.Button( self, id = wx.ID_CANCEL, pos = ( 160, 50 ), size = ( 80, 30 ) )

        if okFunction:
            self.okFunction = okFunction
        elif ( "onOk" in dir( self ) ):
            self.okFunction = self.onOk
        else:
            self.okFunction = lambda x,y: None
            
        if sliderUpdateFunction:
            self.sliderUpdateFunction = sliderUpdateFunction
        elif ( "onSliderupdate" in dir( self ) ):
            self.sliderUpdateFunction = self.onSliderupdate
        else:
            self.sliderUpdateFunction = lambda x,y: None
            
        self.updateDisplay( )


        self.Bind( wx.EVT_SLIDER, self.sliderChange )
        self.Bind( wx.EVT_CLOSE, self.cancel )
        okButton.Bind( wx.EVT_BUTTON, self.ok )
        cancelButton.Bind( wx.EVT_BUTTON, self.cancel )

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
        self.okFunction( self.resolutionValue, self.colorLevelValue )
        self.isOk = True
        self.Destroy( )

    def sliderChange( self, event=None ):
        """
        Internal Function. Called when one of the sliders is changed within the dialog box.

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self.resolutionValue = self.resolutionSlider.GetValue( )
        self.colorLevelValue = self.colorLevelSlider.GetValue( )

        self.updateDisplay( )
        self.sliderUpdateFunction( self.resolutionValue, self.colorLevelValue )

    def updateDisplay( self ):
        """
        Internal Function. Called when one of the sliders is changed to update the values displayed.
        """
        self.resolutionDisplay.SetLabel( "%5d" % self.resolutionValue )
        self.colorLevelDisplay.SetLabel( "%3d" % self.colorLevelValue   )

    def ShowModal( self ):
        """
        Displays the dialog window and waits for the user to click OK or Cancel to return a value.

        :rtype: tuple or boolean
        :returns: The values for resolution and color level in a tuple if OK is clicked. Returns False otherwise.
        """
        wx.Dialog.ShowModal( self )
        if self.isOk:
            return ( self.resolutionValue, self.colorLevelValue )
        return False

    
