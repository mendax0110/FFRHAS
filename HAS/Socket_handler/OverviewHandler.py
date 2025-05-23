from flask import request
from __main__ import socket
import time


from flask import request
from __main__ import socket
import time
import threading

connected_clients = set()
lock = threading.Lock()


@socket.on('connect', namespace='/overview')
def handle_connect():
    sid = request.sid
    print(f"Client connected to /overview: {sid}")
    with lock:
        connected_clients.add(sid)
    socket.start_background_task(target=send_data, sid=sid)


@socket.on('disconnect', namespace='/overview')
def handle_disconnect():
    sid = request.sid
    print(f"Client disconnected from /overview: {sid}")
    with lock:
        connected_clients.discard(sid)


def send_data(sid):
    while True:
        with lock:
            if sid not in connected_clients:
                print(f"Stopping background task for disconnected client: {sid}")
                break
        print("Emitting on overview")

        # PUT YOUR LOGIC HERE

        socket.emit('backendData', "test, test, test", to=sid, namespace='/overview')
        time.sleep(1)
