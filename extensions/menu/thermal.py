"""
thermal.py
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

from extensions.lib.color import pseudocolor

MENU = "Fil&ter.&Comic"
LABEL = "&Thermal Image"
DESCRIPTION = "Some like it hot!"

COLORS = b'\x00\x00\x00' * 2 + b'\x80\x00\xff' * 2 + \
         b'\x00\x00\xff' * 2 + b'\x00\xff\xff' * 2 + \
         b'\x00\xff\x00' * 2 + b'\xff\xff\x00' * 2 + \
         b'\xff\x80\x00' * 2 + b'\xff\x00\x00' * 2

def execute( width, height, data ):
    """
    Converts an image to a "thermal" image. It resembles an image
    taken by a thermal camera.
    
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
    return pseudocolor( width, height, data, COLORS )
    
