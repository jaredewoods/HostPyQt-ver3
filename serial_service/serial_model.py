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
        debug_message: Signal emitted for general log messages.
    """
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    debug_message = pyqtSignal(str)
    log_message = pyqtSignal(str)
    alarm_signal = pyqtSignal(str, str)

    def __init__(self, signal_distributor, flag_state_manager):
        super().__init__()
        self.serial_port = None
        self.reader_thread = None
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        print("SerialModel initialized")

    @staticmethod
    def get_available_ports():
        ports = list_ports.comports()
        port_list = [port.device for port in ports]
        port_list = [""] + port_list
        return port_list

    def connect(self, port, baudrate=9600):
        try:
            self.serial_port = serial.Serial(port,
                                             baudrate,
                                             parity=serial.PARITY_NONE,
                                             stopbits=serial.STOPBITS_ONE,
                                             bytesize=serial.EIGHTBITS,)
            self.reader_thread = SerialReader(self.serial_port, self.signal_distributor, self.flag_state_manager)
            self.reader_thread.data_received.connect(self.data_received.emit)
            self.reader_thread.error_occurred.connect(self.error_occurred.emit)
            # should this be outside the scope?vvvv
            self.reader_thread.debug_message.connect(self.debug_message.emit)
            self.reader_thread.log_message.connect(self.log_message.emit)
            self.reader_thread.alarm_signal.connect(self.alarm_signal.emit)
            self.reader_thread.start()
            self.debug_message.emit(f"Connected to {port} at {baudrate} baudrate")
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
            self.debug_message.emit("Disconnected from serial port")
            return True
        self.error_occurred.emit("Failed to disconnect: Serial port not open")
        return False

    def filter_constructed_command(self, command):
        if "WAIT" in command:
            print(f"we got to pause due to a {command}")
            self.signal_distributor.WAIT_COMMAND_EXECUTOR_SIGNAL.emit(command)
        elif "SEND" in command:
            print(F"we got a XG-X{command}")
            self.signal_distributor.xgx_command_executor.emit(command)
        else:
            print(f"NXC100 command {command}")
            self.write_command_to_serial(command)
            print("d07 SerialModel")

    def write_command_to_serial(self, command):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write(command.encode())
                cleaned_command = command.replace('\r', '').replace('\n', '')
                self.debug_message.emit(f"Command written to serial port: {cleaned_command}")
                self.log_message.emit(f"  (sent)  {cleaned_command}")
                # I believe this is redundant, keep the state_changed
                self.reader_thread.expecting_response = True
                self.signal_distributor.state_changed.emit('completion_received', False, 'update')
                self.signal_distributor.state_changed.emit('response_received', False, 'update')
                print("d08 SerialModel")

            except serial.SerialException as e:
                self.error_occurred.emit(f"Failed to send command: {e}")
        else:
            self.error_occurred.emit("Failed to send command: Serial port not open")


