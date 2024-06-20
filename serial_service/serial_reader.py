# serial_reader.py
import serial
from PyQt6.QtCore import QThread, pyqtSignal

class SerialReader(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)

    def __init__(self, serial_port):
        super().__init__()
        self.serial_port = serial_port
        self.running = True
        self.expecting_response = False

    def run(self):
        self.log_message.emit("SerialReader thread started")
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    data = self.serial_port.readline().decode('utf-8').strip()
                    if data:
                        # self.log_message.emit(f"Raw data received: {data}")
                        if self.validate_response(data):
                            self.expecting_response = False
                            self.log_message.emit(f"Valid data received: {data}")
                        else:
                            self.log_message.emit(f"Unexpected data: {data}")
                else:
                    self.msleep(100)  # Sleep for a short duration to prevent busy waiting
            except serial.SerialException as e:
                self.error_occurred.emit(f"Serial error: {e}")
                self.running = False
            except Exception as e:
                self.error_occurred.emit(f"Unexpected error: {e}")
                self.running = False
        self.log_message.emit("SerialReader thread stopped")

    def stop(self):
        self.running = False
        self.wait()

    def validate_response(self, response):
        # Validate if the response starts with '@' and bits 5, 6, 7, 8 are zeros
        if len(response) < 8:
            return False
        if response[0] != '@':
            return False
        if response[4:8] != '0000':
            return False
        return True
