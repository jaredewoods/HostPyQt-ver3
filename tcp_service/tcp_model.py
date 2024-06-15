# tcp_model.py

import socket

class TCPModel:
    def __init__(self):
        self.tcp_socket = None

    def connect(self, ip_address, port):
        try:
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.connect((ip_address, int(port)))
            return True
        except socket.error as e:
            print(f"Error connecting to {ip_address}:{port} - {e}")
            return False

    def disconnect(self):
        if self.tcp_socket:
            self.tcp_socket.close()
            return True
        return False
