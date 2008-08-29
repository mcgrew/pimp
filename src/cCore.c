static char __doc__[ ] =
"cCore.c\n\
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
\n\
All of the methods in this module can be called using extensions.lib.core\n\
instead of cCore. All functions in this module are imported by that one.\n\
";

#include <Python.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "core.h"

static char stringCopy__doc__[ ] =
    "Makes a real copy of a string. This can only be accomplished through tricks in pure python.\n\
    \n\
    :Parameters:\n\
        indata : string\n\
            The string to be copied.\n\
    \n\
    :rtype: string\n\
    :returns: A real copy of the string so the original data cannot be changed by C extensions.\n\
    ";

PyObject *stringCopy( PyObject *pself, PyObject *pArgs )
{
    char *data, *outData;
    unsigned int dataLen;
    
    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "s#", &data, &dataLen ) )
        return NULL;

    if( !( outData = malloc( dataLen ) ) )
    {
         PyErr_SetString( PyExc_MemoryError, "Memory could not be allocated to copy the string" );
         return NULL;
    }

    memcpy( outData, data, dataLen );

    // Build a python string and return it.
    return Py_BuildValue( "s#",outData, dataLen );


}

//doc string
static char swapChannels__doc__[ ] =
    "Swaps one channel with another in an image. The channels are numbered as follows:\n\
    0. Red\n\
    1. Green\n\
    2. Blue\n\
    3. Alpha (if present)\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image in pixels\n\
        height : int\n\
            The height of the image in pixels\n\
        data : string\n\
            The data as a binary string.\n\
        channel1 : int\n\
            The first of the 2 channels to swap\n\
        channel2 : int\n\
            The second of the 2 channels to swap\n\
    \n\
    :rtype: string\n\
    :returns: The new data as a string.\n\
    ";

PyObject *swapChannels( PyObject *pself, PyObject *pArgs )
{
    int width, height, channel1, channel2, channels, i;
    char *data, tmp;
    Py_ssize_t dataLen;

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#ii", &width, &height, &data, &dataLen, &channel1, &channel2 ) )
        return NULL;

    channels = dataLen / ( width * height );
    
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }
    
    if( ( channel1 < 0 ) || ( channel2 < 0 ) )
    {
         PyErr_SetString( PyExc_IndexError, "Negative values for channel number are not valid" );
         return NULL;
    }

    if( ( channel1 > channels ) || ( channel2 > channels ) )
    {
         PyErr_Format( PyExc_IndexError, "This channel contains only %d channels", channels );
         return NULL;
    }

    for ( i=0; i < dataLen; i+=channels )
    {
        tmp = data[ i+channel1 ];
        data[ i+channel1 ] = data[ i+channel2 ];
        data[ i+channel2 ] = tmp;
    }

    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, data, dataLen );
}


// doc string
static char table__doc__[ ] =
    "Replaces the data in an image based on a substitution table. The table should\n\
    contain 256 values, each containing the value to be substituted. It is treated as a\n\
    lookup table; a value of 205 will be replaced with whatever is at index 205 in the table,\n\
    and so forth.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image in pixels\n\
        height : int\n\
            The height of the image in pixels\n\
        data : string\n\
            The data as a binary string.\n\
        sub_table : tuple\n\
            A tuple containg 256 integer values used for substitution.\n\
    \n\
    :rtype: tuple\n\
    :returns: A tuple ( width, height, data ). Width and height are in pixels, data is a string containing the binary data.\n\
    ";

