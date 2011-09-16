from couchdb_file_reader import CouchdbFileReader
from document import Document

class Database(object):
    def __init__(self, path, name=None, session=None):
        # TODO: handle path/name better
        self.couch_path = path + ".couch"


    def __repr__(self):
        reader = CouchdbFileReader(self.couch_path)
        return str({"path":self.couch_path, "header":reader.header})


    def __getitem__(self, key):
        return self.get(key)


    def changes(self, **opts):
        raise NotImplementedError


    def commit(self):
        raise NotImplementedError


    def compact(self):
        raise NotImplementedError


    def copy(self, src, dest):
        raise NotImplementedError


    def create(self, data):
        raise NotImplementedError


    def delete(self, doc):
        raise NotImplementedError


    def delete_attachment(self, doc, filename):
        raise NotImplementedError


    def get(self, id, default=None, **options):
        reader = CouchdbFileReader(self.couch_path)
        data = reader.get(id)
        return Document(data, data["_id"], data["_rev"])


    def get_attachment(self, id_or_doc, filename, default=None):
        raise NotImplementedError


    def info(self):
        raise NotImplementedError


    def name(self):
        raise NotImplementedError


    def put_attachment(self, doc, content, filename=None, content_type=None):
        raise NotImplementedError


    def query(self, map_fun, reduce_fun=None, language='javascript', wrapper=None, **options):
        raise NotImplementedError


    def revisions(self, id, **options):
        raise NotImplementedError


    def save(self, doc, **options):
        raise NotImplementedError


    def update(self, documents, **options):
        raise NotImplementedError


    def view(self, name, wrapper=None, **options):
        raise NotImplementedError

