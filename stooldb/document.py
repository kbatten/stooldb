class Document(object):
    def __init__(self, data, id, rev):
        self.data = data
        self.id = id
        self.rev = rev

    def __repr__(self):
        return str({"id":self.id, "rev":self.rev, "value":self.data})

    def __getitem__(self, key):
        return data[key]
