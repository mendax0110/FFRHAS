'''
This is the storage module. It is responsible for storing data in the database (simple JSON files)
'''
import os
import sys
import json
import pymongo

class StorageModule:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None
        self.init_db()
