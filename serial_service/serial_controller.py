# serial_controller.py
from PyQt6.QtCore import QObject, pyqtSignal


class SerialController(QObject):
    debug_message = pyqtSignal(str)
    log_message = pyqtSignal(str)
    alarm_signal = pyqtSignal(str, str)

    def __init__(self, model, view, signal_distributor, flag_state_manager):
        super().__init__()
        self.model = model
        self.view = view
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        # TODO this is very incorrect just trying to reset
        # self.command_view.debug_message.connect(self.debug_message.emit)

        self._populate_ports()

        self.view.serial_connect_btn.clicked.connect(self.connect_serial)
        self.view.serial_close_btn.clicked.connect(self.disconnect_serial)

        # Connect model signals to the controller's signals
        self.model.data_received.connect(self.debug_message.emit)
        self.model.error_occurred.connect(self.debug_message.emit)
        self.model.debug_message.connect(self.debug_message.emit)
        self.model.alarm_signal.connect(self.alarm_signal.emit)

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
        debug_message

        """
        port = self.view.serial_port_cbx.currentText()
        baudrate = int(self.view.baud_combo.currentText())
        success = self.model.connect(port, baudrate)
        if success:
            self.update_connection_state(True)
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('serial_connected', True, 'validate')
            # self.debug_message.emit(f"Connected to {port} at {baudrate} baudrate")
            # self.log_message.emit(f"SERIAL CONNECTION to {port} at {baudrate}")
        else:
            self.update_connection_state(False)
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('serial_connected', False, 'validate')
            self.log_message.emit(f"SERIAL CONNECTION FAILED to {port} at {baudrate}")
            self.debug_message.emit(f"Failed to connect to {port}")

    def disconnect_serial(self):
        """
        Responds directly to view.serial_close_btn.
        Disconnects the serial port.
        state_change
        debug_message
        """
        success = self.model.disconnect_serial()
        if success:
            self.update_connection_state(False)
            self.signal_distributor.STATE_CHANGED_SIGNAL.emit('serial_connected', False, 'update')
            self.debug_message.emit("Disconnected from serial port")
            self.log_message.emit("Serial port disconnected")

    def update_connection_state(self, connected):
        self.view.serial_connect_btn.setEnabled(not connected)
        self.view.serial_close_btn.setEnabled(connected)

    @staticmethod
    def on_data_received(data):
        print(f"Data received: {data}")

    @staticmethod
    def on_error_occurred(error):
        print(f"Error occurred: {error}")
