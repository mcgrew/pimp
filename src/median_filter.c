
#define PY_SSIZE_T_CLEAN
#include <Python.h>

const static char __doc__[] =
"median_filter.c\n"
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

/**
 * Optimized selection sort algorithm. This function only sorts as many
 * values as are required by the caller. For the median function, this is
 * slightly more than half, thus speeding up processing significantly.
 *
 * :Parameters:
 *     valueList : char*
 *        The list of values to be sorted
 *     valueListLength : int
 *        The number of elements in the list
 *     valuesNeeded : int
 *        The number of values that need to be sorted
 *
 * :returntype: void
 */
void sort(unsigned char *valueList, int valueListLength, int valuesNeeded)
{
    // selection sort
    int i, j, lowest, tmp;

    if (valuesNeeded == 0)
    {
        valuesNeeded = valueListLength - 1;
    }

    for (i=0; i <= valuesNeeded; i++)
    {
        lowest = i;
        for (j=i+1; j < valueListLength; j++)
        {
            if (valueList[j] < valueList[lowest])
                lowest = j;
       }
        tmp = valueList[lowest];
        valueList[lowest] = valueList[i];
        valueList[i] = tmp;
    }
}

/**
 * Finds the median value in a list of characters (bytes)
 *
 * :Parameters:
 *     valueList : char*
 *         The list of values to find the median of
 *     valueListLength : int
 *        The lenghth of the above list
 *
 * :returntype: int
 * :returns: The median of the values contained in the list.
 */
int findMedian(unsigned char *valueList, int valueListLength)
{
    int valuesNeeded;

    valuesNeeded = (valueListLength >> 1) + 1;


    sort(valueList, valueListLength, valuesNeeded);
    if (valueListLength & 1)
        return valueList[valuesNeeded - 1];
    return (valueList[valuesNeeded - 2] + valueList[valuesNeeded - 1]) >> 1;

}

const static char median_filter__doc__[] =
"Smooths an image by making each pixel appear more like it's neighboring "
    "pixels.\n"
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
":returns: A tuple (width, height, data). Width and height are in pixels, "
    "data is a string containing binary image data.\n";

PyObject *median_filter(PyObject *pself, PyObject *pArgs)
{
    int i, j, k, m, position; // for loop variables
    int width, height;
    Py_ssize_t dataLen;
    unsigned char *data, *newData;
    int size=3; // the default size for a median filter
    unsigned char *valueList; // the list of values to find the median of.
    int valueListLength; // the number of values in the valueList
    int channels; // the number of color channels in this image
    int padding;

    // read in the arguments from python
    if (!PyArg_ParseTuple(pArgs, "iiy#|i",
                &width, &height, &data, &dataLen, &size))
        return NULL;

    channels = dataLen / (width * height);
    
    if ((channels < 3) || (channels > 4))
    {
        PyErr_Format(PyExc_ValueError, "Data contained an invalid number of "
                "channels, 3 or 4 expected, %d recieved (width: %d, "
                "height: %d, bytes: %d)", channels, width, height, dataLen);
        return NULL;
    }

    valueListLength = size * size;
    if (!(valueList = (unsigned char*)malloc(sizeof(char) * valueListLength)))
    {
        PyErr_SetString(PyExc_MemoryError,
                "Memory could not be allocated for the value array");
        return NULL;
    }

    padding = size / 2; // padding to leave around the image in the main loop
    
    if(!(newData = (unsigned char*)calloc(sizeof(char), dataLen)))
    {
        PyErr_SetString(PyExc_MemoryError,
                "Memory could not be allocated for the new image");
        return NULL;
    }

    for (i=padding; i < width - padding; i++)
    {
        for (j=padding; j < height - padding; j++)
        {
            k = i * channels + j * width * channels;
            for (position = k; position < k+3; position++)
            {
                // a list of the values that form a square around this pixel
                for (m=0; m < valueListLength; m++)
                {
                    valueList[m] = data[position + 
                        ((m / size - padding) * width * channels) +
                        ((m % size - padding) * channels)];
                }
                newData[position] = findMedian(valueList, valueListLength);
            }
        }
    }
    
    // Build a python tuple and return it.
    return Py_BuildValue("(iiy#)", width, height, newData, dataLen);

}

static PyMethodDef median_methods[] =
{
    {"execute", median_filter, METH_VARARGS, median_filter__doc__},
    {NULL, NULL} // End of functions
};

static struct PyModuleDef median_module = {
    PyModuleDef_HEAD_INIT,
    "medianfilter",
    __doc__,
    -1,
    median_methods
};

PyMODINIT_FUNC PyInit_median_filter(void)
{
    PyObject *m = PyModule_Create(&median_module);
    PyModule_AddStringConstant(m, "MENU", "Fil&ter");
    PyModule_AddStringConstant(m, "LABEL", "&Median Filter");
    PyModule_AddStringConstant(m, "DESCRIPTION",
            "Applies a median filter to the image");
    return m;
}

