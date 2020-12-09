static char __doc__[ ] =
"invert.c\n\
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
"Inverts the colors in an image.\n\
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
:returns: A tuple ( width, height, data ). Width and height are in pixels, data is a string containing binary data for the image.\n\
";

PyObject *invert_execute( PyObject *pself, PyObject *pArgs )
{
    unsigned char *data;
    unsigned int width, height, i;
    Py_ssize_t dataLen;
    unsigned char channels;

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

    for ( i=0; i < dataLen-channels; i+=channels )
    {
        data[ i   ] = data[ i   ] ^ 0xff;
        data[ i+1 ] = data[ i+1 ] ^ 0xff;
        data[ i+2 ] = data[ i+2 ] ^ 0xff;
    }


    // Build a python tuple and return it.
    return Py_BuildValue( "(iiy#)", width, height, data, dataLen );

}

// map of function names to functions
static PyMethodDef invert_methods[ ] =
{
    { "execute", invert_execute, METH_VARARGS, execute__doc__ },
    { NULL, NULL } // End of functions
};

static struct PyModuleDef invert_module = {
    PyModuleDef_HEAD_INIT,
    "ccore",
    __doc__,
    -1,
    invert_methods
};

PyMODINIT_FUNC PyInit_invert( void )
{
    PyObject *m = PyModule_Create(&invert_module);
    PyModule_AddStringConstant( m, "MENU", "Fil&ter" );
    PyModule_AddStringConstant( m, "LABEL", "In&vert" );
    PyModule_AddStringConstant( m, "DESCRIPTION", "Inverts All Colors In The Image" );
    return m;
}


