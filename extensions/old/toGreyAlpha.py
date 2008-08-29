"""
toGreyAlpha.py
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


#MENU = "&Image.&Mode"
#LABEL = "Grey/Alpha"
#DESCRIPTION = "Convert the image to greyscale with an alpha channel"

def execute( width, height, data ):
    
    channels = len( data ) / ( width * height )

    if ( channels == 2 ):
        return ( width, height, data )

    data = [ ord( c ) for c in data ]

    if channels == 1:
        for i in range( width * height ):
            newdata[ i*2 ] = chr( ord( data[ i*channels ] ) )


    newdata = [ 0 ] * ( width * height * 2 )

    if channels >= 3:
        for i in range( width * height ):
            newdata[ i*2 ] = chr( ( ord( data[ i*channels ] ) + ord( data[ i*channels+1 ] ) + ord( data[ i*channels+2 ] ) ) / 3 )

    data = [ chr( min( i, 255 ) ) for i in newdata ]

    data = ''.join( data )


    return ( width, height, data )
    
