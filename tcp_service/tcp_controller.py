from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

class TCPController(QObject):

    def __init__(self, model, view, signal_distributor):
        super().__init__()
        self.model = model
        self.view = view
        self.signal_distributor = signal_distributor

        self.thread = QThread()
        self.model.moveToThread(self.thread)
        self.thread.start()

        self.view.tcp_connect_btn.clicked.connect(self.connect_tcp)
        self.view.tcp_close_btn.clicked.connect(self.disconnect_tcp)

    @pyqtSlot()
    def connect_tcp(self):
        ip_address = self.view.ip_address_combo.currentText()
        port = self.view.port_combo.currentText()

        success = self.model.connect(ip_address, port)
        if success:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('tcp_connected', True,)
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Connected to {ip_address}:{port}")
            self.signal_distributor.LOG_MESSAGE.emit(f"Connected to {ip_address}:{port}")
        else:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('tcp_connected', False)
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Failed to connect to {ip_address}:{port}")

    @pyqtSlot()
    def disconnect_tcp(self):
        success = self.model.disconnect()
        if success:
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('tcp_connected', False)
            self.signal_distributor.DEBUG_MESSAGE.emit("Disconnected from TCP connection")

    def update_connection_btn_state(self, connected):
        self.view.tcp_connect_btn.setEnabled(not connected)
        self.view.tcp_close_btn.setEnabled(connected)

    @pyqtSlot(str)
    def handle_tcp_command(self, command):
        self.model.send_tcp_command(command)
