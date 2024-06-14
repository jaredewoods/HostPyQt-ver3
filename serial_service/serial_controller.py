# serial_controller.py

class SerialController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
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
            self.view.update_connection_status(True, port)
        else:
            self.view.update_connection_status(False, port)

    def disconnect_serial(self):
        success = self.model.disconnect()
        if success:
            self.view.update_disconnection_status()
