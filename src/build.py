#!/usr/bin/python
"""
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

from distutils.core import setup, Extension
import os
from sys import argv
from glob import glob

# change to the directory this setup file is in
os.chdir( os.path.abspath( os.path.dirname( argv[ 0 ] ) ) )

if not ( 'build' in argv ):
    argv.insert( 1, 'build' )


INCLUDE = [ ]

compiled_plugins =  [
                        'histogramEq',
                        'invert',
                    ]


compiled_libs    =  [
                        'cCore',
                        'color',
                        'nintendize',
                        'medianFilter',
                    ]

all_modules = compiled_plugins + compiled_libs


modules = [ ]
for m in all_modules:
    modules.append( Extension( m, include_dirs = INCLUDE, sources = [ m+'.c' ] ) )
setup( name = m, version = '0.2', ext_modules = modules )

print()

for m in compiled_plugins:
    for filename in glob( os.path.join( "build", "lib.*", m+".*" ) ):
        pluginpath = os.path.join( os.path.pardir, 'extensions','menu', os.path.basename( filename ) )
        print("moving", os.path.basename( filename ), "->", pluginpath)
        #if the compiled file already exists, we have to remove it to make windows happy
        if os.path.exists( pluginpath ):
            os.remove( pluginpath )
        os.renames( filename, pluginpath )


for m in compiled_libs:
    for filename in glob( os.path.join( "build", "lib.*", m+".*" ) ):
        pluginpath = os.path.join( os.path.pardir, 'extensions','lib', os.path.basename( filename ) )
        print("moving", os.path.basename( filename ), "->", pluginpath)
        #if the compiled file already exists, we have to remove it to make windows happy
        if os.path.exists( pluginpath ):
            os.remove( pluginpath )
        os.renames( filename, pluginpath )
