"""
LayeredImage.py
(c) 2007 Thomas McGrew

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

import wx.Image

class LayeredImage:
    """
    An Image class for wx that handles Layers.
    """
    def __init__( self, master, ... ):
        self.Layers = list( )
        self.LayerOffset = list ( )
        self.ActiveLayer = 0
        
    def Blur( self, radius ):
        """
        Blurs the image in both horizontal and vertical directions by the specified pixel radius.

        :Parameters:
            radius : int
                The radius to be used for the blur in pixels.

        :rtype: LayeredImage
        :returns: A blurred version of this image.
        """
        returnvalue = LayeredImage( )
        for Layer in Layers:
            returnvalue.AddLayer( Layer.Blur( radius ) )
        return returnvalue

    def BlurHorizontal( self, radius ):
        """
        Blurs the image in the horizontal direction only.

        :Parameters:
            radius : int
                The radus to be used for the blur in pixels.
                
        :rtype: LayeredImage
        :returns: A blurred version of this image.
        """
        returnvalue = LayeredImage( )
        for Layer in Layers:
            returnvalue.AddLayer( Layer.BlurHorizontal( radius ) )
        return returnvalue

    def BlurVertical( self, radius ):
        """
        Blurs the image in the vertical direction only.

        :Parameters:
            radius : int
                The radius to use for the blur in pixels.

        :rtype: LayeredImage
        :returns: A blurred version of this image.
        """
        returnvalue = LayeredImage( )
        for Layer in Layers:
            returnvalue.AddLayer( Layer.BlurHorizontal( radius ) )
        return returnvalue

    def ComputeHistogram( self, h ):
        """
        :Parameters:
            h :
        """
        pass

    def ConvertAlphatoMask( self, threshold ):
        """
        If the Layers have an alpha channel, this method converts it to a mask.

        :Parameters:
            threshold : int
                The maximum alpha value to convert to a masked pixel

        :rtype: bool
        :returns: True if the operation succeeded.
        """
        returnvalue = False
        for Layer in Layers:
            if Layer.ConvertAlphatoMask( threshold ):
                returnvalue = True
        return returnvalue

    def ConvertColourToAlpha( self, r, g, b ):
        """
        This method converts an image where the original alpha information is only
        available as shades of a color (actually shades of grey), typically when
        you draw anti-aliased text into a bitmap.

        :Parameters:
            r : int
                The value of red in pixels to be converted to alpha
            g : int
                The value of green in pixels to be converted to alpha
            b : int
                The value of blue in pixels to be converted to alpha

        :rtype: bool
        :returns: True if the operation succeeded.
        """
        returnvalue = False
        for Layer in Layers:
            if Layer.ConvertColourToAlpha( r, g, b ):
                returnvalue = True
        return returnvalue

    def ConvertToBitmap( self, depth ):
        """
        Flattens the image and returns it as a wx.Bitmap

        :Parameters:
            depth : int
                The color depth of the bitmap image to be returned.

        :rtype: wx.Bitmap
        :returns: A Bitmap version of the flattened image.
        """
        return self.Flatten.ConvertToBitmap( depth )

    def ConvertToGreyscale( self, lr, lg, lb ):
        """
        Convert to Greyscale image.
        :Parameters:
            lr :
            lg :
            lb :

        :rtype: LayeredImage
        :returns: A greyscale version of this image.
        """
        returnvalue = LayeredImage( )
        for Layer in Layers:
            returnvalue.AddLayer( Layer.ConvertToGreyscale( lr, lg, lb ) )
        return returnvalue

    def ConvertToMono( self, r, g, b ):
        """
        Convert to monochromatic image

        :Parameters:
            r :
            g :
            b :

        :rtype: LayeredImage
        :returns: A Monochromatic version of this image
        """
        returnvalue = LayeredImage( )
        for Layer in Layers:
            returnvalue.AddLayer( Layer.ConvertToMono( r, g, b ) )
        return returnvalue

    def ConvertToMonoBitmap( self, r, g, b ):
        """
        Converto to monochromatic Bitmap image

        :Parameters:
            r :
            b :
            g :

        :rtype: wx.Bitmap
        :returns: A monocromatic Bitmap version of this image.
        """
        return self.Flatten.ConvertToMonoBitmap( r, g, b )

    def Copy( self ):
        """
        Get a copy.

        :rtype: LayeredImage
        :returns: A Layered version of this image.
        """
        returnvalue = LayeredImage( )
        for Layer in Layers:
            returnvalue.AddLayer( Layer.Copy( ) )
        return returnvalue

    def CountColours( self, *args, **kwargs ):
        """
        """
        pass

    def Destroy( self ):
        """
        Destroys the image data.
        """
        for Layer in Layers:
            Layer.Destroy( )
        self.Layers = list( )

    def FindFirstUnusedColour( startR, startG, startB ):
        """
        Find the first color this is not used in the image and has higher RGB values than startR, startG, startB

        :Parameters:
            startR : int
                The red value to start with
            startG : int
                The green value to start with
            startB : int
                The blue value to start with.

        :rtype: tuple
        :returns: a tuple containing a boolean value for success or failure, followed by the r, g, b values of the color.
        """
        r, g, b = startR, startG, startB
        for Layer in Layers:
            success, r, g, b = Layer.FindFirstUnusedColor( r, g, b ):
            if not success:
                break
        return ( success, r, g, b )

    def Flatten( self ):
        """
        Flatten the image

        :rtype: wx.Image
        :returns: A flattened version of this image.
        """
        pass

    def GetAlpha( self, x, y ):
        """
        Get the alpha value for the given pixel in the active layer.

        :Parameters:
            x : int
                The x coordinate of the pixel to retrieve
            y : int
                The y coordinate of the pixel to retrieve
        """
        return self.Layers[ self.ActiveLayer ].GetAlpha( x, y )

    def GetAlphaBuffer( self ):
        pass

    def GetAlphaData( self ):
        pass

    def GetBlue( self, x, y ):
        pass

    def GetData( self ):
        pass

    def GetDataBuffer( self ):
        pass

