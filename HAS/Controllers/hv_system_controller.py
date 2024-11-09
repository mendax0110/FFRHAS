from flask import render_template

class hv_system_controller:
    def __init__(self):
        pass

    def render_template(self):
        return render_template('highvoltagesystem.html', active_page='highvoltagesystem')