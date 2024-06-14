# macro_model.py

import os

class MacroModel:
    def __init__(self):
        self.macro_sequence = {}
        self.recommended_cycles = 0

    def load_macro_file(self, macro_sequence_file_path):
        with open(macro_sequence_file_path, 'r') as file:
            lines = file.readlines()

        if lines and lines[0].startswith("SUGGESTED_CYCLES:"):
            self.recommended_cycles = int(lines[0].split(":")[1].strip())

        self.macro_sequence = self._parse_macro_commands(lines[1:])

    def get_recommended_cycles(self):
        return self.recommended_cycles

    def _parse_macro_commands(self, lines):
        macro_commands = {}
        current_unit = 1

        for line in lines:
            if line.startswith("[unit1"):
                current_unit = 1
            elif line.startswith("[unit2"):
                current_unit = 2
            else:
                command = line.strip().ljust(10, '0')
                macro_commands[current_unit] = macro_commands.get(current_unit, []) + [command]

        return macro_commands

    @staticmethod
    def get_macro_filenames(directory):
        try:
            macro_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            print(f"Macro files in directory {directory}: {macro_files}")
            return macro_files
        except FileNotFoundError:
            print(f"The directory {directory} was not found.")
            return []
