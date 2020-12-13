"""
quick_scale.py
Copyright 2007,2020 Thomas McGrew

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

import wx

from extensions.lib.core import quick_scale

MENU = "&Image"
LABEL = "Image Size"
DESCRIPTION = "Scale The image using a fast, low quality algorithm"


def execute(width, height, data):
    """
    Scales an image using a fast, low quality algorithm.

    :Parameters:
        width : int
            The width of the image being converted
        height : int
            The height of the image being converted
        data : string
            A string containing the data for the image

    :rtype: tuple
    :returns: a tuple containing a width, height, and data as a binary string.
    """
    dialog = ScaleDialog(default_width = width, default_height = height)
    values = dialog.ShowModal()

    if not values:
        return False

    return quick_scale(width, height, data, *values)


class ScaleDialog(wx.Dialog):
    """
    A class for getting input values from the user for the scale filter
    """
    def __init__(self, parent=None, id=-1, ok_func = None,
            title="Scale Image", default_width=1024, default_height=768):
        """
        Initializes the dialog box.

        :Parameters:
            parent : wx.Frame
                The parent of this dialog. Defaults to None.
            id : int
                The id of this dialog. Defaults to -1
            ok_func : function
                An optional additional function to be called when the OK button
                is pressed. Defaults to None
            sliderUpdateFunction : function
                An an optional additional function to be called when one of the
                sliders is changed. Defaults to None.
            title : String
                The title of the dialog box to be displayed in the titlebar.
                Defaults to "Nintendize Options".
            maxResolution : int
                The maximim value to be available on the resolution slider.
                Defaults to 500.
        """
        wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition,
                (240, 165))

        self._width_entry  = wx.TextCtrl(self, -1, value = str(default_width),
                pos = (70, 35), size = (100, 20))
        self._height_entry = wx.TextCtrl(self, -1, value = str(default_height),
                pos = (70, 65), size = (100, 20))
        self._width_entry.SetMaxLength( 5)
        self._height_entry.SetMaxLength(5)

        self._display_panel   = wx.Panel(self, -1, pos=(180, 10), size=(70, 75))
        self._heading_display = wx.StaticText(self._display_panel, pos=(0,  0),
                label="Original")
        self._width_display   = wx.StaticText(self._display_panel, pos=(0, 25),
                label=str(default_width ))
        self._height_display  = wx.StaticText(self._display_panel, pos=(0, 55),
                label=str(default_height))

        self._label_panel  = wx.Panel(self, -1, pos=(10, 35), size=(50, 50))
        self._width_label  = wx.StaticText(self._label_panel, pos=(0,  0),
                label=" Width")
        self._height_label = wx.StaticText(self._label_panel, pos=(0, 30),
                label="Height")

        self._is_ok = False
        ok_button     = wx.Button(self, id = wx.ID_OK,     pos=( 30, 95),
                size=(80, 30))
        cancel_button = wx.Button(self, id = wx.ID_CANCEL, pos=(130, 95),
                size=(80, 30))

        if ok_func:
            self._ok_func = ok_func
        elif hasattr(self, "onOk"):
            self._ok_func = self.onOk
        else:
            self._ok_func = lambda x,y: None

        self._width_entry.Bind( wx.EVT_CHAR, self._validate)
        self._height_entry.Bind(wx.EVT_CHAR, self._validate)
        #self.Bind(wx.EVT_TEXT, self.)
        self.Bind(wx.EVT_CLOSE, self.cancel)
        ok_button.Bind(wx.EVT_BUTTON, self.ok)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel)

    def _validate(self, event):
        """
        Internal Function. Validates input by making sure only the proper
        keypresses are allowed.

        :Parameters:
            event : wx.Event
                The event that triggered the calling of this function. Not
                optional
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_RETURN:
            return self.ok()
        if key_code == wx.WXK_ESCAPE:
            return self.cancel()
        #                  the numbers 0-9
        if not key_code in (*range(48, 59), wx.WXK_BACK, wx.WXK_DELETE,
                wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_HOME, wx.WXK_END, wx.WXK_TAB):
            return
        event.Skip()

    def cancel(self, event=None):
        """
        Internal function. Called when the "Cancel" button is pressed.

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self.Destroy()

    def ok(self, event=None):
        """
        Internal function. Called when the "OK" button is pressed

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self._ok_func(int(self._width_entry.GetValue()),
                int(self._height_entry.GetValue()))
        self._is_ok = True
        self.Destroy()

    def ShowModal(self):
        """
        Displays the dialog window and waits for the user to click OK or Cancel
        to return a value.

        :rtype: tuple or boolean
        :returns: The values for resolution and color level in a tuple if OK is
            clicked. Returns False otherwise.
        """
        wx.Dialog.ShowModal(self)
        if self._is_ok:
            return (int(self._width_entry.GetValue()),
                    int(self._height_entry.GetValue()))
        return False
