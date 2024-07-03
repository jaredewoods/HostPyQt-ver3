# tcp_model.py

import socket
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class TCPModel(QObject):
    def __init__(self, signal_distributor):
        super().__init__()
        self.signal_distributor = signal_distributor
        self.filtered_command = None
        self.unfiltered_command = None
        self.tcp_socket = None
        self.filtered_command = None
        self.decoded_data = None

    def connect(self, ip_address, port):
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.settimeout(1)
            self.tcp_socket.connect((ip_address, int(port)))
            return True
        except socket.error as e:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Error connecting to {ip_address}:{port} - {e}")
            self.signal_distributor.LOG_MESSAGE.emit(f"Error connecting to {ip_address}:{port} - {e}")
            return False

    def disconnect(self):
        if self.tcp_socket:
            try:
                self.tcp_socket.close()
                self.tcp_socket = None
                return True
            except socket.error as e:
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Error disconnecting - {e}")
                self.signal_distributor.LOG_MESSAGE.emit(f"Error disconnecting - {e}")
                return False
        return False

    def send_tcp_command(self, command):
        self.filtered_command = command
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Filtered Command: {self.filtered_command}")
        self.signal_distributor.LOG_MESSAGE.emit(f"  (sent/tcp) {self.filtered_command}")
        try:
            self.tcp_socket.sendall(self.filtered_command.encode())
            self.receive_tcp_data()
            return True
        except socket.error as e:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Error sending data: {e}")
            self.signal_distributor.LOG_MESSAGE.emit(f"Error sending data: {e}")
            return False

    def receive_tcp_data(self):
        try:
            self.tcp_socket.settimeout(5)
            incoming_data = self.tcp_socket.recv(1024)  # Adjust the buffer size as needed
            self.decoded_data = incoming_data.decode()
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Incoming TCP: {incoming_data}")
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Decoded TCP: {self.decoded_data}")
            self.validate_response()
            return self.decoded_data
        except socket.timeout:
            self.signal_distributor.DEBUG_MESSAGE.emit("Receiving data timed out")
            self.signal_distributor.LOG_MESSAGE.emit("Receiving data timed out")
            return None
        except socket.error as e:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Error receiving data: {e}")
            self.signal_distributor.LOG_MESSAGE.emit(f"Error receiving data: {e}")
            return None

    def validate_response(self):
        if self.filtered_command == self.decoded_data:
            self.signal_distributor.LOG_MESSAGE.emit("        (system) Data Acquired")
            self.signal_distributor.MACRO_TRIGGER_SEQ03_SIGNAL.emit()
        else:
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Validation failed: {self.filtered_command} != {self.decoded_data}")
            self.signal_distributor.LOG_MESSAGE.emit(f"Validation failed: {self.filtered_command} != {self.decoded_data}")
