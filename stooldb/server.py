import os

from database import Database



class Server(object):
    def __init__(self, server, full_commit=True, session=None):
        self.server = os.path.abspath(server)


    def __getitem__(self, key):
        return Database(os.path.join(self.server, key))


    def __delitem__(self, key):
        return self.delete(key)


    def config(self):
        raise NotImplementedError


    def create(self, dbname):
        raise NotImplementedError


    def delete(self, dbname):
        raise NotImplementedError


    def replicate(self, source, target, **options):
        raise NotImplementedError


    def stats(self):
        raise NotImplementedError


    def tasks(self):
        raise NotImplementedError


    def uuids(self, count=None):
        raise NotImplementedError


    def version(self):
        raise NotImplementedError
