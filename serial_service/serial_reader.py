# serial_reader.py
import serial
from PyQt6.QtCore import QThread, pyqtSignal

class SerialReader(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)
    state_changed = pyqtSignal()

    def __init__(self, serial_port, signal_distributor, flag_state_manager):
        super().__init__()
        self.serial_port = serial_port
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        self.running = True
        self.expecting_response = False
        self.buffer = ""

    def run(self):
        self.log_message.emit("SerialReader thread started")
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    self.log_message.emit("Data available in the buffer")

                    # Read all available data in the buffer
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    self.buffer += data.decode('utf-8', errors='ignore')
                    self.log_message.emit(f"Raw buffer data received: {data}")
                    self.log_message.emit(f"Current buffer: {self.buffer}")

                    # Check for complete messages (ending with a newline or carriage return)
                    while '\r' in self.buffer or '\n' in self.buffer:
                        if '\r' in self.buffer:
                            delimiter = '\r'
                        else:
                            delimiter = '\n'

                        # Split buffer at the first delimiter
                        message, self.buffer = self.buffer.split(delimiter, 1)
                        message = message.strip()
                        self.log_message.emit(f"Decoded data: {message}")

                        if message:
                            if self.validate_response(message):
                                self.expecting_response = False
                                self.log_message.emit(f"Valid data received: {message}")
                            else:
                                self.log_message.emit(f"Unexpected data: {message}")

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
        self.log_message.emit(f"Validating response: {response}")

        if len(response) < 8:
            self.log_message.emit("Response too short")
            return False
        if response[0] == '@':
            if response[4:8] == '0000':
                self.signal_distributor.state_changed.emit('response_received', True, 'update')
                self.signal_distributor.state_changed.emit('waiting_for_completion', True, 'update')
                self.log_message.emit("Emitted state_changed signal: waiting_for_completion set to True")
                return True
        elif response[0] == '$':
            if response[4:8] == '0000':
                self.signal_distributor.state_changed.emit('waiting_for_completion', False, 'update')
                self.signal_distributor.state_changed.emit('completion_received', True, 'update')
                if not self.flag_state_manager.get_flag_status('macro_running'):
                    self.signal_distributor.state_changed.emit('macro_ready_to_run', True, 'update')
                self.log_message.emit("Emitted state_changed signal: waiting_for_completion set to False")
                return True

        self.log_message.emit(f"Invalid response: {response}")
        return False

