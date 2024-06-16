# macro_controller.py

import os
from PyQt6.QtCore import QObject

class MacroController(QObject):
    def __init__(self, model, view, command_view, signal_distributor):
        super().__init__()
        self.view = view
        self.model = model
        self.command_view = command_view
        self.signal_distributor = signal_distributor
        # Connect the combo box selection change to a method
        self.view.macro_select_cbx.currentIndexChanged.connect(self.on_macro_selection_changed)

        # Populate the macro ComboBox
        self.populate_macro_combobox()

    def on_macro_selection_changed(self):
        selected_file = self.view.macro_select_cbx.currentText()
        if selected_file:
            macro_sequence_file_path = os.path.join(self.get_macro_directory(), selected_file)
            self.load_macro_file(macro_sequence_file_path)

    def get_macro_directory(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_dir = os.path.dirname(current_dir)
        return os.path.join(main_dir, 'resources', 'macro_sequences')

    def load_macro_file(self, file_name):
        macro_directory = self.get_macro_directory()
        file_path = os.path.join(macro_directory, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        suggested_cycles = 0
        macro_commands = []
        for line in lines:
            line = line.strip()
            if line.startswith("SUGGESTED_CYCLES"):
                suggested_cycles = int(line.split(':')[1].strip())
            elif line.startswith("[unit") or line.endswith("end]") or line == "":
                continue
            else:
                macro_commands.append(line)

        # Update the UI elements
        self.view.update_total_cycles(suggested_cycles)
        self.command_view.update_macro_sequence('\n'.join(macro_commands))

        # For testing purposes, print the parsed results
        print("Suggested Cycles:", suggested_cycles)
        print("Macro Commands:", macro_commands)

        return suggested_cycles, macro_commands

    def populate_macro_combobox(self):
        macro_directory = self.get_macro_directory()
        macro_files = self.model.get_macro_filenames(macro_directory)
        self.view.populate_macro_select_combo(macro_files)

