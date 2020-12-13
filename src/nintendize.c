
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <math.h>
#include "core.h"

const static char __doc__[] =
"nintendize.c\n"
"Copyright 2007,2020 Thomas McGrew\n"
"\n"
"This file is part of The Python Image Manipulation Project.\n"
"\n"
"The Python Image Manipulation Project is free software: you can\n"
"redistribute it and/or modify it under the terms of the GNU General\n"
"Public License as published by the Free Software Foundation, either\n"
"version 2 of the License, or (at your option) any later version.\n"
"\n"
"The Python Image Manipulation Project is distributed in the hope\n"
"that it will be useful, but WITHOUT ANY WARRANTY; without even the\n"
"implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR\n"
"PURPOSE. See the GNU General Public License for more details.\n"
"\n"
"You should have received a copy of the GNU General Public License\n"
"along with The Python Image Manipulation Project.  If not, see\n"
"<http://www.gnu.org/licenses/>.\n";

const static char nintendize__doc__[] =
"Pixellates the image and reduces bit quality in a way such that it\n"
"looks like an image from an old video game console.\n"
"\n"
":Parameters:\n"
"    filename : string\n"
"        The name of the file to write to.\n"
"    width : int\n"
"        The width of the image in pixels\n"
"    height : int\n"
"        The height of the image in pixels\n"
"    data : string\n"
"        The data as a binary string.\n"
"\n"
":rtype: tuple\n"
":returns: A tuple (width, height, data). Width and height are in pixels, data "
    "is a binary string.\n";

PyObject *nintendize(PyObject *pself, PyObject *pArgs)
{
    int i, j, k, m, position, maxi, maxj; // for loop variables
    int width, height;
    Py_ssize_t dataLen;
    unsigned char *data, *newData;
    int size; // the size for a median filter
    unsigned int colorlevel = 3; // the number of bits to save per color channel
    unsigned int resolution = 200; // the resolution to pixellate the image to.
    int channels; // the number of color channels in this image
    int thisPixel;
    int tmp_red, tmp_blue, tmp_green;
    int mask;

    // read in the arguments from python
    if (!PyArg_ParseTuple(pArgs, "iiy#|ii", &width, &height, &data, &dataLen,
                &resolution, &colorlevel))
        return NULL;

    // make sure colorlevel is 8 or less (it always should be)
    colorlevel = min(colorlevel, 8);

    size = min(width, height) / resolution;
    // make sure size isn't out of range.
    size = min(size, min(width, height));
    size = max(size, 1);

    channels = dataLen / (width * height);
    // the mask to be used in masking each color channel
    mask = (0xff << (8 - colorlevel)) & 0xff;

    if ((channels < 3) || (channels > 4))
    {
        PyErr_Format(PyExc_ValueError, "Data contained an invalid number of "
                "channels, 3 or 4 expected, %d recieved (width: %d, "
                "height: %d, bytes: %d)", channels, width, height, dataLen);
        return NULL;
    }

    if(!(newData = (unsigned char*)calloc(sizeof(char), dataLen)))
    {
        PyErr_SetString(PyExc_MemoryError,
                "Memory could not be allocated for the new image");
        return NULL;
    }

    maxi = (int)((float)width  - (float)size/2);
    maxj = (int)((float)height - (float)size/2);
    for (i=size/2; i <= maxi; i+=size)
    {
        for (j=size/2; j <= maxj; j+=size)
        {
            position = (i * channels + j * width * channels);
            tmp_red = tmp_blue = tmp_green = 0;
            for (k = 0; k < size; k++)
            {
                // find the average color
                for(m = 0; m < size; m++)
                {
                    thisPixel = position + ((k - size/2) * channels) * width + 
                        ((m - size/2) * channels);
                    tmp_red   += data[thisPixel    ];
                    tmp_green += data[thisPixel + 1];
                    tmp_blue  += data[thisPixel + 2];
               }
            }
            // mask each color
            tmp_red    = clip(tmp_red   / (size * size)) & mask;
            tmp_green  = clip(tmp_green / (size * size)) & mask;
            tmp_blue   = clip(tmp_blue  / (size * size)) & mask;
            // replace the masked off bits with copies of the remaining bits so
            // the image doesn't darken
            for(k = colorlevel; k < 8; k *= 2)
            {
                tmp_red   |= tmp_red   >> k;
                tmp_green |= tmp_green >> k;
                tmp_blue  |= tmp_blue  >> k;
            }
            // fill in the block with the average color
            for (k = 0; k < size; k++)
            {
                for(m = 0; m < size; m++)
                {
                    thisPixel = position + ((k - size/2) * channels) * width +
                        ((m - size/2) * channels);
                    newData[thisPixel    ] = tmp_red;
                    newData[thisPixel + 1] = tmp_green;
                    newData[thisPixel + 2] = tmp_blue;

                }
            }
        }
    }

    // Build a python tuple and return it.
    return Py_BuildValue("(iiy#)", width, height, newData, dataLen);

}

static PyMethodDef nintendize_methods[] =
{
    {"execute", nintendize, METH_VARARGS, nintendize__doc__},
    {NULL, NULL} // End of functions
};

static struct PyModuleDef nintendize_module =
{
    PyModuleDef_HEAD_INIT,
    "nintendize",
    __doc__,
    -1,
    nintendize_methods
};

PyMODINIT_FUNC PyInit_nintendize(void)
{
    PyObject *m = PyModule_Create(&nintendize_module);
    PyModule_AddStringConstant(m, "MENU", "Fil&ter.&Comic");
    PyModule_AddStringConstant(m, "LABEL", "Nindendi&ze");
    PyModule_AddStringConstant(m, "DESCRIPTION", "Nintendize it!");
    return m;
}

