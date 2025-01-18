from datetime import datetime, timezone
import pymongo
from bson.json_util import dumps

class SensorDataRepository:
    def __init__(self, user:str, pwd:str):
        self.__client = pymongo.MongoClient(f"mongodb://{user}:{pwd}@127.0.0.1:27017")  # connection string
        self.__db = self.__client.Test  # use/create db
        self.__test = self.__db.Test  # use/create folder in db

    def get_all(self):
        data = self.__test.find()
        return dumps(data)

    def get_from_sensor(self, sensor_name: str):
        data = self.__test.find({"sensor_name": sensor_name})
        return dumps(data)

    def get_from_sensor_for_range(self, sensor_name: str, start_date: datetime, stop_date: datetime):
        start_date = start_date.astimezone(timezone.utc)
        stop_date = stop_date.astimezone(timezone.utc)
        data = self.__test.find({"sensor_name": f"{sensor_name}",
                                 "timestamp": {"$gte": start_date.isoformat(), "$lte": start_date.isoformat()}
                                 })
        return dumps(data)

    def write_one(self, data: dict):
        self.__test.insert_one(data)

    def write_many(self, data_list: list):
        self.__test.insert_many(data_list)
