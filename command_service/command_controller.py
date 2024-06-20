# command_controller.py
from PyQt6.QtCore import QObject, pyqtSignal

class CommandController(QObject):
    log_message = pyqtSignal(str)  # Define a signal to emit log messages

    def __init__(self, model, view, serial_controller):
        super().__init__()
        self.model = model
        self.view = view
        self.serial_controller = serial_controller
        # Connect the view's signals to the controller's methods
        self.view.start_bit_checkbox.toggled.connect(self.update_model)
        self.view.checksum_checkbox.toggled.connect(self.update_model)
        self.view.carriage_return_checkbox.toggled.connect(self.update_model)
        self.view.dropdown_unit_no.currentTextChanged.connect(self.update_model)
        self.view.dropdown_code.currentTextChanged.connect(self.update_model)
        self.view.entry_parameters.textChanged.connect(self.update_model)
        self.view.single_shot_btn_clicked.connect(self.send_command)
        self.update_view()

    def update_model(self):
        self.model.set_start_bit_checked(self.view.start_bit_checkbox.isChecked())
        self.model.set_checksum_checked(self.view.checksum_checkbox.isChecked())
        self.model.set_carriage_return_checked(self.view.carriage_return_checkbox.isChecked())
        self.model.set_unit_no(self.view.dropdown_unit_no.currentText())
        self.model.set_command_code(self.view.dropdown_code.currentText())
        self.model.set_parameters(self.view.entry_parameters.text())
        self.update_view()

    def update_view(self):
        command = self.model.construct_command()
        self.set_command_text(command)

    def set_command_text(self, text):
        self.view.display_command.setText(text)

    def handle_text_changed(self):
        self.update_view()

    def send_command(self):
        command = self.model.construct_command()
        print(f"Command sent: {command}")
        self.serial_controller.send_command(command)
