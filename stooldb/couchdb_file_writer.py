import glue


class CouchdbFileWriter(object):
    """Couchdb file writer

    Only one writer can be active at a time
    """

    def __init__(self, path):
        self.path = path
