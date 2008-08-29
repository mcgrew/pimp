static char __doc__[ ] =
"color.c\n\
Copyright 2007 Thomas McGrew\n\
\n\
This file is part of The Python Image Manipulation Project.\n\
\n\
The Python Image Manipulation Project is free software: you can\n\
redistribute it and/or modify it under the terms of the GNU General\n\
Public License as published by the Free Software Foundation, either\n\
version 2 of the License, or (at your option) any later version.\n\
\n\
The Python Image Manipulation Project is distributed in the hope\n\
that it will be useful, but WITHOUT ANY WARRANTY; without even the\n\
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR\n\
PURPOSE. See the GNU General Public License for more details.\n\
\n\
You should have received a copy of the GNU General Public License\n\
along with The Python Image Manipulation Project.  If not, see\n\
<http://www.gnu.org/licenses/>.\n\
";

#include <Python.h>
#include "core.h"

static char toGrey__doc__[  ] =
    "Converts image data to 1 channel greyscale format.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image being converted\n\
        height : int\n\
            The height of the image being converted\n\
        data : string\n\
            A string containing the data for the image\n\
    \n\
    :rtype: tuple\n\
    :returns: a tuple containing a width, height, and data as a string\n\
    ";

PyObject *toGrey( PyObject *pself, PyObject *pArgs )
{
    unsigned int width, height, i;
    unsigned int dataLen;
    unsigned char *data, channels;

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#", &width, &height, &data, &dataLen ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
        PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
        return NULL;
    }

    // set each channel the pixel's average
    for ( i=0; i < dataLen; i+=channels )
    {
        data[ i ] = data[ i+1 ] = data[ i+2 ] = ( data[ i ] + data[ i+1 ] + data[ i+2 ] ) / 3;
    }

    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, data, dataLen );
}


static char transform__doc__[  ] =
    "Transforms colors in an image based on float values passed in.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image being converted\n\
        height : int\n\
            The height of the image being converted\n\
        data : string\n\
            A string containing the data for the image\n\
        transform : tuple\n\
            The transform to be applied. Should be a tuple containing 9 values, 3 for each color.\n\
            red   = red * t[0] + green * t[1] + blue  * t[2]\n\
            green = red * t[3] + green * t[4] + blue  * t[5]\n\
            blue  = red * t[6] + green * t[7] + blue  * t[8]\n\
    \n\
    :rtype: tuple\n\
    :returns: a tuple containing a width, height, and data as a string\n\
    ";

PyObject *transform( PyObject *pself, PyObject *pArgs )
{
    unsigned int width, height, i;
    unsigned int dataLen;
    unsigned char *data, channels;
    pixel3 p3;
    float rr, rg, rb, gr, gg, gb, br, bg, bb; // float values used to transform the color.

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#(fffffffff)", &width, &height, &data, &dataLen, &rr, &rg, &rb, &gr, &gg, &gb, &br, &bg, &bb ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
        PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
        return NULL;
    }

    // multiply each pixel by the transform values.
    for ( i=0; i < dataLen; i+=channels )
    {
        p3.red = data[ i ]; p3.green = data[ i+1 ]; p3.blue = data[ i+2 ];

        data[ i   ] = clip( ( int )( p3.red * rr + p3.green * rg + p3.blue * rb ) );
        data[ i+1 ] = clip( ( int )( p3.red * gr + p3.green * gg + p3.blue * gb ) );
        data[ i+2 ] = clip( ( int )( p3.red * br + p3.green * bg + p3.blue * bb ) );

    }

    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, data, dataLen );
}

static char channelBrightness__doc__[  ] =
    "Changes the brightness of individual channels in an image.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image being converted\n\
        height : int\n\
            The height of the image being converted\n\
        data : string\n\
            A string containing the data for the image\n\
    \n\
    :rtype: tuple\n\
    :returns: a tuple containing a width, height, and data as a string\n\
    ";

PyObject *channelBrightness( PyObject *pself, PyObject *pArgs )
{
    unsigned int width, height, i;
    unsigned int dataLen;
    unsigned char *data, channels;
    int r, g, b;


    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#(iii)", &width, &height, &data, &dataLen, &r, &g, &b ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
        PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
        return NULL;
    }

    for ( i=0; i < dataLen; i+=channels )
    {
        data[ i   ] = clip( data[ i   ] + r );
        data[ i+1 ] = clip( data[ i+1 ] + g );
        data[ i+2 ] = clip( data[ i+2 ] + b );
    }

    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, data, dataLen );
}

static char pseudocolor__doc__[  ] =
    "Transforms colors in an image based on float values passed in.\n\
    The data in the image will be replaced with the 16 pixels based\n\
    on intensity of each pixel in the image. The lowest intensities\n\
    will be replaced with first pixels, the highest intensities with\n\
    the last.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image being converted\n\
        height : int\n\
            The height of the image being converted\n\
        data : string\n\
            A string containing the data for the image\n\
        p3 : string\n\
            A string containing data for 16 pixels to be used for replacement.\n\
    \n\
    :rtype: tuple\n\
    :returns: a tuple containing a width, height, and data as a string\n\
    ";

PyObject *pseudocolor( PyObject *pself, PyObject *pArgs )
{
    unsigned int width, height, i;
    unsigned int dataLen, p3Len;
    unsigned char *data, channels;
    pixel3 *p3, thisPixel;


    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#s#", &width, &height, &data, &dataLen, ( char** )&p3, &p3Len ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
        PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
        return NULL;
    }

    if ( p3Len != 48 )
    {
        PyErr_Format( PyExc_ValueError, "Replacement data contained an invalid number of colors, 16 expected, %d recieved", p3Len/3 );
        return NULL;
    }

    for ( i=0; i < dataLen; i+=channels )
    {
        // pick the appropriate replacement based on the first 3 bits of the greyscale value of this pixel.
        thisPixel = p3[ ( ( ( data[ i ] + data[ i+1 ] + data[ i+2 ] ) / 3 ) >> 4 ) ];
        data[ i   ] = thisPixel.red;
        data[ i+1 ] = thisPixel.green;
        data[ i+2 ] = thisPixel.blue;
    }

    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, data, dataLen );
}


static PyMethodDef core_methods[ ] =
{
//  format is as follows:
//  { "python_name"       , c_name            , arg_method  , doc_string               },
    { "toGrey"            , toGrey            , METH_VARARGS, toGrey__doc__            },
    { "transform"         , transform         , METH_VARARGS, transform__doc__         },
    { "channelBrightness" , channelBrightness , METH_VARARGS, channelBrightness__doc__ },
    { "pseudocolor"       , pseudocolor       , METH_VARARGS, pseudocolor__doc__       },
    { NULL, NULL } // End of functions
};

PyMODINIT_FUNC initcolor( void )
{
    ( void )Py_InitModule3( "color", core_methods, __doc__ );
}

