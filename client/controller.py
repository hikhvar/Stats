#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from settings import DefaultSettings
import datetime
import utils
import wx
import model.plots as plots

class Controller(object):

    def __init__(self):
        self.settings = DefaultSettings()
        self.model = self.settings.model(self.settings)
        self.model.load()

    def set_mainframe(self, mainframe):
        self.mainframe = mainframe
        self._update_comboboxes()
        self.mainframe.SatzDeleteListCtrl.set_model(self.model)
        self.mainframe.EventDeleteCtrl.set_model(self.model)
        self._apply_settings_entries()

    def OnEintrag(self, event):
        date = self.mainframe.datepicker_ctrl_eintrag.GetValue()
        date = self._to_datetime(date)
        result = self.mainframe.text_ctrl_satz.GetValue()
        result = float(result.replace(",","."))
        self.mainframe.text_ctrl_satz.SetValue("")
        schuetze = self.mainframe.combo_box_schuetze.GetValue()
        if result > 54.5 or result < 0:
            wx.MessageBox('Wurden die Scheiben ausgetauscht?', 'Fehler', 
                wx.OK | wx.ICON_EXCLAMATION)
        else:
            self.model.add_satz(schuetze, result, date)
            self._update_comboboxes()

    def OnChangeStatsTermin(self, event):
        date = self.mainframe.combo_box_stats_pro_termin.GetValue()
        date = utils.from_human_readable(date)
        data = self.model.get_all_stats(date)
        self.mainframe.SchuetzenListCtrl.update_data(data)

    def OnPlotModeChange(self, event):
        mode = self.mainframe.combo_box_plot_mode.GetValue()
        start_date = self.mainframe.combo_box_plot_start.GetValue()
        if start_date == "":
            start_date = None
        else:
            start_date = utils.from_human_readable(start_date)
        end_date = self.mainframe.combo_box_plot_end.GetValue()
        if end_date == "":
            end_date = None
        else:
            end_date = utils.from_human_readable(end_date)
        axis = self.mainframe.panel_matplotlib.axes
        df = self.model.get_pandas_dataframe()
        events = self.model.events
        plots.draw_plot(mode, axis, df, events, start_date, end_date)
        self.mainframe.panel_matplotlib.canvas.draw()

    def OnCreate(self, event):
        name = self.mainframe.text_ctrl_new_name.GetValue()
        surname = self.mainframe.text_ctrl_new_surname.GetValue()
        self.mainframe.text_ctrl_new_name.SetValue("")
        self.mainframe.text_ctrl_new_surname.SetValue("")
        if not self.model.add_schuetze(name, surname):
            wx.MessageBox('Schütze existiert bereits', 'Fehler', 
                wx.OK | wx.ICON_ERROR)
        self._update_comboboxes()

    def OnDelete(self, event):
        index = self.mainframe.choice_delete.GetSelection()
        name = self.mainframe.choice_delete.GetString(index)
        self.model.delete_schuetze(name)
        self.settings.enable_delete = False
        self._apply_settings_entries()
        self._update_comboboxes()

    def OnDateEditableChange(self, event):
        self.settings.date_chooseable = event.IsChecked()
        self._apply_settings_entries()

    def OnSatzDelete(self, event):
        deleted = self.mainframe.SatzDeleteListCtrl.deleted.keys()
        self.model.delete_satz(deleted)
        self.settings.enable_delete = False
        self._apply_settings_entries()
        self._update_comboboxes()

    def OnEventDelete(self, event):
        deleted = self.mainframe.EventDeleteCtrl.deleted.keys()
        self.model.delete_events(deleted)
        self.settings.enable_delete = False
        self._apply_settings_entries()
        self._update_comboboxes()

    def OnEventEntry(self, event):
        description = self.mainframe.text_ctrl_event_description.GetValue()
        self.mainframe.text_ctrl_event_description.SetValue("")
        date = self.mainframe.datepicker_ctrl_event.GetValue()
        date = self._to_datetime(date)
        self.model.add_event(date, description)
        self._update_comboboxes()

    def OnDeleteEnable(self, event):
        self.settings.enable_delete = event.IsChecked()
        self._apply_settings_entries()

    def _apply_settings_entries(self):
        self.mainframe.DateChangeAbleMenu.Check(self.settings.date_chooseable)
        self.mainframe.DeleteEnableMenu.Check(self.settings.enable_delete)
        self.mainframe.button_delete.Enable(self.settings.enable_delete)
        self.mainframe.satz_delete.Enable(self.settings.enable_delete)
        self.mainframe.button_event_delete.Enable(self.settings.enable_delete)
        self.mainframe.datepicker_ctrl_eintrag.Enable(self.settings.date_chooseable)
    
    def _update_comboboxes(self):
        schuetzen = self.model.get_all_schuetzen()
        schuetzen = map(lambda x: x.get_fullname(), schuetzen)
        if schuetzen is not None:
            self.mainframe.combo_box_schuetze.SetItems(schuetzen)
            self.mainframe.choice_delete.SetItems(schuetzen)
        dates = self.model.get_all_dates()
        if dates is not None:
            self.mainframe.combo_box_stats_pro_termin.SetItems(dates)
            self.mainframe.combo_box_plot_start.SetItems(dates)
            self.mainframe.combo_box_plot_end.SetItems(dates)
        plot_modes = plots.get_plot_modes()
        if plot_modes is not None:
            self.mainframe.combo_box_plot_mode.SetItems(plot_modes)
        self.mainframe.SatzDeleteListCtrl.update_data()
        self.mainframe.EventDeleteCtrl.update_data()

    def _to_datetime(self, wxDateTime):
        """
            convert wx._misc.DateTime to datetime.datetime object.
        """
        year = wxDateTime.GetYear()
        month = wxDateTime.GetMonth() + 1
        day = wxDateTime.GetDay()
        return datetime.datetime(year, month, day)