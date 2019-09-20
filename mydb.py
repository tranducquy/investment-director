
import sqlite3
import common
import mylogger

class MyDB():
    def __init__(self, l=None, dbfile=None):
        if l is None:
            self.logger = mylogger.Logger().myLogger()
        else:
            self.logger = l
        if dbfile is None:
            conf = common.read_conf()
            self.dbfile = conf['dbfile']
        else:
            self.dbfile = dbfile

    def connect_db(self):
        """Connects to the specific database."""
        rv = sqlite3.connect(self.dbfile, isolation_level='EXCLUSIVE')
        rv.row_factory = sqlite3.Row
        return rv

    def get_db(self):
        """Opens a new database connection if there is none yet for the
        current application context.
        """
        if not hasattr(self, 'sqlite_db'):
            self.sqlite_db = self.connect_db()
        return self.sqlite_db

    def close_db(self, error):
        """Closes the database again at the end of the request."""
        if hasattr(self, 'sqlite_db'):
            self.sqlite_db.close()


