"""
bmp.py
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


This extension currently only supports the reading of 4 and 24-bit bitmaps
and the writing of 24-bit bitmaps. Other formats are planned for later implementation.

Bitmap Header Information:

Generic Header
offset  length   purpose
0       2       Store the magic number used to identify the bitmap file. Typical values for these 2 bytes are 0x42 0x4D (ASCII code points for B and M).
2       4       Store the size of the bitmap file using a dword.
6       2       Reserved. Actual value depends on the application that creates the image.
8       2       Reserved. Actual value depends on the application that creates the image.
10      4       Store the offset, i.e. starting address, of the byte where the bitmap data can be found.

OS/2 V1 header:
offset  length  purpose
14      4       Size of this header (12 bytes)
18      2       Store the bitmap width in pixels.
20      2       Store the bitmap height in pixels.
22      2       Store the number of color planes being used.
24      2       Store the number of bits per pixel. Typical values are 1, 4, 8 and 24.

Windows V3 header:
offset  length  purpose
14      4       Size of this header (40 bytes)
18      4       Store the bitmap width in pixels.
22      4       Store the bitmap height in pixels.
26      2       Store the number of color planes being used. Not often used. Typical value is 1.
28      2       Store the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
30      4       Define the compression method being used. See the next table for a list of possible values.
34      4       Store the image size. This is the size of the raw bitmap data (see below), and should not be confused with the file size.
38      4       Store the horizontal resolution of the image. (pixels per meter). Typical value is 3937.
42      4       Store the vertical resolution of the image. (pixels per meter). Typical value is 3937.
46      4       Store the number of colors used.
50      4       Store the number of important colors used. This field can be 0 when every color is important.

Compression Methods (not currently supported)
number  type              comments
0       none              Most common
1       RLE 8-bit/pixel   Can be used only with 8-bit/pixel bitmaps
2       RLE 4-bit/pixel   Can be used only with 4-bit/pixel bitmaps
3       Bit field         Can be used only with 16 and 32-bit/pixel bitmaps.
4       JPEG              The bitmap contains a JPEG image
5       PNG               The bitmap contains a PNG image
"""

#library imports
import struct

# local imports
from wx import Image, BITMAP_TYPE_BMP
from extensions.lib.core import toRGB

# register the extension(s) for this to read
FILE_EXTENSION = "bmp"
# register the file marker for this format ( beginning of the file data )
FILE_MARKER = b"BM"
# description of this format
DESCRIPTION = "Windows Bitmap Format"

def read(filename):
    """
    Reads a bitmap file.

    :Parameters:
        filename : string
            the name of the file to be read.

    :rtype: tuple
    :returns: A tuple ( width, height, data ). Width and height are in pixels, data is a string containing chr(red) + chr(green) + chr(blue) for each pixel.
    """
    image = Image(name = filename)
    return (image.GetWidth(), image.GetHeight(),image.GetData())



def write(filename, width, height, data):
    """
    Writes data out to a bitmap file.

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
    data = toRGB(width, height, data)[2]
    image = Image(width, height)
    image.SetData(data)
    image.SaveFile(name = filename, type = BITMAP_TYPE_BMP)
    return True
