# tcp_controller.py

class TCPController:
    def __init__(self, model, view, flag_state_manager):
        self.model = model
        self.view = view
        self.state_manager = flag_state_manager

        self.view.tcp_connect_btn.clicked.connect(self.connect_tcp)
        self.view.tcp_close_btn.clicked.connect(self.disconnect_tcp)

    def connect_tcp(self):
        ip_address = self.view.ip_address_combo.currentText()
        port = self.view.port_combo.currentText()
        success = self.model.connect(ip_address, port)
        if success:
            self.state_manager.update_state('tcp_connected', True, 'validate')
        else:
            self.state_manager.update_state('tcp_connected', False, 'update')

    def disconnect_tcp(self):
        success = self.model.disconnect()
        if success:
            self.state_manager.update_state('tcp_connected', False, 'update')

    def update_connection_state(self, connected):
        self.view.tcp_connect_btn.setEnabled(not connected)
        self.view.tcp_close_btn.setEnabled(connected)
