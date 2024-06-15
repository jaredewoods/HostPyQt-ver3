# serial_controller.py
from PyQt6.QtCore import QObject, pyqtSignal

class SerialController(QObject):
    log_message = pyqtSignal(str)  # Define a signal to emit log messages

    def __init__(self, model, view, signal_distributor):
        super().__init__()
        self.model = model
        self.view = view
        self.signal_distributor = signal_distributor
        self.populate_ports()

        self.view.serial_connect_btn.clicked.connect(self.connect_serial)
        self.view.serial_close_btn.clicked.connect(self.disconnect_serial)

    def populate_ports(self):
        ports = self.model.get_available_ports()
        self.view.set_ports(ports)

    def connect_serial(self):
        port = self.view.serial_port_cbx.currentText()
        baudrate = int(self.view.baud_combo.currentText())
        success = self.model.connect(port, baudrate)
        if success:
            self.update_connection_state(True, port)
            self.signal_distributor.state_changed.emit('serial_connected', True, 'validate')
            self.log_message.emit(f"Connected to {port} at {baudrate} baudrate")
        else:
            self.update_connection_state(False, port)
            self.signal_distributor.state_changed.emit('serial_connected', False, 'validate')
            self.log_message.emit(f"Failed to connect to {port}")

    def disconnect_serial(self):
        success = self.model.disconnect()
        if success:
            self.update_connection_state(False)
            self.signal_distributor.state_changed.emit('serial_connected', False, 'update')
            self.log_message.emit("Disconnected from serial port")

    def update_connection_state(self, connected, port=None):
        self.view.serial_connect_btn.setEnabled(not connected)
        self.view.serial_close_btn.setEnabled(connected)
