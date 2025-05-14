from flask import render_template, request
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source, Unit
from datetime import datetime
class vacuum_system_controller:
    def __init__(self):
        self.status = {"pumpOn":False, "targetPressure":1000.00, "automatic":False, "handBetrieb":True}
        self.__logger = LoggingRepository()

    def render_template(self):
        return render_template('vacuumsystem.html', active_page='vacuumsystem', pumpOn=self.status["pumpOn"], targetPressure=self.status["targetPressure"], automatic=self.status["automatic"], handBetrieb=self.status["handBetrieb"])

    def start_automatic(self):
        self.status["automatic"] = True
        data = LoggingData(Source.HAS, LoggingType.Info, "started vacuum-automatic", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def stop_automatic(self):
        self.status["automatic"] = False
        data = LoggingData(Source.HAS, LoggingType.Info, "stopped vacuum-automatic", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def pump_on(self):
        self.status["pumpOn"] = True
        data = LoggingData(Source.HAS, LoggingType.Info, "turned pump on", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def pump_off(self):
        self.status["pumpOn"] = False
        data = LoggingData(Source.HAS, LoggingType.Info, "turned pump off", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def set_target_pressure(self):
        try:
            targetPressure = float(request.args.get('targetPressure'))
            self.status["targetPressure"] = targetPressure
            data = LoggingData(Source.HAS, LoggingType.Info, f"set target pressure to: {targetPressure} mbar", datetime.isoformat(datetime.now()))
            self.__logger.write_one(data)
            return '', 200
        except:
            data = LoggingData(Source.HAS, LoggingType.Error, "Error occured trying to set targetPressure", datetime.isoformat(datetime.now()))
            self.__logger.write_one(data)
            return '', 400
