from flask import request
from __main__ import socket
import time
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source, Unit, StateRepository, HighVoltageState, MainSwitchState, MainSwitchStateEnum, System


from flask import request
from __main__ import socket
import time
import threading

connected_clients = {}  # key: sid, value: oldData
lock = threading.Lock()
stateRepository = StateRepository()

@socket.on('connect', namespace='/highvoltagesystem')
def handle_connect():
    sid = request.sid
    print(f"Client connected to /highvoltagesystem: {sid}")
    with lock:
        connected_clients[sid] = None  # Initialize client-specific oldData
    socket.start_background_task(target=send_data, sid=sid)


@socket.on('disconnect', namespace='/highvoltagesystem')
def handle_disconnect():
    sid = request.sid
    print(f"Client disconnected from /highvoltagesystem: {sid}")
    with lock:
        connected_clients.pop(sid, None)


def send_data(sid):
    while True:
        with lock:
            if sid not in connected_clients:
                print(f"Stopping background task for disconnected client: {sid}")
                break
            client_old_data = connected_clients[sid]

        highVoltageState = stateRepository.get_for_system(System.highVoltage)
        mainSwitchState = stateRepository.get_for_system(System.mainSwitch)

        if highVoltageState is None or mainSwitchState is None:
            time.sleep(1)
            continue

        if not data_changed(client_old_data, highVoltageState, mainSwitchState):
            time.sleep(1)
            continue

        with lock:
            connected_clients[sid] = {"highVoltageState":highVoltageState, "mainSwitchState":mainSwitchState}  # Update only this client's state

        dataToEmit = {"highVoltageState":highVoltageState.get_dictionary(), "mainSwitchState":mainSwitchState.get_dictionary()}

        print(f"Emitting to {sid} on /highvoltagesystem")
        socket.emit('backendData', dataToEmit, to=sid, namespace='/highvoltagesystem')
        time.sleep(1)


def data_changed(old: dict, newHighVoltageState: HighVoltageState, newMainSwitchState: MainSwitchState):
    if old is None:
        return True

    oldHighVoltageState = old.get("highVoltageState")
    oldMainSwitchState = old.get("mainSwitchState")

    if oldHighVoltageState.hvOn != newHighVoltageState.hvOn:
        return True
    if oldHighVoltageState.automatic != newHighVoltageState.automatic:
        return True
    if oldHighVoltageState.targetPwm != newHighVoltageState.targetPwm:
        return True
    if oldHighVoltageState.targetFrequency != newHighVoltageState.targetFrequency:
        return True
    if oldMainSwitchState.state != newMainSwitchState.state:
        return True
    return False
