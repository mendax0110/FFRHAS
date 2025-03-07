from datetime import datetime

from flask import render_template, request
from Services.Repositories import SensorDataRepository, SensorData, Unit
import pymongo
from flask.json import dumps

class hv_system_controller:
    def __init__(self):
        self.__repository = SensorDataRepository()

    def render_template(self):
        return render_template('highvoltagesystem.html', active_page='highvoltagesystem')

    def save(self):
        if (request.method == 'POST'):
            data = request.get_json()
            date = data["time"]
            newDate = datetime.strptime(date, "%Y-%m-%d")
            dateAndTime = datetime.combine(newDate.date(), datetime.now().time())
            sensorData = SensorData(data["name"], float(data["value"]), Unit.Celsius, str(dateAndTime))
            self.__repository.write_one(sensorData)
        return dumps(data), 201

    def get(self):
        data = self.__repository.get_all()
        return dumps(data), 200