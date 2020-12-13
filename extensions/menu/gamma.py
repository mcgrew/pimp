"""
gamma.py
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

from extensions.lib.core import table

MENU = "&Filter"
LABEL = "Brightness levels"
DESCRIPTION = "Adjust brightness, contrast, and gamma"



def execute(width, height, data, brightness=None, contrast=None, gamma=None):
    """
    Performs a gamma adjustment on an image. Brightness, contrast, and gamma
    are optional arguments. Either all 3 must be supplied, or none. A dialog
    will appear to request all 3 values if any of them are missing, in which
    case the passed in values are ignored.

    :Parameters:
        width : int
            The width of the image being converted
        height : int
            The height of the image being converted
        data : string
            A string containing the data for the image
        brightness : int
            The value of the change in brightness to apply.
        contrast : float
            The value of the change in contrast to apply.
        gamma : float
            The value of the change in gamma to apply.

    :rtype: tuple
    :returns: a tuple containing a width, height, and data as a binary string.
    """
    if None in (gamma, brightness, contrast):
        dialog = GammaDialog()
        values = dialog.ShowModal()

        if not values:
            return False

        gamma, brightness, contrast = values

    # build a substitution table
    subst_table = list(range(256))

    for i in range(256):
        subst_table[i] = max(min((subst_table[i] + brightness), 255), 0)
        subst_table[i] = min(int(subst_table[i] * contrast), 255)
        subst_table[i] = min(int(subst_table[i] ** gamma / 256 ** (gamma-1)), 255)

    return table(width, height, data, subst_table)




class GammaDialog(wx.Dialog):
    """
    A class for getting input values from the user for the nintendize filter
    """
    def __init__(self, parent=None, id=-1, ok_function=None,
            slider_update_func=None, title="Brightness Adjust"):
        """
        Initializes the dialog box.

        :Parameters:
            parent : wx.Frame
                The parent of this dialog. Defaults to None.
            id : int
                The id of this dialog. Defaults to -1
            ok_function : function
                An optional additional function to be called when the OK button
                is pressed. Defaults to None
            slider_update_func : function
                An an optional additional function to be called when one of the
                sliders is changed. Defaults to None.
            title : String
                The title of the dialog box to be displayed in the titlebar.
                Defaults to "Brightness Adjust".
        """
        wx.Dialog.__init__(self, parent, id, title, wx.DefaultPosition,
                (320, 180))

        self._brightness_slider = wx.Slider(self, -1, value=0, minValue=-255,
                maxValue=255, pos=(80, 10), size=(200, 30))
        self._contrast_slider   = wx.Slider(self, -1, value=1, minValue= -90,
                maxValue= 91, pos=(80, 40), size=(200, 30))
        self._gamma_slider      = wx.Slider(self, -1, value=1, minValue= -90,
                maxValue= 91, pos=(80, 70), size=(200, 30))

        self._display_panel = wx.Panel(self, -1, pos=(280, 10), size=(50, 100))
        self._brighntess_display = \
                wx.StaticText(self._display_panel, pos=(0,  5))
        self._contrast_display = wx.StaticText(self._display_panel, pos=(0, 35))
        self._gamma_display    = wx.StaticText(self._display_panel, pos=(0, 65))

        self._label_panel = wx.Panel(self, -1, pos = (10, 10), size = (70, 90))
        self.brightness_label = wx.StaticText(self._label_panel, pos = (0,  5),
                label="Brightness")
        self.brightness_label = wx.StaticText(self._label_panel, pos = (0, 35),
                label="Contrast"  )
        self._gamma_label      = wx.StaticText(self._label_panel, pos = (0, 65),
                label="Gamma"     )

        self._is_ok = False
        ok_button     = wx.Button(self, id = wx.ID_OK,     pos=( 65, 100),
                size=(80, 30))
        cancel_button = wx.Button(self, id = wx.ID_CANCEL, pos=(165, 100),
                size=(80, 30))

        if ok_function:
            self._ok_function = ok_function
        elif hasattr(self, "onOk"):
            self._ok_function = self.onOk
        else:
            self._ok_function = lambda x,y,z: None

        if slider_update_func:
            self._slider_update_func = slider_update_func
        elif hasattr(self, "onSliderupdate"):
            self._slider_update_func = self.onSliderupdate
        else:
            self._slider_update_func = lambda x,y,z: None

        self._gamma_value = 1
        self._brightness_value = 0
        self._contrast_value = 1
        self._update_display()


        self.Bind(wx.EVT_SLIDER, self._slider_change)
        self.Bind(wx.EVT_CLOSE, self.cancel)
        ok_button.Bind(wx.EVT_BUTTON, self.ok)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel)
#        self.ShowModal()

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
        self._ok_function(self._gamma_value, self._brightness_value,
                self._contrast_value)
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
        if self._gamma_slider.GetValue() >= 1:
            self._gamma_value = (self._gamma_slider.GetValue() + 9) / 10
        else:
            self._gamma_value = \
                    round((self._gamma_slider.GetValue() + 90) / 90, 2)

        self._brightness_value = self._brightness_slider.GetValue()

        if self._contrast_slider.GetValue() >= 1:
            self._contrast_value = (self._contrast_slider.GetValue() + 9) / 10
        else:
            self._contrast_value = \
                    round((self._contrast_slider.GetValue() + 90) / 90, 2)
        self._update_display()
        self._slider_update_func(self._gamma_value, self._brightness_value,
                self._contrast_value)

    def _update_display(self):
        """
        Internal Function. Called when one of the sliders is changed to update
        the values displayed.
        """
        self._gamma_display.SetLabel(     "%3.2f" % self._gamma_value     )
        self._brighntess_display.SetLabel("%3d"   % self._brightness_value)
        self._contrast_display.SetLabel(  "%3.2f" % self._contrast_value  )

    def ShowModal(self):
        """
        Displays the dialog window and waits for the user to click OK or Cancel
        to return a value.

        :rtype: tuple or boolean
        :returns: The values for gamma, brightness, and contrast values in a
        tuple if OK is clicked. Returns False otherwise.
        """
        wx.Dialog.ShowModal(self)
        if self._is_ok:
            return (self._gamma_value, self._brightness_value,
                    self._contrast_value)
        return False
