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

VERSION = "0.1"

from extensions.lib.core import stringCopy

class Image:
    """
    A class for storing image data.
    """
    def __init__( self, width, height, data='' ):
        """
        Creates an Image object.

        :Parameters:
            width : int
                The width of the image
            height : int
                The height of the image in pixels
            data : string
                The optional data for this image formatted as a string containing binary data
        """
        self._width = width
        self._height = height
        self._data = data
        if len( data ):
            self._channels = len( data ) // ( width * height )
            if not ( self._channels in ( 3, 4 ) ):
                raise ValueError( "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )"
                                    % self._channels, width, height, len( data ) )
        else:
            self._channels = 3
            data = '\x00' * ( width * height * 3 ) # create a pure black image.

    def copy( self ):
        """
        Returns a copy of this image.

        :rtype: Image
        :returns: a copy of this image.
        """
        return Image( self.getWidth( ), self.getHeight( ), stringCopy( self.getData( ) ) )
        
    def hasAlpha( self ):
        """
        4 channel images have an alpha channel (RGBA).

        :rtype: bool
        :returns: True if the image has an alpha channel, false otherwise.
        """
        return ( self._channels == 4 )

    def getAlpha( self ):
        """
        Get the alpha channel for this image.

        :rtype: str or bool
        :returns: A string containing only the alpha channel data for this image, or False if it does not contain one.
        """
        if not self.hasAlpha( ):
            return False
        return self._data[ ::4 ]

    def getData( self ):
        """
        Get the binary data for this image.

        :rtype: str
        :returns: All channel data for this image as a string.
        """
        return self._data

    def getBlue( self ):
        """
        Get the blue channel data

        :rtype: string
        :returns: The blue channel data for this image as a string
        """
        return self._data[ 2::self._channels ]

    def getGreen( self ):
        """
        Get the green channel data.

        :rtype: string
        :returns: The green channel data for this image as a string
        """
        return self._data[ 1::self._channels ]

    def getRed( self ):
        """
        Get the red channel data.

        :rtype: string
        :returns: The red channel data for this image as a string
        """
        return self._data[  ::self._channels ]

    def getHeight( self ):
        """
        Get the height of the image.

        :rtype: int
        :returns: The image height in pixels.
        """
        return self._height

    def getWidth( self ):
        """
        Get the width of the image.

        :rtype: int
        :returns: The image width in pixels.
        """
        return self._width

    def getSize( self ):
        """
        Get the image size.

        :rtype: tuple
        :returns: A tuple containing the width and height of the image in pixels.
        """
        return ( self._width, self._height )

    def setData( self, data ):
        """
        Set the data for this image.

        :rtype: bool
        :returns: True if the operation succeeded.
        """
        if not ( len( data ) // ( width * height ) in ( 3, 4 ) ):
            raise ValueError( "The data buffer for this image is the incorrect length. Must be either width * height or width * height * 3" )
        self._data = data
        return True


