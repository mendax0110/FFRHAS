import pymongo
import os

class DbContext():

    @classmethod
    def createDb(cls):
        connectionString = os.getenv("connectionstring", "mongodb://localhost:27017")
        client = pymongo.MongoClient(connectionString)
        db = client.Test
        return db