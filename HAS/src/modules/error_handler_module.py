'''
This is the error handler module. It is responsible for handling errors (web,database,etc.)
'''
import os
import sys
import traceback
import logging
import logging.handlers
import logging.config

class ErrorHandlerModule:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = None
        self.init_logger()