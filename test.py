#!/usr/bin/env python

import sys

import stooldb

try:
    server_db = sys.argv[1]
    try:
        server, dbname = server_db.rsplit("/",1)
    except ValueError:
        server = "."
        dbname = server_db

    # remove .couch if its appended
    dbname = dbname.rsplit(".",1)[0]
except Exception as ex:
#    server = "/Users/kbatten/Library/Application Support/CouchbaseServer/test"
    server = "."
    dbname = "test"

print "server:",server
print "db:",dbname

couch = stooldb.Server(server)
db = couch[dbname]

doc = db["30cce3c46e10bbbfaadb86bed1000fd0"]
