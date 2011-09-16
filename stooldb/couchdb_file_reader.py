import os

import erlang
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

    def get(self, id):
        """Get a document based on its id"""
#        return glue.get_full_doc_info(self.header["fulldocinfo_by_id_btree_state"], id)
        btree_id = CouchdbBtree(self.header["fulldocinfo_by_id_btree_state"], self.fd)
        btree_id.lookup(id)
        return {"_id":"", "_rev":""}


class CouchdbBtree(object):
    def __init__(self, state, fd):
        self.fd = fd
        self.root = state

    def lookup(self, id):
        return self._lookup(self.root, id)

    def _lookup(self, node, key):
        if node == None:
            raise Exception("not found")

        print "----"
        print node[0]
        print "++++"
        self.fd.seek(node[0])
        node_data = self.fd.read(20)
        i = 0
        for x in node_data:
            print "%3d" % ord(x),
            if (i + 1) % 16 == 0:
                print
            i += 1
        print

        self.fd.seek(node[0] + 4)
        node_data = self.fd.read(4000)

        print "===="
        for i in range(15):
            print "%3d" % ord(node_data[i]),
            if (i + 1) % 16 == 0:
                print
        print

        if ord(node_data[0]) != 131:
            print "trying 9"
            self.fd.seek(node[0] + 9)
            node_data = self.fd.read(4000)
            print "===="
            for i in range(300):
                print "%3d" % ord(node_data[i]),
                if (i + 1) % 16 == 0:
                    print
            print

        node_value = erlang.binary_to_term(node_data)
        node_left_key = node_value[1][0][0]
        node_left_node = node_value[1][0][1]
        node_right_node = node_value[1][1][1]

        print node_value

#        if node_key == key:
#            return node_value

        if key <= node_left_key:
            return self._lookup(node_left_node, key)
        else:
            return self._lookup(node_right_node, key)
#        pointer = node[0]
#        _lookup_node(pointer, 
