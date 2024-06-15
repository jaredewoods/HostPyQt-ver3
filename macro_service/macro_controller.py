# macro_controller.py

import os
from PyQt6.QtCore import QObject

class MacroController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.view = view
        self.model = model

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

    def load_macro_file(self, macro_sequence_file_path):
        self.model.load_macro_file(macro_sequence_file_path)
        recommended_cycles = self.model.get_recommended_cycles()
        self.view.update_total_cycles(recommended_cycles)

    def populate_macro_combobox(self):
        macro_directory = self.get_macro_directory()
        macro_files = self.model.get_macro_filenames(macro_directory)
        self.view.populate_macro_select_combo(macro_files)
