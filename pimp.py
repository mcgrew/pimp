#!/usr/bin/env python3
"""
pimp.py
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

#library imports
import wx
import wx.adv

# local imports
import editor

SPLASHSCREEN = False

# ========================================================= SPLASH SCREEN ====================================================================
class Splash(wx.adv.SplashScreen):
    """
    Create a splash screen widget.
    """
    def __init__(self, app, image):
        aBitmap = wx.Image(name = image).ConvertToBitmap()
        self.app = app
        splashStyle = wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT
        splashDuration = 3000 # milliseconds
        wx.adv.SplashScreen.__init__(self, aBitmap, splashStyle, splashDuration, parent=None)
        self.Bind(wx.EVT_CLOSE, self.onExit)

    def onExit(self, evt):
        self.Hide()
        self.app.SetTopWindow(self.app.frame)
        self.app.frame.Show(True)
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...
# ======================================================= END SPLASH SCREEN ================================================================

class App( wx.App ):
    """
    wx.App subclass required by wxPython.
    """
    def OnInit( self ):
        self.frame = editor.Frame( )
        if SPLASHSCREEN:
            splash = Splash( self, "splash.bmp" )
        else:
            self.frame.Show( True )
        return True


class ObjNode( object ):
    """
    A generic Object node. It is designed to work similarly to a javascript object.
    It's intended use is to create a heirarchy of objects
    """
    def __init__( self, value=None ):
        object.__init__( self )
        self.__dict__[ "value" ] = value

    def __setattr__( self, attr, value ):
        if ( attr[ 0 ] == '_' ):
            self.__dict__[ attr ] = value
        elif self.__dict__.has_key( attr ):
            self.__dict__[ attr ].__dict__[ "value" ] = value
        else:
            self.__dict__[ attr ] = ObjNode( value )

    def __getattr__( self, attr ):
        if self.__dict__.has_key( attr ):
            return self.__dict__[ attr ]
        elif attr in dir( self.value ):
            return eval( "self.value."+attr )
        else:
            return None

    def __call__( self, *args ):
        self.value( args )



if __name__ == "__main__":
    g = App( )
    g.MainLoop( )

