from flask import Blueprint
from Controllers.test_controller import test_controller

ffr_blueprint = Blueprint('ffr_blueprint', __name__)

controller = test_controller()

ffr_blueprint.route('/', methods=['GET'])(controller.get_data)
#ffr_blueprint.route('/create', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['GET'])()
#ffr_blueprint.route('/<int:user_id>/edit', *methods*=['POST'])()
#ffr_blueprint.route('/<int:user_id>', *methods*=['DELETE'])()