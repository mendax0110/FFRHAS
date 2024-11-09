from flask import render_template

class systemstatus_controller:
    def __init__(self):
        pass

    def render_template(self):
        return render_template('systemstatus.html', active_page='systemstatus')