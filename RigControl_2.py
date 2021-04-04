#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.1 on Sat Apr  3 20:58:16 2021
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class RigControl(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: RigControl.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("frame")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        rigPanel = wx.BoxSizer(wx.VERTICAL)

        top = wx.BoxSizer(wx.HORIZONTAL)
        rigPanel.Add(top, 1, wx.EXPAND, 0)

        top_col1 = wx.BoxSizer(wx.VERTICAL)
        top.Add(top_col1, 1, wx.EXPAND, 0)

        meter_levels = wx.BoxSizer(wx.VERTICAL)
        top_col1.Add(meter_levels, 1, wx.EXPAND, 0)

        self.acl_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        self.acl_level.SetToolTip(wx.ToolTip("ALC"))
        meter_levels.Add(self.acl_level, 0, wx.ALL | wx.EXPAND, 6)

        self.power_level = wx.Gauge(self.panel_1, wx.ID_ANY, 100)
        self.power_level.SetToolTip(wx.ToolTip("PWR"))
        meter_levels.Add(self.power_level, 0, wx.ALL | wx.EXPAND, 5)

        self.swr_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        self.swr_level.SetToolTip(wx.ToolTip("SWR"))
        meter_levels.Add(self.swr_level, 0, wx.EXPAND, 0)

        self.empty_box_01 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "This box is left empty on purpose", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        top_col1.Add(self.empty_box_01, 0, wx.ALL, 1)

        top_col2 = wx.GridSizer(2, 1, 0, 0)
        top.Add(top_col2, 1, wx.EXPAND, 0)

        self.vfoA_set = wx.ToggleButton(self.panel_1, wx.ID_ANY, "VFO A")
        self.vfoA_set.Enable(False)
        top_col2.Add(self.vfoA_set, 0, 0, 0)

        self.vfoB_set = wx.ToggleButton(self.panel_1, wx.ID_ANY, "VFO B")
        self.vfoB_set.Enable(False)
        top_col2.Add(self.vfoB_set, 0, 0, 0)

        top_col3 = wx.BoxSizer(wx.VERTICAL)
        top.Add(top_col3, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        top_col3.Add(sizer_3, 1, wx.ALL | wx.EXPAND, 1)

        mode = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(mode, 1, wx.EXPAND, 0)

        self.mode_am = wx.ToggleButton(self.panel_1, wx.ID_ANY, "AM")
        mode.Add(self.mode_am, 0, 0, 0)

        self.mode_usb = wx.ToggleButton(self.panel_1, wx.ID_ANY, "USB")
        mode.Add(self.mode_usb, 0, 0, 0)

        self.mode_lsb = wx.ToggleButton(self.panel_1, wx.ID_ANY, "LSB")
        mode.Add(self.mode_lsb, 0, 0, 0)

        self.mode_cw = wx.ToggleButton(self.panel_1, wx.ID_ANY, "CW")
        mode.Add(self.mode_cw, 0, 0, 0)

        self.mode_fm = wx.ToggleButton(self.panel_1, wx.ID_ANY, "FM")
        mode.Add(self.mode_fm, 0, 0, 0)

        self.mode_cwr = wx.ToggleButton(self.panel_1, wx.ID_ANY, "CWR")
        mode.Add(self.mode_cwr, 0, 0, 0)

        self.freq_active_freq = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.freq_active_freq.SetFont(wx.Font(24, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Sans"))
        sizer_3.Add(self.freq_active_freq, 0, wx.EXPAND, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        top_col3.Add(sizer_4, 1, wx.EXPAND, 0)

        self.s_meter_level = wx.Gauge(self.panel_1, wx.ID_ANY, 20)
        sizer_4.Add(self.s_meter_level, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.freq_standby_freq = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.freq_standby_freq.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Sans"))
        sizer_4.Add(self.freq_standby_freq, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        top_col4 = wx.BoxSizer(wx.HORIZONTAL)
        top.Add(top_col4, 1, wx.EXPAND, 0)

        grid_sizer_1 = wx.GridSizer(3, 3, 0, 0)
        top_col4.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        self.button_1 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_1")
        grid_sizer_1.Add(self.button_1, 0, 0, 0)

        self.button_2 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_2")
        grid_sizer_1.Add(self.button_2, 0, 0, 0)

        self.button_3 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_3")
        grid_sizer_1.Add(self.button_3, 0, 0, 0)

        self.button_4 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_4")
        grid_sizer_1.Add(self.button_4, 0, 0, 0)

        self.button_5 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_5")
        grid_sizer_1.Add(self.button_5, 0, 0, 0)

        self.button_6 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_6")
        grid_sizer_1.Add(self.button_6, 0, 0, 0)

        self.button_7 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_7")
        grid_sizer_1.Add(self.button_7, 0, 0, 0)

        self.button_8 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_8")
        grid_sizer_1.Add(self.button_8, 0, 0, 0)

        self.button_9 = wx.ToggleButton(self.panel_1, wx.ID_ANY, "button_9")
        grid_sizer_1.Add(self.button_9, 0, 0, 0)

        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        top_col4.Add(sizer_5, 1, wx.EXPAND, 0)

        self.select_mode = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.select_mode, 0, 0, 0)

        self.select_data_mode = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.select_data_mode, 0, 0, 0)

        self.select_filter = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.select_filter, 0, 0, 0)

        self.select_agc = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.select_agc, 0, 0, 0)

        self.select_att = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.select_att, 0, 0, 0)

        self.select_preamp = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_5.Add(self.select_preamp, 0, 0, 0)

        middle = wx.BoxSizer(wx.HORIZONTAL)
        rigPanel.Add(middle, 1, wx.EXPAND, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "Something nifty goes here later")
        middle.Add(self.text_ctrl_1, 0, 0, 0)

        bottom = wx.BoxSizer(wx.HORIZONTAL)
        rigPanel.Add(bottom, 1, wx.EXPAND, 0)

        bottom_col1 = wx.BoxSizer(wx.VERTICAL)
        bottom.Add(bottom_col1, 1, wx.EXPAND, 0)

        self.af_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col1.Add(self.af_level, 0, wx.EXPAND, 0)

        self.agc_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col1.Add(self.agc_level, 0, wx.EXPAND, 0)

        self.nr_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col1.Add(self.nr_level, 0, wx.EXPAND, 0)

        self.pbt_low_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col1.Add(self.pbt_low_level, 0, wx.EXPAND, 0)

        bottom_col2 = wx.BoxSizer(wx.VERTICAL)
        bottom.Add(bottom_col2, 1, wx.EXPAND, 0)

        self.rf_gain_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col2.Add(self.rf_gain_level, 0, wx.EXPAND, 0)

        self.rf_power_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col2.Add(self.rf_power_level, 0, wx.EXPAND, 0)

        self.nb_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col2.Add(self.nb_level, 0, wx.EXPAND, 0)

        self.pbt_high_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col2.Add(self.pbt_high_level, 0, wx.EXPAND, 0)

        bottom_col3 = wx.BoxSizer(wx.VERTICAL)
        bottom.Add(bottom_col3, 1, wx.EXPAND, 0)

        self.filter_width = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col3.Add(self.filter_width, 0, wx.EXPAND, 0)

        self.lcd_brightness = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col3.Add(self.lcd_brightness, 0, wx.EXPAND, 0)

        self.nb_depth_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col3.Add(self.nb_depth_level, 0, wx.EXPAND, 0)

        bottom_col4 = wx.BoxSizer(wx.VERTICAL)
        bottom.Add(bottom_col4, 1, wx.EXPAND, 0)

        self.if_shift = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col4.Add(self.if_shift, 0, wx.EXPAND, 0)

        self.notch_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col4.Add(self.notch_level, 0, wx.EXPAND, 0)

        self.nb_width_level = wx.Gauge(self.panel_1, wx.ID_ANY, 10)
        bottom_col4.Add(self.nb_width_level, 0, wx.EXPAND, 0)

        self.panel_1.SetSizer(rigPanel)

        self.Layout()
        # end wxGlade

# end of class RigControl

class MyApp(wx.App):
    def OnInit(self):
        self.frame = RigControl(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
