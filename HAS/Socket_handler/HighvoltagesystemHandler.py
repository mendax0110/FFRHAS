from flask import request
from __main__ import socket
import time


from flask import request
from __main__ import socket
import time
import threading

connected_clients = set()
lock = threading.Lock()


@socket.on('connect', namespace='/highvoltagesystem')
def handle_connect():
    sid = request.sid
    print(f"Client connected to /highvoltagesystem: {sid}")
    with lock:
        connected_clients.add(sid)
    socket.start_background_task(target=send_data, sid=sid)


@socket.on('disconnect', namespace='/highvoltagesystem')
def handle_disconnect():
    sid = request.sid
    print(f"Client disconnected from /highvoltagesystem: {sid}")
    with lock:
        connected_clients.discard(sid)


def send_data(sid):
    while True:
        with lock:
            if sid not in connected_clients:
                print(f"Stopping background task for disconnected client: {sid}")
                break
        print("Emitting on highvoltagesystem")

        # PUT YOUR LOGIC HERE

        socket.emit('backendData', "test, test, test", to=sid, namespace='/highvoltagesystem')
        time.sleep(1)
