"""
sepia.py
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

from extensions.lib.color import channelBrightness, toGrey
from extensions.lib.core  import table
from extensions.menu.gamma import execute as gamma

MENU = "&Image.&Color"
LABEL = "&Sepia Tone"
DESCRIPTION = "Convert this image to sepia tone"

def execute( width, height, data ):
    """
    Converts the colors in an image to resemble a sepia tone photograph.
    
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
    pass1 = toGrey( width, height, data )[ 2 ]
    pass2 = channelBrightness( width, height, pass1, ( 0, -18, -35 ) )[ 2 ]
    # now adjust the gamma
    return gamma( width, height, pass2, brightness=0, contrast=1.1, gamma=0.8 )
    