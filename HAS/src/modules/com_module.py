'''
This is the communication module. It is responsible for sending and receiving data from the uC.
'''
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