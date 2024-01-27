## 
# @file main.py
# @brief Main class definition \class HAS
# @date 2021-04-05
# @author placeholder
import os
import sys
from modules import com_module, storage_module, error_handler_module, webservice_module

# 
class HAS:
    def __init__(self):
        self.port = 5000
        self.baudrate = 115200
        self.db_name = 'has_db'
        self.log_file = 'has.log'
        self.com_module = com_module.CommunicationModule(self.port, self.baudrate)
        self.storage_module = storage_module.StorageModule(self.db_name)
        self.error_handler_module = error_handler_module.ErrorHandlerModule(self.log_file)
        self.webservice_module = webservice_module.WebServiceModule(self.port)
