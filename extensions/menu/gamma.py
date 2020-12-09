"""
gamma.py
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
from time import sleep
import wx

from extensions.lib.core import table

MENU = "&Filter"
LABEL = "Brightness levels"
DESCRIPTION = "Adjust brightness, contrast, and gamma"

           

def execute( width, height, data, brightness=None, contrast=None, gamma=None ):
    """
    Performs a gamma adjustment on an image. Brightness, contrast, and gamma
    are optional arguments. Either all 3 must be supplied, or none. A dialog
    will appear to request all 3 values if any of them are missing, in which
    case the passed in values are ignored.
        
    :Parameters:
        width : int
            The width of the image being converted
        height : int
            The height of the image being converted
        data : string
            A string containing the data for the image
        brightness : int
            The value of the change in brightness to apply.
        contrast : float
            The value of the change in contrast to apply.
        gamma : float
            The value of the change in gamma to apply.
    
    :rtype: tuple
    :returns: a tuple containing a width, height, and data as a binary string.
    """
    if ( None in ( gamma, brightness, contrast ) ):
        dialog = gammaDialog( )
        values = dialog.ShowModal( )
        
        if not values:
            return False
        
        gamma, brightness, contrast = values
    
    # build a substitution table
    substTable = list(range(256))
    
    for i in range( 256 ):
        substTable[ i ] = max( min( ( substTable[ i ] + brightness ), 255 ), 0 )
        substTable[ i ] = min( int( substTable[ i ] * contrast ), 255 )
        substTable[ i ] = min( int( substTable[ i ] ** gamma / 256 ** ( gamma-1 ) ), 255 )
        
    return table( width, height, data, substTable )




class gammaDialog( wx.Dialog ):
    """
    A class for getting input values from the user for the nintendize filter
    """
    def __init__( self, parent=None, id=-1, okFunction=None, sliderUpdateFunction=None, title="Brightness Adjust" ):
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
                The title of the dialog box to be displayed in the titlebar. Defaults to "Brightness Adjust".
        """
        wx.Dialog.__init__( self, None, -1, title, wx.DefaultPosition, ( 310, 110 ) )

        self.brightnessSlider = wx.Slider( self, -1, value = 0, minValue = -255, maxValue = 255, pos = ( 70, 10 ), size = ( 200, 20 ) )
        self.contrastSlider   = wx.Slider( self, -1, value = 1, minValue =  -90, maxValue =  91, pos = ( 70, 30 ), size = ( 200, 20 ) )
        self.gammaSlider      = wx.Slider( self, -1, value = 1, minValue =  -90, maxValue =  91, pos = ( 70, 50 ), size = ( 200, 20 ) )

        self.displayPanel = wx.Panel( self, -1, pos = ( 270, 10 ), size = ( 50, 100 ) )
        self.brightnessDisplay = wx.StaticText( self.displayPanel, pos = ( 0,  0 ) )
        self.contrastDisplay   = wx.StaticText( self.displayPanel, pos = ( 0, 20 ) )
        self.gammaDisplay      = wx.StaticText( self.displayPanel, pos = ( 0, 40 ) )

        self.labelPanel = wx.Panel( self, -1, pos = ( 0, 10 ), size = ( 70, 60 ) )
        self.brightnessLabel = wx.StaticText( self.labelPanel, pos = ( 0,  0 ), label="Brightness" )
        self.contrastLabel   = wx.StaticText( self.labelPanel, pos = ( 0, 20 ), label="Contrast"   )
        self.gammaLabel      = wx.StaticText( self.labelPanel, pos = ( 0, 40 ), label="Gamma"      )

        self.isOk = False
        okButton     = wx.Button( self, id = wx.ID_OK,     pos = (  60, 70 ), size = ( 80, 30 ) )
        cancelButton = wx.Button( self, id = wx.ID_CANCEL, pos = ( 160, 70 ), size = ( 80, 30 ) )

        if okFunction:
            self.okFunction = okFunction
        elif ( "onOk" in dir( self ) ):
            self.okFunction = self.onOk
        else:
            self.okFunction = lambda x,y,z: None
            
        if sliderUpdateFunction:
            self.sliderUpdateFunction = sliderUpdateFunction
        elif ( "onSliderupdate" in dir( self ) ):
            self.sliderUpdateFunction = self.onSliderupdate
        else:
            self.sliderUpdateFunction = lambda x,y,z: None
            
        self.gammaValue = 1
        self.brightnessValue = 0
        self.contrastValue = 1
        self.updateDisplay( )


        self.Bind( wx.EVT_SLIDER, self.sliderChange )
        self.Bind( wx.EVT_CLOSE, self.cancel )
        okButton.Bind( wx.EVT_BUTTON, self.ok )
        cancelButton.Bind( wx.EVT_BUTTON, self.cancel )
#        self.ShowModal( )

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
        self.okFunction( self.gammaValue, self.brightnessValue, self.contrastValue )
        self.isOk = True
        self.Destroy( )

    def sliderChange( self, event=None ):
        """
        Internal Function. Called when one of the sliders is changed within the dialog box.

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        if ( self.gammaSlider.GetValue( ) >= 1 ):
            self.gammaValue = float( self.gammaSlider.GetValue( ) + 9 ) / 10
        else:
            self.gammaValue = round( float( self.gammaSlider.GetValue( ) + 90 ) / 90, 2 )

        self.brightnessValue = self.brightnessSlider.GetValue( )

        if ( self.contrastSlider.GetValue( ) >= 1 ):
            self.contrastValue = float( self.contrastSlider.GetValue( ) + 9 ) / 10
        else:
            self.contrastValue = round( float( self.contrastSlider.GetValue( ) + 90 ) / 90, 2 )
        self.updateDisplay( )
        self.sliderUpdateFunction( self.gammaValue, self.brightnessValue, self.contrastValue )

    def updateDisplay( self ):
        """
        Internal Function. Called when one of the sliders is changed to update the values displayed.
        """
        self.gammaDisplay.SetLabel(      "%3.2f" % self.gammaValue      )
        self.brightnessDisplay.SetLabel( "%3d"   % self.brightnessValue )
        self.contrastDisplay.SetLabel(   "%3.2f" % self.contrastValue   )

    def ShowModal( self ):
        """
        Displays the dialog window and waits for the user to click OK or Cancel to return a value.

        :rtype: tuple or boolean
        :returns: The values for gamma, brightness, and contrast values in a tuple if OK is clicked. Returns False otherwise.
        """
        wx.Dialog.ShowModal( self )
        if self.isOk:
            return ( self.gammaValue, self.brightnessValue, self.contrastValue )
        return False


