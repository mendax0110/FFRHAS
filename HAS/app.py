import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, blueprints, request
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

socket = SocketIO(app, cors_allowed_origins="*")

client = EswClient()

import Socket_handler.HighvoltagesystemHandler
import Socket_handler.OverviewHandler
import Socket_handler.SystemstatusHandler
import Socket_handler.VacuumsystemHandler

if __name__ == "__main__":
    api_thread = threading.Thread(target=client.start_fetching, args=(0.1, 5), daemon=True)
    queue_thread = threading.Thread(target=client.start_fetching_from_queue, daemon=True)
    api_thread.start()
    queue_thread.start()
    socket.run(app, host = "0.0.0.0" ,debug=True, port=5000)