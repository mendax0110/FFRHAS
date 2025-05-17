from flask import Blueprint
from Controllers.hv_system_controller import hv_system_controller

hv_system_blueprint = Blueprint('highvoltagesystem', __name__)

controller = hv_system_controller()

hv_system_blueprint.route('/', methods=['GET'])(controller.render_template)
hv_system_blueprint.route('/StartHighVoltage', methods=['GET'])(controller.start_high_voltage)
hv_system_blueprint.route('/StopHighVoltage', methods=['GET'])(controller.stop_high_voltage)
hv_system_blueprint.route('/StartAutomatic', methods=['GET'])(controller.start_automatic)
hv_system_blueprint.route('/StopAutomatic', methods=['GET'])(controller.stop_automatic)
hv_system_blueprint.route('/setTargetFrequency', methods=['GET'])(controller.set_target_frequency)
hv_system_blueprint.route('/setTargetPwm', methods=['GET'])(controller.set_target_pwm)