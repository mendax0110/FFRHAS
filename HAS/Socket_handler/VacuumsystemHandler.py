from flask import request
from __main__ import socket
import time
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source, Unit, StateRepository, VacuumState, MainSwitchState, MainSwitchStateEnum, System, Sensor, SensorData, SensorDataRepository


from flask import request
from __main__ import socket
import time
import threading

connected_clients = {}  # key: sid, value: oldData
lock = threading.Lock()
stateRepository = StateRepository()
sensorDataRepository = SensorDataRepository()

@socket.on('connect', namespace='/vacuumsystem')
def handle_connect():
    sid = request.sid
    print(f"Client connected to /vacuumsystem: {sid}")
    with lock:
        connected_clients[sid] = None  # Initialize client-specific oldData
    socket.start_background_task(target=send_data, sid=sid)


@socket.on('disconnect', namespace='/vacuumsystem')
def handle_disconnect():
    sid = request.sid
    print(f"Client disconnected from /vacuumsystem: {sid}")
    with lock:
        connected_clients.pop(sid, None)


def send_data(sid):
    while True:
        with lock:
            if sid not in connected_clients:
                print(f"Stopping background task for disconnected client: {sid}")
                break
            client_old_data = connected_clients[sid]

        vacuumState = stateRepository.get_for_system(System.vacuum)
        mainSwitchState = stateRepository.get_for_system(System.mainSwitch)
        pressure = sensorDataRepository.get_newest_from_sensor(Sensor.get_actual_pressure.name)

        targetPressure = None
        try:
            targetPressure = sensorDataRepository.get_newest_from_sensor(Sensor.target_pressure.name)
        except:
            targetPressure = None

        if vacuumState is None or mainSwitchState is None or pressure is None or targetPressure is None:
            time.sleep(1)
            continue

        if targetPressure.value > -1:
            vacuumState.targetPressure = targetPressure.value

        StateRepository.update_state_for(vacuumState)

        if not state_data_changed(client_old_data, vacuumState, mainSwitchState) and not sensor_data_changed(client_old_data, pressure):
            time.sleep(1)
            continue

        with lock:
            connected_clients[sid] = {"vacuumState": vacuumState, "mainSwitchState":mainSwitchState, "pressure":pressure }  # Update only this client's state

        dataToEmit = {"vacuumstate": vacuumState.get_dictionary(), "mainSwitchState": mainSwitchState.get_dictionary(), "pressure": pressure.get_dictionary()}

        print(f"Emitting to {sid} on /vacuumsystem")
        socket.emit('backendData', dataToEmit, to=sid, namespace='/vacuumsystem')
        time.sleep(1)


def state_data_changed(old: dict, newVacuumState: VacuumState, newMainSwitchState: MainSwitchState):
    if old is None:
        return True

    oldVacuumState = old.get("vacuumState")
    oldMainSwitchState = old.get("mainSwitchState")

    if oldVacuumState.pumpOn != newVacuumState.pumpOn:
        return True
    if oldVacuumState.automatic != newVacuumState.automatic:
        return True
    if oldVacuumState.targetPressure != newVacuumState.targetPressure:
        return True
    if oldMainSwitchState.state != newMainSwitchState.state:
        return True
    return False

def sensor_data_changed(old: dict, pressure: SensorData):
    if old is None:
        return True

    oldPressure = old.get("pressure")

    if oldPressure.value != pressure.value:
        return True
    return False
