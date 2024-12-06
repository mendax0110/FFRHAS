from flask import render_template, request
import pymongo
from bson.json_util import dumps

class hv_system_controller:
    def __init__(self):
        pass

    def render_template(self):
        return render_template('highvoltagesystem.html', active_page='highvoltagesystem')

    def save(self):
        client = pymongo.MongoClient("mongodb://admin:secret@mongodb:27017")  # connection string
        db = client.Test  # use/create db
        test = db.Test  # use/create folder in db
        if (request.method == 'POST'):
            data = request.get_json()
            test.insert_one(data)
        return dumps(data), 201

    def get(self):
        client = pymongo.MongoClient("mongodb://admin:secret@mongodb:27017")  # connection string
        db = client.Test  # use/create db
        test = db.Test  # use/create folder in db
        data = test.find()
        return dumps(data), 200