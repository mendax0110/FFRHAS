from datetime import datetime

from flask import render_template, request
from Services.Repositories import SensorDataRepository, SensorData, Unit, LoggingData, LoggingType, LoggingRepository, Source, HighVoltageState, System, StateRepository
import pymongo
from flask.json import dumps

class hv_system_controller:
    def __init__(self):
        self.__logger = LoggingRepository()
        self.__sensorRepository = SensorDataRepository()
        self.__stateRepository = StateRepository()

    def render_template(self):
        highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
        if highVoltageState is None:
            highVoltageState = HighVoltageState(False, 25, 50, False, False)
            self.__stateRepository.update_state_for(highVoltageState)

        return render_template('highvoltagesystem.html',
                               active_page='highvoltagesystem',
                               hvOn=highVoltageState.hvOn,
                               targetFrequency=highVoltageState.targetFrequency,
                               targetPwm=highVoltageState.targetPwm,
                               automatic=highVoltageState.automatic,
                               handBetrieb=highVoltageState.handBetrieb)

    def start_high_voltage(self):
        highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
        highVoltageState.hvOn = True
        self.__stateRepository.update_state_for(highVoltageState)
        data = LoggingData(Source.HAS, LoggingType.Info, "started high-voltage", datetime.isoformat(datetime.now()))
        # self.__logger.write_one(data)
        return '', 200

    def stop_high_voltage(self):
        highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
        highVoltageState.hvOn = False
        self.__stateRepository.update_state_for(highVoltageState)
        data = LoggingData(Source.HAS, LoggingType.Info, "stopped high-voltage", datetime.isoformat(datetime.now()))
        #self.__logger.write_one(data)
        return '', 200

    def start_automatic(self):
        highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
        highVoltageState.automatic = True
        self.__stateRepository.update_state_for(highVoltageState)
        data = LoggingData(Source.HAS, LoggingType.Info, "started high-voltage-automatic", datetime.isoformat(datetime.now()))
        #self.__logger.write_one(data)
        return '', 200

    def stop_automatic(self):
        highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
        highVoltageState.automatic = False
        self.__stateRepository.update_state_for(highVoltageState)
        data = LoggingData(Source.HAS, LoggingType.Info, "stopped high-voltage-automatic", datetime.isoformat(datetime.now()))
        #self.__logger.write_one(data)
        return '', 200

    def set_target_frequency(self):
        try:
            target_frequency = float(request.args.get('targetFrequency'))
            highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
            highVoltageState.targetFrequency = target_frequency
            self.__stateRepository.update_state_for(highVoltageState)
            data = LoggingData(Source.HAS, LoggingType.Info, f"set target frequency to: {target_frequency} kHz",
                               datetime.isoformat(datetime.now()))
            # self.__logger.write_one(data)
            return '', 200
        except:
            data = LoggingData(Source.HAS, LoggingType.Error, "Error occured trying to set target Frequency",
                               datetime.isoformat(datetime.now()))
            # self.__logger.write_one(data)
            return '', 400

    def set_target_pwm(self):
        try:
            target_pwm = float(request.args.get('targetPwm'))
            highVoltageState = self.__stateRepository.get_for_system(System.highVoltage)
            highVoltageState.targetPwm = target_pwm
            self.__stateRepository.update_state_for(highVoltageState)
            data = LoggingData(Source.HAS, LoggingType.Info, f"set target pwm to: {target_pwm} kHz",
                               datetime.isoformat(datetime.now()))
            # self.__logger.write_one(data)
            return '', 200
        except:
            data = LoggingData(Source.HAS, LoggingType.Error, "Error occured trying to set target pwm",
                               datetime.isoformat(datetime.now()))
            # self.__logger.write_one(data)
            return '', 400