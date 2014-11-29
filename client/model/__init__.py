import uuid as uuid_module
import utils

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

    def get_all_stats(self, date):
        """
            return a list of lists with all stats.
        """
        return [["Noname", "1","54.5","50","0.1", "alle"]]

    def get_plot_modes(self):
        """
            return a list of strings with all available plot modes.
        """
        return ["Not implemented"]

    def draw_plot(self, mode, axis, start=None, end=None):
        """
            plot the requested mode on the given matplotlib axis.
            The time interval is specified by the timestamps start and end.
        """
        pass


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




