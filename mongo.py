import os
from pymongo import MongoClient

client = None
db = None
collection = None

def init():
    global client
    global db
    global collection
    
    mongo_url = os.environ.get('MONGOHQ_URL', 'localhost:27017')
    client = MongoClient(mongo_url)
    db = client['icarus']
    collection = db.prices

#### Mongo DB config command (unique index)
# db.prices.ensureIndex( {name: 1}, { unique: true, dropDups: true, sparse: true} )