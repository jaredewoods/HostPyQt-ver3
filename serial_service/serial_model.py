# serial_model.py
import serial
from serial.tools import list_ports
from PyQt6.QtCore import QObject, pyqtSignal
from serial_service.serial_reader import SerialReader

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
    timeout_occurred = pyqtSignal(str)
    valid_response_received = pyqtSignal(str)  # Signal for valid response

    def __init__(self):
        super().__init__()
        self.serial_port = None
        self.reader_thread = None

    @staticmethod
    def get_available_ports():
        ports = list_ports.comports()
        port_list = [port.device for port in ports]
        port_list = [""] + port_list
        return port_list

    def connect(self, port, baudrate=9600):
        try:
            self.serial_port = serial.Serial(port, baudrate)
            self.reader_thread = SerialReader(self.serial_port)
            self.reader_thread.data_received.connect(self.data_received.emit)
            self.reader_thread.error_occurred.connect(self.error_occurred.emit)
            self.reader_thread.log_message.connect(self.log_message.emit)
            self.reader_thread.timeout_occurred.connect(self.timeout_occurred.emit)
            self.reader_thread.valid_response_received.connect(self.valid_response_received.emit)
            self.reader_thread.start()
            self.log_message.emit(f"Connected to {port} at {baudrate} baudrate")
            return True
        except serial.SerialException as e:
            self.error_occurred.emit(f"Error connecting to {port}: {e}")
            return False

    def disconnect_serial(self):
        if self.reader_thread:
            self.reader_thread.stop()
            self.reader_thread = None
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.log_message.emit("Disconnected from serial port")
            return True
        self.error_occurred.emit("Failed to disconnect: Serial port not open")
        return False

    def _send_command(self, command):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.log_message.emit(f"Writing command to serial port: {command}")
                self.serial_port.write(command.encode())
                self.log_message.emit(f"Command written to serial port: {command}")
                self.reader_thread.expecting_response = True
                self.reader_thread.timer.start(self.reader_thread.timeout * 1000)  # Start the response timer
            except serial.SerialException as e:
                self.error_occurred.emit(f"Failed to send command: {e}")
        else:
            self.error_occurred.emit("Failed to send command: Serial port not open")

