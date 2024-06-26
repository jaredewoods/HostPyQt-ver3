# tcp_controller.py

from PyQt6.QtCore import QObject, pyqtSignal

class TCPController(QObject):
    debug_message = pyqtSignal(str)  # Define a signal to emit log messages
    log_message = pyqtSignal(str)  # Define a signal to emit

    def __init__(self, model, view, signal_distributor):
        super().__init__()
        self.model = model
        self.view = view
        self.signal_distributor = signal_distributor

        self.view.tcp_connect_btn.clicked.connect(self.connect_tcp)
        self.view.tcp_close_btn.clicked.connect(self.disconnect_tcp)

    def connect_tcp(self):
        ip_address = self.view.ip_address_combo.currentText()
        port = self.view.port_combo.currentText()
        success = self.model.connect(ip_address, port)
        if success:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('tcp_connected', True, 'validate')
            self.debug_message.emit(f"Connected to {ip_address}:{port}")
            self.log_message.emit(f"Connected to {ip_address}:{port}")
        else:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('tcp_connected', False, 'update')
            self.debug_message.emit(f"Failed to connect to {ip_address}:{port}")

    def disconnect_tcp(self):
        success = self.model.disconnect()
        if success:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('tcp_connected', False, 'update')
            self.debug_message.emit("Disconnected from TCP connection")

    def update_connection_btn_state(self, connected):
        self.view.tcp_connect_btn.setEnabled(not connected)
        self.view.tcp_close_btn.setEnabled(connected)
