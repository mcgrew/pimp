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

from extensions.lib.core import spatial

MENU = "Fil&ter.&Smooth"
LABEL = "Gaussian"
DESCRIPTION = "Smooth Image"

FILTER = ( 2,  4,  5,  4,  2,
           4,  9, 12,  9,  4,
           5, 12, 15, 12,  5,
           4,  9, 12,  9,  4,
           2,  4,  5,  4,  2)

           

def execute( width, height, data ):
    """
    Smooths an image evenly on a 3x3 area.
        
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
    return spatial( width, height, data, FILTER )

