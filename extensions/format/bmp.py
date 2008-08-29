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
from extensions.lib.core import swapChannels

# register the extension(s) for this to read
FILE_EXTENSION = "bmp"
# register the file marker for this format ( beginning of the file data )
FILE_MARKER = "BM"
# description of this format
DESCRIPTION = "Windows Bitmap Format"

def read( filename ):
    """
    Reads a windows bitmap file.

    :Parameters:
        filename : string
            the name of the file to be read.

    :rtype: tuple
    :returns: A tuple ( width, height, data ). Width and height are in pixels, data is a string containing chr(red) + chr(green) + chr(blue) for each pixel.
    """
    imageData = str( )
    imageFile = open( filename, 'rb' )
    #=========================== READ THE FILE HEADER ========================================    
    fileHeader = imageFile.read( 14 )
    if ( fileHeader[ :2 ] != 'BM' ):
        log( "Warning: Incorrectly formatted bitmap file" )
    dataAddress = struct.unpack( 'I', fileHeader[ 10: ] )[ 0 ]
    infoHeader = imageFile.read( dataAddress - 14 )
    infoHeaderSize = struct.unpack( 'I', infoHeader[ :4 ] )[ 0 ]

    #============================ READ THE INFOHEADER ==========================================    
    if ( infoHeaderSize == 24 ): # OS/2 V1 Header
        width, height, colorPlanes, bpp = struct.unpack( "HHHH", infoHeader[ 4:12 ] )
        
    elif ( infoHeaderSize == 40 ): # Windows V3 Header
        width, height, colorPlanes, bpp, compression = struct.unpack( 'IIHHI', infoHeader[ 4:20 ] )
        
    else:
        imageFile.close( )
        raise ImageFormatError( "Unable to parse header information" )
    #========================================================================================
    
    if compression:
        imageFile.close( )
        raise ImageReadError( "Compressed bitmap images are not currently supported" )

    if bpp == 4:
        # 16 colors are reserved for this depth of images. The following are the 20 reserved
        # Windows colors. The 4 commented out are omitted from this palette.
        colors = {   0: "\x00\x00\x00",   1: "\x80\x00\x00",   2: "\x00\x80\x00",   3: "\x80\x80\x00",
                     4: "\x00\x00\x80",   5: "\x80\x00\x80",   6: "\x00\x80\x80",   7: "\xc0\xc0\xc0",
                     #8: "\xc0\xdc\xc0",   9: "\xa6\xca\xf0", 246: "\xff\xfb\xf0", 247: "\xa0\xa0\xa4",
                   248: "\x80\x80\x80", 249: "\xff\x00\x00", 250: "\x00\xff\x00", 251: "\xff\xff\x00",
                   252: "\x00\x00\xff", 253: "\x00\xff\xff", 254: "\x00\xff\xff", 255: "\xff\xff\xff" }
        palette = colors.values( )

        data = imageFile.read( )
        try:
            translatedData = str( )
            for i in range( len( data ) ):
                pixels = ord( data[ i ] )
                translatedData += palette[ pixels >> 4 ] + palette[ pixels & 0xf ]
            imageData = [ translatedData[ i*width*3 : (i+1)*width*3 ] for i in range( height ) ]
            imageData.reverse( )
            imageData = ''.join( imageData )
        except IndexError:
            raise ImageReadError( "This image appears to be corrupted." )

    elif bpp == 24:
        eof = width * height * 3
        while ( len( imageData ) < eof ):
            data = imageFile.read( width * 3 )
            #throw away the extra \0 padding at the end of a line (if any)
            padding = ( -width * 3 ) % 4
            if padding:
                imageFile.seek( imageFile.tell( ) + padding )
            imageData = data + imageData
        # swap the red and blue channels, the channels are stored in reverse order
        # from what we need in the file
        imageData = swapChannels( width, height, imageData, 0, 2 )[ 2 ]
    else:
        imageFile.close( )
        raise ImageFormatError( "Images of %d bpp are not supported" % depth )
    imageFile.close( )

    return ( width, height, imageData )



def write( filename, width, height, data ):
    """
    Writes data out to a windows bitmap file.

    :Parameters:
        filename : string
            The name of the file to write to.
        width : int
            The width of the image in pixels
        height : int
            The height of the image in pixels
        data : string
            The data as a binary string.

    :rtype: boolean
    :returns: True on success
    """
    bpp = 24

    if bpp == 4:
        # 16 colors are reserved for this depth of images.
        colors = { "\x00\x00\x00": 0, "\x80\x00\x00": 1, "\x00\x80\x00": 2, "\x80\x80\x00": 3,
                   "\x00\x00\x80": 4, "\x80\x00\x80": 5, "\x00\x80\x80": 6, "\xc0\xc0\xc0": 7,
                   "\x80\x80\x80": 8, "\xff\x00\x00": 9, "\x00\xff\x00":10, "\xff\xff\x00":11,
                   "\x00\x00\xff":12, "\x00\xff\xff":13, "\x00\xff\xff":14, "\xff\xff\xff":15 }
        
        data = [ data[ i*width*3 : (i+1)*width*3 ] for i in range( height ) ]
        data.reverse( ) #reverse the bytes ( they are stored this way in bmp format )
        rawdata = ''.join( data )
        # I'm not sure of the easiest way to transform the raw data into the format I need here.
        # Color #7 is causing the problem, otherwise I could just bitmask it with 0xc0.
        # If I do that, I won't be able to tell the difference between 0xff and 0xc0.
        
    
    if bpp == 24:
        #swap the red and blue channels to make it easier to write this format
        data = swapChannels( width, height, data, 0, 2 )[ 2 ]
        
        # split data into a list of rows
        data = [ data[ i*width*3 : (i+1)*width*3 ] for i in range( height ) ]
        padding = "\x00" * ( ( -width * 3 ) % 4 ) # make each row an even multiple of 4.
        data.reverse( ) #reverse the bytes ( they are stored this way in bmp format )
        bmpdata = padding.join( data )
            
    # create the header (Windows V3)
    filesize = len( bmpdata ) + 54
    header = "BM"

    header += struct.pack( "IHHI", filesize, 0, 0, 54 ) # The main file header

    header += struct.pack( "IIIHHIIIIII", 40, width, height, 1, bpp, 0, len( bmpdata ), 3937, 3937, 0, 0 ) # Windows V3 header

    imageFile = open( filename, 'wb' )
    imageFile.write( header + bmpdata )
    imageFile.close( )
    return True
