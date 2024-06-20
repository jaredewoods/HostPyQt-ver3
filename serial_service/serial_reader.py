# serial_reader.py
import serial
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

class SerialReader(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)
    timeout_occurred = pyqtSignal(str)

    def __init__(self, serial_port, timeout=1):
        super().__init__()
        self.serial_port = serial_port
        self.timeout = timeout
        self.running = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)

    def run(self):
        self.timer.moveToThread(self)  # Move the timer to the same thread
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    data = self.serial_port.readline().decode('utf-8').strip()
                    if data:
                        self.data_received.emit(f"Received: {data}")
                        self.timer.stop()  # Stop the timer when data is received
                else:
                    if not self.timer.isActive():
                        self.timer.start(self.timeout * 1000)  # Start the timer if it's not active
            except serial.SerialException as e:
                self.error_occurred.emit(f"Serial error: {e}")
                self.running = False
            except Exception as e:
                self.error_occurred.emit(f"Unexpected error: {e}")
                self.running = False

    def on_timeout(self):
        self.timeout_occurred.emit("Timeout: No response received.")
        self.timer.stop()  # Ensure the timer stops after the timeout

    def stop(self):
        self.running = False
        self.timer.stop()
        self.wait()
