# serial_controller.py

class SerialController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.populate_ports()

        self.view.serial_connect_btn.clicked.connect(self.connect_serial)
        # self.view.serial_close_button.clicked.connect(self.close_serial)

    def populate_ports(self):
        ports = self.model.get_available_ports()
        self.view.set_ports(ports)

    def connect_serial(self):
        port = self.view.serial_port_cbx.currentText()
        baudrate = int(self.view.baud_combo.currentText())
        success = self.model.connect(port, baudrate)
        if success:
            print(f"Connected to {port}")

        else:
            print(f"Failed to connect to {port}")
            self.view.update_serial_connection_status(False)