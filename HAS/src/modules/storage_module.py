## 
# @file storage_module.py
# @brief Storage module class definition \class StorageModule
# @date 2021-04-05
# @author placeholder
import os
import sys
import json
import pymongo

class StorageModule:
    def __init__(self, db_name):
        self.db_name = db_name
        self.db = None
        self.init_db()
