#!/usr/bin/python
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

# local imports
import editor

SPLASHSCREEN = True

# ========================================================= SPLASH SCREEN ====================================================================
class Splash(wx.SplashScreen):
    """
    Create a splash screen widget.
    """
    def __init__(self, app, image):
        aBitmap = wx.Image(name = image).ConvertToBitmap()
        self.app = app
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 3000 # milliseconds
        wx.SplashScreen.__init__(self, aBitmap, splashStyle, splashDuration, parent=None)
        self.Bind(wx.EVT_CLOSE, self.onExit)
        wx.Yield()

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


if __name__ == "__main__":
    g = App( )
    g.MainLoop( )

