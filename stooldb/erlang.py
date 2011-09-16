"""Python implementation of Erlang builtins for reading and writing data files"""

__all__=["binary_to_term"]

import struct

ETERM = 131
ATOM_CACHE_REF = 82
SMALL_INTEGER_EXT = 97
INTEGER_EXT = 98
FLOAT_EXT = 99
ATOM_EXT = 100
REFERENCE_EXT = 101
PORT_EXT = 102
PID_EXT = 103
SMALL_TUPLE_EXT = 104
LARGE_TUPLE_EXT = 105
NIL_EXT = 106
STRING_EXT = 107
LIST_EXT = 108
BINARY_EXT = 109
SMALL_BIG_EXT = 110
LARGE_BIG_EXT = 111
NEW_REFERENCE_EXT = 114
SMALL_ATOM_EXT = 115
FUN_EXT = 117
NEW_FUN_EXT = 112
EXPORT_EXT = 113
BIT_BINARY_EXT = 77
NEW_FLOAT_EXT = 70


class QuickLog(object):
    def __init__(self, active=True):
        self.active = active
        self.indent = 0

    def dprint(self, msg):
        if self.active:
            if self.indent < 1:
                print msg
            else:
                print " "*(self.indent-1),msg

log = QuickLog()


# recursive function
# returns data, length
# data is the python representation of the erlang binary
# length is the number of bytes of the erlang binary
def _binary_to_term_len(bin):
    tag = ord(bin[0])
    data = bin[1:]

    if tag == ETERM:
        log.dprint("ETERM " + `ETERM`)
        return _binary_to_term_len(data)
    elif tag == ATOM_CACHE_REF:
        log.dprint("ATOM_CACHE_REF " + `ATOM_CACHE_REF`)
        return struct.unpack(">B", data[0])[0], 1 + 1
    elif tag == SMALL_INTEGER_EXT:
        log.dprint("SMALL_INTEGER_EXT " + `SMALL_INTEGER_EXT`)
        return struct.unpack(">B",data[0])[0], 1 + 1
    elif tag == INTEGER_EXT:
        log.dprint("INTEGER_EXT " + `INTEGER_EXT`)
        return struct.unpack(">I",data[0:4])[0], 1 + 4
    elif tag == FLOAT_EXT:
        log.dprint("FLOAT_EXT " + `FLOAT_EXT`)
        print data[0:31]
        return float(data[0:31]), 1 + 31
    elif tag == ATOM_EXT:
        log.dprint("ATOM_EXT " + `ATOM_EXT`)
        length = struct.unpack(">H",data[0:2])[0]
        log.indent += 1
        log.dprint("data = " + data[2:2+length])
        log.indent -= 1
        return data[2:2+length], 1 + 2 + length
    elif tag == REFERENCE_EXT:
        log.dprint("REFERENCE_EXT " + `REFERENCE_EXT`)
        node, offset = _binary_to_term_len(data)
        return (node,
                struct.unpack(">I",data[offset:offset+4])[0],
                struct.unpack(">B",data[offset+4:offset+4+1])[0]), 1 + offset + 4 + 1
    elif tag == PORT_EXT:
        log.dprint("PORT_EXT " + `PORT_EXT`)
        node, offset = _binary_to_term_len(data)
        return (node,
                struct.unpack(">I",data[offset:offset+4])[0],
                struct.unpack(">B",data[offset+4:offset+4+1])[0]), 1 + offset + 4 + 1
    elif tag == PID_EXT:
        log.dprint("PID_EXT " + `PID_EXT`)
        node, offset = _binary_to_term_len(data)
        return (node,
                struct.unpack(">I",data[offset:offset+4])[0],
                struct.unpack(">I",data[offset+4:offset+4+4])[0],
                struct.unpack(">B",data[offset+4+4:offset+4+4+1])[0]), 1 + offset + 4 + 4 + 1
    elif tag == SMALL_TUPLE_EXT:
        log.dprint("SMALL_TUPLE_EXT " + `SMALL_TUPLE_EXT`)
        log.indent += 1 # debug
        arity = struct.unpack(">B",data[0])[0]
        log.dprint("arity = " + `arity`)
        elements = []
        offset = 1
        for i in range(arity):
            element, length = _binary_to_term_len(data[offset:])
            elements.append(element)
            offset += length
        log.indent -= 1 # debug
        return tuple(elements), 1 + offset
    elif tag == LARGE_TUPLE_EXT:
        log.dprint("LARGE_TUPLE_EXT " + `LARGE_TUPLE_EXT`)
        log.indent += 1 # debug
        arity = struct.unpack(">I",data[0:4])[0]
        log.dprint("arity = " + `arity`)
        elements = []
        offset = 4
        for i in range(arity):
            element, length = _binary_to_term_len(data[offset:])
            elements.append(element)
            offset += length
        log.indent -= 1 # debug
        return tuple(elements), 4 + offset
    elif tag == NIL_EXT:
        log.dprint("NIL_EXT " + `NIL_EXT`)
        return None, 1
    elif tag == STRING_EXT:
        log.dprint("STRING_EXT " + `STRING_EXT`)
        pass
    elif tag == LIST_EXT:
        log.dprint("LIST_EXT " + `LIST_EXT`)
        log.indent += 1 # debug
        length = struct.unpack(">I",data[0:4])[0]
        log.dprint("length = " + `length`)
        elements = []
        offset = 4
        # length + 1 because of tail
        for i in range(length+1):
            element, length = _binary_to_term_len(data[offset:])
            elements.append(element)
            offset += length
        return elements, 1 + offset
    elif tag == BINARY_EXT:
        log.dprint("BINARY_EXT " + `BINARY_EXT`)
        log.indent += 1 # debug
        length = struct.unpack(">I",data[0:4])[0]
        log.dprint("length = " + `length`)
        log.dprint("data = " + data[4:4+length])
        log.indent -= 1 # debug
        return data[4:4+length], 1 + 4 + length
    elif tag == SMALL_BIG_EXT:
        pass
    elif tag == LARGE_BIG_EXT:
        pass
    elif tag == NEW_REFERENCE_EXT:
        pass
    elif tag == SMALL_ATOM_EXT:
        pass
    elif tag == FUN_EXT:
        pass
    elif tag == NEW_FUN_EXT:
        pass
    elif tag == EXPORT_EXT:
        pass
    elif tag == BIT_BINARY_EXT:
        pass
    elif tag == NEW_FLOAT_EXT:
        pass
    else:
#        raise Exception("Unknown erlang term type (tag: {0})".format(tag))
#        log.dprint("UNKNOWN " + `tag`)
#        return _binary_to_term_len(data[5:])
        return None


# deserialize erlang term
def binary_to_term(bin):
    """Decode erlang binary data into python values"""

    return _binary_to_term_len(bin)[0]
