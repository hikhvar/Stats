#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import model.json_model
import model.sqlite_model

class DefaultSettings(object):

    def __init__(self):
        self.date_chooseable = False
        self.enable_delete = False
        self.model = None


class JSONSettings(DefaultSettings):

    def __init__(self):
        super(JSONSettings, self).__init__(self)
        self.store_dir = "data"
        self.schuetzen_file = "schuetzen.json.gz"
        self.data_file = "data.json.gz"
        self.event_file = "events.json.gz"
        self.model = model.json_model.CompressedJSONModel


class SQLiteSettings(DefaultSettings):

    def __init__(self):
        super(SQLiteSettings, self).__init__(self)
        self.database_file = "data/database.db"
        self.model = model.sqlite_model.SQLiteModel
