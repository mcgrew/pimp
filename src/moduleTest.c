
#include <Python.h>
#include <stdlib.h>
#include <stdio.h>

// doc string
static char reverse_doc[ ] = "Reverses a string";

// reverses a string
static PyObject *moduleTest_reverse( PyObject *pself, PyObject *pArgs )
{
	char *pString, *reversedString;
	int pStringLen, i;

	if ( !PyArg_ParseTuple( pArgs, "s#", &pString, &pStringLen ) )
		return NULL;
	
	reversedString = malloc( pStringLen );

	for ( i=0; i < pStringLen; i++ )
	{
		reversedString[ i ] = pString[ pStringLen - i - 1 ];
	}

	return Py_BuildValue( "s#", reversedString, pStringLen );
		
}

// map of function names to functions
static PyMethodDef moduleTest_methods[ ] = 
{
	{ "reverse", moduleTest_reverse, METH_VARARGS, reverse_doc },
	{ NULL, NULL } // End of functions
};

PyMODINIT_FUNC initmoduleTest( void )
{
	Py_InitModule( "moduleTest", moduleTest_methods );
}
