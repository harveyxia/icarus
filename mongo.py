import os
from pymongo import MongoClient

client = None
db = None
collection = None

def init():
    global client
    global db
    global collection
    
    # if os.environ.get('MONGOHQ_URL'):
    #     client = MongoClient(os.environ.get('MONGOHQ_URL'))
    #     db = client['app27112589']
    # else:
    #     client = MongoClient('localhost:27017')
    #     db = client['icarus']
    # else:   # MongoHQ db
    client = MongoClient('mongodb://harvey:test@ds159220.mlab.com:59220/heroku_gj60ddzp/icarus')
    db = client['icarus']
        
    collection = db['round_trip']

#### Mongo DB config command (unique index)
# db.prices.ensureIndex( {name: 1}, { unique: true, dropDups: true, sparse: true} )