PyObject *table( PyObject *pself, PyObject *pArgs )
{
    unsigned char *data;
    unsigned int width, height;
    unsigned int dataLen;
    int channels;

    unsigned int i, sub_table[ 256 ];

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#(iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii)", &width, &height, &data, &dataLen,
        &sub_table[   0 ], &sub_table[   1 ], &sub_table[   2 ], &sub_table[   3 ], &sub_table[   4 ], &sub_table[   5 ], &sub_table[   6 ], &sub_table[   7 ],
        &sub_table[   8 ], &sub_table[   9 ], &sub_table[  10 ], &sub_table[  11 ], &sub_table[  12 ], &sub_table[  13 ], &sub_table[  14 ], &sub_table[  15 ],
        &sub_table[  16 ], &sub_table[  17 ], &sub_table[  18 ], &sub_table[  19 ], &sub_table[  20 ], &sub_table[  21 ], &sub_table[  22 ], &sub_table[  23 ],
        &sub_table[  24 ], &sub_table[  25 ], &sub_table[  26 ], &sub_table[  27 ], &sub_table[  28 ], &sub_table[  29 ], &sub_table[  30 ], &sub_table[  31 ],
        &sub_table[  32 ], &sub_table[  33 ], &sub_table[  34 ], &sub_table[  35 ], &sub_table[  36 ], &sub_table[  37 ], &sub_table[  38 ], &sub_table[  39 ],
        &sub_table[  40 ], &sub_table[  41 ], &sub_table[  42 ], &sub_table[  43 ], &sub_table[  44 ], &sub_table[  45 ], &sub_table[  46 ], &sub_table[  47 ],
        &sub_table[  48 ], &sub_table[  49 ], &sub_table[  50 ], &sub_table[  51 ], &sub_table[  52 ], &sub_table[  53 ], &sub_table[  54 ], &sub_table[  55 ],
        &sub_table[  56 ], &sub_table[  57 ], &sub_table[  58 ], &sub_table[  59 ], &sub_table[  60 ], &sub_table[  61 ], &sub_table[  62 ], &sub_table[  63 ],
        &sub_table[  64 ], &sub_table[  65 ], &sub_table[  66 ], &sub_table[  67 ], &sub_table[  68 ], &sub_table[  69 ], &sub_table[  70 ], &sub_table[  71 ],
        &sub_table[  72 ], &sub_table[  73 ], &sub_table[  74 ], &sub_table[  75 ], &sub_table[  76 ], &sub_table[  77 ], &sub_table[  78 ], &sub_table[  79 ],
        &sub_table[  80 ], &sub_table[  81 ], &sub_table[  82 ], &sub_table[  83 ], &sub_table[  84 ], &sub_table[  85 ], &sub_table[  86 ], &sub_table[  87 ],
        &sub_table[  88 ], &sub_table[  89 ], &sub_table[  90 ], &sub_table[  91 ], &sub_table[  92 ], &sub_table[  93 ], &sub_table[  94 ], &sub_table[  95 ],
        &sub_table[  96 ], &sub_table[  97 ], &sub_table[  98 ], &sub_table[  99 ], &sub_table[ 100 ], &sub_table[ 101 ], &sub_table[ 102 ], &sub_table[ 103 ],
        &sub_table[ 104 ], &sub_table[ 105 ], &sub_table[ 106 ], &sub_table[ 107 ], &sub_table[ 108 ], &sub_table[ 109 ], &sub_table[ 110 ], &sub_table[ 111 ],
        &sub_table[ 112 ], &sub_table[ 113 ], &sub_table[ 114 ], &sub_table[ 115 ], &sub_table[ 116 ], &sub_table[ 117 ], &sub_table[ 118 ], &sub_table[ 119 ],
        &sub_table[ 120 ], &sub_table[ 121 ], &sub_table[ 122 ], &sub_table[ 123 ], &sub_table[ 124 ], &sub_table[ 125 ], &sub_table[ 126 ], &sub_table[ 127 ],
        &sub_table[ 128 ], &sub_table[ 129 ], &sub_table[ 130 ], &sub_table[ 131 ], &sub_table[ 132 ], &sub_table[ 133 ], &sub_table[ 134 ], &sub_table[ 135 ],
        &sub_table[ 136 ], &sub_table[ 137 ], &sub_table[ 138 ], &sub_table[ 139 ], &sub_table[ 140 ], &sub_table[ 141 ], &sub_table[ 142 ], &sub_table[ 143 ],
        &sub_table[ 144 ], &sub_table[ 145 ], &sub_table[ 146 ], &sub_table[ 147 ], &sub_table[ 148 ], &sub_table[ 149 ], &sub_table[ 150 ], &sub_table[ 151 ],
        &sub_table[ 152 ], &sub_table[ 153 ], &sub_table[ 154 ], &sub_table[ 155 ], &sub_table[ 156 ], &sub_table[ 157 ], &sub_table[ 158 ], &sub_table[ 159 ],
        &sub_table[ 160 ], &sub_table[ 161 ], &sub_table[ 162 ], &sub_table[ 163 ], &sub_table[ 164 ], &sub_table[ 165 ], &sub_table[ 166 ], &sub_table[ 167 ],
        &sub_table[ 168 ], &sub_table[ 169 ], &sub_table[ 170 ], &sub_table[ 171 ], &sub_table[ 172 ], &sub_table[ 173 ], &sub_table[ 174 ], &sub_table[ 175 ],
        &sub_table[ 176 ], &sub_table[ 177 ], &sub_table[ 178 ], &sub_table[ 179 ], &sub_table[ 180 ], &sub_table[ 181 ], &sub_table[ 182 ], &sub_table[ 183 ],
        &sub_table[ 184 ], &sub_table[ 185 ], &sub_table[ 186 ], &sub_table[ 187 ], &sub_table[ 188 ], &sub_table[ 189 ], &sub_table[ 190 ], &sub_table[ 191 ],
        &sub_table[ 192 ], &sub_table[ 193 ], &sub_table[ 194 ], &sub_table[ 195 ], &sub_table[ 196 ], &sub_table[ 197 ], &sub_table[ 198 ], &sub_table[ 199 ],
        &sub_table[ 200 ], &sub_table[ 201 ], &sub_table[ 202 ], &sub_table[ 203 ], &sub_table[ 204 ], &sub_table[ 205 ], &sub_table[ 206 ], &sub_table[ 207 ],
        &sub_table[ 208 ], &sub_table[ 209 ], &sub_table[ 210 ], &sub_table[ 211 ], &sub_table[ 212 ], &sub_table[ 213 ], &sub_table[ 214 ], &sub_table[ 215 ],
        &sub_table[ 216 ], &sub_table[ 217 ], &sub_table[ 218 ], &sub_table[ 219 ], &sub_table[ 220 ], &sub_table[ 221 ], &sub_table[ 222 ], &sub_table[ 223 ],
        &sub_table[ 224 ], &sub_table[ 225 ], &sub_table[ 226 ], &sub_table[ 227 ], &sub_table[ 228 ], &sub_table[ 229 ], &sub_table[ 230 ], &sub_table[ 231 ],
        &sub_table[ 232 ], &sub_table[ 233 ], &sub_table[ 234 ], &sub_table[ 235 ], &sub_table[ 236 ], &sub_table[ 237 ], &sub_table[ 238 ], &sub_table[ 239 ],
        &sub_table[ 240 ], &sub_table[ 241 ], &sub_table[ 242 ], &sub_table[ 243 ], &sub_table[ 244 ], &sub_table[ 245 ], &sub_table[ 246 ], &sub_table[ 247 ],
        &sub_table[ 248 ], &sub_table[ 249 ], &sub_table[ 250 ], &sub_table[ 251 ], &sub_table[ 252 ], &sub_table[ 253 ], &sub_table[ 254 ], &sub_table[ 255 ] ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }

    for ( i=0; i < 256; i++ )
    {
        if ( sub_table[ i ] > 255 )
        {
            PyErr_SetString( PyExc_ValueError, "Invalid value in substitution table, must be in range( 256 )" );
            return NULL;
        }
    }

    // convert the image using the table
    for ( i=0; i < dataLen; i+=channels )
    {
            data[ i   ] = sub_table[ data[ i   ] ];
            data[ i+1 ] = sub_table[ data[ i+1 ] ];
            data[ i+2 ] = sub_table[ data[ i+2 ] ];
    }

    
    // Build and return a python tuple.
    return Py_BuildValue( "(iis#)", width, height, data, dataLen );

}

