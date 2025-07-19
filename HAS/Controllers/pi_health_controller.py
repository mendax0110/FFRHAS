from flask import Blueprint, jsonify, render_template
from Services.pi_health_service import run_health_checks

pi_health_bp = Blueprint('pi_health', __name__)

@pi_health_bp.route('/health', methods=['GET'])
def pi_health():
    result = run_health_checks()
    return jsonify(result)

@pi_health_bp.route('/view', methods=['GET'])
def pi_health_view():
    return render_template('piHealth.html', active_page='pi_health')