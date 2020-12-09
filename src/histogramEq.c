static char __doc__[ ] =
"histogram_eq.c\n\
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

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stdio.h>


// doc string
static char execute__doc__[ ] =
"Performs a histogram equalization on an image.\n\
\n\
:Parameters:\n\
    filename : string\n\
        The name of the file to write to.\n\
    width : int\n\
        The width of the image in pixels\n\
    height : int\n\
        The height of the image in pixels\n\
    data : string\n\
        The data as a binary string.\n\
\n\
:rtype: tuple\n\
:returns: a tuple containing a width, height, and data as a binary string.\n\
";

PyObject *execute( PyObject *pself, PyObject *pArgs )
{
    unsigned char *data;
    unsigned int width, height;
    Py_ssize_t dataLen;
    unsigned char channels;

    unsigned char *histogram_sum;
    unsigned int i;
    float pixelcount;
    unsigned long long *histogram_table;

    // convert the passed in python argument to C types.
    if ( !PyArg_ParseTuple( pArgs, "iiy#", &width, &height, &data, &dataLen ) )
        return NULL;

    channels = dataLen / ( width * height );
    if ( ( channels < 3 ) || ( channels > 4 ) )
    {
         PyErr_Format( PyExc_ValueError, "Data contained an invalid number of channels, 3 or 4 expected, %d recieved ( width: %d, height: %d, bytes: %d )",
                        channels, width, height, dataLen );
         return NULL;
    }

    // allocate memory
    if ( !( histogram_sum    = malloc( 256 * sizeof( char ) ) ) ||
         !( histogram_table  = calloc( 256, sizeof( long long ) ) ) )
    {
         PyErr_SetString( PyExc_MemoryError, "Memory could not be allocated to create histogram tables" );
         return NULL;
    }

    // count the number of greyscale pixels of each value ( 0 - 255 )
    for ( i=0; i <= ( dataLen - channels ); i+=channels )
    {
        histogram_table[ ( 1 + data[ i ] + data[ i+1 ] + data[ i+2 ] ) / 3  ]++;
    }

    // build a histogram table
    pixelcount = width * height;
    histogram_sum[ 0 ] = ( histogram_table[ 0 ] * 255 / pixelcount );
    for ( i=1; i < 256; i++ )
    {
        histogram_sum[ i ] = histogram_table[ i ] * 255 / pixelcount + histogram_sum[ i-1 ];
    }

    // convert the image using the histogram table
    for ( i=0; i < dataLen-channels+1; i+=channels )
    {
        data[ i   ] = histogram_sum[ data[ i   ] ];
        data[ i+1 ] = histogram_sum[ data[ i+1 ] ];
        data[ i+2 ] = histogram_sum[ data[ i+2 ] ];
    }


    // free all used memory
    free( histogram_table );
    free( histogram_sum );

    // Build and return a python tuple.
    return Py_BuildValue( "(iiy#)", width, height, data, dataLen );


}

// map of function names to functions
static PyMethodDef methods[ ] =
{
    { "execute", execute, METH_VARARGS, execute__doc__ },
    { NULL, NULL } // End of functions
};

static struct PyModuleDef histogramEq_module = {
    PyModuleDef_HEAD_INIT,
    "ccore",
    __doc__,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_histogramEq( void )
{
    PyObject *m = PyModule_Create(&histogramEq_module);
    PyModule_AddStringConstant( m, "MENU", "Fil&ter" );
    PyModule_AddStringConstant( m, "LABEL", "&Equalize Histogram" );
    PyModule_AddStringConstant( m, "DESCRIPTION", "Equalize the histogram of this image" );
    return m;
}