/**
 * Parses a tuple passed in as a filter for the spatial operations
 *
 * Parameters:
 *     PyFilter : PyObject*
 *         The python tuple to be parsed
 *     CFilter : int**
 *        The address of a pointer into which the values will be placed.
 *
 * returntype: int
 * returns: The size of the resulting square filter on one side ( the square root of the number of values )
 */
int parseFilter( PyObject *PyFilter, int **CFilter )
{
    Py_ssize_t position;
    int size;
    long numberOfFilterValues;

    numberOfFilterValues = PyTuple_Size( PyFilter );

    size = sqrt( numberOfFilterValues );
    
    //filter size should be an odd number. if not, decrement it
    if ( ! ( size & 1 ) )
        size--;

   numberOfFilterValues = size * size;

    *CFilter = calloc( sizeof( int ), numberOfFilterValues );

   for ( position = 0; position < numberOfFilterValues; position++ )
   {
        (*CFilter)[ position ] = ( int )PyInt_AsLong( PyTuple_GetItem( PyFilter, position ) );
   }

   return size;
}

static char spatial__doc__[ ] =
    "Implements an arbitrary spatial filter on the image.\n\
    The filter should be a tuple containing integers.\n\
    The number of elements should be the square of an odd number.\n\
    The filter will be truncated to the nearest square of an odd number if this is not the case.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image in pixels\n\
        height : int\n\
            The height of the image in pixels\n\
        data : string\n\
            The data as a string - chr(red) + chr(green) + chr(blue) for each pixel.\n\
        filter : tuple\n\
            A 9 element tuple containing the filter values.\n\
        filterTotal : int\n\
            The total weight of the filter the final result is to be divided by. This is optional and automatically determined if left out.\n\
    \n\
    :rtype: tuple\n\
    :returns: A tuple ( width, height, data ). Width and height are in pixels, data is a string containing chr(red) + chr(green) + chr(blue) for each pixel.\n\
    ";

