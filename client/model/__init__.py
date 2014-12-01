import uuid as uuid_module
import utils
import collections
import pandas as pd
import numpy as np

class Model (object):
    """
        Dummy Class for testing.
    """

    def __init__(self, settings):
        self.settings = settings

    def add_satz(self, schuetze, result, date):
        print "Added", schuetze, result, date
        print "Add not implemented"

    def add_schuetze(self, name, surname):
        """
            add the schuetze with the given name and surname.
        """
        print "Added schuetze", name, surname

    def get_all_schuetzen(self):
        """ 
            returns a list of Schuetzen
        """
        return [Schuetze("No", "Name")]

    def get_all_dates(self):
        """ 
            return a list of dates with shooting results.
        """
        return ["1.1.2013"]

    def get_all_satz_entries(self):
        """
            return a list of all Satz objects 
            stored in the model.
        """
        return [Satz()]

    def get_all_event_entries(self):
        """
            return a list of all Event objects
            stored in the model.
        """
        return [Event()]

    def get_schuetze_by_uuid(self, uuid):
        schuetzen = self.get_all_schuetzen()
        for s in schuetzen:
            if s.uuid == uuid:
                return s

    def get_schuetze_by_fullname(self, fullname):
        schuetzen = self.get_all_schuetzen()
        for s in schuetzen:
            if s.get_fullname() == fullname:
                return s

    def get_pandas_dataframe(self):
        def uuid_mapping(uuid):
            s = self.get_schuetze_by_uuid(uuid)
            return s.get_fullname()
        data = collections.defaultdict(list)
        for entry in self.get_all_satz_entries():
            for key, value in entry.to_dict(uuid_mapping).iteritems():
                data[key].append(value)
        df = pd.DataFrame(data)
        if len(df) >= 1:
            df['human_readable'] = df.date.apply(utils.to_human_readable)
        return df

    def get_all_stats(self, date):
        df = self.get_pandas_dataframe()
        df = df[df.date == date]
        grouped = df.groupby(df.schuetze)
        agg = grouped["result"].agg(func=[min, max, np.mean, np.std])
        retval = []
        for schuetze, values in agg.iterrows():
            tmp = [schuetze]
            tmp.append(round(values["min"],1))
            tmp.append(round(values["max"],1))
            tmp.append(round(values["mean"],2))
            tmp.append(round(values["std"],3))
            results = list(grouped["result"].get_group(schuetze))
            results = map(lambda x: round(x,1), results)
            tmp.append(str(results)[1:-1])
            
            retval.append(tmp)
        return retval

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

    def get_all_dates(self):
        dates = set([])
        for entry in self.get_all_satz_entries():
            dates.add(entry.date)
        if len(dates) == 0:
            return None
        dates = sorted(list(dates))
        dates = map(lambda x: utils.to_human_readable(x), dates)
        return dates


class Schuetze(object):

    def __init__(self, name=None, surname=None, uuid=None):
        self.name = name
        self.surname = surname
        if uuid is None:
            self.uuid = uuid_module.uuid4()
        else:
            self.uuid = uuid

    def get_fullname(self):
        return "%s %s" % (self.name, self.surname)

    def __str__(self):
        return "name: %s, surname: %s, uuid: %s" % (self.name, self.surname, self.uuid)


class Event(object):

    def __init__(self, date=None, description=None, uuid=None):
        self.date = date
        self.description = description
        if uuid is None:
            self.uuid = uuid_module.uuid4()
        else:
            self.uuid = uuid

    def get_human_readable_date(self):
        return utils.to_human_readable(self.date)


class Satz(object):

    def __init__(self, schuetze_uuid=None, date=None, result=None, uuid=None):
        self.schuetze_uuid = schuetze_uuid
        self.date = date
        self.result = result
        self.delete = False
        if uuid is None:
            self.uuid = uuid_module.uuid4()
        else:
            self.uuid = uuid

    def to_dict(self, uuid_mapping=None):
        """
            uuid_mapping is a function which get the uuid 
            of a schuetze and return his fullname.
            If not given, the schuetze field in the data 
            dictionary is not set.
        """
        dic = {
            "schuetze_uuid": self.schuetze_uuid,
            "date": self.date,
            "result": self.result,
            "uuid": self.uuid
        }
        if uuid_mapping is not None:
            fullname = uuid_mapping(self.schuetze_uuid)
            dic["schuetze"] = fullname
        return dic

    def get_human_readable_date(self):
        return utils.to_human_readable(self.date)