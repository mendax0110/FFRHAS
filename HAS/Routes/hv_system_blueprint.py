from flask import Blueprint
from Controllers.hv_system_controller import hv_system_controller

hv_system_blueprint = Blueprint('highvoltagesystem', __name__)

controller = hv_system_controller()

hv_system_blueprint.route('/', methods=['GET'])(controller.render_template)
hv_system_blueprint.route('/get', methods=['GET'])(controller.get)
hv_system_blueprint.route('/save', methods=['POST'])(controller.save)