import pymongo

class DbContext():
    connectionString = "mongodb://localhost:27017"

    def __init__(self):
        pass

    @classmethod
    def createDb(cls):
        client = pymongo.MongoClient(DbContext.connectionString)
        db = client.Test
        return db