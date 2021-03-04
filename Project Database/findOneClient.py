# import the MongoClient class
from pymongo import MongoClient
import json

# build a new client instance of MongoClient
mongo_client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')

# create new database and collection instance
db = mongo_client.clients
col = db.base

# enter filename to be displayed
filename = input("Enter filename: ")

# make an API call to the MongoDB server
findClient = col.find_one({'client_id' : filename})

if(findClient):
    findClient.pop("_id")
    print(json.dumps(findClient, indent=4))
else:
    print('\nClient with ID %s does not exists.' % (filename))