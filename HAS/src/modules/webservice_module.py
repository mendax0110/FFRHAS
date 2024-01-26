'''
This is the web service module. It is responsible for handling web requests (GET, POST, etc.)
'''
import os
import sys
import json
from flask import Flask, request, jsonify

class WebServiceModule:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.init_routes()
        self.app.run(host='localhost')