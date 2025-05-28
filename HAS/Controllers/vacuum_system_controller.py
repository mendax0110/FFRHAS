from flask import render_template, request
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source, Unit, StateRepository, VacuumState, System
from datetime import datetime
from Services.http_clients import EswClient
import Services.endpoints as endpoint
class vacuum_system_controller:
    def __init__(self):
        self.__logger = LoggingRepository()
        self.__stateRepository = StateRepository()

    def render_template(self):
        vacuumState = self.__stateRepository.get_for_system(System.vacuum)
        if (vacuumState == None):
            vacuumState = VacuumState(False, 1000, False, False)
        self.__stateRepository.update_state_for(vacuumState)
        return render_template('vacuumsystem.html', active_page='vacuumsystem', pumpOn=vacuumState.pumpOn, targetPressure=vacuumState.targetPressure, automatic=vacuumState.automatic, handBetrieb=vacuumState.handBetrieb)

    def start_automatic(self):
        vacuumState = self.__stateRepository.get_for_system(System.vacuum)
        vacuumState.automatic = True
        self.__stateRepository.update_state_for(vacuumState)
        data = LoggingData(Source.HAS, LoggingType.Info, "started vacuum-automatic", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def stop_automatic(self):
        vacuumState = self.__stateRepository.get_for_system(System.vacuum)
        vacuumState.automatic = False
        self.__stateRepository.update_state_for(vacuumState)
        data = LoggingData(Source.HAS, LoggingType.Info, "stopped vacuum-automatic", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def pump_on(self):
        with EswClient.lock:
            EswClient.endpointQueue.append(endpoint.pumpOn)
        vacuumState = self.__stateRepository.get_for_system(System.vacuum)
        vacuumState.pumpOn = True
        self.__stateRepository.update_state_for(vacuumState)
        data = LoggingData(Source.HAS, LoggingType.Info, "turned pump on", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def pump_off(self):
        with EswClient.lock:
            EswClient.endpointQueue.append(endpoint.pumpOff)
        vacuumState = self.__stateRepository.get_for_system(System.vacuum)
        vacuumState.pumpOn = False
        self.__stateRepository.update_state_for(vacuumState)
        data = LoggingData(Source.HAS, LoggingType.Info, "turned pump off", datetime.isoformat(datetime.now()))
        self.__logger.write_one(data)
        return '', 200

    def set_target_pressure(self):
        try:
            targetPressure = float(request.args.get('targetPressure'))
            with EswClient.lock:
                EswClient.endpointQueue.append(endpoint.pressureControlMode)
                EswClient.endpointQueue.append(endpoint.setTargetPressure(targetPressure))
            vacuumState = self.__stateRepository.get_for_system(System.vacuum)
            vacuumState.targetPressure = targetPressure
            self.__stateRepository.update_state_for(vacuumState)
            data = LoggingData(Source.HAS, LoggingType.Info, f"set target pressure to: {targetPressure} mbar", datetime.isoformat(datetime.now()))
            self.__logger.write_one(data)
            return '', 200
        except:
            data = LoggingData(Source.HAS, LoggingType.Error, "Error occured trying to set targetPressure", datetime.isoformat(datetime.now()))
            self.__logger.write_one(data)
            return '', 400
