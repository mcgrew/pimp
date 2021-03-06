"""
nintendize.py
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

from extensions.lib import nintendize

MENU = "Fil&ter.&Comic"
LABEL = "Nintendi&ze"
DESCRIPTION = "Nintendize it!"

def execute(width, height, data, resolution=None, color_level=None):
    """
    Pixellates the image and reduces bit quality in a way such that it
    looks like an image from an old video game console. Resolution and
    colorLevel are optional, either both or none should be provided. A
    dialog will appear requesting both values if one is not supplied,
    in which case the passed in values are ignored.

    :Parameters:
        filename : string
            The name of the file to write to.
        width : int
            The width of the image in pixels
        height : int
            The height of the image in pixels
        data : string
            The data as a string - chr(red) + chr(green) + chr(blue) for each
            pixel.
        resolution : int
            The resolution value to apply to the image.
        colorLevel : int
            The colorLevel value to apply to the image

    :rtype: tuple
    :returns: A tuple (width, height, data). Width and height are in pixels,
        data is a binary string.
    """
    if None in (resolution, color_level):
        dialog = NintendizeDialog(max_resolution = min(width, height))
        values = dialog.ShowModal()

        if not values:
            return False

        resolution, colorlevel = values

    return nintendize.execute(width, height, data, resolution, colorlevel)


class NintendizeDialog(wx.Dialog):
    """
    A class for getting input values from the user for the nintendize filter
    """
    def __init__(self, parent=None, id=-1, ok_func=None,
            slider_update_func=None, title="Nintendize Options",
            max_resolution=500):
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
                Defaults to "Nintendize Options".
            max_resolution : int
                The maximim value to be available on the resolution slider.
                Defaults to 500.
        """
        wx.Dialog.__init__(self, parent, id, title,
                wx.DefaultPosition,(330, 140))

        self._resolution_value = 200
        self._color_level_value = 2

        self._resolution_slider = wx.Slider(self, -1,
                value=self._resolution_value, minValue=1,
                maxValue=max_resolution, pos=(80, 10), size=(200, 30))
        self._color_level_slider = wx.Slider(self, -1,
                value=self._color_level_value, minValue= 1, maxValue=8,
                pos=(80, 40), size=(200, 30))

        self._display_panel = wx.Panel(self, -1, pos=(280, 10), size=(60, 100))
        self._resolution_display = wx.StaticText(self._display_panel, pos=(0,  5))
        self._color_level_display = wx.StaticText(self._display_panel, pos=(0, 35))

        self._label_panel = wx.Panel(self, -1, pos=(10, 10), size=(70, 60))
        self._resolution_label = wx.StaticText(self._label_panel, pos=(0,  5),
                label="Resolution")
        self._color_level_label = wx.StaticText(self._label_panel, pos=(0, 35),
                label="Color Level")

        self._is_ok = False
        ok_button     = wx.Button(self, id=wx.ID_OK,     pos=( 65, 70),
                size=(80, 30))
        cancel_button = wx.Button(self, id=wx.ID_CANCEL, pos=(165, 70),
                size=(80, 30))

        if ok_func:
            self._ok_func = ok_func
        elif hasattr(self, "onOk"):
            self._ok_func = self.onOk
        else:
            self._ok_func = lambda x,y: None

        if slider_update_func:
            self._slider_update_func = slider_update_func
        elif hasattr(self, "onSliderupdate"):
            self._slider_update_func = self.onSliderupdate
        else:
            self._slider_update_func = lambda x,y: None

        self._update_display()


        self.Bind(wx.EVT_SLIDER, self.sliderChange)
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
        self._ok_func(self._resolution_value, self._color_level_value)
        self._is_ok = True
        self.Destroy()

    def sliderChange(self, event=None):
        """
        Internal Function. Called when one of the sliders is changed within the
        dialog box.

        :Parameters:
            event : wx.Event
                Event generated by clicking a button. The argument is ignored.
        """
        self._resolution_value = self._resolution_slider.GetValue()
        self._color_level_value = self._color_level_slider.GetValue()

        self._update_display()
        self._slider_update_func(self._resolution_value,
                self._color_level_value)

    def _update_display(self):
        """
        Internal Function. Called when one of the sliders is changed to update
        the values displayed.
        """
        self._resolution_display.SetLabel("%5d" % self._resolution_value)
        self._color_level_display.SetLabel("%3d" % self._color_level_value)

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
            return (self._resolution_value, self._color_level_value)
        return False