PyObject *spatial( PyObject *pself, PyObject *pArgs )
{
    unsigned char *data, *outdata;
    PyObject *PyFilter; // The Python version of the filter (tuple)
    int *filter; // The C version of the filter
    int width, height, i, j, k, m, position, tmp;
    int dataLen; // the length of the data passed in
    int filterTotal=0; // the total weight of the filter (the number to divide the total by
    int filterSize; // the width (and height) of the filter;
    int channels; // the number of channels in the passed in image ( 1-4 )
    int edgeSize, numberOfElements;

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#O!|i", &width, &height, &data, &dataLen, &PyTuple_Type, &PyFilter, &filterTotal ) )
        return NULL;

    filterSize = ( int )PyTuple_Size( PyFilter );

    filterSize = parseFilter( PyFilter, &filter );
    numberOfElements = filterSize * filterSize;
    edgeSize = ( filterSize / 2 );

    // How many color channels are in this image?
    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }

    if ( !( outdata = calloc( dataLen, sizeof( char ) ) ) )
    {
         PyErr_SetString( PyExc_MemoryError, "Memory could not be allocated to create the new image" );
         return NULL;
    }

    // find the total weight for the filter ( if it's not already set )
    if ( !filterTotal )
    {
        for ( i=0; i < numberOfElements; i++ )
        {
            filterTotal += filter[ i ];
        }
        filterTotal = abs( filterTotal );
    }
    // set it to 1 if it is 0, can't divide by zero
    if (!filterTotal)
        filterTotal = 1;

    // apply the filter
    // we need something here to deal with the edges.
    // for now they are left black.
    for ( i= edgeSize * channels; i < ( width - edgeSize )*channels; i+=channels )
    {
        for ( j= edgeSize; j < height - edgeSize ; j++ )
        {
            k = i + j * width * channels;
            for ( position = k; position < k + 3; position++ )
            {
                tmp = 0;
                // calculate the sum of multiplying the pixels by the appropriate filter elements, then divide by the total weight.
                for( m = 0; m < numberOfElements; m++ )
                {
                    tmp += data[ position + ( ( m / filterSize - edgeSize ) * width * channels ) + ( ( m % filterSize - edgeSize ) * channels ) ] * filter[ m ];
                }
                outdata[ position ] = clip( abs( tmp / filterTotal ) );
                    // old algorithm for a 5x5 filter. left here for reference.
//                 outdata[ position ] = clip( abs(    data[ position - 2 * width * channels - 2 * channels ] * filter[  0 ] +
//                                                     data[ position - 2 * width * channels - 1 * channels ] * filter[  1 ] +
//                                                     data[ position - 2 * width * channels                ] * filter[  2 ] +
//                                                     data[ position - 2 * width * channels + 1 * channels ] * filter[  3 ] +
//                                                     data[ position - 2 * width * channels + 2 * channels ] * filter[  4 ] +
//                                                     data[ position -     width * channels - 2 * channels ] * filter[  5 ] +
//                                                     data[ position -     width * channels - 1 * channels ] * filter[  6 ] +
//                                                     data[ position -     width * channels                ] * filter[  7 ] +
//                                                     data[ position -     width * channels + 1 * channels ] * filter[  8 ] +
//                                                     data[ position -     width * channels + 2 * channels ] * filter[  9 ] +
//                                                     data[ position                        - 2 * channels ] * filter[ 10 ] +
//                                                     data[ position                        - 1 * channels ] * filter[ 11 ] +
//                                                     data[ position                                       ] * filter[ 12 ] +
//                                                     data[ position                        + 1 * channels ] * filter[ 13 ] +
//                                                     data[ position                        + 2 * channels ] * filter[ 14 ] +
//                                                     data[ position +     width * channels - 2 * channels ] * filter[ 15 ] +
//                                                     data[ position +     width * channels - 1 * channels ] * filter[ 16 ] +
//                                                     data[ position +     width * channels                ] * filter[ 17 ] +
//                                                     data[ position +     width * channels + 1 * channels ] * filter[ 18 ] +
//                                                     data[ position +     width * channels + 2 * channels ] * filter[ 19 ] +
//                                                     data[ position + 2 * width * channels - 2 * channels ] * filter[ 20 ] +
//                                                     data[ position + 2 * width * channels - 1 * channels ] * filter[ 21 ] +
//                                                     data[ position + 2 * width * channels                ] * filter[ 22 ] +
//                                                     data[ position + 2 * width * channels + 1 * channels ] * filter[ 23 ] +
//                                                     data[ position + 2 * width * channels + 2 * channels ] * filter[ 24 ] ) / filterTotal );
            }
        }
    }

    // copy the alpha data ( without modification )
    if ( channels == 4 ) // 4 channel images contain an alpha channel
    {
        for ( i = channels-1; i < dataLen; i+=channels )
        {
            outdata[ i ] = data[ i ];
        }
    }

    // free up unused memory
    free( filter );

    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, outdata, dataLen );

}


