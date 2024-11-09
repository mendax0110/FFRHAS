from flask import Flask, render_template, blueprints
from Routes.overview_blueprint import overview_blueprint
from Routes.vacuum_system_blueprint import vacuum_system_blueprint
from Routes.hv_system_blueprint import hv_system_blueprint
from Routes.systemstatus_blueprint import systemstatus_blueprint
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(overview_blueprint, url_prefix='/')
app.register_blueprint(vacuum_system_blueprint, url_prefix='/vacuumsystem')
app.register_blueprint(hv_system_blueprint, url_prefix='/highvoltagesystem')
app.register_blueprint(systemstatus_blueprint, url_prefix='/systemstatus')
CORS(app)


if __name__ == "__main__":
    app.run(host = "0.0.0.0" ,debug=True, port=5000)