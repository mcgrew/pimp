"""
image.py
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

# import the core methods from the shared object file
from extensions.lib.cCore import *

from wx import Image, Bitmap, EmptyImage


def dataToBitmap( width, height, data ):
    """
    Converts data to a wx.Bitmap.

    :Parameters:
        width : int
            The width of the image (in pixels).
        height : int
            The height of the image (in pixels).
        data : string
            The image as a string of bytes.
    
    :rtype: wx.Bitmap
    :returns: a wx.Bitmap containing the image data.
    """
    
    image = Image( width, height )
    image.SetData( toRGB( width, height, bytes(data) )[ 2 ] )
    return image.ConvertToBitmap( )
    

