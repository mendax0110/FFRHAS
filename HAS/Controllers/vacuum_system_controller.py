from flask import render_template

class vacuum_system_controller:
    def __init__(self):
        pass

    def render_template(self):
        return render_template('vacuumsystem.html', active_page='vacuumsystem')