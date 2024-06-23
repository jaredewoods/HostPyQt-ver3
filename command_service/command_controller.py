# command_controller.py
from PyQt6.QtCore import QObject, pyqtSignal

class CommandController(QObject):
    debug_message = pyqtSignal(str)
    log_message = pyqtSignal(str)

    def __init__(self, model, view, serial_controller, signal_distributor):
        super().__init__()
        self.model = model
        self.view = view
        self.serial_controller = serial_controller
        self.signal_distributor = signal_distributor
        # Connect the view's signals to the controller's methods
        self.view.start_bit_checkbox.toggled.connect(self.update_model)
        self.view.checksum_checkbox.toggled.connect(self.update_model)
        self.view.carriage_return_checkbox.toggled.connect(self.update_model)
        self.view.dropdown_unit_no.currentTextChanged.connect(self.update_model)
        self.view.dropdown_code.currentTextChanged.connect(self.update_model)
        self.view.entry_parameters.textChanged.connect(self.update_model)
        self.view.single_shot_btn_clicked.connect(self.send_single_shot)
        self.view.run_next_command.connect(self.run_next_command)
        self.view.signal_cycle_completed.connect(self.signal_cycle_completed)
        self.update_view()

    def signal_cycle_completed(self):
        self.signal_distributor.macro_trigger_seq04.emit()

    def run_next_command(self):
        self.signal_distributor.macro_trigger_seq00.emit()
        print("Triggering SEQ00 from CommandCOntroller.run_next_object")

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

    def send_single_shot(self):
        self.send_command()
        self.signal_distributor.state_changed.emit('macro_ready_to_run', False, 'update')

    def send_command(self):
        command = self.model.construct_command()
        print(f"Command sent: {command}")
        self.serial_controller.send_command(command)


    def handle_wait_command(self, command):
        self.command = command
        self.wait_time = command[6:10]  # Extract parameter values starting from the 9th character
        print(f"Handling WAIT command: {command}")
        print(f"Parameter values: {self.wait_time}")

    def handle_xgx_command(self, command):
        print(f"Handling XG-X command: {command}")