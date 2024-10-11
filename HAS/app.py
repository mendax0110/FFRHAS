from flask import Flask, render_template, blueprints
from Routes.ffr_blueprint import ffr_blueprint

app = Flask(__name__)

app.register_blueprint(ffr_blueprint, url_prefix='/get_data_from_backend')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)