#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import model.json_model

class DefaultSettings(object):

    def __init__(self):
        self.date_chooseable = False
        self.enable_delete = False
        self.store_dir = "data"
        self.schuetzen_file = "schuetzen.json"
        self.data_file = "data.json"
        self.model = model.json_model.JSONModel