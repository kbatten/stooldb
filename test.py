#!/usr/bin/env python

import sys

import stooldb

try:
    server_db = sys.argv[1]
    try:
        server, dbname = server_db.rsplit("/",1)
    except ValueError:
        server = "server/"
        dbname = server_db

    # remove .couch if its appended
    dbname = dbname.rsplit(".",1)[0]
    docid=""
except Exception as ex:
#    server = "/Users/kbatten/Library/Application Support/CouchbaseServer/test"
    server = "server/"
    dbname = "autodiscovery"
    docid="03713cb29a236ae1b0c90139d000160f"


print "fetching server",server
couch = stooldb.Server(server)
print couch
print "fetching db",dbname
db = couch[dbname]
print db
print "fetching doc",docid
doc = db[docid]
print doc
