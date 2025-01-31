from enum import Enum
from datetime import datetime, timezone
import pymongo
from bson.json_util import dumps


class Unit(Enum):
    Celsius = 1
    Volt = 2
    Ampere = 3
    mbar = 4
    Hz = 5


class SensorData:
    def __init__(self, sensorName: str, value: float, unit: Unit, timestamp: str):
        '''
        :param sensorName: Name of the sensor
        :param value: Value of the sensor
        :param unit: Unit of the sensor
        :param timestamp: Timestamp in the format: 2025-01-04T15:30:00Z
        '''
        self.DataDict = {"sensor_name": sensorName, "value": value, "unit": unit.name, "timestamp": timestamp}


class SensorDataRepository:
    def __init__(self):
        self.__client = pymongo.MongoClient(f"mongodb://admin:secret@mongodb:27017")  # connection string
        self.__db = self.__client.Test  # use/create db
        self.__sensorData = self.__db.SensorData  # use/create folder in db

    def get_all(self):
        data = self.__sensorData.find()
        return dumps(data)

    def get_from_sensor(self, sensor_name: str):
        data = self.__sensorData.find({"sensor_name": sensor_name})
        return dumps(data)

    def get_from_sensor_for_range(self, sensor_name: str, start_date: datetime, stop_date: datetime):
        start_date = start_date.astimezone(timezone.utc)
        stop_date = stop_date.astimezone(timezone.utc)
        data = self.__sensorData.find({"sensor_name": f"{sensor_name}",
                                 "timestamp": {"$gte": start_date.isoformat(), "$lte": start_date.isoformat()}
                                       })
        return dumps(data)

    def write_one(self, data: SensorData):
        self.__sensorData.insert_one(data.DataDict)

    def write_many(self, data_list: list):
        self.__sensorData.insert_many(data_list)


class Source(Enum):
    HAS = 1
    ESW = 2


class LoggingType(Enum):
    Error = 1
    Info = 2


class LoggingData:
    def __init__(self, source: Source, type: LoggingType, message: str, timestamp: str):
        '''
        :param source: Source of the logging
        :param type: Type of the logging
        :param message: Description or exception
        :param timestamp: Timestamp in the format: 2025-01-04T15:30:00Z
        '''
        self.DataDict = {"source":source.name, "type": type.name, "message": message, "timestamp": timestamp}


class LoggingRepository:
    def __init__(self):
        self.__client = pymongo.MongoClient(f"mongodb://admin:secret@mongodb:27017")  # connection string
        self.__db = self.__client.Test  # use/create db
        self.__logging = self.__db.Logging  # use/create folder in db

    def get_all(self):
        data = self.__logging.find()
        return dumps(data)

    def get_from_source(self, source: Source):
        data = self.__logging.find({"source": source.name})
        return dumps(data)

    def get_from_source_for_range(self, source: Source, start_date: datetime, stop_date: datetime):
        start_date = start_date.astimezone(timezone.utc)
        stop_date = stop_date.astimezone(timezone.utc)
        data = self.__logging.find({"source": f"{source.name}",
                                 "timestamp": {"$gte": start_date.isoformat(), "$lte": start_date.isoformat()}
                                    })
        return dumps(data)

    def write_one(self, data: LoggingData):
        self.__logging.insert_one(data.DataDict)

    def write_many(self, data_list: list):
        self.__logging.insert_many(data_list)
