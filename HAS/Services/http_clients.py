import datetime
import random
import time

import requests

from Services.Repositories import SensorDataRepository, SensorData, LoggingRepository, LoggingData, LoggingType, Source, Unit
from requests import request


class EswClient:
    def __init__(self, endpoints: list):
        self.__fetching = False
        self.__endpoints = endpoints
        self.__repository = SensorDataRepository()
        self.__logger = LoggingRepository()

    def start_fetching(self):
        self.__fetching = True
        while self.__fetching:
            for endpoint in self.__endpoints:
                # fetch data from uC
                try:
                    data = self.fetch_api_endpoint(endpoint)
                    # save data to DB
                    self.save_to_db(data)
                except Exception as ex:
                    print(f"[ERROR] {ex}")
                    data = LoggingData(Source.HAS, LoggingType.Error, str(ex), datetime.datetime.isoformat())
                    self.__logger.write_one(data)

            time.sleep(10)

    def stop_fetching(self):
        self.__fetching = False

    def fetch_api_endpoint(self, endpoint: str):
        raw_response = requests.get(endpoint)

        response = raw_response.json()
        
        return response

    def save_to_db(self, data: dict):
        self.__repository.write_one(data)
