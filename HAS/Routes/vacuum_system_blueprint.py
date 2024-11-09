from flask import Blueprint
from Controllers.vacuum_system_controller import vacuum_system_controller

vacuum_system_blueprint = Blueprint('vacuumsystem', __name__)

controller = vacuum_system_controller()

vacuum_system_blueprint.route('/', methods=['GET'])(controller.render_template)
#ffr_blueprint.route('/create', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['GET'])()
#ffr_blueprint.route('/<int:user_id>/edit', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['DELETE'])()