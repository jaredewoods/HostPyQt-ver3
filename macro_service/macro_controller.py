# macro_controller.py

import os
import logging
from PyQt6.QtCore import QObject, pyqtSignal

class MacroController(QObject):

    def __init__(self, model, view):
        super().__init__()
        self.view = view
        self.model = model

        # Populate the macro ComboBox
        self.populate_macro_combobox()

    def populate_macro_combobox(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_dir = os.path.dirname(current_dir)
        macro_directory = os.path.join(main_dir, 'resources', 'macro_sequences')
        macro_files = self.model.get_macro_filenames(macro_directory)
        self.view.populate_macro_select_combo(macro_files)
        print("macro_controller1")
