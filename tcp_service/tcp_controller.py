# tcp_controller.py

class TCPController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.tcp_connect_btn.clicked.connect(self.connect_tcp)
        self.view.tcp_close_btn.clicked.connect(self.disconnect_tcp)

    def connect_tcp(self):
        ip_address = self.view.ip_address_combo.currentText()
        port = self.view.port_combo.currentText()
        success = self.model.connect(ip_address, port)
        if success:
            self.view.update_connection_status(True, ip_address, port)
        else:
            self.view.update_connection_status(False, ip_address, port)

    def disconnect_tcp(self):
        success = self.model.disconnect()
        if success:
            self.view.update_disconnection_status()
