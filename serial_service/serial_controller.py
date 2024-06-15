# serial_controller.py

class SerialController:
    def __init__(self, model, view, signal_distributor):
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
            self.signal_distributor.emit_state_change('serial_connected', True, 'validate')
        else:
            self.update_connection_state(False, port)
            self.signal_distributor.emit_state_change('serial_connected', False, 'validate')

    def disconnect_serial(self):
        success = self.model.disconnect()
        if success:
            self.update_connection_state(False)
            self.signal_distributor.emit_state_change('serial_connected', False, 'update')

    def update_connection_state(self, connected, port=None):
        self.view.serial_connect_btn.setEnabled(not connected)
        self.view.serial_close_btn.setEnabled(connected)
