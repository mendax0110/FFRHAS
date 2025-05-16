from flask import request
from __main__ import socket
import time
from Services.Repositories import LoggingRepository, LoggingData, LoggingType, Source, Unit, StateRepository, VacuumState, System


from flask import request
from __main__ import socket
import time
import threading

connected_clients = {}  # key: sid, value: oldData
lock = threading.Lock()
stateRepository = StateRepository()

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
        if vacuumState is None:
            time.sleep(1)
            continue

        if not data_changed(client_old_data, vacuumState):
            time.sleep(1)
            continue

        with lock:
            connected_clients[sid] = vacuumState  # Update only this client's state

        print(f"Emitting to {sid} on /vacuumsystem")
        socket.emit('backendData', vacuumState.get_dictionary(), to=sid, namespace='/vacuumsystem')
        time.sleep(1)


def data_changed(old: VacuumState, new: VacuumState):
    if old is None:
        return True
    if old.pumpOn != new.pumpOn:
        return True
    if old.automatic != new.automatic:
        return True
    if old.targetPressure != new.targetPressure:
        return True
    return False
