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
import sys
import os
import wx
import wx.adv

# local imports
import editor

SPLASHSCREEN = True

class Splash(wx.adv.SplashScreen):
    """
    Create a splash screen widget.
    """
    def __init__(self, app, image):
        bitmap = wx.Image(name = image).ConvertToBitmap()
        self.app = app
        splash_style = wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT
        splash_length = 3000 # milliseconds
        wx.adv.SplashScreen.__init__(self, bitmap, splash_style, splash_length,
                parent=None)
        self.Bind(wx.EVT_CLOSE, self.onExit)

    def onExit(self, evt):
        self.Hide()
        self.app.SetTopWindow(self.app.frame)
        self.app.frame.Show(True)
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...
# =========================== END SPLASH SCREEN ================================

class App(wx.App):
    """
    wx.App subclass required by wxPython.
    """
    def OnInit(self):
        self.frame = editor.Frame()
        filename = None
        if len(sys.argv) >= 2 and os.path.exists(sys.argv[1]):
            filename = sys.argv[1]
        if SPLASHSCREEN and not filename:
            splash = Splash(self, "splash.bmp")
        else:
            self.frame.Show(True)
            if filename:
                self.frame.open_file(filename)
        return True

if __name__ == "__main__":
    g = App()
    g.MainLoop()
