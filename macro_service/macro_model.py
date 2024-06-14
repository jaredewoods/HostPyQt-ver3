# macro_model.py

import os

class MacroModel:

    @staticmethod
    def get_macro_filenames(directory):
        try:
            macro_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            print(f"Macro files in directory {directory}: {macro_files}")
            return macro_files
        except FileNotFoundError:
            print(f"The directory {directory} was not found.")
            return []
