# serial_model.py
import serial
from serial.tools import list_ports


class SerialModel:
    def __init__(self):
        pass

    @staticmethod
    def get_available_ports():
        ports = list_ports.comports()
        port_list = [port.device for port in ports]
        port_list = [""] + port_list
        return port_list
    