// PyObject *addImages( PyObject *pself, PyObject *pArgs )
// {
//     int width1, height1, width2, height2;
//     int dataLen1, dataLen2;
//     char *data1, *data2;
//     int i, j; // for loop variables
// 
//         if ( !PyArg_ParseTuple( pArgs, "iis#", &width, &height, &data, &dataLen ) )
//         return NULL;
// 
//     channels1 = dataLen1 / ( width1 * height1 );
//     channels2 = dataLen2 / ( width2 * height2 );
//     
//     if ( ( channels1 < 3 ) || ( channels1 > 4 ) )
//     {
//          PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 0-4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
//                         channels1, width1, height1, dataLen1 );
//          return NULL;
//     }
//     if ( ( channels2 < 3 ) || ( channels2 > 4 ) )
//     {
//          PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 0-4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
//                         channels2, width2, height2, dataLen2 );
//          return NULL;
//     }
// 
//     j = 0;
//     if ( channels2 >= 3 )
//     {
//         for ( i=0; i < dataLen1-channels1; i+=channels1 )
//         {
// 
//         }
//     }
//
//     // Build a python tuple and return it.
//     return Py_BuildValue( "(iis#)", width1, height1, data, dataLen );
// 
// }


static char quickScale__doc__[  ] =
    "Scales an image using a fast, low quality algorithm.\n\
    \n\
    :Parameters:\n\
        width : int\n\
            The width of the image being converted\n\
        height : int\n\
            The height of the image being converted\n\
        data : string\n\
            A string containing the data for the image\n\
        newWidth : int\n\
            The new width for the image.\n\
        newHeight : int\n\
            The new height for the image\n\
    \n\
    :rtype: tuple\n\
    :returns: a tuple containing a width, height, and data as a string.\n\
    ";

PyObject *quickScale( PyObject *pself, PyObject *pArgs )
{
    int i, j, k; //  loop variables
    int width, height, dataLen, newWidth, newHeight, channels;
    float xRatio, yRatio; // the scaling ratios
    unsigned char *data, *newData; // the image data
    int oldPosition, newPosition; // position pointers for the images
    
    // convert the passed in python argument to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#ii", &width, &height, &data, &dataLen, &newWidth, &newHeight ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }

    if ( !( newData = malloc( newWidth * newHeight * channels ) ) )
    {
            PyErr_SetString( PyExc_MemoryError, "Memory could not be allocated to create the new image" );
        return NULL;
    }

    xRatio = ( float )width  / ( float )newWidth ;
    yRatio = ( float )height / ( float )newHeight;

    // grab each pixel from a relative position in the original image and place it at ( i, j ) in the new image
    // this will produce fairly good results when scaling down, less so when scaling up.
    for ( i=0; i < newWidth; i++)
    {
        for ( j=0; j < newHeight; j++ )
        {
            newPosition = ( i + j * newWidth ) * channels;
            oldPosition = ( (int)( i * xRatio ) + (int)( j * yRatio ) * width ) * channels;
            for ( k=0; k < channels; k++ )
            {
                newData[ newPosition + k ] = data[ oldPosition + k ];
            }
        }
    }
    
    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)",  newWidth, newHeight, newData, ( newWidth * newHeight * channels ) );
}

