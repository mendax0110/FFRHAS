import time
from threading import Thread

from flask import Flask, render_template, blueprints
from Routes.overview_blueprint import overview_blueprint
from Routes.vacuum_system_blueprint import vacuum_system_blueprint
from Routes.hv_system_blueprint import hv_system_blueprint
from Routes.systemstatus_blueprint import systemstatus_blueprint
from Routes.time_blueprint import time_blueprint
from flask_cors import CORS
from Services.http_clients import EswClient
import threading
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.register_blueprint(overview_blueprint, url_prefix='/')
app.register_blueprint(vacuum_system_blueprint, url_prefix='/vacuumsystem')
app.register_blueprint(hv_system_blueprint, url_prefix='/highvoltagesystem')
app.register_blueprint(systemstatus_blueprint, url_prefix='/systemstatus')
app.register_blueprint(time_blueprint, url_prefix='/time')
CORS(app)

socketio = SocketIO(app)

def sendMessage():
    while True:
        socketio.emit('newDataAvailable', {'data': False})
        time.sleep(3)

        socketio.emit('newDataAvailable', {'data': True})
        time.sleep(3)

eswEndpoints = [
    "http://192.168.1.3/temperature_sensor_1",
    "http://192.168.1.3/temperature_sensor_2"
]

client = EswClient(eswEndpoints)


if __name__ == "__main__":
    api_thread = threading.Thread(target=client.start_fetching, daemon=True)
    api_thread.start()
    socketio.start_background_task(sendMessage)
    socketio.run(app ,host = "0.0.0.0" ,debug=True, port=5000, allow_unsafe_werkzeug=True)
