# macro_controller.py

import os
from PyQt6.QtCore import QObject, pyqtSignal

class MacroController(QObject):
    start_signal = pyqtSignal()
    """The MacroController class handles the logic for loading, parsing, and displaying macro commands.

    Args:
        model (Model): The model object.
        view (View): The view object.
        command_view (CommandView): The command view object.
        signal_distributor (SignalDistributor): The signal distributor object.
        flag_state_manager (FlagStateManager): The flag state manager object.
    """
    def __init__(self, model, view, command_view, signal_distributor, flag_state_manager):
        super().__init__()
        self.macro_commands = None
        self.view = view
        self.model = model
        self.command_view = command_view
        self.signal_distributor = signal_distributor
        self.flag_state_manager = flag_state_manager
        self.view.macro_select_cbx.activated.connect(self.on_macro_dropdown_activated)
        self.view.macro_start_btn.clicked.connect(self.set_macro_running_flag_true)
        self.view.macro_stop_btn.clicked.connect(self.set_macro_running_flag_false)

        self.populate_macro_combobox()

    def set_macro_running_flag_true(self):
        self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_running", True, "update")

    def set_macro_running_flag_false(self):
        self.signal_distributor.STATE_CHANGED_SIGNAL.emit("macro_running", False, "update")

    @staticmethod
    def get_macro_directory():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_dir = os.path.dirname(current_dir)
        return os.path.join(main_dir, 'resources', 'macro_sequences')

    def populate_macro_combobox(self):
        macro_directory = self.get_macro_directory()
        macro_files = self.model.get_macro_filenames(macro_directory)
        self.view.populate_macro_select_combo(macro_files)

    def on_macro_dropdown_activated(self, index):
        selected_file = self.view.macro_select_cbx.currentText()
        print(f"Dropdown activated: {selected_file}")  # Debug statement
        if selected_file:
            self.handle_macro_file_selection(selected_file)
            self.command_view.clear_fields()  # Clear fields in CommandView
        # Select the first item in the QListWidget
        if self.command_view.macro_sequence_display.count() > 0:
            self.command_view.macro_sequence_display.setCurrentRow(0)

    def update_macro_ready_state(self):
        serial_connected = self.flag_state_manager.get_flag_status('serial_connected')
        macro_ready = serial_connected
        self.signal_distributor.STATE_CHANGED_SIGNAL.emit('macro_ready_to_run', macro_ready, 'update')

    def handle_macro_file_selection(self, selected_file):
        macro_sequence_file_path = os.path.join(self.get_macro_directory(), selected_file)
        self.load_macro_file(macro_sequence_file_path)
        self.view.macro_start_btn.setEnabled(True)
        self.update_macro_ready_state()
        self.load_macro_sequence_line()  # Initialize the first command without arguments

    @staticmethod
    def read_macro_file(file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    def parse_macro_file_content(self, lines):
        suggested_cycles = 0
        macro_commands = []
        current_unit = None
        for line in lines:
            line = line.strip()
            self.signal_distributor.DEBUG_MESSAGE.emit(f"Parsing line: {line}")

            if line.startswith("SUGGESTED_CYCLES"):
                suggested_cycles = int(line.split(':')[1].strip())
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Found suggested cycles: {suggested_cycles}")  # Debug statement
            elif line.startswith("[unit") and "start" in line:
                current_unit = int(line.split("unit")[1].split()[0])
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Entering unit: {current_unit}")  # Debug statement
            elif line.startswith("unit") and "end" in line:
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Exiting unit: {current_unit}")  # Debug statement
                current_unit = None
            elif current_unit is not None and line:
                macro_commands.append((line, current_unit))
                self.signal_distributor.DEBUG_MESSAGE.emit(f"Added command: {line} (Unit {current_unit})")  # Debug statement
        return suggested_cycles, macro_commands

    def update_ui_with_macro_data(self, suggested_cycles, macro_commands):
        self.view.update_total_cycles(suggested_cycles)
        formatted_commands = [f"{unit}{command}" for command, unit in macro_commands]
        self.command_view.update_macro_sequence('\n'.join(formatted_commands))

    def load_macro_file(self, file_name):
        macro_directory = self.get_macro_directory()
        file_path = os.path.join(macro_directory, file_name)
        lines = self.read_macro_file(file_path)
        suggested_cycles, macro_commands = self.parse_macro_file_content(lines)
        self.update_ui_with_macro_data(suggested_cycles, macro_commands)
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Suggested Cycles: {suggested_cycles}")
        self.signal_distributor.DEBUG_MESSAGE.emit(f"Macro Commands: {macro_commands}")
        self.macro_commands = macro_commands
        return suggested_cycles, macro_commands

    def load_macro_sequence_line(self):
        selected_item = self.command_view.macro_sequence_display.currentItem()
        if selected_item:
            full_command_with_unit = selected_item.text()
            unit_number = full_command_with_unit[0]
            full_command = full_command_with_unit[1:]
            command = full_command[:4]
            parameters = full_command[4:]

            print(f"Loading command: {command}, unit: {unit_number}, parameters: {parameters}")  # Debug statement
            self.load_command_into_view(command, unit_number, parameters)
            return full_command
        else:
            print("No item selected")  # Debug statement
            return None

    def load_command_into_view(self, command, unit, parameters):
        print(f"Setting command: {command}, unit: {unit}, parameters: {parameters}")  # Debug statement
        self.command_view.set_command(command)
        self.command_view.set_unit_number(unit)
        self.command_view.set_parameters(parameters)
        self.command_view.set_code(command)
