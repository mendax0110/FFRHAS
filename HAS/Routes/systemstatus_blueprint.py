from flask import Blueprint
from Controllers.systemstatus_controller import systemstatus_controller

systemstatus_blueprint = Blueprint('systemstatus', __name__)

controller = systemstatus_controller()

systemstatus_blueprint.route('/', methods=['GET'])(controller.render_template)
#ffr_blueprint.route('/create', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['GET'])()
#ffr_blueprint.route('/<int:user_id>/edit', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['DELETE'])()