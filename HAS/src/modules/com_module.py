## 
# @file com_module.py
# @brief Communication module class definition
# @class CommunicationModule
# @date 2021-04-05
# @author placeholder
import os
import sys
import serial
import socket


class CommunicationModule:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.sock = None