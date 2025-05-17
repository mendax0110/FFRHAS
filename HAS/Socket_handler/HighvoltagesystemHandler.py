from flask import request
from __main__ import socket
import time
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source, Unit, StateRepository, HighVoltageState, System


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
        if highVoltageState is None:
            time.sleep(1)
            continue

        if not data_changed(client_old_data, highVoltageState):
            time.sleep(1)
            continue

        with lock:
            connected_clients[sid] = highVoltageState  # Update only this client's state

        print(f"Emitting to {sid} on /highvoltagesystem")
        socket.emit('backendData', highVoltageState.get_dictionary(), to=sid, namespace='/highvoltagesystem')
        time.sleep(1)


def data_changed(old: HighVoltageState, new: HighVoltageState):
    if old is None:
        return True
    if old.hvOn != new.hvOn:
        return True
    if old.automatic != new.automatic:
        return True
    if old.targetPwm != new.targetPwm:
        return True
    if old.targetFrequency != new.targetFrequency:
        return True
    if old.handBetrieb != new.handBetrieb:
        return True
    return False
