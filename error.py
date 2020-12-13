"""
error.py
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

class ImageFormatError(Exception):
    """
    An exception to be raised in the event of a problem reading the file.
    """
    def __init__(self, message = None):
        Exception.__init__(self, message)

class ImageReadError(Exception):
    """
    An exception to be raised in the event of a problem reading the file.
    """
    def __init__(self, message = None):
        Exception.__init__(self, message)

class UnsupportedImageTypeError(Exception):
    """
    An exception to be raised in the event that there is no plugin to handle
    the specified image format.
    """
    def __init__(self, message = None):
        Exception.__init__(self, message)

class ExtensionError(Exception):
    """
    An exception to be raised in the event that an extension malfuncions
    (returning invalid data, etc).
    """
    def __init__(self, message = None):
        Exception.__init__(self, message)
