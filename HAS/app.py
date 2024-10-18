import os

from flask import Flask, render_template, blueprints
from Routes.ffr_blueprint import ffr_blueprint
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(ffr_blueprint, url_prefix='/get_data_from_backend')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host = "0.0.0.0" ,debug=True, port=5000)