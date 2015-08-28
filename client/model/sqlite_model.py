__author__ = 'christoph'

from model import Model, Schuetze, Satz, Event
import sqlite3
import os.path

class SQLiteModel(Model):


    def __init__(self, settings):
        super(SQLiteModel, self).__init__(settings)
        self.connection = self._get_connection()

    def _init_database(self):
        if os.path.isfile(self.settings.database_file):
            pass
        else:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute("""CREATE TABLE schuetzen (id INTEGER PRIMARY KEY, name TEXT, surname TEXT, uuid TEXT).""")
            cur.execute("""CREATE TABLE satz (id INTEGER PRIMARY KEY,  schuetzen_id INTEGER, date TEXT, result REAL, uuid TEXT, FOREIGN KEY(schuetzen_id) REFERENCES schuetzen(id))""")
            cur.execute("""CREATE TABLE event (id INTEGER PRIMARY KEY, date TEXT, description TEXT, uuid TEXT)""")
            conn.commit()

    def _get_connection(self):
        conn = sqlite3.connect(self.settings.database_file)
        return conn

    def add_schuetze(self, name, surname):
        pass