# serial_controller.py

class SerialController:
    def __init__(self, model, view, flag_state_manager):
        self.model = model
        self.view = view
        self.state_manager = flag_state_manager
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
            self.view.update_connection_state_for_serial_buttons(True, port)
            self.state_manager.update_state('serial_connected', True, 'validate')
        else:
            self.view.update_connection_state_for_serial_buttons(False, port)

    def disconnect_serial(self):
        success = self.model.disconnect()
        if success:
            self.view.update_disconnection_state_for_serial_buttons()
            self.state_manager.update_state('serial_connected', False, 'update')
