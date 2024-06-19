# serial_model.py
import serial
from serial.tools import list_ports
from PyQt6.QtCore import QObject, pyqtSignal

class SerialModel(QObject):
    """
    Model responsible for managing the serial connection and communication.

    Attributes:
        data_received: Signal emitted when data is received from the serial port.
        error_occurred: Signal emitted when an error occurs.
    """
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_port = None

    @staticmethod
    def get_available_ports():
        ports = list_ports.comports()
        port_list = [port.device for port in ports]
        port_list = [""] + port_list
        return port_list

    def connect(self, port, baudrate=9600):
        try:
            self.serial_port = serial.Serial(port, baudrate)
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {port}: {e}")
            return False

    def disconnect_serial(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            return True
        return False

    def send_command(self, command):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(command.encode())
                print(f"Command sent: {command}")
                self.read_response()
            except serial.SerialException as e:
                print(f"Failed to send command: {e}")
                self.error_occurred.emit(f"Failed to send command: {e}")

    def read_response(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                response = self.serial_port.read_until(b'\r')
                response_str = response.decode().strip()
                print(f"Response received: {response_str}")
                self.data_received.emit(response_str)
            except serial.SerialException as e:
                print(f"Failed to read response: {e}")
                self.error_occurred.emit(f"Failed to read response: {e}")