"""Glue functions to help port the erlang code to python"""

import sys
from hashlib import md5
import os
import struct
from erlang import *


#### couch_file.erl ####

SIZE_BLOCK = 4096

# read the header from a couch file
# start searching at the last full block
def read_header(fd):
    # get file size
    fd.seek(0, os.SEEK_END)
    filesize = fd.tell()
    # get last full block index
    block = filesize / SIZE_BLOCK

    header = find_header(fd, block)
    if header:
        return binary_to_term(header)
    else:
        return None


# search blocks in reverse order
def find_header(fd, block):
    while block >= 0:
        header = load_header(fd, block)
        if header:
            return header
        block -= 1


# header is:
# 0  : 1
# 1-4: header length
# 5+ : header data / prefix
def load_header(fd, block):
    # read in the entire block
    fd.seek(block * SIZE_BLOCK, 0)
    block_data = fd.read(SIZE_BLOCK)

    # check first byte
    if ord(block_data[0]) != 1:
        return None

    # seperate into header length and header
    header_len = struct.unpack(">I", block_data[1:5])[0]
    rest_block = block_data[5:]

    # check to see if the header continues in the next block
    total_bytes = calculate_total_read_len(5, header_len)
    if total_bytes <= len(rest_block):
         raw_bin = rest_block[:total_bytes]
    else:
        # TODO: handle longer headers
        raise Exception("header goes outside block boundry")

    raw_bin_noprefix = remove_block_prefixes(1,raw_bin)

    # if md5 sums match then this is a valid header
    md5_sig = raw_bin_noprefix[:16]
    header_bin = raw_bin_noprefix[16:]
    if md5_sig == md5(header_bin).digest():
        return header_bin


# TODO: find out what this is supposed to do
# it seems that this can probably be simplified/clarified
def calculate_total_read_len(block_offset, final_len):
    if block_offset == 0:
        return calculate_total_read_len(1, final_len) + 1
    block_left = SIZE_BLOCK - block_offset
    if block_left >= final_len:
        return final_len
    else:
        print final_len
        print block_left
        if ((final_len - block_left) % (SIZE_BLOCK -1)) == 0:
            x = 0
        else:
            x = 1
        return final_len + ((final_len - block_left) / (SIZE_BLOCK - 1)) + x
    

# TODO: find out what this is supposed to do
def remove_block_prefixes(block_offset, bin):
    if not bin:
        return []
    if block_offset == 0:
        return remove_block_prefixes(bin[1:])
    block_bytes_available = SIZE_BLOCK - block_offset
    if len(bin) > block_bytes_available:
        data_block = bin[:block_bytes_available]
        rest = bin[block_bytes_available:]
        return data_block + remove_block_prefixes(0, rest)
    else:
        return bin


#### couch_db.erl ####
def get_full_doc_info(db, id):
    return get_full_doc_infos(db, [id])[0]

def get_full_doc_infos(db, ids):
    return lookup(db["fulldocinfo_by_id_btree"], ids)


#### couch_btree.erl ####
def lookup():
    pass
