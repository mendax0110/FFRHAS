from flask import render_template

class overview_controller:
    def __init__(self):
        pass

    def render_template(self):
        return render_template('overview.html', active_page='overview')