"""Python implementation of Erlang builtins"""

__all__=["binary_to_term"]

import struct

SIZE_BLOCK = 4096

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


# return the length of a binary term in bytes
# incuding tag and any header information
def _get_binary_size(bin):
    tag = ord(bin[0])
    data = bin[1:]

    if tag == SMALL_TUPLE_EXT:
        arity = struct.unpack(">B",data[0])[0]
        offset = 1
        for i in range(arity):
            offset += _get_binary_size(data[offset:])
        return 1 + offset
    if tag == ATOM_EXT:
        length = struct.unpack(">H",data[0:2])[0]
        return 1 + 2 + length
    if tag == SMALL_INTEGER_EXT:
        return 1 + 1
    if tag == INTEGER_EXT:
        return 1 + 4
    if tag == NIL_EXT:
        return 1
    if tag == LIST_EXT:
        length = struct.unpack(">I",data[0:4])[0]
        offset = 4
        # length + 1 because of tail
        for i in range(length + 1):
            offset += _get_binary_size(data[offset:])
        return 1 + offset
    if tag == BINARY_EXT:
        length = struct.unpack(">I",data[0:4])[0]
        return 1 + 4 + length

    raise Exception("Unknown erlang term type (tag: {0})".format(tag))


# deserialize erlang term
def binary_to_term(bin):
    """Decode erlang binary data into python values"""

    # strip 131 header
    if ord(bin[0]) == 131:
        bin = bin[1:]

    tag = ord(bin[0])
    data = bin[1:]

    if tag == SMALL_TUPLE_EXT:
        arity = struct.unpack(">B",data[0])[0]
        elements = []
        offset = 1
        for i in range(arity):
            elements.append(binary_to_term(data[offset:]))
            offset += _get_binary_size(data[offset:])
        return tuple(elements)
    if tag == ATOM_EXT:
        length = struct.unpack(">H",data[0:2])[0]
        return data[2:2+length]
    if tag == SMALL_INTEGER_EXT:
        return struct.unpack(">B",data[0])[0]
    if tag == INTEGER_EXT:
        return struct.unpack(">I",data[0:4])[0]
    if tag == NIL_EXT:
        return None
    if tag == LIST_EXT:
        length = struct.unpack(">I",data[0:4])[0]
        elements = []
        offset = 4
        # length + 1 because of tail
        for i in range(length+1):
            elements.append(binary_to_term(data[offset:]))
            offset += _get_binary_size(data[offset:])
        return elements
    if tag == BINARY_EXT:
        length = struct.unpack(">I",data[0:4])[0]
        return data[4:4+length]

    raise Exception("Unknown erlang term type (tag: {0})".format(tag))
