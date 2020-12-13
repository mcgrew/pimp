"""
nintendize.py
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

import wx

from extensions.lib import median_filter

MENU = "Fil&ter"
LABEL = "&Median Filter"
DESCRIPTION = "Smooths an image by making each pixel appear more like it's " \
        "neighboring pixels"

def execute(width, height, data, filter_size=None):
    """
    Smooths an image by making each pixel appear more like it's neighboring
    pixels.

    :Parameters:
        filename : string
            The name of the file to write to.
        width : int
            The width of the image in pixels
        height : int
            The height of the image in pixels
        data : string
            The data as a binary string.
        filter_size : int
            The size of the filter to be applied to the image. A dialog box will
            request this value if it is not supplied.

    :rtype: tuple
    :returns: a tuple containing a width, height, and data as a binary string.
    """
    if filter_size is None:
        dialog = MedianFilterDialog()
        values = dialog.ShowModal()

        if not values:
            return False

        filter_size = values

    return median_filter.execute(width, height, data, filter_size)


class MedianFilterDialog(wx.Dialog):
    """
    A class for getting input values from the user for the nintendize filter
    """
    def __init__(self, parent=None, id=-1, ok_func=None,
            slider_update_func=None, title="Median Filter Options"):
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
            slider_update_func : function
                An an optional additional function to be called when one of the
                sliders is changed. Defaults to None.
            title : String
                The title of the dialog box to be displayed in the titlebar.
                Defaults to "Median Filter Options".
        """
        wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition,
                (320, 130))

        self._filter_size_val = 3

        self.filterSizeSlider   = wx.Slider(self, -1,
                value=self._filter_size_val, minValue=3, maxValue=15,
                pos=(80, 10), size=(200, 30))

        self._display_panel = wx.Panel(self, -1, pos=(280, 10), size=(50, 30))
        self._filter_size_display = \
                wx.StaticText(self._display_panel, pos=(0, 5))

        self._label_panel = wx.Panel(self, -1, pos = (10, 10), size = (70, 30))
        self._filter_size_label = wx.StaticText(self._label_panel, pos=(0, 5),
                label="Filter Size"  )

        self._is_ok = False
        ok_button     = wx.Button(self, id = wx.ID_OK,
                pos=(65, 50), size=(80, 30))
        cancel_button = wx.Button(self, id = wx.ID_CANCEL,
                pos=(165, 50), size=(80, 30))

        if ok_func:
            self._ok_func = ok_func
        elif hasattr(self, "onOk"):
            self._ok_func = self.onOk
        else:
            self._ok_func = lambda x: None # a dummy function

        if slider_update_func:
            self._slider_update_func = slider_update_func
        elif hasattr(self, "onSliderupdate"):
            self._slider_update_func = self.onSliderupdate
        else:
            self._slider_update_func = lambda x: None # a dummy function

        self._update_display()


        self.Bind(wx.EVT_SLIDER, self._slider_change)
        self.Bind(wx.EVT_CLOSE, self.cancel)
        ok_button.Bind(wx.EVT_BUTTON, self.ok)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel)

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
        self._ok_func(self._filter_size_val)
        self._is_ok = True
        self.Destroy()

    def _slider_change(self, event=None):
        """
        Internal Function. Called when one of the sliders is changed within the
        dialog box.

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self._filter_size_val = self.filterSizeSlider.GetValue()

        self._update_display()
        self._slider_update_func(self._filter_size_val)

    def _update_display(self):
        """
        Internal Function. Called when one of the sliders is changed to update
        the values displayed.
        """
        self._filter_size_display.SetLabel("%2d" % self._filter_size_val)

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
            return self._filter_size_val
        return False
