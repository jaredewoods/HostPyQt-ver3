# serial_controller.py
from PyQt6.QtCore import QObject, pyqtSignal

class SerialController(QObject):
    log_message = pyqtSignal(str)

    def __init__(self, model, view, signal_distributor):
        super().__init__()
        self.model = model
        self.view = view
        self.signal_distributor = signal_distributor
        self._populate_ports()

        self.view.serial_connect_btn.clicked.connect(self.connect_serial)
        self.view.serial_close_btn.clicked.connect(self.disconnect_serial)

        # Connect model signals to the controller's signals
        self.model.data_received.connect(self.log_message.emit)
        self.model.error_occurred.connect(self.log_message.emit)
        self.model.log_message.connect(self.log_message.emit)

    def _populate_ports(self):
        """
        MVC Populates the ports in the view.

        """
        ports = self.model.get_available_ports()
        self.view.set_ports(ports)

    def connect_serial(self):
        """
        Responds directly to view.serial_connect_btn.
        Connects to the serial port
        Updates 'serial_connected' via signal_distributor
        log_message

        """
        port = self.view.serial_port_cbx.currentText()
        baudrate = int(self.view.baud_combo.currentText())
        success = self.model.connect(port, baudrate)
        if success:
            self._update_connection_state(True)
            self.signal_distributor.state_changed.emit('serial_connected', True, 'validate')
            self.log_message.emit(f"Connected to {port} at {baudrate} baudrate")
        else:
            self._update_connection_state(False)
            self.signal_distributor.state_changed.emit('serial_connected', False, 'validate')
            self.log_message.emit(f"Failed to connect to {port}")

    def disconnect_serial(self):
        """
        Responds directly to view.serial_close_btn.
        Disconnects the serial port.
        state_change
        log_message
        """
        success = self.model.disconnect_serial()
        if success:
            self._update_connection_state(False)
            self.signal_distributor.state_changed.emit('serial_connected', False, 'update')
            self.log_message.emit("Disconnected from serial port")

    def send_command(self, command):
        """
        Sends a command through the serial port.
        """
        self.model.write_command(command)

    def _update_connection_state(self, connected):
        self.view.serial_connect_btn.setEnabled(not connected)
        self.view.serial_close_btn.setEnabled(connected)

    def on_data_received(self, data):
        print(f"Data received: {data}")

    def on_error_occurred(self, error):
        print(f"Error occurred: {error}")