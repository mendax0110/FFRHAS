import datetime
import random
import threading
import time

import requests

from Services.Repositories import SensorDataRepository, SensorData, LoggingRepository, LoggingData, LoggingType, Source, Unit, StateRepository, System, HighVoltageState, VacuumState, MainSwitchState, MainSwitchStateEnum,StateBase
from requests import request
from .endpoints import sensorEndpoints, stateEndpoints, loggingEndpoints


class EswClient:
    pauseEndpointQueue = False
    endpointQueue = []
    lock = threading.Lock()
    def __init__(self):
        self.__fetching = False
        self.__fetchingQueue = False
        self.__sensorDataRepository = SensorDataRepository()
        self.__stateRepository = StateRepository()
        self.__logger = LoggingRepository()

    def start_fetching(self):
        self.__fetching = True
        while self.__fetching:
            for endpoint in sensorEndpoints:
                # fetch data from uC
                try:
                    data = self.fetch_api_endpoint(endpoint)
                    sensordata = SensorData(data["sensor_name"], data["value"], data["unit"], data["timestamp"])
                    self.__sensorDataRepository.write_one(sensordata)
                except Exception as ex:
                    print(f"[ERROR in SensorData] {ex}")
                    data = LoggingData(Source.HAS, LoggingType.Error, str(ex), datetime.datetime.isoformat(datetime.datetime.now()))
                    self.__logger.write_one(data)

            vacuumState = self.__stateRepository.get_for_system(System.vacuum)
            highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
            mainSwitchState = self.__stateRepository.get_for_system(System.mainSwitch)

            if vacuumState is None:
                vacuumState = VacuumState(False, 1000, False)
            if highVoltageState is None:
                highVoltageState = HighVoltageState(False, 25, 50, False)
            if mainSwitchState is None:
                mainSwitchState = MainSwitchState(MainSwitchStateEnum.off.name)

            for endpoint in stateEndpoints:
                # fetch data from uC
                try:
                    data = self.fetch_api_endpoint(endpoint.get("url"))

                    self.overwrite_state(vacuumState, highVoltageState, mainSwitchState, endpoint.get("system"), endpoint.get("parameter"), data["value"])

                except Exception as ex:
                    print(f"[ERROR in StateData] {ex}")
                    data = LoggingData(Source.HAS, LoggingType.Error, str(ex), datetime.datetime.isoformat(datetime.datetime.now()))
                    self.__logger.write_one(data)

            self.__stateRepository.update_state_for(vacuumState)
            self.__stateRepository.update_state_for(highVoltageState)
            self.__stateRepository.update_state_for(mainSwitchState)

            for endpoint in loggingEndpoints:
                try:
                    data = self.fetch_api_endpoint(endpoint.get("url"))

                    if data["value"] == 1:
                        message = endpoint.get("infoMessage")
                        loggingType = LoggingType.Info
                    else:
                        message = endpoint.get("errorMessage")
                        loggingType = LoggingType.Error

                    loggingData = LoggingData(Source.ESW, loggingType, message, datetime.datetime.isoformat(datetime.datetime.now()))
                    self.__logger.write_one(loggingData)
                except Exception as ex:
                    print(f"[ERROR in loggingData] {ex}")
                    data = LoggingData(Source.HAS, LoggingType.Error, str(ex), datetime.datetime.isoformat(datetime.datetime.now()))
                    self.__logger.write_one(data)

            sleepTime = 5
            print(f"sleeping for {sleepTime} seconds")
            time.sleep(sleepTime)

    def stop_fetching(self):
        self.__fetching = False

    def start_fetching_from_queue(self):
        self.__fetchingQueue = True

        while(self.__fetchingQueue):
            if EswClient.pauseEndpointQueue:
                time.sleep(0.1) #nötig um anderen Threads CPU zugriffszeit zu lassen
                continue
            if len(EswClient.endpointQueue) == 0:
                time.sleep(0.1) #nötig um anderen Threads CPU zugriffszeit zu lassen
                continue

            try:
                with EswClient.lock:
                    endpoint = EswClient.endpointQueue.pop(-1)
                response = requests.get(endpoint)
                loggingData = LoggingData(Source.HAS, LoggingType.Info, f"response on fetching: {endpoint}: {response.raw}", datetime.datetime.isoformat(datetime.datetime.now()))
                self.__logger.write_one(loggingData)
            except Exception as ex:
                print(f"[ERROR in empty queue] {ex}")
                loggingData = LoggingData(Source.HAS, LoggingType.Error, f"error in fetching queue item: {ex}", datetime.datetime.isoformat(datetime.datetime.now()))
                self.__logger.write_one(loggingData)

    def stop_fetching_from_queue(self):
        self.__fetchingQueue = False

    def fetch_api_endpoint(self, endpoint: str):
        try:
            response = requests.get(endpoint, timeout=3)
            print(response.content)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch {endpoint}: {e}")

    def overwrite_state(self, vacuumState:VacuumState, highVoltageState:HighVoltageState, mainSwitchState:MainSwitchState, system:System, parameter:str, data):
        if system == System.mainSwitch:
            if parameter == "state":
                mainSwitchState.state = int(data)

        if system == System.vacuum:
            if parameter == "pumpOn":
                vacuumState.pumpOn = int(data)

        if system == System.highVoltage:
            if parameter == "hvOn":
                highVoltageState.hvOn = int(data)

    def send_command(self, endpoint:str):
        EswClient.endpointQueue.append(endpoint)
