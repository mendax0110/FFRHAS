from flask import Blueprint
from Controllers.hv_system_controller import hv_system_controller

hv_system_blueprint = Blueprint('highvoltagesystem', __name__)

controller = hv_system_controller()

hv_system_blueprint.route('/', methods=['GET'])(controller.render_template)
#ffr_blueprint.route('/create', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['GET'])()
#ffr_blueprint.route('/<int:user_id>/edit', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['DELETE'])()