# serial_reader.py
import serial
from PyQt6.QtCore import QThread, pyqtSignal

class SerialReader(QThread):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)
    state_changed = pyqtSignal

    def __init__(self, serial_port, signal_distributor, flag_state_manager):
        super().__init__()
        self.serial_port = serial_port
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
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
        if len(response) < 8:
            return False
        if response[0] == '@':
            if response[4:8] == '0000':
                self.signal_distributor.state_changed.emit('response_received', True, 'update')
                self.signal_distributor.state_changed.emit('waiting_for_completion', True, 'update')
                print("Emitted state_changed signal: waiting_for_completion set to True")
                return True
        elif response[0] == '$':
            if response[4:8] == '0000':
                # Emit the state_changed signal for a valid command completion
                self.signal_distributor.state_changed.emit('waiting_for_completion', False, 'update')
                self.signal_distributor.state_changed.emit('completion_received', True, 'update')
                if not self.flag_state_manager.get_flag_status('macro_running'):
                    self.signal_distributor.state_changed.emit('macro_ready_to_run', True, 'update')

                print("Emitted state_changed signal: waiting_for_completion set to False")
                return True
        return False

