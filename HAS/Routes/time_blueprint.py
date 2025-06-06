from flask import Blueprint
from Controllers.time_controller import TimeController

time_blueprint = Blueprint('time', __name__)

controller = TimeController()

time_blueprint.route('/', methods=['GET'])(controller.get_time)