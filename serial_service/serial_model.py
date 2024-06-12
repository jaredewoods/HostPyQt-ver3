# serial_model.py
import serial
from serial.tools import list_ports


class SerialModel:
    def __init__(self):
        pass

    @staticmethod
    def get_available_ports():
        ports = list_ports.comports()
        return [port.device for port in ports]
    