from flask import Flask, render_template, blueprints
from Routes.ffr_blueprint import ffr_blueprint

app = Flask(__name__)

app.register_blueprint(ffr_blueprint, url_prefix='/get_data_from_backend')

@app.route('/')
def index():
    return render_template('index.html')

# We need 0.0.0.0 to be able to access the HAS in the Docker-Contianer
# Otherwise we cannot access it from the host or other machines which are trying to access the host
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
