## 
# @file webservice_module.py
# @brief Web service module class definition \class WebServiceModule
# @date 2021-04-05
# @author placeholder
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