from flask import Blueprint
from Controllers.overview_controller import overview_controller

overview_blueprint = Blueprint('overview', __name__)

controller = overview_controller()

overview_blueprint.route('/', methods=['GET'])(controller.render_template)
#ffr_blueprint.route('/create', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['GET'])()
#ffr_blueprint.route('/<int:user_id>/edit', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['DELETE'])()