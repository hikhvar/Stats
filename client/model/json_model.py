#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pandas as pd
import os.path
import os
import json
import utils
import numpy as np
import pprint
from model import Model, Schuetze, Satz, Event
import uuid
import plots
import gzip

class JSONModel(Model):
    """
        A JSON based model. Stores everything in a JSON file. 
        On Start load it from from the file. 
        For each entry append it to the file.
    """

    def __init__(self, settings):
        super(JSONModel, self).__init__(settings)
        self.openfunction = open
        self.data = []
        self.schuetzen = []
        self.events = []

    def load(self):
        """
            load the data from store dir or create store dir
            if not exists.
        """
        if os.path.exists(self.settings.store_dir):
            self.data = self._load_data(self.settings.store_dir)
            self.schuetzen = self._load_schuetzen(self.settings.store_dir)
            self.events = self._load_events(self.settings.store_dir)
        else:
            os.makedirs(self.settings.store_dir)

    def _generic_load_data(self, filename, cls):
        data = []
        filepath = os.path.join(self.settings.store_dir, filename)
        if not os.path.exists(filepath):
            return data
        with self.openfunction(filepath, "r") as f:
            for line in f:
                instance = cls.from_json(line)
                data.append(instance)
        return data

    def _load_data(self, dirpath):
        """
            load the data from the file.
        """
        return self._generic_load_data(self.settings.data_file, JSONSatz)

    def _load_schuetzen(self, dirpath):
        return self._generic_load_data(self.settings.schuetzen_file, JSONSchuetze)

    def _load_events(self, dirpath):
        return self._generic_load_data(self.settings.event_file, JSONEvent)

    def _generic_add_data(self, obj, filename):
        filepath = os.path.join(self.settings.store_dir, filename)
        with self.openfunction(filepath, "a") as f:
            string = obj.to_json()
            f.write(string)
            f.write("\n")

    def _gerneric_rewrite_data(self, datalist, filename):
        filepath = os.path.join(self.settings.store_dir, filename)
        with self.openfunction(filepath, "w") as f:
            for obj in datalist:
                f.write(obj.to_json())
                f.write("\n")

    def schuetze_exists(self, fullname):
        """
            return true if there is a schuetze
            with this full name.
        """
        schuetzen = self.get_all_schuetzen()
        for s in schuetzen:
            if s.get_fullname() == fullname:
                return True
        return False

    def add_schuetze(self, name, surname):
        """
            add the schuetze with the given name and surname.
        """
        new = JSONSchuetze(name, surname)
        if not self.schuetze_exists(new.get_fullname()):
            self.schuetzen.append(new)
            self._generic_add_data(new, self.settings.schuetzen_file)
            return True
        else:
            return False

    def add_satz(self, fullname, result, date):
        s = self.get_schuetze_by_fullname(fullname)
        entry = JSONSatz(
            schuetze_uuid=s.uuid,
            result=result,
            date=utils.to_timestamp(date))
        self.data.append(entry)
        self._generic_add_data(entry, self.settings.data_file)

    def add_event(self, date, description):
        entry = JSONEvent(
            date=utils.to_timestamp(date),
            description=description)
        self.events.append(entry)
        self._generic_add_data(entry, self.settings.event_file)

    def delete_schuetze(self, fullname):
        """
            Delete the schuetze with this fullname.
        """
        dels = self.get_schuetze_by_fullname(fullname)
        if dels is not None:
            remove = []
            for entry in self.data:
                if entry.schuetze_uuid == dels.uuid:
                    remove.append(entry)
            for entry in remove:
                self.data.remove(entry)
            self.schuetzen.remove(dels)
            self._gerneric_rewrite_data(self.schuetzen, self.settings.schuetzen_file)
            self._gerneric_rewrite_data(self.data, self.settings.data_file)

    def delete_satz(self, uuids):
        """
            delete the given set/list of satze identified by their uuid.
        """
        remove = []
        for entry in self.data:
            if entry.uuid in uuids:
                remove.append(entry)
        for entry in remove:
            self.data.remove(entry)
        self._gerneric_rewrite_data(self.data, self.settings.data_file)

    def delete_events(self, uuids):
        remove = []
        for entry in self.events:
            if entry.uuid in uuids:
                remove.append(entry)
        for entry in remove:
            self.events.remove(entry)
        self._gerneric_rewrite_data(self.events, self.settings.event_file)

    def get_all_schuetzen(self):
        return self.schuetzen

    def get_all_dates(self):
        dates = set([])
        for entry in self.data:
            dates.add(entry.date)
        if len(dates) == 0:
            return None
        dates = sorted(list(dates))
        dates = map(lambda x: utils.to_human_readable(x), dates)
        return dates

    def get_all_satz_entries(self):
        return self.data

    def get_all_event_entries(self):
        return self.events

class CompressedJSONModel(JSONModel):

    def __init__(self, settings):
        super(CompressedJSONModel, self).__init__(settings)
        self.openfunction = gzip.open


class JSONSchuetze(Schuetze):

    @classmethod
    def from_json(cls, jsonstring):
        dic = json.loads(jsonstring)
        dic["uuid"] = uuid.UUID(dic["uuid"])
        return cls(**dic)

    def to_json(self):
        dic = {
            "name":self.name,
            "surname": self.surname,
            "uuid": str(self.uuid)
        }
        return json.dumps(dic)


class JSONEvent(Event):

    @classmethod
    def from_json(cls, jsonstring):
        d = json.loads(jsonstring)
        d["date"] = float(d["date"])
        if "uuid" in d:
            d["uuid"] = uuid.UUID(d["uuid"])
        return cls(**d)

    def to_json(self):
        dic = {
            "date": self.date,
            "description": self.description,
            "uuid": str(self.uuid)
        }
        return json.dumps(dic)

    def __repr__(self):
        return "JSONEvent[date=%s,uuid=%s]" % (self.date, str(self.uuid))


class JSONSatz(Satz):

    @classmethod
    def from_json(cls, jsonstring):
        d = json.loads(jsonstring)
        d["date"] = float(d["date"])
        d["result"] = float(d["result"])
        d["schuetze_uuid"] = uuid.UUID(d["schuetze_uuid"])
        if "uuid" in d:
            d["uuid"] = uuid.UUID(d["uuid"])
        return cls(**d)

    def to_json(self):
        dic = self.to_dict()
        dic["uuid"] = str(dic["uuid"])
        dic["schuetze_uuid"] = str(dic["schuetze_uuid"])
        return json.dumps(dic)