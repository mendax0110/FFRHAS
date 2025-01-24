import random
import time
from Services.Repositories import SensorDataRepository


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
                data = self.fetch_api_endpoint(endpoint)
                # save data to DB
                self.save_to_db(data)

            time.sleep(10)

    def stop_fetching(self):
        self.__fetching = False

    def fetch_api_endpoint(self, endpoint: str):
        #TODO: replace testdata with real code
        random_generator = random.Random()
        test = random_generator.randint(1, 50)

        response = {
            "sensor_name": "temperature_sensor_1",
            "value": test,
            "unit": "Celsius",
            "timestamp": "2025-01-04T15:30:00Z"
        }
        return response

    def save_to_db(self, data: dict):
        self.__repository.write_one(data)