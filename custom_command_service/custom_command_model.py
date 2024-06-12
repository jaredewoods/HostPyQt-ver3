# custom_command_model.py

class CustomCommandModel:
    def __init__(self):
        self._start_bit_checked = True

    def set_start_bit_checked(self, value):
        self._start_bit_checked = value

    def is_start_bit_checked(self):
        return self._start_bit_checked