static char toRGB__doc__[  ] =
    " Converts image data to 3 channel RGB format.\n\
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
    :returns: a tuple containing a width, height, and data as a string in RGB format\n\
    ";

PyObject *toRGB( PyObject *pself, PyObject *pArgs )
{
       unsigned int width, height, i;
       unsigned int dataLen, pixelCount;
       unsigned char *data, *newData, channels;

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#", &width, &height, &data, &dataLen ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3-4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }

    if ( channels == 3 )
    {
        // return the original data, it's already in RGB format.
        return Py_BuildValue( "(iis#)", width, height, data, dataLen );
    }

    // allocate memory for the new data
    if( !( newData = malloc( width * height * 3 ) ) )
    {
         PyErr_SetString( PyExc_MemoryError, "Memory could not be allocated to create the new image" );
         return NULL;
    }

    pixelCount = width * height;

    // this is an RGBA image, copy only the first 3 channels
    for( i=0; i < pixelCount; i++ )
    {
        newData[ i*3   ] = data[ i*channels   ];
        newData[ i*3+1 ] = data[ i*channels+1 ];
        newData[ i*3+2 ] = data[ i*channels+2 ];
    }
    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, newData, ( width * height * 3 ) );

}

static char toRGBA__doc__[  ] =
    " Converts image data to 4 channel RGBA format.\n\
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
    :returns: a tuple containing a width, height, and data as a string in RGB format with an Alpha Channel\n\
    ";

PyObject *toRGBA( PyObject *pself, PyObject *pArgs )
{
       unsigned int width, height, i;
       unsigned int dataLen, pixelCount;
       unsigned char *data, *newData, channels;

    // convert the passed in python arguments to C types.
    if ( !PyArg_ParseTuple( pArgs, "iis#", &width, &height, &data, &dataLen ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3-4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }

    if ( channels == 4 )
    {
        // return the original data, it's already in RGBA format.
        return Py_BuildValue( "(iis#)", width, height, data, dataLen );
    }

    // allocate memory for the new data
    if( !( newData = malloc( width * height * 4 ) ) )
    {
         PyErr_SetString( PyExc_MemoryError, "Memory could not be allocated to create the new image" );
         return NULL;
    }

    pixelCount = width * height;

    // this is an RGB image, copy the first 3 channels and set the alpha channel to 255
    for( i=0; i < pixelCount; i++ )
    {
        newData[ i*4   ] = data[ i*channels   ];
        newData[ i*4+1 ] = data[ i*channels+1 ];
        newData[ i*4+2 ] = data[ i*channels+2 ];
        newData[ i*4+3 ] = 255;
    }
    // Build a python tuple and return it.
    return Py_BuildValue( "(iis#)", width, height, newData, ( width * height * 4 ) );

}

// map of function names to functions
static PyMethodDef core_methods[ ] =
{
//  format is as follows:
//  { "python_name"  , c_name     , arg_method  , doc_string          },
    { "spatial"     , spatial     , METH_VARARGS, spatial__doc__      },
    { "table"       , table       , METH_VARARGS, table__doc__        },
    { "stringCopy"  , stringCopy  , METH_VARARGS, stringCopy__doc__   },
    { "swapChannels", swapChannels, METH_VARARGS, swapChannels__doc__ },
    { "quickScale"  , quickScale  , METH_VARARGS, quickScale__doc__   },
    { "toRGB"       , toRGB       , METH_VARARGS, toRGB__doc__        },
    { "toRGBA"      , toRGBA      , METH_VARARGS, toRGBA__doc__       },
    { NULL, NULL } // End of functions
};

PyMODINIT_FUNC initcCore( void )
{
    ( void )Py_InitModule3( "cCore", core_methods, __doc__ );
}


