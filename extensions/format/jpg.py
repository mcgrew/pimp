"""
jpg.py
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

# I'm taking the easy way out for now in this one.

from wx import Image, BITMAP_TYPE_JPEG
from extensions.lib.core import to_rgb

# register the extension(s) for this to read
FILE_EXTENSION = ("jpg", "jpeg")
# register the file marker for this format (beginning of the file data)
FILE_MARKER = b"\xff\xe0"
# description of this format
DESCRIPTION = "Jpeg Format"

def read( filename ):
    """
    Reads a jpeg file.

    :Parameters:
        filename : string
            the name of the file to be read.

    :rtype: tuple
    :returns: A tuple (width, height, data). Width and height are in pixels,
        data is a string containing chr(red) + chr(green) + chr(blue) for each
        pixel.
    """
    image = Image(name = filename)
    return (image.GetWidth(), image.GetHeight(), image.GetData())



def write(filename, width, height, data):
    """
    Writes data out to a jpeg file.

    :Parameters:
        filename : string
            The name of the file to write to.
        width : int
            The width of the image in pixels
        height : int
            The height of the image in pixels
        data : string
            The data as a string.

    :rtype: boolean
    :returns: True on success
    """
    data = to_rgb(width, height, data)[2]
    image = Image(width, height)
    image.SetData(data)
    image.SaveFile(name = filename, type = BITMAP_TYPE_JPEG)
    return True
