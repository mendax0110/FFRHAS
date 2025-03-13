from datetime import datetime, timezone
from flask.json import dumps
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source


class time_controller:
    def __init__(self):
        pass

    def get_time(self):
        now = datetime.now(timezone.utc)  # Get current time in UTC
        iso_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        response = {"time": iso_string}
        loggingRepository = LoggingRepository()
        loggingData = LoggingData(Source.HAS, LoggingType.Info, "time was requested", iso_string)
        loggingRepository.write_one(loggingData)
        return dumps(response), 201
