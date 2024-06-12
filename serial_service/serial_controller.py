# serial_controller.py

class SerialController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.populate_ports()

    def populate_ports(self):
        ports = self.model.get_available_ports()
        self.view.set_ports(ports)
