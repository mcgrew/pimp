"""
edge_detect.py
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

from extensions.lib.color import to_grey
from extensions.menu.invert import execute as invert

MENU = "Fil&ter.&Comic"
LABEL = "X-Ray"
DESCRIPTION = "I can see inside you..."


def execute(width, height, data):
    """
    Changes an image to greyscale and inverts the colors so as to make it
    appear more like an x-ray photo.

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
    return invert(*to_grey(width, height, data))
