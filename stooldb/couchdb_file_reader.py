import glue

class CouchdbFileReader(object):
    def __init__(self, path):
        self.path = path
        self.fd = file(self.path, "rb")
        header_raw = glue.read_header(self.fd)

        if header_raw[1] != 6:
            raise Exception("Incorrect disk version header")

        # header for disk version 6
        self.header = {}
        self.header["disk_version"] = header_raw[1]
        self.header["update_seq"] = header_raw[2]
        self.header["unused"] = header_raw[3]
        self.header["fulldocinfo_by_id_btree_state"] = header_raw[4]
        self.header["docinfo_by_seq_btree_state"] = header_raw[5]
        self.header["local_docs_btree_state"] = header_raw[6]
        self.header["purge_seq"] = header_raw[7]
        self.header["purged_docs"] = header_raw[8]
        self.header["security_ptr"] = header_raw[9]
        self.header["revs_limit" ] = header_raw[10]
