#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import wx.lib.mixins.listctrl
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import utils

class SchuetzenListCtrl(wx.ListCtrl, wx.lib.mixins.listctrl.ColumnSorterMixin):

    def __init__(self, parent, schuetzen=[]):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES)
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 5)
        self.InsertColumn(0,"Schuetze", width=wx.LIST_AUTOSIZE)
        self.InsertColumn(1,"Schlechtester", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.InsertColumn(2,"Bester", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.InsertColumn(3,"Mittelwert", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.InsertColumn(4,"Standard Abweichung", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.InsertColumn(5,"Alle", width=wx.LIST_AUTOSIZE)
        self.itemDataMap = schuetzen
        self.SetItemCount(len(schuetzen))
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)

    def OnColClick(self,event):
        event.Skip()

    def OnGetItemText(self, item, col):
        s = self.itemDataMap[item][col]
        return str(s)

    def GetListCtrl(self):
        return self

    def update_data(self, schuetzen):
        valid = isinstance(schuetzen, list)
        if not valid:
            return False
        columns = self.GetColumnCount()
        for value in schuetzen:
            valid = valid and len(value) == columns
        if not valid:
            return False 
        self.itemDataMap = schuetzen
        self.SetItemCount(len(self.itemDataMap))
        self.Refresh()


class PlotPanel(wx.Panel):

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

        #x = range(1, 20)
        #y = map(lambda x: x*x, x)
        #self.axes.plot(x,y)

class SatzCheckListCtrl(wx.ListCtrl, wx.lib.mixins.listctrl.CheckListCtrlMixin):

    def __init__(self, parent, *args, **kwargs):
        wx.ListCtrl.__init__( self, parent, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        wx.lib.mixins.listctrl.CheckListCtrlMixin.__init__(self)
        self._make_clear()
        self.data = []
        self.deleted = {}
        self.model = None

    def set_model(self, model):
        self.model = model
        self.update_data()

    def _make_clear(self):
        """
            first delete all columns than reset them empty.
        """
        self.ClearAll()
        self.InsertColumn(0,"Schuetze", width=wx.LIST_AUTOSIZE)
        self.InsertColumn(1,"Datum", width=wx.LIST_AUTOSIZE)
        self.InsertColumn(2,"Ringe", width=wx.LIST_AUTOSIZE)
        self.InsertColumn(3,"UUID", width=wx.LIST_AUTOSIZE)

    def update_data(self):
        if self.model is None:
            return
        self.data = []
        self._make_clear()
        for entry in self.model.data:
            self.data.append(entry)
            sch = self.model.get_schuetze_by_uuid(entry.schuetze_uuid)
            info = [sch.get_fullname(), entry.get_human_readable_date(), entry.result, str(entry.uuid)]
            self.Append(info)
        for col in xrange(4):
            if col == 2:
                self.SetColumnWidth(col, -2)
            else:
                self.SetColumnWidth(col, -1)

    def OnCheckItem(self, index, flag):
        obj = self.data[index]
        if not flag:
            del self.deleted[obj.uuid]
        else:
            self.deleted[obj.uuid] = obj
