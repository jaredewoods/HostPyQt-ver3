# serial_model.py
import serial
from serial.tools import list_ports
from PyQt6.QtCore import QObject, pyqtSignal
# TODO: fix delay and command sent logging
class SerialModel(QObject):
    """
    Model responsible for managing the serial connection and communication.

    Attributes:
        data_received: Signal emitted when data is received from the serial port.
        error_occurred: Signal emitted when an error occurs.
        log_message: Signal emitted for general log messages.
    """
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)

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
            self.serial_port = serial.Serial(port, baudrate, timeout=1)
            self.log_message.emit(f"Connected to {port} at {baudrate} baudrate")
            return True
        except serial.SerialException as e:
            self.error_occurred.emit(f"Error connecting to {port}: {e}")
            return False

    def disconnect_serial(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.log_message.emit("Disconnected from serial port")
            return True
        self.error_occurred.emit("Failed to disconnect: Serial port not open")
        return False

    def send_command(self, command):
        if self.serial_port and self.serial_port.is_open:
            print(f"Command sent: {command}")
            self.log_message.emit(f"Command sent: {command}")
            try:
                self.serial_port.write(command.encode())
                self.read_response()
            except serial.SerialException as e:
                self.error_occurred.emit(f"Failed to send command: {e}")
        else:
            self.error_occurred.emit("Failed to send command: Serial port not open")

    def read_response(self):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.log_message.emit("Waiting for response...")
                response = self.serial_port.read_until(b'\r')
                response_str = response.decode().strip()
                if response_str:
                    self.data_received.emit(response_str)
                    self.log_message.emit(f"Response received: {response_str}")
                else:
                    self.error_occurred.emit("Timeout: No response received.")
                    self.log_message.emit("Timeout: No response received.")
            except serial.SerialException as e:
                self.error_occurred.emit(f"Failed to read response: {e}")
                self.log_message.emit(f"Failed to read response: {e}")
        else:
            self.error_occurred.emit("Failed to read response: Serial port not open")
