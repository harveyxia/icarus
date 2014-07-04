from pymongo import MongoClient

client = None
db = None
collection = None

def init():
    global client
    global db
    global collection
    
    client = MongoClient('localhost', 27017)
    db = client['icarus']
    collection = db.prices

#### Mongo DB config command (unique index)
# db.prices.ensureIndex( {name: 1}, { unique: true, dropDups: true, sparse: true} )