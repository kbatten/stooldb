import os
import struct

import erlang
import glue

class CouchdbFileReader(object):
    def __init__(self, path):
        self.path = path
        self.fd = file(self.path, "rb")

        self.update_header()


    def update_header(self):
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
#        btree_id = CouchdbBtree(self.header["fulldocinfo_by_id_btree_state"], self.fd)
        btree_id = CouchdbBtree(self.header["docinfo_by_seq_btree_state"], self.fd)
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

        offset = node[0]

        print "----"
        print "file offset ", offset
        print "block offset", 4096 * (offset/4096),4096 * (1+offset/4096)
        print "block space ", 4096 * (1+offset/4096) - offset
        print "++++"
        self.fd.seek(offset)
        length = struct.unpack(">I", self.fd.read(4))[0]

        print "reading " + `length` + " bytes"

        self.fd.seek(offset + 4)
        prefix = self.fd.read(1)
        if ord(prefix) == 1:
            print "skipping 5 bytes"
            print_bin(self.fd.read(4))
            length -= 5

        node_data = self.fd.read(length)

        print_bin(node_data)

        node_value = erlang.binary_to_term(node_data)

        node_left_key = node_value[1][0][0]
        node_left_node = node_value[1][0][1]
        node_right_node = node_value[1][1][1]

        print node_value

#        if node_key == key:
#            return node_value

        if key <= node_left_key:
            print "going left"
            return self._lookup(node_left_node, key)
        else:
            print "going right"
            return self._lookup(node_right_node, key)
#        pointer = offset
#        _lookup_node(pointer, 


def print_bin(bin):
    print "===="
    i = 0
    for c in bin:
        print "%3d" % ord(c),
        if (i + 1) % 16 == 0:
            print
        i += 1
    print
