from flask import Blueprint
from Controllers.time_controller import time_controller

time_blueprint = Blueprint('time', __name__)

controller = time_controller()

time_blueprint.route('/', methods=['GET'])(controller.get_time)