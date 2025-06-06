from enum import Enum
from datetime import datetime, timezone
import pymongo
from bson.json_util import dumps
from abc import ABC, abstractmethod
from typing import Type, Dict, Optional

#connectionString = f"mongodb://admin:secret@mongodb:27017"
connectionString = f"mongodb://localhost:27017"

class Unit(Enum):
    Celsius = 1
    Volt = 2
    Ampere = 3
    mbar = 4
    Hz = 5


class SensorData:
    def __init__(self, sensorName: str, value: float, unit: str, timestamp: str):
        '''
        :param sensorName: Name of the sensor
        :param value: Value of the sensor
        :param unit: Unit of the sensor
        :param timestamp: Timestamp in the format: 2025-01-04T15:30:00Z
        '''
        self.DataDict = {"sensor_name": sensorName, "value": value, "unit": unit, "timestamp": timestamp}   # temporary use unit of esw


class SensorDataRepository:
    def __init__(self):
        self.__client = pymongo.MongoClient(connectionString)  # connection string
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
        self.__client = pymongo.MongoClient(connectionString)  # connection string
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


class System(Enum):
    highVoltage = 1
    vacuum = 2
    mainSwitch = 3

class StateBase(ABC):
    def __init__(self):
        self.system = ''

    @classmethod
    @abstractmethod
    def from_dictionary(cls, data: dict) -> 'StateBase':
        pass

    @abstractmethod
    def get_dictionary(self) -> 'dict':
        pass

class VacuumState(StateBase):
    def __init__(self, pumpOn: bool, targetPressure: float, automatic: bool):
        self.system = System.vacuum.name
        self.__pumpOn = pumpOn
        self.targetPressure = targetPressure
        self.automatic = automatic

    @property
    def pumpOn(self):
        return self.__pumpOn

    @pumpOn.setter
    def pumpOn(self, state):
        if isinstance(int, state):
            self.__pumpOn = state == 1
        elif isinstance(bool, state):
            self.__pumpOn = state
        else:
            raise ValueError("pumpOn must be either bool or int")

    @classmethod
    def from_dictionary(cls, data: dict) -> 'VacuumState':
        data = data.copy()
        data.pop("_id", None)  # Entfernt MongoDB-ID, falls vorhanden

        try:
            return cls(
                pumpOn=bool(data["pumpOn"]),
                targetPressure=float(data["targetPressure"]),
                automatic=bool(data["automatic"])
            )
        except KeyError as e:
            raise ValueError(f"Missing field in data: {e}")

    def get_dictionary(self) -> 'dict':
        return {"system":self.system, "pumpOn": self.pumpOn, "targetPressure": self.targetPressure, "automatic": self.automatic}


class HighVoltageState(StateBase):
    def __init__(self, hvOn: bool, targetFrequency: float, targetPwm: float, automatic: bool):
        self.system = System.highVoltage.name
        self.__hvOn = hvOn
        self.targetFrequency = targetFrequency
        self.targetPwm = targetPwm
        self.automatic = automatic

    @property
    def hvOn(self):
        return self.__hvOn

    @hvOn.setter
    def hvOn(self, state):
        if isinstance(int, state):
            self.__hvOn = state == 1
        elif isinstance(bool, state):
            self.__hvOn = state
        else:
            raise ValueError("hvOn must be either bool or int")

    @classmethod
    def from_dictionary(cls, data: dict) -> 'HighVoltageState':
        data = data.copy()
        data.pop("_id", None)  # Entfernt MongoDB-ID, falls vorhanden

        try:
            return cls(
                hvOn = data['hvOn'],
                targetFrequency= data['targetFrequency'],
                targetPwm= data['targetPwm'],
                automatic = data['automatic']
            )
        except KeyError as e:
            raise ValueError(f"Missing field in data: {e}")

    def get_dictionary(self) -> 'dict':
        return {'hvOn':self.hvOn, 'targetFrequency':self.targetFrequency, 'targetPwm':self.targetPwm, 'automatic':self.automatic}

class MainSwitchStateEnum(Enum):
    off = 0,
    manual = 1,
    remote = 2,
    invalid = 3

class MainSwitchState(StateBase):
    def __init__(self, state: str, ):
        self.system = System.mainSwitch.name
        self.__state = state

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        if isinstance(state, int):
            try:
                enum_state = MainSwitchStateEnum(state)
                self.__state = enum_state.name  # Speichert den Namen als String
            except ValueError:
                raise ValueError(f"{state} is not a valid MainSwitchStateEnum val")
        else:
            raise ValueError("state must be a integer")


    @classmethod
    def from_dictionary(cls, data: dict) -> 'MainSwitchState':
        data = data.copy()
        data.pop("_id", None)  # Entfernt MongoDB-ID, falls vorhanden

        try:
            return cls(
                state = data['state'],
            )
        except KeyError as e:
            raise ValueError(f"Missing field in data: {e}")

    def get_dictionary(self) -> 'dict':
        return {'state':self.__state}


# Mapping System enum to state classes
STATE_CLASS_MAP: Dict[System, Type[StateBase]] = {
    System.vacuum: VacuumState,
    System.highVoltage: HighVoltageState,
    System.mainSwitch: MainSwitchState
}


class StateRepository:
    def __init__(self):
        self.__client = pymongo.MongoClient(connectionString)  # connection string
        self.__db = self.__client.Test  # use/create db
        self.__state = self.__db.State  # use/create folder in db


    def get_for_system(self, system: System) -> Optional[StateBase]:
        data = self.__state.find_one({"system": system.name})
        if data is None:
            return None

        state_cls = STATE_CLASS_MAP.get(system)
        if not state_cls:
            raise ValueError(f"No state class registered for system: {system.name}")

        return state_cls.from_dictionary(data)

    def update_state_for(self, status: StateBase):
        self.__state.update_one(
            {"system": status.system},  # Filter by system name
            {"$set": status.get_dictionary()},              # Set the new data
            upsert=True                             # Insert if it doesn't exist
        )

