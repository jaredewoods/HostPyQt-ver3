# serial_reader.py
import serial
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
import re

class SerialReader(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)
    timeout_occurred = pyqtSignal(str)
    valid_response_received = pyqtSignal(str)  # Signal for valid response

    def __init__(self, serial_port, timeout=5):
        super().__init__()
        self.serial_port = serial_port
        self.timeout = timeout
        self.running = True
        self.expecting_response = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.timer.setSingleShot(True)  # Ensure the timer only runs once per start

    def run(self):
        self.timer.moveToThread(self)  # Move the timer to the same thread
        self.log_message.emit("SerialReader thread started")
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    data = self.serial_port.readline().decode('utf-8').strip()
                    if data:
                        self.log_message.emit(f"Raw data received: {data}")
                        if self.validate_response(data):
                            self.valid_response_received.emit(data)
                            self.timer.stop()  # Stop the timer when valid data is received
                            self.expecting_response = False
                            self.log_message.emit(f"Valid data received: {data}")
                        else:
                            self.log_message.emit(f"Ignored invalid data: {data}")
                else:
                    self.msleep(100)  # Sleep for a short duration to prevent busy waiting
            except serial.SerialException as e:
                self.error_occurred.emit(f"Serial error: {e}")
                self.running = False
            except Exception as e:
                self.error_occurred.emit(f"Unexpected error: {e}")
                self.running = False
        self.log_message.emit("SerialReader thread stopped")

    def on_timeout(self):
        self.timeout_occurred.emit("Timeout: No response received.")
        self.expecting_response = False
        self.timer.stop()  # Ensure the timer stops after the timeout

    def stop(self):
        self.running = False
        self.timer.stop()
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
