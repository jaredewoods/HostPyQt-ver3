# serial_reader.py
import serial
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot

class SerialReader(QThread):
    alarm_signal = pyqtSignal(str, str)
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
        self.signal_distributor.DEBUG_MESSAGE.emit("SerialReader thread started")
        while self.running:
            try:
                if self.serial_port.in_waiting:
                    self.signal_distributor.DEBUG_MESSAGE.emit("Data available in the buffer")

                    # Read all available data in the buffer
                    data = self.serial_port.read(self.serial_port.in_waiting)
                    self.buffer += data.decode('utf-8', errors='ignore')
                    self.signal_distributor.DEBUG_MESSAGE.emit(f"Raw buffer data received: {data}")
                    self.signal_distributor.DEBUG_MESSAGE.emit(f"Current buffer: {self.buffer.replace('\r', '<CR>')}")

                    # Check for complete messages (ending with a newline or carriage return)
                    while '\r' in self.buffer or '\n' in self.buffer:
                        if '\r' in self.buffer:
                            delimiter = '\r'
                        else:
                            delimiter = '\n'

                        # Split buffer at the first delimiter
                        message, self.buffer = self.buffer.split(delimiter, 1)
                        if message:
                            self.signal_distributor.LOG_MESSAGE.emit(f"        (received)  {message.strip()}")

                        message = message.strip()
                        self.signal_distributor.DEBUG_MESSAGE.emit(f"Decoded data: {message}")

                        if message:
                            if self.validate_response(message):
                                self.expecting_response = False
                                self.signal_distributor.DEBUG_MESSAGE.emit(f"Valid data received: {message}")
                            else:
                                self.signal_distributor.DEBUG_MESSAGE.emit(f"Unexpected data: {message}")

                else:
                    self.msleep(100)  # Sleep for a short duration to prevent busy waiting
            except serial.SerialException as e:
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Serial error: {e}")
                self.running = False
            except Exception as e:
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Unexpected error: {e}")
                self.running = False
        self.signal_distributor.DEBUG_MESSAGE.emit("SerialReader thread stopped")

    def stop(self):
        self.running = False
        self.wait()

    @pyqtSlot(str)
    def validate_response(self, response):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Validating response: {response}")

        if len(response) < 8:
            self.signal_distributor.DEBUG_MESSAGE.emit("Response too short")
            return False
        if response[0] == '@':
            if response[4:8] == '0000':
                self.signal_distributor.STATE_CHANGED_SIGNAL.emit('response_received', True, 'update')
                self.signal_distributor.STATE_CHANGED_SIGNAL.emit('waiting_for_completion', True, 'update')
                self.signal_distributor.DEBUG_MESSAGE.emit("Emitted state_changed signal: waiting_for_completion set to True")
                self.signal_distributor.MACRO_TRIGGER_SEQ02_SIGNAL.emit()
                return True
            else:
                self.signal_distributor.STATE_CHANGED_SIGNAL.emit('alarm_received', False, 'update')
                alarm_code = response[4:8]
                subcode = response[9:12]
                self.signal_distributor.ALARM_MESSAGE.emit(alarm_code, subcode)
                return False

        elif response[0] == '$':
            if response[4:8] == '0000':
                self.signal_distributor.STATE_CHANGED_SIGNAL.emit('waiting_for_completion', False, 'update')
                self.signal_distributor.STATE_CHANGED_SIGNAL.emit('completion_received', True, 'update')
                if not self.flag_state_manager.get_flag_status('macro_running'):
                    self.signal_distributor.STATE_CHANGED_SIGNAL.emit('macro_ready_to_run', True, 'update')
                self.signal_distributor.DEBUG_MESSAGE.emit("Emitted state_changed signal: waiting_for_completion set to False")
                self.signal_distributor.MACRO_TRIGGER_SEQ03_SIGNAL.emit()
                return True
            else:
                self.signal_distributor.STATE_CHANGED_SIGNAL.emit('alarm_received', True, 'update')
                alarm_code = response[4:8]
                subcode = response[9:12]
                self.signal_distributor.ALARM_MESSAGE.emit(alarm_code, subcode)
                return False

        self.signal_distributor.DEBUG_MESSAGE.emit(f"Invalid response: {response}")
        return False
