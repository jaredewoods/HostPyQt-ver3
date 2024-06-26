# command_controller.py
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class CommandController(QObject):

    def __init__(self, model, view, signal_distributor):
        super().__init__()
        self.timer = None
        self.command = None
        self.xgx_command = None
        self.wait_time = None
        self.model = model
        self.view = view
        self.signal_distributor = signal_distributor

        # Connect the view's User Interface to the controller's methods
        self.view.start_bit_checkbox.toggled.connect(self.update_model)
        self.view.checksum_checkbox.toggled.connect(self.update_model)
        self.view.carriage_return_checkbox.toggled.connect(self.update_model)
        self.view.dropdown_unit_no.currentTextChanged.connect(self.update_model)
        self.view.dropdown_code.currentTextChanged.connect(self.update_model)
        self.view.entry_parameters.textChanged.connect(self.update_model)
        self.view.run_next_command.connect(self.run_next_command)
        self.update_view()

    def signal_cycle_completed(self):
        self.signal_distributor.MACRO_TRIGGER_SEQ04_SIGNAL.emit()

    def run_next_command(self):
        self.signal_distributor.MACRO_TRIGGER_SEQ01_SIGNAL.emit()

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
        self.construct_command()
        self.signal_distributor.STATE_CHANGED_SIGNAL.emit('macro_ready_to_run', False, 'update')

    def construct_command(self):
        constructed_command = self.model.construct_command()
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Command Constructed: {constructed_command}")
        self.signal_distributor.FILTER_CONSTRUCTED_COMMAND_SIGNAL.emit(constructed_command)

    def handle_wait_command(self, command):
        self.wait_time = command
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Wait Time: {self.wait_time}ms")
        self.signal_distributor.LOG_MESSAGE.emit(f'  (host) WAIT{self.wait_time}, wait for {int(self.wait_time)/1000}secs')
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_wait_complete)
        self.timer.start(int(self.wait_time))

    def on_wait_complete(self):
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Wait time of {self.wait_time} seconds completed.")
        self.signal_distributor.LOG_MESSAGE.emit(f'        (host) {int(self.wait_time)/1000} secs wait completed')
        self.signal_distributor.MACRO_TRIGGER_SEQ03_SIGNAL.emit()

    def handle_xgx_command(self, command):
        self.command = command
        self.xgx_command = command[6:8]
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Handling XG-X command: {self.command}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Parameter values: {self.xgx_command}")
