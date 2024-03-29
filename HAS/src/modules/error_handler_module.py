## 
# @file error_handler_module.py
# @brief Error handler module class definition \class ErrorHandlerModule
# @date 2021-04-05
# @author placeholder
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