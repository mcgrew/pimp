"""
pimpgui.py
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

# library imports
import os
from glob import glob
from sys import argv, platform
import wx

from image import Image

# import the core module
from error import ImageFormatError, UnsupportedImageTypeError, ExtensionError
import extensions.lib.core



# constants
VERSION = "0.1"
TITLE = "The PIMP"
DEBUG = False
MAXIMUM_UNDO_LIMIT = 10

#make sure we are in the right directory
os.chdir(os.path.abspath(os.path.dirname(argv[0])))

# C extensions
if platform == "win32":
    C_EXTENSIONS = ".pyd"
else:
    C_EXTENSIONS = ".so"

# create dictionaries for storing file reader extensions.
file_reader = {'ext' : dict(), 'marker' : dict()}


def reload_extensions():
    """
    Reloads file reader extensions. Currently does not re-parse already loaded
    extensions but will load new ones.
    """
    load_extensions()

def load_extensions():
    """
    Scans extension directories for available extensions and attempts to load
    them.
    """
    # file reader extension path
    format_ext_pkg = ("extensions", "format")
    format_ext_dir = os.path.join(os.getcwd(), *format_ext_pkg)

    debug("Loading file format extensions")
    file_fmt_ext = \
            glob(f'{format_ext_dir}{os.sep}*.py') + \
            glob(f'{format_ext_dir}{os.sep}*{C_EXTENSIONS}')
    for f in file_fmt_ext:
        module = os.path.basename(f)
        # import the module into a temporary variable for checking
        module_name = '.'.join(format_ext_pkg + (module[:module.rindex(".")],))
        exec ("import %s" % module_name)
        tmp = eval(module_name)
        if hasattr(tmp, "FILE_EXTENSION"):
            if type(tmp.FILE_EXTENSION) in (list, tuple):
                for ext in tmp.FILE_EXTENSION:
                    file_reader['ext'][ext.lower()] = tmp
            else:
                file_reader['ext'][tmp.FILE_EXTENSION.lower()] = tmp
        if hasattr(tmp, "FILE_MARKER"):
            file_reader['marker'][tmp.FILE_MARKER] = tmp
    for ext in file_reader['ext']:
        debug(f"Loaded fileHandler for {ext} files")
    debug()

# ================================ FRAME CLASS =================================
class Frame(wx.Frame):
    """
    The Frame object is used as the main application window.
    """
    def __init__(self):
        """
        Creates a new Frame object.
        """
        wx.Frame.__init__(self, None, -1, TITLE, wx.DefaultPosition,
                wx.DefaultSize)
        self._image = None
        self.set_image_file(None)
        self._scroller = wx.ScrolledWindow(self)
        self._panel = wx.Panel(self._scroller)
        self._scroller.EnableScrolling(True, True)
        self._extensions = dict()
        self.CreateStatusBar()
        self._build_menu()
        self._load_menu_extensions()
        self._undo_stack = list()
        self._redo_stack = list()
        self._window_is_dirty = False

        #self.Bind(wx.EVT_SIZE, self.onSize)
        self._panel.Bind(wx.EVT_SIZE, self.onPanelSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_MOVE, self.onMove)
        self.Bind(wx.EVT_IDLE, self.onIdle)

    def set_image(self, image):
        """
        Sets the image for the application.

        :Parameters:
            image : Image
                The image to be displayed.
        """
        width = image.get_width()
        height = image.get_height()
        # set the sizes of our main frame and inner panel
        self._scroller.SetScrollbars(1, 1, width, height)
        self.SetSize((width + 5, height + 52))
        self._panel.SetSize((width, height))
        # set the image and repaint the frame to display it.
        self._image = image
        self.Refresh()

    # ============================== EVENT HANDLERS ============================
    def Refresh(self):
        """
        This method overrides the Refresh method of the wx.Frame class. The
        Refresh() method doesn't seem to work correctly on all versions of
        wxPython, so I'm replacing it with one that should work anywhere.
        """
        self._window_is_dirty = True

    def onMove(self, event=None):
        """
        Internal Function. Called when the window is moved.
        """
        self.Refresh()

    def onPanelSize(self, event=None):
        """
        Internal Function. Called when the window is resized.
        """
        self.Refresh()

    def onIdle(self, event=None):
        """
        Internal Function. Called when the application becomes idle.
        """
        # Is the window marked dirty?
        if self._window_is_dirty:
            self._window_is_dirty = False
            # check to see if scroll bars are needed.
            self._check_scrollbars()
            # repaint the window
            self.paint()

    def onPaint(self, event=None):
        """
        Internal Function. Called when repainting the window.
        """
        self.paint()

    def paint(self):
        """
        Internal Function. Called when the window needs to be repainted.
        """
        if self._image:
            dc = wx.WindowDC(self._panel)
            dc.DrawBitmap(self._get_bitmap(), 0, 0)

    def _check_scrollbars(self, event=None):
        if self._image:
            # turn off the scrollbars by default
            x_scroll = 0
            y_scroll = 0
            if self.GetSize()[0] < self._panel.GetSize()[0] + 5:
                x_scroll = 5 # enable the horizontal scrollbar
            if self.GetSize()[1] < self._panel.GetSize()[1]  + 52:
                y_scroll = 5 # enable the vertical scrollbar
            self._scroller.SetScrollRate(x_scroll, y_scroll)

    # ================================ END EVENT HANDLERS ==================================

    def _get_bitmap(self):
        """
        Returns a copy of the application's image for display. This allows a
        different image to be displayed on the screen than is stored internally,
        i.e. for zooming.
        """
        return extensions.lib.core.data_to_bitmap(self._image.get_width(),
                                                  self._image.get_height(),
                                                  self._image.get_data())

    def _zoom(self, event=None):
        """
        As of yet, this does nothing.
        """

    def _build_menu(self):
        """
        Internal Function. Builds the menu bar for the application.
        """
        self.menu_bar = wx.MenuBar()
        self.SetMenuBar(self.menu_bar)
        menus = list()
        file_menu = wx.Menu()
        self.menu_bar.Append(file_menu, "&File")
        edit_menu = wx.Menu()
        self.menu_bar.Append(edit_menu, "&Edit")
        # ============ ADD ITEMS TO THE MENU =============
        self.Bind(wx.EVT_MENU, self.open_file,
                file_menu.Append(-1, "&Open", "Open a file"))
        self.Bind(wx.EVT_MENU, self.save_file,
                file_menu.Append(-1, "&Save", "Save the file"))
        self.Bind(wx.EVT_MENU, self.save_as,
                file_menu.Append(-1, "&Save As",
                    "Save the file under a different name"))
        self.Bind(wx.EVT_MENU, self._reload_menu_extensions,
                file_menu.Append(-1, "Reload Extensions",
                    "Reload all PIMP extensions"))
        self.Bind(wx.EVT_MENU, self.onExit,
                file_menu.Append(-1, "E&xit", "Close the program"))
        self.Bind(wx.EVT_MENU, self.undo, edit_menu.Append(-1,
            "&Undo", "Undo the last change"))
        self.Bind(wx.EVT_MENU, self.redo,
                edit_menu.Append(-1, "&Redo", "Redo the last undone change"))

    def set_image_file(self, filename):
        """
        Internal Function. Updates the name of the current file being edited and
        displays it in the titlebar.
        """
        self.image_filename = filename
        if self.image_filename:
            self.SetTitle(os.path.basename(filename) + " - " + TITLE)
        else:
            self.SetTitle(TITLE)


    # ========================== STATIC MENU METHODS ===========================
    def open_file(self, event=None):
        """
        Opens an image file
        """
        filename = None
        if isinstance(event, str):
            filename = event
        if not filename:
            dialog = wx.FileDialog(self, style = wx.FD_OPEN)
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetPath()
            dialog.Destroy()
        if filename:
            self.set_image_file(filename)
            self.set_image(read(filename))
            # clear the undo and redo stacks
            self._undo_stack = list()
            self._redo_stack = list()

    def save_file(self, event=None):
        """
        Saves the file out to the previously defined image.
        """
        if self.image_filename:
            write(self.image_filename, self._image)
        else:
            self.save_as()

    def save_as(self, event=None):
        """
        Saves the file under a different filename
        """
        dialog = wx.FileDialog(self, style = wx.FD_SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.set_image_file(dialog.GetPath())
            self.save_file()
        dialog.Destroy()

    def undo(self, event=None):
        """
        Rolls back the last change made to an image.
        """
        if self._undo_stack:
            self._redo_stack.append(self._image)
            self.set_image(self._undo_stack.pop())

    def redo(self, event=None):
        """
        Reapplies the last undone change to an image.
        """
        if self._redo_stack:
            self._undo_stack.append(self._image)
            self.set_image(self._redo_stack.pop())


    # ====================== EXTENSION LOADING METHODS =========================
    def _reload_menu_extensions(self, event=None):
        """
        Internal function. Reloads the menu extensions.
        """
        # This function doens't work quite right. Python caches the modules it
        # loads somehow and a call to reload() is needed to completely reload
        # them.
        debug("RELOADING EXTENSIONS")
        #reload the fileformat extensions
        reload_extensions()
        #reload the default menu items
        self._build_menu()
        # reload the menu extensions
        self._load_menu_extensions()


    def _load_menu_extensions(self):
        """
        Internal Function. Loads Extensions that create menu items.
        """
        # menu item extension path
        menu_ext_pkg = ("extensions", "menu")
        menu_ext_dir = os.path.join(os.getcwd(), *menu_ext_pkg)

        debug("Loading menu items")
        menu_ext = \
                glob(f'{menu_ext_dir}{os.sep}*.py') + \
                glob(f'{menu_ext_dir}{os.sep}*{C_EXTENSIONS}')
        for f in menu_ext:
            module_file = os.path.basename(f)
            module_name = '.'.join((*menu_ext_pkg,
                module_file[: module_file.index(".")]))
            module = getattr(__import__(module_name).menu,
                    module_name[module_name.rfind('.')+1:])

            if hasattr(module, "MENU") and hasattr(module, "LABEL"):
                self._extensions['.'.join((module.MENU, module.LABEL))] = module

                #insert this into the proper menu (and possibly submenu)

                # split up the menu path to see if it contains submenus
                menu_path = module.MENU.split('.')

                menu_pos = self.menu_bar.FindMenu(menu_path[0])
                if menu_pos == -1:
                    self.menu_bar.Append(wx.Menu(), menu_path[0])
                    menu_pos = self.menu_bar.FindMenu(menu_path[0])

                menu = self.menu_bar.GetMenu(menu_pos)
                menu_list = self._find_menu(menu, menu_path[1:])
                self._add_menu_item(module, menu_list[-1] if menu_list else menu)
                debug(f"Loaded module {module_file}")

            else:
                # the module does not have the correct 'constants' defined.
                debug(f"{module_file} is not a valid module.")
        debug()

    def _find_menu(self, menu, menu_path):
        """
        Finds a menu for adding an item to.
        """
        if not menu_path:
            return []
        items = menu.GetMenuItems()
        for m in items:
            if hasattr(m, 'GetName'):
                if m.GetName().replace('&', '') == menu_path[0].replace('&',''):
                    return m, *self._find_menu(m, menu_path[1:])
        m = menu.Append(-1, menu_path[0], wx.Menu())
        return m, *self._find_menu(m, menu_path[1:])

    def _add_menu_item(self, module, menu):
        """
        Adds a new menu item
        """
        if not hasattr(menu, 'Append'):
            menu = menu.GetSubMenu()
        if hasattr(module, "DESCRIPTION"):
            description = module.DESCRIPTION
        else:
            description = str()
        # create and bind a handler to a menuItem.
        self.Bind(wx.EVT_MENU, self._filter_handler(module.execute),
                menu.Append(-1, module.LABEL, description))

    def _filter_handler(self, handler):
        """
        Internal Function. Creates a custom dynamic handler for menu items.
        """
        # define a new function and return it.
        def f(evt):
            if self._image:
                new_img_data = handler(self._image.get_width(),
                        self._image.get_height(),
                        extensions.lib.core.string_copy(
                            bytes(self._image.get_data())))
            else:
                handler(1, 1, "\x00")
                new_img_data = False
            # set this frame's image to the one returned by the filter.
            if (new_img_data and len(new_img_data) == 3):
                self._redo_stack = list()
                self._undo_stack.append(self._image)
                while len(self._undo_stack) > MAXIMUM_UNDO_LIMIT:
                    del self._undo_stack[0]
                self.set_image(Image(*new_img_data))
        return f
    # =================== END EXTENSION LOADING METHODS ========================


    def onExit(self, event):
        """
        Internal function. Closes the program.
        """
        self.Close(True)

# ============================ END FRAME CLASS =================================

def write(filename, image):
    """
    Writes an image out to file. The image format must be supported by a file
    format extension.

    :Parameters:
        filename : string
            The path to the file to be written.
        image : Image
            The Image containing the data to be written.
    """
    width, height = image.get_size()
    img_ext = filename[filename.index('.') + 1 :].lower() # get the file ext

    if img_ext not in file_reader['ext']:
        raise UnsupportedImageTypeError(f"File extension '{img_ext}' has no "
            "extension associated with it")
    if not hasattr(file_reader['ext'][img_ext], "write"):
        raise UnsupportedImageTypeError("The extension for handling files of "
            f"type '{img_ext}' contains no method for writing.")
    try:
        return file_reader['ext'][img_ext].write(filename, width, height,
                extensions.lib.core.string_copy(bytes(image.get_data())))
    except:
        raise # TODO: show an error dialog


def read(filename):
    """
    Calls the appropriate extension to read the image file, if one exists.

    :Paramters:
        filename : string
            The name of the file to be read.
    """
    img_ext = filename[filename.index('.') + 1:].lower() # get the file ext
    try:
        if not img_ext in file_reader['ext']:
            raise UnsupportedImageTypeError(f"File extension '{img_ext}' has "
                "no extension associated with it")
        if not hasattr(file_reader['ext'][img_ext], "read"):
            raise UnsupportedImageTypeError("The extension for handling files "
                f"of type '{img_ext}' contains no method for reading.")
        img_data =  file_reader['ext'][img_ext].read(filename)

    except ImageFormatError as message:
        debug(message)
        image_file = open(filename, 'rb')
        file_marker = image_file.read(2)
        image_file.close()
        if not file_marker not in file_reader['marker']:
            image_file.close()
            raise UnsupportedImageTypeError(
                    "This image type has no extension associated with it")

        if hasattr(file_reader['marker'][file_marker], 'DESCRIPTION'):
            debug(f"File '{filename}' was found to be an incorrectly named as "
                f"a '{file_reader['marker'][file_marker].DESCRIPTION}' file)")
        else:
            debug("File '{filename}' was found to be an incorrectly named file")
        img_data = file_reader['marker'][file_marker].read(filename)

    if len(img_data) != 3:
        raise ExtensionError(f"File format extension for '{img_ext}' returned "
           "an invalid number of arguments")
    width, height, data = img_data
    returnvalue = Image(width, height, data)

    return returnvalue


def debug(string=""):
    """
    Internal Function that handles debug output for the program.
    """
    if DEBUG:
        print(string)

load_extensions() # call the function to load all available extensions.
