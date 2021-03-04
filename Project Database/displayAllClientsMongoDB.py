import pymongo 
import json
  
# https://www.geeksforgeeks.org/how-to-fetch-data-from-mongodb-using-python/
 
client = pymongo.MongoClient('mongodb+srv://research-project:cGeNVHwDOQBIjXAM@cluster0.mrfjn.mongodb.net/clients?retryWrites=true&w=majority') 

# Database Name 
db = client["clients"] 
 
# Collection Name 
col = db["base"] 

x = col.find()
  
for data in x: 
    data.pop("_id")
    print("\n",json.dumps(data, indent=4))