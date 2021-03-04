# import the MongoClient class
from pymongo import MongoClient

# import the Pandas library
import pandas

# these libraries are optional
import json
import time
import os
import sys

# build a new client instance of MongoClient
mongo_client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')

# create new database and collection instance
db = mongo_client.clients
col = db.base

# enter filename to be displayed
filename = input("Enter filename: ")

# make an API call to the MongoDB server
#cursor = col.find()
#cursor = col.find_one({'client_id' : filename})

#cursor.pop("_id")
#cursor.pop("file_name")

col.update_one(
	{"client_id" : filename},
	{"$set": 
		{"client_id":"100"}
	},upsert=True
)

#col.update(
#	{"client_id" : filename},
#	{"$push" :
#		{"contents" : "100"}
#	}
#)


#col.Doc.update({cursor},{"$set": "eee"})
