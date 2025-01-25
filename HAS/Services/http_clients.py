import random
import time

import requests

from Services.Repositories import SensorDataRepository
from requests import request


class EswClient:
    def __init__(self, endpoints: list):
        self.__fetching = False
        self.__endpoints = endpoints
        self.__repository = SensorDataRepository()

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
                    print("[ERROR]" + ex)

            time.sleep(10)

    def stop_fetching(self):
        self.__fetching = False

    def fetch_api_endpoint(self, endpoint: str):
        raw_response = requests.get(endpoint)
        print("[received]" + str(raw_response.json()))
        response = raw_response.json()

        return response

    def save_to_db(self, data: dict):
        self.__repository.write_one(data)
