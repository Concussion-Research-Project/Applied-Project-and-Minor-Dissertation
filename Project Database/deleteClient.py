# import the MongoClient class
from pymongo import MongoClient
import json

# build a new client instance of MongoClient
mongo_client = MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority')

# create new database and collection instance
db = mongo_client.clients
collectionBase = db.base
collectionTest2 = db.test2

# enter filename to be displayed
filename = input("Enter filename: ")

# make an API call to the MongoDB server
findClient = collectionBase.find_one({'client_id' : filename})
collectionBase.delete_one(findClient)

findClient = collectionTest2.find_one({'client_id' : filename})
collectionTest2.delete_one(findClient)