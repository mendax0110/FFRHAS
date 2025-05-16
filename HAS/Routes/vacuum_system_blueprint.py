from flask import Blueprint
from Controllers.vacuum_system_controller import vacuum_system_controller

vacuum_system_blueprint = Blueprint('vacuumsystem', __name__)

controller = vacuum_system_controller()

vacuum_system_blueprint.route('/', methods=['GET'])(controller.render_template)
vacuum_system_blueprint.route('/startAutomatic', methods=['GET'])(controller.start_automatic)
vacuum_system_blueprint.route('/stopAutomatic', methods=['GET'])(controller.stop_automatic)
vacuum_system_blueprint.route('/pumpOn', methods=['GET'])(controller.pump_on)
vacuum_system_blueprint.route('/pumpOff', methods=['GET'])(controller.pump_off)
vacuum_system_blueprint.route('/setTargetPressure', methods=['GET'])(controller.set_target_pressure)