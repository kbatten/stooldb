#!/usr/bin/env python

import sys

from stooldb import glue

try:
    filename = sys.argv[1]
except:
    filename = "test.couch"

print "opening", filename
fd = open(filename, "rb")

header = glue.read_header(fd)
if not header:
    sys.exit()

print "found header"
print header
