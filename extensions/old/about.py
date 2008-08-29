"""
about.py
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

VERSION = "0.1"
ABOUT_DESCRIPTION = \
"""The Python Image Manipulation Project is an image processing
project primarily intended for image enhancement."""
LICENCE = \
"""The Python Image Manipulation Project is free software: you can
redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either
version 2 of the License, or (at your option) any later version."""

MENU = "&Help"
LABEL = "About"
DESCRIPTION = "About The PIMP"

def execute( *args ):
    
    aboutInfo = wx.AboutDialogInfo( )
    aboutInfo.setIcon( 'icon.png', wx.BITMAP_TYPE_PNG )
    aboutInfo.SetName( "The P.I.M.P" )
    aboutInfo.SetVersion( VERSION )
    aboutInfo.SetDescription( ABOUT_DESCRIPTION )
    aboutInfo.SetCopyright( "Copyright 2007 Thomas McGrew" )
    aboutInfo.setWebSite( "http://python.poundbang.org" )
    aboutInfo.setLicence( LICENCE )
    aboutInfo.AddDeveloper( "Thomas McGrew" )
    aboutInfo.AddDocWriter( "Thomas McGrew" )
    aboutInfo.AddArtist( "Thomas McGrew" )
    aboutInfo.AddTranslator( "Thomas McGrew" )
    
    wx.AboutBox( aboutInfo )

